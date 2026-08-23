import os
import sys
import pytest

# Ensure backend and site-packages paths are accessible
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_PACKAGES = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\Lib\site-packages"
for p in [SITE_PACKAGES, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import RISK_WEIGHTS, SCORE_CLEAR_MAX, SCORE_REVIEW_MAX, SCORE_FLAGGED_MIN
from schemas import (
    GPSExtractionResult, LocationCheckResult, SignalStatusEnum,
    DuplicateCheckResult, WebSearchCheckResult, SatelliteCheckResult,
    GenAIForensicResult, GhostWorkerResult, MusterRollCheckResult,
    ChronoCheckResult, MaterialCheckResult, VerdictEnum
)
from services.scoring_service import compute_composite_risk_score

VECTOR_ORDER = [
    ("duplicate_asset", 40),
    ("web_asset_reuse", 40),
    ("location_mismatch", 35),
    ("ground_truth_anomaly", 30),
    ("ghost_worker_muster_roll", 30),
    ("material_milestone_mismatch", 25),
    ("visual_ai_tampering", 20),
    ("chrono_weather_mismatch", 15),
    ("unverifiable_gps", 10),
    ("file_quality_outlier", 5)
]


def _build_and_evaluate_combination(mask: int):
    """
    Evaluates a specific binary signal combination mask (0 to 1023)
    against the backend scoring engine and an independent mathematical oracle.
    """
    flags = {}
    expected_raw_score = 0

    for bit_idx, (vec_name, weight) in enumerate(VECTOR_ORDER):
        is_active = bool((mask >> bit_idx) & 1)
        flags[vec_name] = is_active
        if is_active:
            expected_raw_score += weight

    expected_clamped_score = min(100, max(0, expected_raw_score))

    if expected_clamped_score <= SCORE_CLEAR_MAX:
        expected_verdict = VerdictEnum.CLEAR
    elif expected_clamped_score <= SCORE_REVIEW_MAX:
        expected_verdict = VerdictEnum.REVIEW
    else:
        expected_verdict = VerdictEnum.FLAGGED

    # Construct vector result objects
    d_res = DuplicateCheckResult(
        match_found=flags["duplicate_asset"],
        status=SignalStatusEnum.FLAGGED if flags["duplicate_asset"] else SignalStatusEnum.PASS,
        hamming_distance=0 if flags["duplicate_asset"] else None,
        message=""
    )
    w_res = WebSearchCheckResult(
        match_found=flags["web_asset_reuse"],
        status=SignalStatusEnum.FLAGGED if flags["web_asset_reuse"] else SignalStatusEnum.PASS,
        similarity_score=0.95 if flags["web_asset_reuse"] else 0.0,
        message=""
    )
    l_res = LocationCheckResult(
        claimed_latitude=25.3176,
        claimed_longitude=82.9739,
        location_match=not flags["location_mismatch"],
        distance_metres=5000.0 if flags["location_mismatch"] else 100.0,
        status=SignalStatusEnum.MISMATCH if flags["location_mismatch"] else SignalStatusEnum.MATCH,
        message=""
    )
    s_res = SatelliteCheckResult(
        status=SignalStatusEnum.ANOMALY if flags["ground_truth_anomaly"] else SignalStatusEnum.PASS,
        construction_found=not flags["ground_truth_anomaly"],
        message=""
    )
    g_res = GenAIForensicResult(
        status=SignalStatusEnum.FLAGGED if flags["visual_ai_tampering"] else SignalStatusEnum.PASS,
        is_suspicious=flags["visual_ai_tampering"],
        confidence=0.95 if flags["visual_ai_tampering"] else 0.90,
        reason=""
    )
    gps_res = GPSExtractionResult(
        gps_found=not flags["unverifiable_gps"],
        latitude=25.3176 if not flags["unverifiable_gps"] else None,
        longitude=82.9739 if not flags["unverifiable_gps"] else None
    )
    ghost_res = GhostWorkerResult(
        anomaly_detected=False,
        quality_check={"status": "REVIEW" if flags["file_quality_outlier"] else "PASS"},
        status=SignalStatusEnum.PASS,
        message=""
    )
    m_res = MusterRollCheckResult(
        status=SignalStatusEnum.FLAGGED if flags["ghost_worker_muster_roll"] else SignalStatusEnum.PASS,
        muster_roll_provided=True,
        total_workers_listed=10,
        flagged_workers_count=2 if flags["ghost_worker_muster_roll"] else 0,
        suspected_ghost_wage_leakage=50000.0 if flags["ghost_worker_muster_roll"] else 0.0,
        discrepancies=[],
        message=""
    )
    c_res = ChronoCheckResult(
        status=SignalStatusEnum.FLAGGED if flags["chrono_weather_mismatch"] else SignalStatusEnum.PASS,
        confidence_score=0.9,
        is_consistent=not flags["chrono_weather_mismatch"],
        message=""
    )
    mat_res = MaterialCheckResult(
        claimed_material_or_milestone="Asphalt",
        detected_surface_material="Mud" if flags["material_milestone_mismatch"] else "Asphalt",
        status=SignalStatusEnum.FLAGGED if flags["material_milestone_mismatch"] else SignalStatusEnum.PASS,
        is_mismatch=flags["material_milestone_mismatch"],
        confidence_score=0.9,
        reason=""
    )

    actual_res = compute_composite_risk_score(
        d_res, w_res, l_res, s_res, g_res, gps_res, ghost_res, m_res, c_res, mat_res
    )

    return expected_raw_score, expected_clamped_score, expected_verdict, actual_res


class TestAll1024CombinatorialScoring:
    def test_all_1024_signal_combinations_exhaustive(self):
        """
        Exhaustively iterates over all 2^10 = 1,024 combinatorial states
        and verifies independent oracle calculation vs backend engine.
        """
        passed_count = 0
        total_count = 1024

        verdict_counts = {
            VerdictEnum.CLEAR: 0,
            VerdictEnum.REVIEW: 0,
            VerdictEnum.FLAGGED: 0
        }

        for mask in range(total_count):
            expected_raw, expected_clamped, expected_verdict, actual_res = _build_and_evaluate_combination(mask)

            assert actual_res.risk_score == expected_clamped, (
                f"Combination mask {mask} (binary: {bin(mask)}) score mismatch: "
                f"Expected {expected_clamped}, got {actual_res.risk_score}"
            )
            assert actual_res.verdict == expected_verdict, (
                f"Combination mask {mask} verdict mismatch: "
                f"Expected {expected_verdict}, got {actual_res.verdict}"
            )

            verdict_counts[actual_res.verdict] += 1
            passed_count += 1

        assert passed_count == total_count
        # Ensure that all 3 verdict classes are actively represented across the domain
        assert verdict_counts[VerdictEnum.CLEAR] > 0
        assert verdict_counts[VerdictEnum.REVIEW] > 0
        assert verdict_counts[VerdictEnum.FLAGGED] > 0
        print(f"\n[COMBINATORIAL COMPLETE] Tested {passed_count}/1024 states: CLEAR={verdict_counts[VerdictEnum.CLEAR]}, REVIEW={verdict_counts[VerdictEnum.REVIEW]}, FLAGGED={verdict_counts[VerdictEnum.FLAGGED]}")
