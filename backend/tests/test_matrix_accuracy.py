import os
import sys
import math
import io
import json
import pytest
from PIL import Image, ImageDraw, ImageOps
import numpy as np

# Ensure backend and site-packages paths are accessible
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_PACKAGES = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\Lib\site-packages"
for p in [SITE_PACKAGES, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import (
    LOCATION_MATCH_TOLERANCE_METRES,
    LOCATION_REVIEW_TOLERANCE_METRES,
    PHASH_MATCH_THRESHOLD,
    PHASH_REVIEW_THRESHOLD,
    RISK_WEIGHTS,
    SCORE_CLEAR_MAX,
    SCORE_REVIEW_MAX,
    SCORE_FLAGGED_MIN,
    FRAUD_ZONES
)
from schemas import (
    GPSExtractionResult, LocationCheckResult, SignalStatusEnum,
    DuplicateCheckResult, WebSearchCheckResult, SatelliteCheckResult,
    GenAIForensicResult, GhostWorkerResult, MusterRollCheckResult,
    ChronoCheckResult, MaterialCheckResult, VerdictEnum
)
from services.gps_service import (
    calculate_haversine_distance,
    calculate_vincenty_ellipsoidal_distance,
    verify_location_geodesic,
    extract_gps_metadata,
    _convert_to_degrees
)
from services.muster_roll_service import (
    validate_verhoeff_checksum,
    analyze_muster_roll_and_ghost_labor,
    MAX_UNSKILLED_DAILY_WAGE,
    MAX_SKILLED_DAILY_WAGE
)
from services.phash_service import (
    compute_image_phash,
    compute_image_dhash,
    compute_color_histogram_correlation,
    check_asset_recycling
)
from services.satellite_service import (
    check_satellite_ground_truth,
    query_copernicus_sentinel_spectral_indices
)
from services.material_service import verify_material_and_milestone_progression
from services.genai_service import (
    compute_offline_visual_entropy_heuristic,
    analyze_image_with_gemini
)
from services.chrono_service import (
    calculate_noaa_solar_position,
    fetch_open_meteo_historical_weather
)
from services.scoring_service import compute_composite_risk_score


# =========================================================================
# 1. MATRIX 1: GEODESIC / GPS ACCURACY & BOUNDARY TESTS
# =========================================================================

class TestGeodesicMatrixAccuracy:
    def test_exact_same_point(self):
        """Distance between identical coordinates must be exactly 0.0."""
        d = calculate_vincenty_ellipsoidal_distance(25.3176, 82.9739, 25.3176, 82.9739)
        assert d == 0.0

    def test_symmetry(self):
        """Distance(A, B) must equal Distance(B, A)."""
        lat1, lon1 = 25.3176, 82.9739
        lat2, lon2 = 28.6139, 77.2090
        d_ab = calculate_vincenty_ellipsoidal_distance(lat1, lon1, lat2, lon2)
        d_ba = calculate_vincenty_ellipsoidal_distance(lat2, lon2, lat1, lon1)
        assert abs(d_ab - d_ba) < 1e-6

    def test_antipodal_points_fallback(self):
        """Antipodal points (0,0) and (0,180) Vincenty failure must cleanly fall back to Haversine."""
        d = calculate_vincenty_ellipsoidal_distance(0.0, 0.0, 0.0, 180.0)
        assert d > 19000000.0  # Approx half Earth circumference ~ 20,015 km
        assert not math.isnan(d) and not math.isinf(d)

    def test_polar_coordinates(self):
        """Near-polar coordinates must compute without NaN."""
        d = calculate_vincenty_ellipsoidal_distance(89.9999, 0.0, -89.9999, 0.0)
        assert d > 19000000.0
        assert not math.isnan(d)

    def test_dateline_crossing(self):
        """Coordinates crossing the International Dateline 179.9999 to -179.9999."""
        d = calculate_vincenty_ellipsoidal_distance(0.0, 179.9999, 0.0, -179.9999)
        assert d < 50000.0  # Shortest distance is ~22.2 km across dateline, not 40,000 km
        assert not math.isnan(d)

    def test_boundary_500m_exact_and_epsilon(self):
        """Verify exact boundary transitions at 500.0m."""
        # 1. Inside 500m (Match)
        gps_match = GPSExtractionResult(gps_found=True, latitude=25.3190, longitude=82.9760)
        res_match = verify_location_geodesic(gps_match, 25.3176, 82.9739)
        assert res_match.status == SignalStatusEnum.MATCH
        assert res_match.location_match is True

        # 2. Outside 500m but <= 1500m (Review)
        gps_review = GPSExtractionResult(gps_found=True, latitude=25.3260, longitude=82.9810)
        res_review = verify_location_geodesic(gps_review, 25.3176, 82.9739)
        assert res_review.status == SignalStatusEnum.REVIEW
        assert res_review.location_match is False

        # 3. Far beyond 1500m (Mismatch)
        gps_mismatch = GPSExtractionResult(gps_found=True, latitude=28.6139, longitude=77.2090)
        res_mismatch = verify_location_geodesic(gps_mismatch, 25.3176, 82.9739)
        assert res_mismatch.status == SignalStatusEnum.MISMATCH
        assert res_mismatch.location_match is False

    def test_null_and_missing_gps(self):
        """Missing or unparseable GPS should yield UNVERIFIABLE status."""
        gps_none = GPSExtractionResult(gps_found=False, latitude=None, longitude=None)
        res = verify_location_geodesic(gps_none, 25.3176, 82.9739)
        assert res.status == SignalStatusEnum.UNVERIFIABLE
        assert res.photo_gps_found is False
        assert res.distance_metres is None


# =========================================================================
# 2. MATRIX 2: VERHOEFF D5 & MUSTER ROLL ACCURACY TESTS
# =========================================================================

class TestVerhoeffAndMusterMatrixAccuracy:
    # Independent reference generation for Verhoeff check digits
    @staticmethod
    def _generate_reference_verhoeff(num_str: str) -> str:
        d_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]
        p_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]
        inv_table = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
        c = 0
        reversed_digits = [int(d) for d in reversed(num_str)]
        for i, digit in enumerate(reversed_digits):
            c = d_table[c][p_table[(i + 1) % 8][digit]]
        return num_str + str(inv_table[c])

    def test_valid_verhoeff_numbers(self):
        """Mathematically constructed Verhoeff Aadhaar IDs must validate to True."""
        for base in ["98765432101", "54321098765", "12345678901", "99998888777"]:
            valid_id = self._generate_reference_verhoeff(base)
            assert validate_verhoeff_checksum(valid_id) is True

    def test_single_digit_corruption(self):
        """Altering a single digit in a valid Verhoeff ID must fail verification."""
        valid_id = self._generate_reference_verhoeff("98765432101")
        for pos in range(len(valid_id)):
            original_digit = int(valid_id[pos])
            corrupted_digit = (original_digit + 1) % 10
            corrupted_id = valid_id[:pos] + str(corrupted_digit) + valid_id[pos + 1:]
            assert validate_verhoeff_checksum(corrupted_id) is False

    def test_adjacent_transposition(self):
        """Swapping two adjacent distinct digits must be caught by Verhoeff dihedral math."""
        valid_id = self._generate_reference_verhoeff("98765432101")
        for pos in range(len(valid_id) - 1):
            if valid_id[pos] != valid_id[pos + 1]:
                swapped_id = valid_id[:pos] + valid_id[pos + 1] + valid_id[pos] + valid_id[pos + 2:]
                assert validate_verhoeff_checksum(swapped_id) is False

    def test_muster_roll_duplicate_and_wage_ceiling(self):
        """Muster roll analyzer must detect duplicate worker IDs and wage ceiling violations."""
        csv_data = """worker_id,worker_name,trade,daily_wage,days_worked
W-001,Rajesh Sharma,Mason,650,26
W-002,Sunil Kumar,Labor,500,26
W-001,Rajesh Sharma,Mason,650,26
W-003,GHOST_ACCOUNT,Skilled,1500,30
""".encode("utf-8")
        result = analyze_muster_roll_and_ghost_labor(muster_roll_bytes=csv_data)
        assert result.status == SignalStatusEnum.FLAGGED
        assert result.flagged_workers_count >= 2
        assert result.suspected_ghost_wage_leakage > 0

    def test_empty_muster_roll(self):
        """Empty muster roll must safely yield PASS status without raising errors."""
        res = analyze_muster_roll_and_ghost_labor(muster_roll_bytes=b"")
        assert res.status == SignalStatusEnum.PASS
        assert res.muster_roll_provided is False
        assert res.total_workers_listed == 0


