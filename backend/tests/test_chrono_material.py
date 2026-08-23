import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.chrono_service import verify_chrono_and_solar_forensics
from services.material_service import verify_material_and_milestone_progression
from schemas import SignalStatusEnum, GenAIForensicResult


def test_chrono_forensics_clean_and_mismatch():
    # Clean check
    clean_res = verify_chrono_and_solar_forensics(
        extracted_timestamp="2024:07:15 11:30:00",
        claimed_timestamp="2024-07-15 11:30",
        latitude=25.3176,
        longitude=82.9739
    )
    assert clean_res.status == SignalStatusEnum.PASS
    assert clean_res.solar_azimuth_degrees is not None

    # Mismatch check
    mismatch_res = verify_chrono_and_solar_forensics(
        extracted_timestamp="2024:07:15 14:00:00",
        claimed_timestamp="2024-07-15 WEATHER_MISMATCH",
        latitude=25.4358,
        longitude=81.8463
    )
    assert mismatch_res.status == SignalStatusEnum.FLAGGED
    assert mismatch_res.weather_inconsistency_detected is True


def test_material_milestone_progression():
    # Clean match: Claimed Asphalt, Detected Asphalt
    clean_mat = verify_material_and_milestone_progression(
        claimed_milestone_or_material="Finished Bituminous Asphalt"
    )
    assert clean_mat.status == SignalStatusEnum.PASS
    assert clean_mat.is_mismatch is False

    # Mismatch: Claimed 100% Asphalt, but unpaved mud surface detected
    mismatch_mat = verify_material_and_milestone_progression(
        claimed_milestone_or_material="100% Asphalt Paved",
        image_notes="UNPAVED MUD GRAVEL DETECTED"
    )
    assert mismatch_mat.status == SignalStatusEnum.FLAGGED
    assert mismatch_mat.is_mismatch is True
    assert mismatch_mat.milestone_alignment_score < 0.50
