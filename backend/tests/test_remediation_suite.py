import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import init_db, save_audit_record, get_audit_by_id, get_db_connection, save_citizen_report, get_all_citizen_reports
from services.crypto_service import generate_sha256_seal, recompute_and_verify_seal

class TestRemediationSuite(unittest.TestCase):
    def setUp(self):
        """Ensure database schema is initialized before tests."""
        init_db()
        self.client = TestClient(app)

    def test_crypto_deterministic_hash_and_tamper_detection(self):
        """Tests that deterministic canonical serialization produces identical hash and detects changes."""
        audit_data = {
            "dossier_id": "DOSSIER-TEST-CRYPTO-001",
            "risk_score": 85,
            "status": "FLAGGED",
            "contractor_name": "M/s Apex Civil Constructions Ltd.",
            "tender_id": "TDR-2024-TEST-001"
        }

        hash1 = generate_sha256_seal(audit_data)
        hash2 = generate_sha256_seal(audit_data)
        self.assertEqual(hash1, hash2, "Identical payloads must produce identical SHA-256 seal")

        # Modify payload and verify hash changes
        tampered_data = dict(audit_data)
        tampered_data["risk_score"] = 10
        hash_tampered = generate_sha256_seal(tampered_data)
        self.assertNotEqual(hash1, hash_tampered, "Altered payload must produce distinct SHA-256 seal")

    def test_verify_nonexistent_dossier_returns_404(self):
        """Security Test: Nonexistent dossier must return HTTP 404, never AUTHENTIC."""
        response = self.client.get("/api/verify/DOSSIER-NONEXISTENT-999999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("not found", data["detail"].lower())

    def test_verify_valid_dossier_and_tamper_detection(self):
        """
        Security Test:
        1. Valid persisted record returns AUTHENTIC_RECORD_VERIFIED and MATCH_CONFIRMED.
        2. Directly tampering with the SQLite row causes /verify to detect MISMATCH and ALTERED.
        """
        test_dossier_id = "DOSSIER-TEST-VERIFY-002"
        contractor = "Varanasi Highway Developers Ltd."
        tender = "TDR-2024-TEST-002"
        status = "FLAGGED"
        risk_score = 90

        audit_payload = {
            "dossier": {"dossier_id": test_dossier_id},
            "project_metadata": {
                "project_name": "Test Highway Resurfacing",
                "scheme": "PMGSY",
                "contractor_name": contractor,
                "tender_id": tender,
                "claim_amount": "₹50,00,000",
                "claimed_latitude": 25.3176,
                "claimed_longitude": 82.9739
            },
            "status": status,
            "risk_score": risk_score,
            "decision_reason": "Test audit record",
            "recommended_action": "Hold funds",
            "dossier_id": test_dossier_id,
            "contractor_name": contractor,
            "tender_id": tender
        }

        # Compute valid seal and store in SQLite
        valid_seal = generate_sha256_seal(audit_payload)
        audit_payload["dossier"]["crypto_verification"] = {"sha256_seal": valid_seal}

        save_audit_record(audit_payload, is_demo=True)

        # 1. Verify valid record
        res_valid = self.client.get(f"/api/verify/{test_dossier_id}")
        self.assertEqual(res_valid.status_code, 200)
        valid_data = res_valid.json()
        self.assertEqual(valid_data["status"], "AUTHENTIC_RECORD_VERIFIED")
        self.assertTrue(valid_data["verified"])
        self.assertEqual(valid_data["sha256_seal_status"], "MATCH_CONFIRMED")
        self.assertEqual(valid_data["ledger_integrity"], "UNALTERED")
        self.assertEqual(valid_data["sha256_seal"], valid_seal)

        # 2. Tamper directly with the SQLite database row (simulate unauthorized modification)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE audits SET risk_score = 10, verdict = 'CLEAR' WHERE dossier_id = ?", (test_dossier_id,))
        conn.commit()
        conn.close()

        # 3. Call verify again - must detect tampering!
        res_tampered = self.client.get(f"/api/verify/{test_dossier_id}")
        self.assertEqual(res_tampered.status_code, 200)
        tampered_data = res_tampered.json()
        self.assertEqual(tampered_data["status"], "INTEGRITY_CHECK_FAILED")
        self.assertFalse(tampered_data["verified"])
        self.assertEqual(tampered_data["sha256_seal_status"], "MISMATCH")
        self.assertEqual(tampered_data["ledger_integrity"], "ALTERED")

    def test_citizen_report_persistence_and_retrieval(self):
        """Persistence Test: Citizen reports must be stored in SQLite and retrievable via GET /api/citizen/reports."""
        citizen_report_data = {
            "audit_id": "CIT-AUDIT-TEST-003",
            "project_id": "PROJ-RURAL-TEST-003",
            "project_name": "Gram Sadak Rural Works",
            "citizen_notes": "Road only 50% completed despite 100% claim.",
            "risk_score": 75,
            "verdict": "FLAGGED"
        }

        save_citizen_report(citizen_report_data)

        reports = get_all_citizen_reports()
        self.assertGreater(len(reports), 0)
        found = any(r["audit_id"] == "CIT-AUDIT-TEST-003" for r in reports)
        self.assertTrue(found, "Citizen report must be persisted in SQLite")

        # Verify API endpoint
        response = self.client.get("/api/citizen/reports")
        self.assertEqual(response.status_code, 200)
        api_data = response.json()
        self.assertGreater(api_data["count"], 0)
        self.assertTrue(any(r["audit_id"] == "CIT-AUDIT-TEST-003" for r in api_data["reports"]))

    def test_demo_audit_does_not_mutate_contractor_integrity(self):
        """Abuse Protection Test: Demo/benchmark executions must not alter live contractor ratings."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT past_violations, integrity_score FROM contractors WHERE contractor_id = 'CONT-001'")
        initial_contractor = cursor.fetchone()
        init_violations = initial_contractor["past_violations"]
        init_score = initial_contractor["integrity_score"]
        conn.close()

        demo_audit = {
            "dossier": {"dossier_id": "DOSSIER-DEMO-TEST-004"},
            "project_metadata": {
                "project_name": "Benchmark Test Run",
                "scheme": "PMGSY",
                "contractor_name": "M/s Apex Civil Constructions Ltd.",
                "tender_id": "TDR-BENCHMARK-004",
                "claim_amount": "₹25,00,000",
                "claimed_latitude": 25.3176,
                "claimed_longitude": 82.9739
            },
            "status": "FLAGGED",
            "risk_score": 95,
            "decision_reason": "Benchmark run",
            "recommended_action": "Hold",
            "dossier_id": "DOSSIER-DEMO-TEST-004",
            "contractor_name": "M/s Apex Civil Constructions Ltd.",
            "tender_id": "TDR-BENCHMARK-004"
        }

        # Save with is_demo=True
        save_audit_record(demo_audit, is_demo=True)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT past_violations, integrity_score FROM contractors WHERE contractor_id = 'CONT-001'")
        post_contractor = cursor.fetchone()
        conn.close()

        self.assertEqual(post_contractor["past_violations"], init_violations, "Demo audit must not increment contractor past violations")
        self.assertEqual(post_contractor["integrity_score"], init_score, "Demo audit must not decrement contractor integrity score")


if __name__ == "__main__":
    unittest.main()
