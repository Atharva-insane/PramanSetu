import os
import sys

# Add site-packages and backend directories before any third-party imports
SITE_PACKAGES = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\Lib\site-packages"
PARENT_DIR = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI"
CIVIC_DIR = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI"
BACKEND_DIR = r"C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\backend"

for p in [SITE_PACKAGES, PARENT_DIR, CIVIC_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

import json
import io
import math
from PIL import Image, ImageDraw

from schemas import (
    GPSExtractionResult, SignalStatusEnum, DuplicateCheckResult,
    WebSearchCheckResult, LocationCheckResult, SatelliteCheckResult,
    GenAIForensicResult, GhostWorkerResult, MusterRollCheckResult,
    ChronoCheckResult, MaterialCheckResult
)
from services.gps_service import calculate_vincenty_ellipsoidal_distance, verify_location_geodesic
from services.muster_roll_service import validate_verhoeff_checksum, analyze_muster_roll_and_ghost_labor
from services.phash_service import compute_image_phash
from services.satellite_service import check_satellite_ground_truth
from services.scoring_service import compute_composite_risk_score, RISK_WEIGHTS

print("=" * 80)
print(" PRAMANSETU (CIVICAUDIT AI) - PRECISION MATRIX ACCURACY AUDIT")
print("=" * 80)

# =========================================================================
# MATRIX 1: WGS-84 VINCENTY GEODESIC DISTANCE & THRESHOLD ACCURACY
# =========================================================================
print("\n[TEST 1] WGS-84 Geodesic Distance Matrix & Boundary Thresholds:")
# 1.1 Match <= 500m
gps_1 = GPSExtractionResult(gps_found=True, latitude=25.3190, longitude=82.9760)
geo_res_1 = verify_location_geodesic(gps_1, 25.3176, 82.9739)
print(f"  * Boundary 1 (<500m): Calc Distance = {geo_res_1.distance_metres:.1f}m | Match = {geo_res_1.location_match} | Status = {geo_res_1.status}")
assert geo_res_1.distance_metres <= 500.0 and geo_res_1.location_match == True and geo_res_1.status == SignalStatusEnum.MATCH, "Failed <500m Match test"

# 1.2 Review Range 500m - 1500m
gps_2 = GPSExtractionResult(gps_found=True, latitude=25.3260, longitude=82.9810)
geo_res_2 = verify_location_geodesic(gps_2, 25.3176, 82.9739)
print(f"  * Boundary 2 (500m-1500m): Calc Distance = {geo_res_2.distance_metres:.1f}m | Match = {geo_res_2.location_match} | Status = {geo_res_2.status}")
assert 500.0 < geo_res_2.distance_metres <= 1500.0 and geo_res_2.location_match == False and geo_res_2.status == SignalStatusEnum.REVIEW, "Failed Review range test"

# 1.3 Critical Mismatch > 1500m (Varanasi to New Delhi)
gps_3 = GPSExtractionResult(gps_found=True, latitude=28.6139, longitude=77.2090)
geo_res_3 = verify_location_geodesic(gps_3, 25.3176, 82.9739)
print(f"  * Boundary 3 (>1500m Inter-City): Calc Distance = {geo_res_3.distance_metres/1000:.1f} km | Match = {geo_res_3.location_match} | Status = {geo_res_3.status}")
assert geo_res_3.distance_metres > 1500.0 and geo_res_3.location_match == False and geo_res_3.status == SignalStatusEnum.MISMATCH, "Failed >1500m Mismatch test"
print("  >>> MATRIX 1 RESULT: 100% ACCURATE (PASSED)")

# =========================================================================
# MATRIX 2: VERHOEFF D5 DIHEDRAL CHECK DIGIT & WAGE CEILING AUDIT
# =========================================================================
print("\n[TEST 2] Verhoeff D5 Dihedral Aadhaar Math & Wage Leakage Matrix:")
# 2.1 Test Mathematically Valid Aadhaar Numbers
valid_aadhaars = ["987654321012", "543210987652"]
for a in valid_aadhaars:
    is_valid = validate_verhoeff_checksum(a)
    print(f"  * Verhoeff Checksum for Valid ID [{a}]: Valid = {is_valid}")
    assert is_valid == True, f"Valid Aadhaar {a} falsely failed"

# 2.2 Test Invalid / Forged Aadhaar Numbers
invalid_aadhaars = ["123456789012", "456789012345", "999988887777"]
for a in invalid_aadhaars:
    is_valid = validate_verhoeff_checksum(a)
    print(f"  * Verhoeff Checksum for Forged ID [{a}]: Valid = {is_valid}")
    assert is_valid == False, f"Forged Aadhaar {a} falsely passed"

# 2.3 Muster Roll CSV Parsing & Financial Leakage Summation
sample_csv = """worker_id,worker_name,trade,daily_wage,days_worked
W-101,Ramesh Kumar,Unskilled Labor,450,26
W-102,Suresh Singh,Mason / Skilled,650,24
123456789012,GHOST_WORKER_01,Skilled Labor,1450,30
W-101,Ramesh Kumar,Duplicate Entry,500,26
""".encode('utf-8')

muster_res = analyze_muster_roll_and_ghost_labor(muster_roll_bytes=sample_csv)
print(f"  * Muster Roll Workers Audited: {muster_res.total_workers_listed}")
print(f"  * Flagged Ghost/Discrepancy Entries: {muster_res.flagged_workers_count}")
print(f"  * Calculated Financial Leakage: INR {muster_res.suspected_ghost_wage_leakage:,.2f}")
print(f"  * Signal Status: {muster_res.status}")
assert muster_res.flagged_workers_count >= 2, "Failed to catch ghost workers and duplicate IDs"
assert muster_res.suspected_ghost_wage_leakage > 0, "Financial wage leakage calculation failed"
print("  >>> MATRIX 2 RESULT: 100% ACCURATE (PASSED)")

# =========================================================================
# MATRIX 3: 64-BIT DCT PERCEPTUAL HASH (pHash) ACCURACY
# =========================================================================
print("\n[TEST 3] 64-bit DCT Perceptual Hashing (Asset Recycling Matrix):")
# Pattern 1: Horizontal stripes
img1 = Image.new("RGB", (200, 200), color=(255, 255, 255))
d1 = ImageDraw.Draw(img1)
for y in range(0, 200, 20):
    d1.rectangle([0, y, 200, y + 10], fill=(0, 0, 0))

# Pattern 2: Identical copy of Image 1
img2 = img1.copy()

# Pattern 3: Concentric Circles (distinct high-frequency DCT structure)
img3 = Image.new("RGB", (200, 200), color=(255, 255, 255))
d3 = ImageDraw.Draw(img3)
for r in range(10, 100, 15):
    d3.ellipse([100 - r, 100 - r, 100 + r, 100 + r], outline=(0, 0, 0), width=5)

h1 = compute_image_phash(img1)
h2 = compute_image_phash(img2)
h3 = compute_image_phash(img3)

dist_identical = h1 - h2
dist_different = h1 - h3

print(f"  * pHash Image 1 (Stripes): {h1}")
print(f"  * pHash Image 2 (Identical Stripes): {h2} -> Hamming Distance = {dist_identical} (<= 5: Match = True)")
print(f"  * pHash Image 3 (Concentric Circles): {h3} -> Hamming Distance = {dist_different} (<= 5: Match = False)")
assert dist_identical == 0, "Identical images must have Hamming distance 0"
assert dist_different > 5, "Different pattern images must have Hamming distance > 5"
print("  >>> MATRIX 3 RESULT: 100% ACCURATE (PASSED)")

# =========================================================================
# MATRIX 4: SATELLITE ANOMALY ZONE POINT-IN-POLYGON (PIP) ACCURACY
# =========================================================================
print("\n[TEST 4] Satellite Ground-Truth Anomaly Zones (Point-in-Polygon Matrix):")
sat_inside = check_satellite_ground_truth(25.4358, 81.8463)
print(f"  * Coordinates (25.4358, 81.8463) [Yamuna Riverbed]: Status = {sat_inside.status} | Zone = {sat_inside.zone}")
assert sat_inside.status == SignalStatusEnum.ANOMALY and sat_inside.zone is not None, "Failed Yamuna floodplain detection"

sat_outside = check_satellite_ground_truth(25.3176, 82.9739)
print(f"  * Coordinates (25.3176, 82.9739) [Varanasi Rural]: Status = {sat_outside.status}")
assert sat_outside.status == SignalStatusEnum.PASS, "Clean site falsely flagged"
print("  >>> MATRIX 4 RESULT: 100% ACCURATE (PASSED)")

# =========================================================================
# MATRIX 5: COMPOSITE RISK SCORING & CAPACITY CLAMPING
# =========================================================================
print("\n[TEST 5] Composite Risk Scoring & Clamping (250-pt pool to 0-100):")
print(f"  * Configured System Weights: {RISK_WEIGHTS}")
total_system_weight = sum(RISK_WEIGHTS.values())
print(f"  * Sum of all 10 Risk Weights: {total_system_weight} Points (Capacity Pool)")
assert total_system_weight == 250, f"Expected 250 total weight pool, got {total_system_weight}"

# Base Clean Signals
d_clean = DuplicateCheckResult(match_found=False, status=SignalStatusEnum.PASS, message="")
w_clean = WebSearchCheckResult(match_found=False, status=SignalStatusEnum.PASS, message="")
l_clean = LocationCheckResult(claimed_latitude=25.3176, claimed_longitude=82.9739, location_match=True, distance_metres=100.0, status=SignalStatusEnum.MATCH, message="")
s_clean = SatelliteCheckResult(status=SignalStatusEnum.PASS, construction_found=True, message="")
g_clean = GenAIForensicResult(status=SignalStatusEnum.PASS, is_tampered=False, confidence_score=0.9, explanation="")
gps_clean = GPSExtractionResult(gps_found=True, latitude=25.3176, longitude=82.9739)
ghost_clean = GhostWorkerResult(anomaly_detected=False, status=SignalStatusEnum.PASS, message="")
m_clean = MusterRollCheckResult(status=SignalStatusEnum.PASS, muster_roll_provided=True, total_workers_listed=10, flagged_workers_count=0, suspected_ghost_wage_leakage=0, discrepancies=[], message="")
c_clean = ChronoCheckResult(status=SignalStatusEnum.PASS, confidence_score=0.9, is_consistent=True, message="")
mat_clean = MaterialCheckResult(claimed_material_or_milestone="Asphalt", detected_surface_material="Asphalt", status=SignalStatusEnum.PASS, confidence_score=0.9, is_consistent=True, reason="")

# 5.1 Test Baseline Zero Score
score_zero = compute_composite_risk_score(
    d_clean, w_clean, l_clean, s_clean, g_clean, gps_clean, ghost_clean, m_clean, c_clean, mat_clean
)
print(f"  * Zero Signals Triggered: Final Score = {score_zero.risk_score}/100 | Verdict = {score_zero.verdict}")
assert score_zero.risk_score == 0 and score_zero.verdict == "CLEAR", "Zero score test failed"

# 5.2 Test Location Mismatch Only (+35 pts)
l_mismatch = LocationCheckResult(claimed_latitude=25.3176, claimed_longitude=82.9739, location_match=False, distance_metres=12000.0, status=SignalStatusEnum.MISMATCH, message="")
score_review = compute_composite_risk_score(
    d_clean, w_clean, l_mismatch, s_clean, g_clean, gps_clean, ghost_clean, m_clean, c_clean, mat_clean
)
print(f"  * Location Mismatch Only (+35 pts): Final Score = {score_review.risk_score}/100 | Verdict = {score_review.verdict}")
assert score_review.risk_score == 35 and score_review.verdict == "REVIEW", "Review score test failed"

# 5.3 Test Multi-Vector Overflow Clamping (> 100 pts -> Clamped to 100)
d_dup = DuplicateCheckResult(match_found=True, status=SignalStatusEnum.MATCH, hamming_distance=0, message="")  # 40
w_dup = WebSearchCheckResult(match_found=True, status=SignalStatusEnum.MATCH, similarity_score=0.95, message="") # 40
s_anom = SatelliteCheckResult(status=SignalStatusEnum.ANOMALY, construction_found=False, message="")                 # 30
# Total = 40 + 40 + 35 + 30 = 145 pts -> Clamped to 100
score_overflow = compute_composite_risk_score(
    d_dup, w_dup, l_mismatch, s_anom, g_clean, gps_clean, ghost_clean, m_clean, c_clean, mat_clean
)
print(f"  * Overflow Signals (40+40+35+30 = 145 pts): Clamped Score = {score_overflow.risk_score}/100 | Verdict = {score_overflow.verdict}")
assert score_overflow.risk_score == 100 and score_overflow.verdict == "FLAGGED", "Clamping test failed"
print("  >>> MATRIX 5 RESULT: 100% ACCURATE (PASSED)")

print("\n" + "=" * 80)
print(" ALL 5 FORENSIC MATRICES TESTED AND VERIFIED 100% ACCURATE & COMPLIANT!")
print("=" * 80)
