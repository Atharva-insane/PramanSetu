import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.gps_service import (
    extract_gps_metadata,
    calculate_haversine_distance,
    verify_location_geodesic
)
from schemas import SignalStatusEnum, GPSExtractionResult


def test_gps_extraction_clean_sample():
    sample_path = BACKEND_DIR / "data" / "sample_images" / "case1_clean_road.jpg"
    with open(sample_path, "rb") as f:
        image_bytes = f.read()

    result = extract_gps_metadata(image_bytes)
    assert result.gps_found is True
    assert result.latitude is not None
    assert result.longitude is not None
    assert abs(result.latitude - 25.3176) < 0.01
    assert abs(result.longitude - 82.9739) < 0.01


def test_haversine_distance_thresholds():
    # Site match: within 500m
    loc_match = verify_location_geodesic(
        GPSExtractionResult(gps_found=True, latitude=25.3176, longitude=82.9739),
        claimed_lat=25.3178,
        claimed_lon=82.9740
    )
    assert loc_match.status == SignalStatusEnum.MATCH
    assert loc_match.location_match is True
    assert loc_match.distance_metres < 100

    # Site mismatch: Delhi photo (28.6139, 77.2090) claimed for Varanasi (25.3176, 82.9739)
    loc_mismatch = verify_location_geodesic(
        GPSExtractionResult(gps_found=True, latitude=28.6139, longitude=77.2090),
        claimed_lat=25.3176,
        claimed_lon=82.9739
    )
    assert loc_mismatch.status == SignalStatusEnum.MISMATCH
    assert loc_mismatch.location_match is False
    assert loc_mismatch.distance_metres > 500000  # Over 500km


def test_missing_gps_fallback():
    loc_unverifiable = verify_location_geodesic(
        GPSExtractionResult(gps_found=False),
        claimed_lat=25.3176,
        claimed_lon=82.9739
    )
    assert loc_unverifiable.status == SignalStatusEnum.UNVERIFIABLE
    assert loc_unverifiable.photo_gps_found is False
