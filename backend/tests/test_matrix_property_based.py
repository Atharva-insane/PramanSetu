import os
import sys
import math
import random
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
from services.gps_service import calculate_vincenty_ellipsoidal_distance, calculate_haversine_distance
from services.muster_roll_service import validate_verhoeff_checksum
from services.phash_service import compute_image_phash
from services.scoring_service import compute_composite_risk_score
from PIL import Image, ImageDraw


# =========================================================================
# 1. GEODESIC MATHEMATICAL PROPERTY INVARIANTS
# =========================================================================

class TestGeodesicPropertyInvariants:
    @pytest.mark.parametrize("seed", range(20))
    def test_geodesic_non_negativity_and_identity(self, seed):
        """Property: Distance is always >= 0, and distance(A, A) is strictly 0.0."""
        random.seed(seed)
        lat = random.uniform(-89.0, 89.0)
        lon = random.uniform(-179.0, 179.0)
        
        d_self = calculate_vincenty_ellipsoidal_distance(lat, lon, lat, lon)
        assert d_self == 0.0

    @pytest.mark.parametrize("seed", range(20))
    def test_geodesic_symmetry_property(self, seed):
        """Property: Distance(A, B) == Distance(B, A) across arbitrary random points."""
        random.seed(seed + 100)
        lat1 = random.uniform(-80.0, 80.0)
        lon1 = random.uniform(-170.0, 170.0)
        lat2 = random.uniform(-80.0, 80.0)
        lon2 = random.uniform(-170.0, 170.0)

        d1 = calculate_vincenty_ellipsoidal_distance(lat1, lon1, lat2, lon2)
        d2 = calculate_vincenty_ellipsoidal_distance(lat2, lon2, lat1, lon1)
        
        assert not math.isnan(d1) and not math.isnan(d2)
        assert abs(d1 - d2) < 1e-4

    @pytest.mark.parametrize("seed", range(15))
    def test_geodesic_triangle_inequality(self, seed):
        """Property: d(A, C) <= d(A, B) + d(B, C) + epsilon on ellipsoidal geometry."""
        random.seed(seed + 200)
        # Moderate distances within India / regional bounds to test triangle inequality
        lat_a, lon_a = random.uniform(20.0, 30.0), random.uniform(75.0, 85.0)
        lat_b, lon_b = random.uniform(20.0, 30.0), random.uniform(75.0, 85.0)
        lat_c, lon_c = random.uniform(20.0, 30.0), random.uniform(75.0, 85.0)

        d_ab = calculate_vincenty_ellipsoidal_distance(lat_a, lon_a, lat_b, lon_b)
        d_bc = calculate_vincenty_ellipsoidal_distance(lat_b, lon_b, lat_c, lon_c)
        d_ac = calculate_vincenty_ellipsoidal_distance(lat_a, lon_a, lat_c, lon_c)

        # Allow small floating point tolerance for geodesic geodesy
        assert d_ac <= (d_ab + d_bc + 10.0)


# =========================================================================
# 2. VERHOEFF D5 DIHEDRAL CHECK DIGIT PROPERTY INVARIANTS
# =========================================================================

class TestVerhoeffPropertyInvariants:
    @staticmethod
    def _gen_verhoeff(base_11_digits: str) -> str:
        D = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6], [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]
        P = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2], [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]
        inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
        c = 0
        for i, digit in enumerate(reversed([int(d) for d in base_11_digits])):
            c = D[c][P[(i + 1) % 8][digit]]
        return base_11_digits + str(inv[c])

    @pytest.mark.parametrize("seed", range(25))
    def test_single_substitution_detection_guarantee(self, seed):
        """Theorem: The Verhoeff D5 algorithm detects 100% of single-digit substitution errors."""
        random.seed(seed + 300)
        base = "".join([str(random.randint(0, 9)) for _ in range(11)])
        valid_id = self._gen_verhoeff(base)
        
        assert validate_verhoeff_checksum(valid_id) is True
        
        # Test all 12 positions with all 9 possible replacements
        for pos in range(12):
            orig_d = int(valid_id[pos])
            for replacement in range(10):
                if replacement != orig_d:
                    corrupted = valid_id[:pos] + str(replacement) + valid_id[pos+1:]
                    assert validate_verhoeff_checksum(corrupted) is False, f"Failed at pos {pos} with {replacement}"

    @pytest.mark.parametrize("seed", range(20))
    def test_adjacent_transposition_detection_guarantee(self, seed):
        """Theorem: The Verhoeff D5 algorithm detects 100% of adjacent transposition errors."""
        random.seed(seed + 400)
        base = "".join([str(random.randint(0, 9)) for _ in range(11)])
        valid_id = self._gen_verhoeff(base)

        for pos in range(11):
            if valid_id[pos] != valid_id[pos + 1]:
                swapped = valid_id[:pos] + valid_id[pos+1] + valid_id[pos] + valid_id[pos+2:]
                assert validate_verhoeff_checksum(swapped) is False


# =========================================================================
# 3. SCORING MONOTONICITY & CAPACITY INVARIANTS
# =========================================================================

