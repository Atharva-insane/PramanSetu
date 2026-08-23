import base64
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from config import JWT_SECRET_KEY, JWT_EXPIRATION_HOURS

# Cryptographic Salt & Iteration configuration for PBKDF2
PBKDF2_ITERATIONS = 100_000


def _base64url_encode(data: bytes) -> str:
    """Encodes bytes into URL-safe base64 string without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _base64url_decode(data: str) -> bytes:
    """Decodes URL-safe base64 string, restoring required padding."""
    padding = b"=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data.encode("utf-8") + padding)


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Computes PBKDF2-HMAC-SHA256 password hash with cryptographic salt."""
    if not salt:
        salt = _base64url_encode(hashlib.sha256(str(time.time_ns()).encode()).digest()[:16])
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS,
        dklen=32
    )
    return f"{salt}${_base64url_encode(key)}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against the stored PBKDF2 hash in constant time."""
    try:
        salt, expected_hash = hashed_password.split("$")
        computed = hash_password(plain_password, salt=salt)
        return hmac.compare_digest(computed, hashed_password)
    except Exception:
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a cryptographically signed RFC-7519 HMAC-SHA256 JWT access token.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(hours=JWT_EXPIRATION_HOURS)

    to_encode.update({
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "iss": "pramansetu-auth-authority"
    })

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _base64url_encode(json.dumps(to_encode, separators=(",", ":")).encode("utf-8"))

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(JWT_SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validates token signature and expiration, returning the payload if valid.
    """
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(JWT_SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()

        if not hmac.compare_digest(_base64url_encode(expected_sig), signature_b64):
            return None

        payload_bytes = _base64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))

        now_ts = int(datetime.now(timezone.utc).timestamp())
        if payload.get("exp", 0) < now_ts:
            return None  # Token expired

        return payload
    except Exception:
        return None


# Pre-configured institutional users with pre-computed PBKDF2 hashes
INSTITUTIONAL_USERS: Dict[str, Dict[str, Any]] = {
    "cvo_officer": {
        "username": "cvo_officer",
        "full_name": "Dr. Surendra Mohan Sharma, IAS",
        "role": "CVO",
        "department": "Central Vigilance Directorate & Anti-Corruption Cell",
        "password_hash": hash_password("CVO@Praman2026!", salt="sAltCvo2026")
    },
    "ddo_officer": {
        "username": "ddo_officer",
        "full_name": "Er. Rajeshwar Nath Sharma",
        "role": "DDO",
        "department": "Public Works Department (PWD) Disbursing Office",
        "password_hash": hash_password("DDO@Praman2026!", salt="sAltDdo2026")
    },
    "evaluator_officer": {
        "username": "evaluator_officer",
        "full_name": "Sunil Kumar Verma",
        "role": "EVALUATOR",
        "department": "State Quality Monitoring & Technical Audit Bureau",
        "password_hash": hash_password("Eval@Praman2026!", salt="sAltEval2026")
    },
    "admin_user": {
        "username": "admin_user",
        "full_name": "System Administrator",
        "role": "ADMIN",
        "department": "National Informatics Centre & Platform Operations",
        "password_hash": hash_password("Admin@Praman2026!", salt="sAltAdmin2026")
    },
    "citizen_user": {
        "username": "citizen_user",
        "full_name": "Ramesh Kumar Yadav",
        "role": "CITIZEN",
        "department": "Social Audit Society of Uttar Pradesh",
        "password_hash": hash_password("Citizen@Praman2026!", salt="sAltCitizen2026")
    }
}


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates credentials against institutional directory."""
    user = INSTITUTIONAL_USERS.get(username.strip())
    if not user:
        return None
    if verify_password(password, user["password_hash"]):
        return {
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
            "department": user["department"]
        }
    return None