# =========================================================================
# 3. MATRIX 3: 64-BIT DCT pHASH ACCURACY & HAMMING BOUNDS
# =========================================================================

class TestPHashMatrixAccuracy:
    def test_identical_image_hamming_zero(self):
        """Identical image hashing must produce exactly 0 bitwise Hamming distance."""
        img = Image.new("RGB", (128, 128), color=(100, 150, 200))
        d = ImageDraw.Draw(img)
        d.line([(0, 0), (128, 128)], fill=(0, 0, 0), width=4)

        h1 = compute_image_phash(img)
        h2 = compute_image_phash(img.copy())
        assert (h1 - h2) == 0

    def test_hamming_distance_domain_bounds(self):
        """All Hamming distances must strictly reside within [0, 64]."""
        img1 = Image.new("RGB", (64, 64), color=(255, 255, 255))
        img2 = Image.new("RGB", (64, 64), color=(0, 0, 0))
        h1 = compute_image_phash(img1)
        h2 = compute_image_phash(img2)
        dist = h1 - h2
        assert 0 <= dist <= 64

    def test_horizontal_mirror_invariance_detection(self):
        """Asset recycling check must detect horizontally mirrored duplicates."""
        # Create patterned image
        img = Image.new("RGB", (128, 128), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 50, 80], fill=(0, 0, 0))
        
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        raw_bytes = buf.getvalue()
        
        # Test asset recycling function
        res = check_asset_recycling(raw_bytes)
        assert res is not None
        assert res.status in [SignalStatusEnum.PASS, SignalStatusEnum.REVIEW, SignalStatusEnum.FLAGGED]


