import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.satellite_service import check_satellite_ground_truth
from schemas import SignalStatusEnum


def test_satellite_anomaly_zone_hit():
    # Prayagraj anomaly zone: 25.4358, 81.8463
    result = check_satellite_ground_truth(25.4358, 81.8463)
    assert result.status == SignalStatusEnum.ANOMALY
    assert result.construction_found is False
    assert "Prayagraj" in str(result.zone)


def test_satellite_safe_zone():
    # Varanasi coordinates outside anomaly zone: 25.3176, 82.9739
    result = check_satellite_ground_truth(25.3176, 82.9739)
    assert result.status == SignalStatusEnum.PASS
    assert result.construction_found is True


def test_satellite_null_gps():
    result = check_satellite_ground_truth(None, None)
    assert result.status == SignalStatusEnum.UNVERIFIABLE
    assert result.construction_found is None
