import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.crypto_service import generate_sha256_seal, generate_verification_qr_data

def test_crypto_seal_and_qr():
    audit_data = {
        "dossier_id": "DOSSIER-202407-TEST01",
        "risk_score": 90,
        "status": "FLAGGED",
        "contractor_name": "M/s Apex Civil Constructions Ltd.",
        "tender_id": "TDR-2024-UP-8819",
        "duplicate_check": {"hamming_distance": 0},
        "location_check": {"distance_metres": 580000},
        "muster_roll_check": {"suspected_ghost_wage_leakage": 315000}
    }
    
    sha_seal = generate_sha256_seal(audit_data)
    assert len(sha_seal) == 64, f"Expected 64-char SHA256, got {len(sha_seal)}"
    
    qr_data = generate_verification_qr_data(
        audit_data["dossier_id"],
        sha_seal,
        audit_data["risk_score"],
        audit_data["status"]
    )
    
    assert "http://localhost:3000/verify" in qr_data["verification_url"]
    assert "DOSSIER-202407-TEST01" in qr_data["verification_url"]
    assert "IN-GOV-LEDGER" in qr_data["blockchain_ledger_ref"]
    print("ALL CRYPTO SERVICE TESTS PASSED!")

if __name__ == "__main__":
    test_crypto_seal_and_qr()
