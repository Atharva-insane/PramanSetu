import json
import os
from typing import Optional, Dict, Any
from config import CONTRACTORS_DB_PATH
from schemas import ContractorProfileResult


def get_contractor_risk_profile(contractor_name: str) -> ContractorProfileResult:
    """
    Retrieves historical contractor integrity ratings, recorded fraud flags,
    and vigilance warnings from the central contractor database.
    """
    if not os.path.exists(CONTRACTORS_DB_PATH):
        return ContractorProfileResult(
            contractor_id="CONT-GEN-999",
            contractor_name=contractor_name,
            integrity_score=85,
            star_rating=4.0,
            risk_tier="STANDARD",
            total_flags=0,
            is_repeat_offender=False,
            cvo_alert=None
        )

    try:
        with open(CONTRACTORS_DB_PATH, "r", encoding="utf-8") as f:
            db_data = json.load(f)
    except Exception:
        db_data = {"contractors": []}

    contractor_name_clean = contractor_name.strip().lower()

    for item in db_data.get("contractors", []):
        stored_name = item.get("contractor_name", "").strip().lower()
        if contractor_name_clean in stored_name or stored_name in contractor_name_clean:
            flags_count = item.get("flags_recorded", 0)
            is_repeat = flags_count >= 2
            return ContractorProfileResult(
                contractor_id=item.get("contractor_id", "CONT-UP-000"),
                contractor_name=item.get("contractor_name", contractor_name),
                integrity_score=item.get("integrity_score", 75),
                star_rating=float(item.get("star_rating", 3.5)),
                risk_tier=item.get("risk_tier", "LOW_RISK"),
                total_flags=flags_count,
                is_repeat_offender=is_repeat,
                cvo_alert=item.get("cvo_recommendation")
            )

    # Default profile for new/unregistered contractor
    return ContractorProfileResult(
        contractor_id=f"CONT-NEW-{abs(hash(contractor_name)) % 1000:03d}",
        contractor_name=contractor_name,
        integrity_score=80,
        star_rating=4.0,
        risk_tier="UNVERIFIED_NEW",
        total_flags=0,
        is_repeat_offender=False,
        cvo_alert="First-time applicant - standard vigilance screening active."
    )
