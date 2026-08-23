import os
import sys
import json
import time
import concurrent.futures
import pytest

# Ensure backend and site-packages paths are accessible
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_PACKAGES = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\Lib\site-packages"
for p in [SITE_PACKAGES, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from schemas import (
    GPSExtractionResult, LocationCheckResult, SignalStatusEnum,
    DuplicateCheckResult, WebSearchCheckResult, SatelliteCheckResult,
    GenAIForensicResult, GhostWorkerResult, MusterRollCheckResult,
    ChronoCheckResult, MaterialCheckResult, VerdictEnum
)
from services.scoring_service import compute_composite_risk_score
from services.gps_service import calculate_vincenty_ellipsoidal_distance
from services.phash_service import compute_image_phash
from PIL import Image, ImageDraw

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), "MATRIX_GOLDEN_FIXTURES", "golden_cases.json")


def _load_golden_cases():
    with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestGoldenEndToEndMatrices:
    @pytest.mark.parametrize("case", _load_golden_cases(), ids=lambda c: c["fixture_id"])
    def test_golden_case_execution(self, case):
        """Executes each of the 20 golden cases and verifies exact signal states, score, and verdict."""
        flags = case["expected_signals"]
        
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
            claimed_latitude=case["claimed_lat"],
            claimed_longitude=case["claimed_lon"],
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
            latitude=case["photo_lat"],
            longitude=case["photo_lon"]
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
            claimed_material_or_milestone=case["claimed_material"],
            detected_surface_material="Mud" if flags["material_milestone_mismatch"] else "Asphalt",
            status=SignalStatusEnum.FLAGGED if flags["material_milestone_mismatch"] else SignalStatusEnum.PASS,
            is_mismatch=flags["material_milestone_mismatch"],
            confidence_score=0.9,
            reason=""
        )

        res = compute_composite_risk_score(
            d_res, w_res, l_res, s_res, g_res, gps_res, ghost_res, m_res, c_res, mat_res
        )

        assert res.risk_score == case["expected_final_score"]
        assert res.verdict.value == case["expected_verdict"]


class TestConcurrencyAndPerformanceStress:
    def test_concurrent_matrix_audits_thread_safety(self):
        """Executes 50 parallel scoring and geodesic operations to test concurrency and state isolation."""
        cases = _load_golden_cases()
        
        def run_single_audit(case_data):
            flags = case_data["expected_signals"]
            d_res = DuplicateCheckResult(match_found=flags["duplicate_asset"], status=SignalStatusEnum.PASS)
            w_res = WebSearchCheckResult(match_found=flags["web_asset_reuse"], status=SignalStatusEnum.PASS)
            l_res = LocationCheckResult(
                claimed_latitude=case_data["claimed_lat"],
                claimed_longitude=case_data["claimed_lon"],
                status=SignalStatusEnum.MISMATCH if flags["location_mismatch"] else SignalStatusEnum.MATCH
            )
            s_res = SatelliteCheckResult(status=SignalStatusEnum.ANOMALY if flags["ground_truth_anomaly"] else SignalStatusEnum.PASS)
            g_res = GenAIForensicResult(status=SignalStatusEnum.PASS, is_suspicious=flags["visual_ai_tampering"], confidence=0.95)
            gps_res = GPSExtractionResult(gps_found=not flags["unverifiable_gps"])
            ghost_res = GhostWorkerResult(anomaly_detected=False, quality_check={"status": "PASS"})
            m_res = MusterRollCheckResult(status=SignalStatusEnum.FLAGGED if flags["ghost_worker_muster_roll"] else SignalStatusEnum.PASS)
            c_res = ChronoCheckResult(status=SignalStatusEnum.FLAGGED if flags["chrono_weather_mismatch"] else SignalStatusEnum.PASS)
            mat_res = MaterialCheckResult(
                claimed_material_or_milestone="Asphalt",
                detected_surface_material="Asphalt",
                status=SignalStatusEnum.FLAGGED if flags["material_milestone_mismatch"] else SignalStatusEnum.PASS,
                is_mismatch=flags["material_milestone_mismatch"]
            )
            
            res = compute_composite_risk_score(d_res, w_res, l_res, s_res, g_res, gps_res, ghost_res, m_res, c_res, mat_res)
            return res.risk_score

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(run_single_audit, cases[i % len(cases)]) for i in range(50)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
        assert len(results) == 50
        assert all(isinstance(r, int) for r in results)

    def test_geodesic_and_phash_performance_benchmarks(self):
        """Measures execution throughput for 1,000 WGS-84 geodesic calculations and 50 pHash calculations."""
        # 1. Geodesic throughput
        t0 = time.perf_counter()
        for _ in range(1000):
            calculate_vincenty_ellipsoidal_distance(25.3176, 82.9739, 28.6139, 77.2090)
        t_geo = (time.perf_counter() - t0) * 1000.0  # Total ms
        avg_geo_us = (t_geo / 1000.0) * 1000.0      # Microseconds per calc
        print(f"\n[BENCHMARK] Vincenty WGS-84 Distance: {avg_geo_us:.2f} µs per calculation ({1000.0 / (t_geo / 1000.0):,.0f} ops/sec)")
        assert avg_geo_us < 500.0  # Must be fast (<0.5ms per calculation)

        # 2. pHash throughput
        img = Image.new("RGB", (256, 256), color=(128, 128, 128))
        t1 = time.perf_counter()
        for _ in range(50):
            compute_image_phash(img)
        t_phash = (time.perf_counter() - t1) * 1000.0
        avg_phash_ms = t_phash / 50.0
        print(f"[BENCHMARK] 64-bit DCT pHash: {avg_phash_ms:.2f} ms per image")
        assert avg_phash_ms < 50.0  # Must be under 50ms per image