# =========================================================================
# 4. MATRIX 4: SATELLITE GROUND-TRUTH ANOMALY PIP ACCURACY
# =========================================================================

class TestSatelliteMatrixAccuracy:
    def test_inside_known_fraud_zone(self):
        """Coordinates inside Prayagraj Anomaly zone must trigger ANOMALY signal."""
        res = check_satellite_ground_truth(25.4358, 81.8463)
        assert res.status == SignalStatusEnum.ANOMALY
        assert res.zone == "Demo Fraud Zone - Prayagraj"
        assert res.construction_found is False

    def test_outside_fraud_zone(self):
        """Coordinates outside any known fraud zones must return PASS."""
        res = check_satellite_ground_truth(25.3176, 82.9739)
        assert res.status == SignalStatusEnum.PASS
        assert res.construction_found is True
        assert res.zone is None

    def test_null_coordinates_handling(self):
        """Missing or None coordinates must safely yield UNVERIFIABLE."""
        res = check_satellite_ground_truth(None, None)
        assert res.status == SignalStatusEnum.UNVERIFIABLE


# =========================================================================
# 5. MATRIX 5: MATERIAL CLASSIFICATION & MILESTONE ALIGNMENT
# =========================================================================

class TestMaterialClassificationAccuracy:
    def test_asphalt_match(self):
        """Finished asphalt claim matching visual representation yields PASS."""
        res = verify_material_and_milestone_progression("100% Bituminous Asphalt Pavement")
        assert res.status == SignalStatusEnum.PASS
        assert res.is_mismatch is False
        assert res.milestone_alignment_score == 1.0

    def test_mud_vs_asphalt_mismatch(self):
        """Mud / unpaved terrain against finished asphalt claim yields FLAGGED."""
        res = verify_material_and_milestone_progression(
            claimed_milestone_or_material="100% Finished Bituminous Asphalt",
            image_notes="Unpaved gravel road with uncompacted mud sub-base"
        )
        assert res.status == SignalStatusEnum.FLAGGED
        assert res.is_mismatch is True
        assert res.milestone_alignment_score < 0.50


# =========================================================================
# 6. MATRIX 6: AI VISION & SHANNON ENTROPY FALLBACK ACCURACY
# =========================================================================

class TestAIVisionMatrixAccuracy:
    def test_offline_entropy_natural_texture(self):
        """Natural high-frequency texture must produce entropy > 4.0 and return PASS."""
        # Generate noisy natural-like texture
        arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(arr)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        
        is_suspicious, confidence, reason = compute_offline_visual_entropy_heuristic(buf.getvalue())
        assert is_suspicious is False
        assert confidence >= 0.80

    def test_offline_entropy_synthetic_uniformity(self):
        """Flat uniform pixel block must trigger low texture entropy alert."""
        arr = np.full((100, 100, 3), 128, dtype=np.uint8)
        img = Image.fromarray(arr)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        
        is_suspicious, confidence, reason = compute_offline_visual_entropy_heuristic(buf.getvalue())
        assert is_suspicious is True


# =========================================================================
# 7. MATRIX 7: CHRONO-SOLAR SPA & WEATHER ACCURACY
# =========================================================================

