import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import init_db, save_audit_record, get_audit_by_id, get_db_connection
from services.auth_service import hash_password, verify_password, create_access_token, decode_access_token, authenticate_user
from services.pki_service import get_signature_provider
from rate_limiter import InMemoryRateLimiter


class TestProductionHardening(unittest.TestCase):
    def setUp(self):
        init_db()
        self.client = TestClient(app)

    # ==========================================
    # 1. AUTHENTICATION & JWT SECURITY TESTS
    # ==========================================

    def test_password_hashing_and_verification(self):
        """Tests PBKDF2-HMAC-SHA256 password hashing with cryptographic salt."""
        pwd = "TestSecurePassword123!"
        hashed = hash_password(pwd)
        self.assertTrue(verify_password(pwd, hashed), "Password verification must succeed for valid password")
        self.assertFalse(verify_password("WrongPassword", hashed), "Password verification must fail for invalid password")

    def test_jwt_token_lifecycle(self):
        """Tests RFC-7519 HMAC-SHA256 JWT access token generation and decoding."""
        user_data = {"sub": "officer_test", "role": "CVO", "dept": "Vigilance"}
        token = create_access_token(user_data)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split(".")), 3, "JWT must consist of header, payload, and signature")

        decoded = decode_access_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["sub"], "officer_test")
        self.assertEqual(decoded["role"], "CVO")

    def test_auth_login_endpoint(self):
        """Tests POST /api/auth/login endpoint for institutional users."""
        res_valid = self.client.post("/api/auth/login", json={"username": "cvo_officer", "password": "CVO@Praman2026!"})
        self.assertEqual(res_valid.status_code, 200)
        data = res_valid.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["user"]["role"], "CVO")

        res_invalid = self.client.post("/api/auth/login", json={"username": "cvo_officer", "password": "WrongPassword"})
        self.assertEqual(res_invalid.status_code, 401)

    # ==========================================
    # 2. RBAC & PERMISSION TESTS
    # ==========================================

    def test_rbac_protected_pki_sign_endpoint(self):
        """Tests that PKI signing requires DDO, CVO, or ADMIN role."""
        # 1. Anonymous request -> 401
        res_anon = self.client.post("/api/pki/sign", json={
            "dossier_id": "DOSSIER-TEST-01",
            "document_payload": {"test": "data"},
            "officer_dn": "Er. Sharma",
            "token_id": "DSC-001"
        })
        self.assertEqual(res_anon.status_code, 401)

        # 2. Citizen role request -> 403 Forbidden
        citizen_token = create_access_token({"sub": "citizen_user", "role": "CITIZEN"})
        res_citizen = self.client.post(
            "/api/pki/sign",
            json={"dossier_id": "DOSSIER-TEST-01", "document_payload": {"test": "data"}, "officer_dn": "Er. Sharma", "token_id": "DSC-001"},
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        self.assertEqual(res_citizen.status_code, 403)

        # 3. CVO role request -> 200 OK
        cvo_token = create_access_token({"sub": "cvo_officer", "role": "CVO"})
        res_cvo = self.client.post(
            "/api/pki/sign",
            json={"dossier_id": "DOSSIER-TEST-01", "document_payload": {"test": "data"}, "officer_dn": "Er. Sharma", "token_id": "DSC-001"},
            headers={"Authorization": f"Bearer {cvo_token}"}
        )
        self.assertEqual(res_cvo.status_code, 200)
        self.assertEqual(res_cvo.json()["status"], "SIGNATURE_APPLIED")

    # ==========================================
    # 3. RATE LIMITING TESTS
    # ==========================================

    def test_sliding_window_rate_limiter(self):
        """Tests in-memory sliding window rate limiter burst throttling."""
        limiter = InMemoryRateLimiter()
        client_id = "test_client_ip_1"

        # Allow 5 requests under limit of 5
        for _ in range(5):
            allowed, _ = limiter.is_allowed(client_id, "test_action", 5)
            self.assertTrue(allowed)

        # 6th request must be throttled
        allowed_6th, retry_after = limiter.is_allowed(client_id, "test_action", 5)
        self.assertFalse(allowed_6th)
        self.assertGreater(retry_after, 0)

    # ==========================================
    # 4. FILE SECURITY & MAGIC BYTES TESTS
    # ==========================================

    def test_file_security_invalid_magic_bytes_rejected(self):
        """Tests that fake image files with non-image magic bytes are rejected with HTTP 400."""
        fake_shell_payload = b"<?php echo 'malicious shell'; ?>"
        response = self.client.post(
            "/api/audit",
            data={"claimed_latitude": 25.3176, "claimed_longitude": 82.9739},
            files={"image": ("shell.jpg", fake_shell_payload, "image/jpeg")}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid file signature", response.json()["detail"].lower())

    # ==========================================
    # 5. PKI PROVIDER SIGNING & VERIFICATION TESTS
    # ==========================================

    def test_pki_signature_provider_lifecycle(self):
        """Tests cryptographic digital signature creation and verification lifecycle."""
        provider = get_signature_provider("DEV_SOFTWARE")
        doc_payload = {
            "dossier_id": "DOSSIER-PKI-TEST-01",
            "risk_score": 90,
            "verdict": "FLAGGED",
            "contractor": "M/s Apex Civil Constructions Ltd."
        }

        sig_block = provider.sign_document_digest(doc_payload, "Er. Rajeshwar Nath Sharma", "DSC-2026-001")
        self.assertEqual(sig_block["status"], "VALID_SIGNATURE")
        self.assertIn("signature_value", sig_block)

        # Verify signature against valid document
        is_valid, msg = provider.verify_document_signature(doc_payload, sig_block)
        self.assertTrue(is_valid, msg)

        # Verify signature against tampered document (must fail)
        tampered_doc = dict(doc_payload)
        tampered_doc["risk_score"] = 10
        is_tampered_valid, tampered_msg = provider.verify_document_signature(tampered_doc, sig_block)
        self.assertFalse(is_tampered_valid, "Tampered document must fail digital signature verification")

    # ==========================================
    # 6. DATA ISOLATION & DEMO AUDIT TAGGING
    # ==========================================

    def test_demo_audit_tagging_in_database(self):
        """Tests that demo benchmarks are explicitly tagged with audit_type='DEMO'."""
        demo_payload = {
            "dossier": {"dossier_id": "DOSSIER-DEMO-TAG-01"},
            "project_metadata": {
                "project_name": "Demo Benchmark",
                "contractor_name": "M/s Apex Civil Constructions Ltd.",
                "tender_id": "TDR-DEMO-01",
                "claim_amount": "₹10,00,000",
                "claimed_latitude": 25.4358,
                "claimed_longitude": 81.8463
            },
            "status": "FLAGGED",
            "risk_score": 85,
            "dossier_id": "DOSSIER-DEMO-TAG-01",
            "contractor_name": "M/s Apex Civil Constructions Ltd.",
            "tender_id": "TDR-DEMO-01"
        }

        save_audit_record(demo_payload, is_demo=True, created_by="evaluator_officer", created_by_role="EVALUATOR")

        record = get_audit_by_id("DOSSIER-DEMO-TAG-01")
        self.assertIsNotNone(record)
        self.assertEqual(record["audit_type"], "DEMO")
        self.assertEqual(record["created_by"], "evaluator_officer")
        self.assertEqual(record["created_by_role"], "EVALUATOR")


if __name__ == "__main__":
    unittest.main()
