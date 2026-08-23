import os
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Base Directories
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Database & Storage
DB_PATH = BASE_DIR / "mock_db.json"
WEB_DB_PATH = BASE_DIR / "mock_web_db.json"
CONTRACTORS_DB_PATH = BASE_DIR / "mock_contractors_db.json"
SAMPLE_IMAGES_DIR = BASE_DIR / "data" / "sample_images"

# API & Server Settings
API_TITLE = "PramanSetu (प्रमाण सेतु) — National Evidence Intelligence Gateway"
API_VERSION = "2.1.0"
API_DESCRIPTION = (
    "Production-Hardened AI-Assisted Pre-Approval Multi-Vector Forensic Gateway for Public Infrastructure Claims, "
    "Milestone Verification, and Citizen Social Audits."
)

# CORS Configuration (Environment-controlled allowlist, no wildcard with credentials)
ALLOWED_ORIGINS_ENV = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001")
CORS_ORIGINS: List[str] = [origin.strip() for origin in ALLOWED_ORIGINS_ENV.split(",") if origin.strip()]

# Authentication & JWT Security Settings
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "pramansetu-hardened-institution-hmac-sha256-key-v2")
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Rate Limiting Settings (Requests per minute per IP/identity)
RATE_LIMIT_AUDIT_PER_MIN: int = int(os.getenv("RATE_LIMIT_AUDIT_PER_MIN", "60"))
RATE_LIMIT_CITIZEN_PER_MIN: int = int(os.getenv("RATE_LIMIT_CITIZEN_PER_MIN", "120"))
RATE_LIMIT_VERIFY_PER_MIN: int = int(os.getenv("RATE_LIMIT_VERIFY_PER_MIN", "300"))

# File Security Bounds
MAX_UPLOAD_SIZE_BYTES: int = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", str(15 * 1024 * 1024)))  # 15MB limit
ALLOWED_IMAGE_MIMES: List[str] = ["image/jpeg", "image/png", "image/webp", "image/tiff"]

# Gemini 2.0 Flash Settings
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = "gemini-2.0-flash"
GEMINI_CONFIDENCE_THRESHOLD: float = 0.70

# Geodesic & Spatial Verification Thresholds
MAX_ALLOWED_GEO_DISTANCE_METRES: float = 500.0  # 500m tolerance for worksite corridor
LOCATION_MATCH_TOLERANCE_METRES: float = 500.0
LOCATION_REVIEW_TOLERANCE_METRES: float = 1500.0
EARTH_RADIUS_METRES: float = 6371000.0

# Perceptual Hashing (pHash) Thresholds
PHASH_MATCH_THRESHOLD: int = 5    # <= 5: Flagged asset reuse
PHASH_REVIEW_THRESHOLD: int = 10  # 6-10: Review suspicious similarity

# Geospatial Ground-Truth Anomaly Zones (Mock Satellite Prototype)
FRAUD_ZONES: List[Dict[str, Any]] = [
    {
        "zone_id": "ZONE-UP-001",
        "name": "Demo Fraud Zone - Prayagraj",
        "latitude": 25.4358,
        "longitude": 81.8463,
        "radius_metres": 1000.0,
        "reason": "Satellite earth-observation indicates zero physical construction activity in designated zone."
    },
    {
        "zone_id": "ZONE-DL-002",
        "name": "Demo Fraud Zone - Yamuna Floodplain",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "radius_metres": 2000.0,
        "reason": "Environmental satellite radar detects soil instability & unauthorized sand extraction."
    },
    {
        "zone_id": "ZONE-BR-003",
        "name": "Demo Fraud Zone - Patna Bypass",
        "latitude": 25.5941,
        "longitude": 85.1376,
        "radius_metres": 1500.0,
        "reason": "Multi-spectral imaging confirms stagnant waterlogged terrain unsuitable for bitumen laying."
    }
]

# 10-Vector Composite Risk Weight Table (Total: 235 Points Calibrated Scale)
RISK_WEIGHTS: Dict[str, int] = {
    "duplicate_asset": 40,
    "web_asset_reuse": 40,
    "location_mismatch": 35,
    "ground_truth_anomaly": 30,
    "ghost_worker_muster_roll": 30,
    "material_milestone_mismatch": 25,
    "visual_ai_tampering": 20,
    "chrono_weather_mismatch": 15,
    "unverifiable_gps": 10,
    "file_quality_outlier": 5
}

# Verdict Decision Thresholds
SCORE_CLEAR_MAX: int = 24
SCORE_REVIEW_MAX: int = 59
SCORE_FLAGGED_MIN: int = 60
