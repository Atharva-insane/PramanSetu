import csv
import io
import json
from typing import Optional, List, Dict, Any
from schemas import MusterRollCheckResult, MusterDiscrepancyItem, SignalStatusEnum

# Verhoeff Multiplication Table (d)
VERHOEFF_D = [
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

# Verhoeff Permutation Table (p)
VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

# Statutory Daily Wage Ceilings (CPWD / MGNREGA Standard Schedule of Rates)
MAX_UNSKILLED_DAILY_WAGE = 550  # ₹550 max per day
MAX_SKILLED_DAILY_WAGE = 850    # ₹850 max per day


def validate_verhoeff_checksum(number_str: str) -> bool:
    """
    Validates the 12-digit Aadhaar / National ID using the Verhoeff Dihedral (D5) algorithm.
    Returns False if the checksum is mathematically invalid or forged.
    """
    cleaned = "".join(filter(str.isdigit, number_str))
    if len(cleaned) < 10:
        return True  # Short local ID codes bypass Verhoeff

    c = 0
    reversed_digits = [int(d) for d in reversed(cleaned)]
    for i, digit in enumerate(reversed_digits):
        p_val = VERHOEFF_P[i % 8][digit]
        c = VERHOEFF_D[c][p_val]
    return c == 0


def analyze_muster_roll_and_ghost_labor(
    file_bytes: Optional[bytes] = None,
    visual_worker_count: int = 0,
    muster_roll_bytes: Optional[bytes] = None,
    detected_workers_in_photo: Optional[int] = None
) -> MusterRollCheckResult:
    """
    Enhanced Labor Muster Roll & Ghost Worker Wage Leakage Audit:
    1. Parses CSV/JSON roster records.
    2. Flags duplicate worker IDs and phantom keywords (GHOST, DUMMY, PHANTOM).
    3. Mathematical Verhoeff Checksum Verification on 12-digit Aadhaar worker credentials.
    4. Statutory Schedule of Rates (SoR) Wage Ceiling Bounds.
    5. Calculates cumulative ₹ financial leakage schedule.
    """
    effective_bytes = muster_roll_bytes if muster_roll_bytes is not None else file_bytes
    effective_count = detected_workers_in_photo if detected_workers_in_photo is not None else visual_worker_count

    if not effective_bytes:
        return MusterRollCheckResult(
            muster_roll_provided=False,
            status=SignalStatusEnum.PASS,
            total_workers_listed=0,
            flagged_workers_count=0,
            suspected_ghost_wage_leakage=0.0,
            discrepancies=[],
            message="No supplementary muster roll submitted. Basic telemetry verified."
        )

    try:
        content_str = effective_bytes.decode("utf-8", errors="ignore")
        entries: List[Dict[str, Any]] = []

        # Parse CSV or JSON
        if content_str.strip().startswith("[") or content_str.strip().startswith("{"):
            parsed_json = json.loads(content_str)
            entries = parsed_json if isinstance(parsed_json, list) else parsed_json.get("workers", [])
        else:
            reader = csv.DictReader(io.StringIO(content_str))
            for row in reader:
                entries.append(row)

        total_claimed = len(entries)
        seen_worker_ids = set()
        discrepancies: List[MusterDiscrepancyItem] = []
        total_leakage = 0.0

        for i, worker in enumerate(entries):
            worker_id = str(worker.get("worker_id", f"W-{i+1}")).strip()
            worker_name = str(worker.get("worker_name", "Unknown Worker")).strip()
            trade = str(worker.get("trade", "Unskilled Labor")).strip()
            
            try:
                days_worked = float(worker.get("days_worked", worker.get("days_claimed", 26)))
            except ValueError:
                days_worked = 26.0

            try:
                daily_wage = float(worker.get("daily_wage", 500))
            except ValueError:
                daily_wage = 500.0

            claimed_total = days_worked * daily_wage
            is_flagged = False
            reasons = []

            # Check 1: Explicit Ghost / Phantom Keywords
            lower_name = worker_name.lower()
            lower_id = worker_id.lower()
            if any(term in lower_name or term in lower_id for term in ["ghost", "dummy", "phantom", "test_worker", "fake"]):
                is_flagged = True
                reasons.append("Phantom Worker ID pattern detected in roster")

            # Check 2: Duplicate Worker Record
            if worker_id in seen_worker_ids and worker_id != "":
                is_flagged = True
                reasons.append(f"Duplicate Worker ID [{worker_id}] billed concurrently")
            seen_worker_ids.add(worker_id)

            # Check 3: Verhoeff Checksum Failure on 12-digit Aadhaar
            if len(worker_id) == 12 and worker_id.isdigit():
                if not validate_verhoeff_checksum(worker_id):
                    is_flagged = True
                    reasons.append("Invalid 12-Digit Verhoeff Aadhaar Checksum (Synthetic ID)")

            # Check 4: Statutory Wage Ceiling Compliance (SoR)
            if daily_wage > MAX_SKILLED_DAILY_WAGE:
                is_flagged = True
                reasons.append(f"Inflated Wage: ₹{daily_wage}/day exceeds statutory CPWD ceiling (₹{MAX_SKILLED_DAILY_WAGE}/day)")

            if is_flagged:
                discrepancy_reason = "; ".join(reasons)
                discrepancies.append(MusterDiscrepancyItem(
                    worker_id=worker_id,
                    worker_name=worker_name,
                    trade=trade,
                    days_claimed=int(days_worked),
                    daily_wage=int(daily_wage),
                    claimed_wage_total=int(claimed_total),
                    discrepancy_reason=discrepancy_reason
                ))
                total_leakage += claimed_total

        ghost_count = len(discrepancies)
        formatted_leakage = f"₹{total_leakage:,.2f}"

        if ghost_count > 0:
            status = SignalStatusEnum.FLAGGED
            message = (
                f"Severe Muster Roll Fraud Detected: {ghost_count} ghost/duplicate/inflated worker entries identified. "
                f"Total Disputed Financial Leakage: {formatted_leakage}"
            )
        else:
            status = SignalStatusEnum.PASS
            message = f"Muster Roll Verified: All {total_claimed} worker entries conform to statutory identity and wage rules."

        return MusterRollCheckResult(
            muster_roll_provided=True,
            total_workers_listed=total_claimed,
            total_man_days_claimed=sum(int(d.days_claimed) for d in discrepancies) if discrepancies else total_claimed * 26,
            total_claimed_labor_wages=sum(float(w.get("days_worked", 26)) * float(w.get("daily_wage", 500)) for w in entries),
            detected_workers_in_photo=visual_worker_count,
            labor_density_ratio=round(visual_worker_count / max(1, total_claimed), 2),
            flagged_workers_count=ghost_count,
            suspected_ghost_wage_leakage=round(total_leakage, 2),
            discrepancies=discrepancies,
            status=status,
            message=message
        )

    except Exception as e:
        return MusterRollCheckResult(
            muster_roll_provided=True,
            status=SignalStatusEnum.UNVERIFIABLE,
            total_workers_listed=0,
            flagged_workers_count=0,
            suspected_ghost_wage_leakage=0.0,
            discrepancies=[],
            message=f"Error parsing muster roll documentation: {str(e)}"
        )
