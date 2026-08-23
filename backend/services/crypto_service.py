import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from schemas import CryptoVerificationSeal


def canonical_json_bytes(data: Dict[str, Any]) -> bytes:
    """
    Serializes a dictionary into deterministic canonical JSON bytes:
    1. Keys sorted alphabetically at all nested depths.
    2. Zero extra whitespace separators (',', ':').
    3. Strict UTF-8 character encoding.
    Note: Deterministic canonical JSON serialization used for SHA-256 hashing.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def generate_sha256_seal(audit_data: Dict[str, Any]) -> str:
    """
    Computes a deterministic, tamper-evident SHA-256 cryptographic seal
    across core audit findings and project metadata.
    """
    metadata = audit_data.get("project_metadata", {}) if isinstance(audit_data.get("project_metadata"), dict) else {}
    contractor = str(audit_data.get("contractor_name") or metadata.get("contractor_name") or "")
    tender_id = str(audit_data.get("tender_id") or metadata.get("tender_id") or "")
    status = str(audit_data.get("status") or audit_data.get("verdict") or "")
    risk_score = int(audit_data.get("risk_score", 0))
    dossier = audit_data.get("dossier", {}) if isinstance(audit_data.get("dossier"), dict) else {}
    dossier_id = str(audit_data.get("dossier_id") or dossier.get("dossier_id") or tender_id)

    hashable_payload = {
        "contractor": contractor,
        "dossier_id": dossier_id,
        "risk_score": risk_score,
        "status": status,
        "tender_id": tender_id,
    }

    raw_bytes = canonical_json_bytes(hashable_payload)
    return hashlib.sha256(raw_bytes).hexdigest()


def recompute_and_verify_seal(db_record: Dict[str, Any]) -> Tuple[bool, str, str]:
    """
    Reconstructs the original hashable payload from the stored database record,
    canonically serializes it, recomputes the SHA-256 digest, and checks against stored seal.
    Returns (is_valid, recomputed_hash, stored_hash).
    """
    stored_seal = str(db_record.get("sha256_seal") or "")
    recomputed_seal = generate_sha256_seal(db_record)
    is_valid = bool(stored_seal and stored_seal == recomputed_seal and stored_seal != "UNAVAILABLE")
    return is_valid, recomputed_seal, stored_seal


class DictCryptoVerificationSeal(dict):
    """Hybrid dictionary and object wrapper for backwards compatibility."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)


def generate_verification_qr_data(
    dossier_id: str,
    sha256_seal: str,
    risk_score: Optional[int] = None,
    verdict: Optional[str] = None,
    base_verify_url: str = "http://localhost:3000/verify"
) -> DictCryptoVerificationSeal:
    """
    Generates QR verification code metadata and canonical certificate stamp.
    """
    verification_url = f"{base_verify_url}?dossier_id={dossier_id}"
    
    qr_payload = {
        "issuing_authority": "PramanSetu National Vigilance Gateway",
        "dossier_id": dossier_id,
        "sha256_checksum": sha256_seal,
        "statutory_mandate": "GFR 2017 Rule 175",
        "verification_url": verification_url
    }

    raw_qr_bytes = canonical_json_bytes(qr_payload)
    qr_hash = hashlib.sha256(raw_qr_bytes).hexdigest()

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return DictCryptoVerificationSeal(
        sha256_seal=sha256_seal,
        qr_verification_code=qr_hash[:32].upper(),
        verification_url=verification_url,
        blockchain_ledger_ref=f"IN-GOV-LEDGER-SHA256-{qr_hash[:12].upper()}",
        timestamp_utc=now_utc,
        issuer="PramanSetu Central Vigilance Directorate",
        statutory_mandate="General Financial Rules (GFR 2017) Rule 175"
    )
