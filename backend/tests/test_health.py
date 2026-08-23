import sys
import os
from pathlib import Path

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config import (
    CORS_ORIGINS,
    RISK_WEIGHTS,
    SCORE_CLEAR_MAX,
    SCORE_REVIEW_MAX,
    SCORE_FLAGGED_MIN,
    FRAUD_ZONES
)
from schemas import (
    VerdictEnum,
    SignalStatusEnum,
    RiskAssessment,
    HealthResponse,
    AuditResponse
)
from services.gps_service import calculate_haversine_distance


def test_config_and_scoring_weights():
    assert "http://localhost:3000" in CORS_ORIGINS
    assert RISK_WEIGHTS["duplicate_asset"] == 40
    assert RISK_WEIGHTS["location_mismatch"] == 35
    assert RISK_WEIGHTS["ground_truth_anomaly"] == 30
    assert RISK_WEIGHTS["visual_ai_tampering"] == 20
    assert RISK_WEIGHTS["unverifiable_gps"] == 10
    assert RISK_WEIGHTS["file_quality_outlier"] == 5
    assert SCORE_CLEAR_MAX == 24
    assert SCORE_REVIEW_MAX == 59
    assert SCORE_FLAGGED_MIN == 60
    assert len(FRAUD_ZONES) >= 1


def test_haversine_distance_calculation():
    # Same point distance should be 0
    d0 = calculate_haversine_distance(25.4358, 81.8463, 25.4358, 81.8463)
    assert round(d0, 1) == 0.0

    # Distance between Prayagraj and Delhi (~570km)
    d_delhi = calculate_haversine_distance(25.4358, 81.8463, 28.6139, 77.2090)
    assert 500000 < d_delhi < 700000


def test_schemas_instantiation():
    health = HealthResponse(
        status="operational",
        version="2.0.0",
        service="PramanSetu (प्रमाण सेतु) Multi-Vector Forensic Gateway",
        gemini_configured=False,
        anomaly_zones_count=2,
        mock_db_records=5,
        mock_web_db_records=3,
        contractors_count=3
    )
    assert health.status == "operational"
    assert health.mock_db_records == 5
    assert health.mock_web_db_records == 3
    assert health.contractors_count == 3


if __name__ == "__main__":
    test_config_and_scoring_weights()
    test_haversine_distance_calculation()
    test_schemas_instantiation()
    print("All Phase 1 foundational tests PASSED successfully!")
