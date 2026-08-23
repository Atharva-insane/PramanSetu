import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.scoring_service import compute_composite_risk_score
from schemas import (
    DuplicateCheckResult,
    WebSearchCheckResult,
    LocationCheckResult,
    SatelliteCheckResult,
    GenAIForensicResult,
    GPSExtractionResult,
    GhostWorkerResult,
    MusterRollCheckResult,
    ChronoCheckResult,
    MaterialCheckResult,
    VerdictEnum,
    SignalStatusEnum
)


def test_scoring_clean_project():
    res = compute_composite_risk_score(
        duplicate_res=DuplicateCheckResult(match_found=False, status=SignalStatusEnum.PASS),
        web_res=WebSearchCheckResult(match_found=False, status=SignalStatusEnum.PASS),
        location_res=LocationCheckResult(photo_gps_found=True, claimed_latitude=25.3, claimed_longitude=82.9, distance_metres=50, status=SignalStatusEnum.MATCH),
        satellite_res=SatelliteCheckResult(status=SignalStatusEnum.PASS, construction_found=True),
        genai_res=GenAIForensicResult(status=SignalStatusEnum.PASS, is_suspicious=False),
        gps_res=GPSExtractionResult(gps_found=True, latitude=25.3, longitude=82.9),
        ghost_worker_res=GhostWorkerResult(quality_check={"status": "PASS"}),
        muster_res=MusterRollCheckResult(status=SignalStatusEnum.PASS),
        chrono_res=ChronoCheckResult(status=SignalStatusEnum.PASS),
        material_res=MaterialCheckResult(claimed_material_or_milestone="Asphalt", detected_surface_material="Asphalt", status=SignalStatusEnum.PASS)
    )
    assert res.risk_score == 0
    assert res.verdict == VerdictEnum.CLEAR
    assert "routine" in res.recommended_action.lower()


def test_scoring_high_risk_flagged_project():
    res = compute_composite_risk_score(
        duplicate_res=DuplicateCheckResult(match_found=True, status=SignalStatusEnum.FLAGGED, hamming_distance=2),
        web_res=WebSearchCheckResult(match_found=False, status=SignalStatusEnum.PASS),
        location_res=LocationCheckResult(photo_gps_found=True, claimed_latitude=25.3, claimed_longitude=82.9, distance_metres=14000, status=SignalStatusEnum.MISMATCH),
        satellite_res=SatelliteCheckResult(status=SignalStatusEnum.ANOMALY, zone="Demo Fraud Zone", construction_found=False),
        genai_res=GenAIForensicResult(status=SignalStatusEnum.PASS),
        gps_res=GPSExtractionResult(gps_found=True, latitude=28.6, longitude=77.2),
        ghost_worker_res=GhostWorkerResult(quality_check={"status": "PASS"}),
        muster_res=MusterRollCheckResult(status=SignalStatusEnum.PASS),
        chrono_res=ChronoCheckResult(status=SignalStatusEnum.PASS),
        material_res=MaterialCheckResult(claimed_material_or_milestone="Asphalt", detected_surface_material="Asphalt", status=SignalStatusEnum.PASS)
    )
    # Duplicate (40) + Location Mismatch (35) + Satellite Anomaly (30) = 100 (clamped)
    assert res.risk_score == 100
    assert res.verdict == VerdictEnum.FLAGGED
    assert "freeze" in res.recommended_action.lower() or "hold" in res.recommended_action.lower()