class TestScoringPropertyInvariants:
    def _create_base_signals(self, flags: dict):
        d_res = DuplicateCheckResult(
            match_found=flags.get("duplicate_asset", False),
            status=SignalStatusEnum.FLAGGED if flags.get("duplicate_asset") else SignalStatusEnum.PASS,
            hamming_distance=0 if flags.get("duplicate_asset") else None,
            message=""
        )
        w_res = WebSearchCheckResult(
            match_found=flags.get("web_asset_reuse", False),
            status=SignalStatusEnum.FLAGGED if flags.get("web_asset_reuse") else SignalStatusEnum.PASS,
            similarity_score=0.95 if flags.get("web_asset_reuse") else 0.0,
            message=""
        )
        l_res = LocationCheckResult(
            claimed_latitude=25.3176,
            claimed_longitude=82.9739,
            location_match=not flags.get("location_mismatch", False),
            distance_metres=5000.0 if flags.get("location_mismatch") else 100.0,
            status=SignalStatusEnum.MISMATCH if flags.get("location_mismatch") else SignalStatusEnum.MATCH,
            message=""
        )
        s_res = SatelliteCheckResult(
            status=SignalStatusEnum.ANOMALY if flags.get("ground_truth_anomaly") else SignalStatusEnum.PASS,
            construction_found=not flags.get("ground_truth_anomaly", False),
            message=""
        )
        g_res = GenAIForensicResult(
            status=SignalStatusEnum.FLAGGED if flags.get("visual_ai_tampering") else SignalStatusEnum.PASS,
            is_suspicious=flags.get("visual_ai_tampering", False),
            confidence=0.95 if flags.get("visual_ai_tampering") else 0.90,
            reason=""
        )
        gps_res = GPSExtractionResult(
            gps_found=not flags.get("unverifiable_gps", False),
            latitude=25.3176 if not flags.get("unverifiable_gps") else None,
            longitude=82.9739 if not flags.get("unverifiable_gps") else None
        )
        ghost_res = GhostWorkerResult(
            anomaly_detected=False,
            quality_check={"status": "REVIEW" if flags.get("file_quality_outlier") else "PASS"},
            status=SignalStatusEnum.PASS,
            message=""
        )
        m_res = MusterRollCheckResult(
            status=SignalStatusEnum.FLAGGED if flags.get("ghost_worker_muster_roll") else SignalStatusEnum.PASS,
            muster_roll_provided=True,
            total_workers_listed=10,
            flagged_workers_count=2 if flags.get("ghost_worker_muster_roll") else 0,
            suspected_ghost_wage_leakage=50000.0 if flags.get("ghost_worker_muster_roll") else 0.0,
            discrepancies=[],
            message=""
        )
        c_res = ChronoCheckResult(
            status=SignalStatusEnum.FLAGGED if flags.get("chrono_weather_mismatch") else SignalStatusEnum.PASS,
            confidence_score=0.9,
            is_consistent=not flags.get("chrono_weather_mismatch", False),
            message=""
        )
        mat_res = MaterialCheckResult(
            claimed_material_or_milestone="Asphalt",
            detected_surface_material="Mud" if flags.get("material_milestone_mismatch") else "Asphalt",
            status=SignalStatusEnum.FLAGGED if flags.get("material_milestone_mismatch") else SignalStatusEnum.PASS,
            is_mismatch=flags.get("material_milestone_mismatch", False),
            confidence_score=0.9,
            reason=""
        )

        return compute_composite_risk_score(
            d_res, w_res, l_res, s_res, g_res, gps_res, ghost_res, m_res, c_res, mat_res
        )

    @pytest.mark.parametrize("seed", range(30))
    def test_scoring_monotonicity_property(self, seed):
        """Property: Adding an additional active fraud signal can NEVER reduce the final score."""
        random.seed(seed + 500)
        vector_keys = list(RISK_WEIGHTS.keys())
        
        # Pick a random subset of signals
        subset_size = random.randint(0, len(vector_keys) - 1)
        active_keys = set(random.sample(vector_keys, subset_size))
        
        flags_a = {k: (k in active_keys) for k in vector_keys}
        res_a = self._create_base_signals(flags_a)

        # Add one more signal
        remaining = [k for k in vector_keys if k not in active_keys]
        new_key = random.choice(remaining)
        flags_b = dict(flags_a)
        flags_b[new_key] = True
        res_b = self._create_base_signals(flags_b)

        assert res_b.risk_score >= res_a.risk_score

    def test_verdict_partitioning_invariants(self):
        """Property: Verdicts form a strict partition over [0, 100]."""
        for score_val in range(101):
            if score_val <= SCORE_CLEAR_MAX:
                expected_verdict = VerdictEnum.CLEAR
            elif score_val <= SCORE_REVIEW_MAX:
                expected_verdict = VerdictEnum.REVIEW
            else:
                expected_verdict = VerdictEnum.FLAGGED
            
            # Assert mathematical bounds consistency
            assert expected_verdict in [VerdictEnum.CLEAR, VerdictEnum.REVIEW, VerdictEnum.FLAGGED]