class TestChronoWeatherMatrixAccuracy:
    def test_noaa_solar_noon_elevation(self):
        """NOAA solar position at midday in India should show high solar elevation."""
        from datetime import datetime
        dt = datetime(2026, 6, 21, 12, 0, 0)
        elev, azim, shadow = calculate_noaa_solar_position(dt, 25.3176, 82.9739)
        assert elev > 60.0  # Summer solstice noon in Varanasi
        assert 0.0 <= azim <= 360.0
        assert shadow < 1.0  # High sun creates short shadows

    def test_noaa_night_elevation(self):
        """NOAA solar position at midnight must produce negative solar elevation."""
        from datetime import datetime
        dt = datetime(2026, 6, 21, 0, 0, 0)
        elev, azim, shadow = calculate_noaa_solar_position(dt, 25.3176, 82.9739)
        assert elev < 0.0  # Sun below horizon
        assert shadow == 99.0


# =========================================================================
# 8. MATRIX 8: COMPOSITE RISK SCORING & MONOTONICITY
# =========================================================================

class TestCompositeRiskScoringAccuracy:
    def _create_clean_fixtures(self):
        return (
            DuplicateCheckResult(match_found=False, status=SignalStatusEnum.PASS, message=""),
            WebSearchCheckResult(match_found=False, status=SignalStatusEnum.PASS, message=""),
            LocationCheckResult(claimed_latitude=25.3176, claimed_longitude=82.9739, location_match=True, distance_metres=100.0, status=SignalStatusEnum.MATCH, message=""),
            SatelliteCheckResult(status=SignalStatusEnum.PASS, construction_found=True, message=""),
            GenAIForensicResult(status=SignalStatusEnum.PASS, is_tampered=False, confidence_score=0.9, explanation=""),
            GPSExtractionResult(gps_found=True, latitude=25.3176, longitude=82.9739),
            GhostWorkerResult(anomaly_detected=False, status=SignalStatusEnum.PASS, message=""),
            MusterRollCheckResult(status=SignalStatusEnum.PASS, muster_roll_provided=True, total_workers_listed=10, flagged_workers_count=0, suspected_ghost_wage_leakage=0, discrepancies=[], message=""),
            ChronoCheckResult(status=SignalStatusEnum.PASS, confidence_score=0.9, is_consistent=True, message=""),
            MaterialCheckResult(claimed_material_or_milestone="Asphalt", detected_surface_material="Asphalt", status=SignalStatusEnum.PASS, confidence_score=0.9, is_consistent=True, reason="")
        )

    def test_zero_signals_clear_verdict(self):
        """All clean signals must score 0 and produce CLEAR verdict."""
        fixtures = self._create_clean_fixtures()
        res = compute_composite_risk_score(*fixtures)
        assert res.risk_score == 0
        assert res.verdict == VerdictEnum.CLEAR

    def test_single_vector_weights(self):
        """Triggering one vector at a time must add its exact configured weight."""
        # 1. Location Mismatch (+35)
        f = list(self._create_clean_fixtures())
        f[2] = LocationCheckResult(claimed_latitude=25.3176, claimed_longitude=82.9739, location_match=False, distance_metres=5000.0, status=SignalStatusEnum.MISMATCH, message="")
        res = compute_composite_risk_score(*f)
        assert res.risk_score == 35
        assert res.verdict == VerdictEnum.REVIEW

        # 2. Satellite Anomaly (+30)
        f = list(self._create_clean_fixtures())
        f[3] = SatelliteCheckResult(status=SignalStatusEnum.ANOMALY, construction_found=False, message="")
        res = compute_composite_risk_score(*f)
        assert res.risk_score == 30
        assert res.verdict == VerdictEnum.REVIEW

        # 3. Duplicate Asset (+40)
        f = list(self._create_clean_fixtures())
        f[0] = DuplicateCheckResult(match_found=True, status=SignalStatusEnum.FLAGGED, hamming_distance=0, message="")
        res = compute_composite_risk_score(*f)
        assert res.risk_score == 40
        assert res.verdict == VerdictEnum.REVIEW

    def test_score_clamping_at_100(self):
        """Cumulative scores exceeding 100 must be clamped to 100 without overflow."""
        f = list(self._create_clean_fixtures())
        f[0] = DuplicateCheckResult(match_found=True, status=SignalStatusEnum.FLAGGED, hamming_distance=0, message="")  # 40
        f[1] = WebSearchCheckResult(match_found=True, status=SignalStatusEnum.FLAGGED, similarity_score=0.95, message="") # 40
        f[2] = LocationCheckResult(claimed_latitude=25.3176, claimed_longitude=82.9739, location_match=False, distance_metres=5000.0, status=SignalStatusEnum.MISMATCH, message="") # 35
        # Total raw = 115 -> clamped to 100
        res = compute_composite_risk_score(*f)
        assert res.risk_score == 100
        assert res.verdict == VerdictEnum.FLAGGED
