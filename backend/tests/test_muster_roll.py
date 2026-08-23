import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.muster_roll_service import analyze_muster_roll_and_ghost_labor
from schemas import SignalStatusEnum


def test_muster_roll_ghost_labor_detection():
    csv_path = BACKEND_DIR / "data" / "sample_images" / "case5_muster_roll.csv"
    with open(csv_path, "rb") as f:
        csv_bytes = f.read()

    # Pass 0 detected workers in photo against 31 claimed in muster roll
    result = analyze_muster_roll_and_ghost_labor(
        muster_roll_bytes=csv_bytes,
        detected_workers_in_photo=0
    )

    assert result.muster_roll_provided is True
    assert result.total_workers_listed >= 25
    assert result.flagged_workers_count > 0
    assert result.suspected_ghost_wage_leakage > 0
    assert result.status == SignalStatusEnum.FLAGGED
    assert len(result.discrepancies) > 0


def test_muster_roll_clean_submission():
    clean_csv = """worker_id,name,trade,days_worked,daily_wage
W-01,Sunil Kumar,Mason,20,500
W-02,Rajesh Patel,Helper,20,400
W-03,Anil Gupta,Helper,20,400
""".encode("utf-8")

    result = analyze_muster_roll_and_ghost_labor(
        muster_roll_bytes=clean_csv,
        detected_workers_in_photo=3
    )

    assert result.muster_roll_provided is True
    assert result.total_workers_listed == 3
    assert result.flagged_workers_count == 0
    assert result.status == SignalStatusEnum.PASS
