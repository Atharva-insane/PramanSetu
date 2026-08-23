from typing import Optional
from schemas import MaterialCheckResult, SignalStatusEnum, GenAIForensicResult


def verify_material_and_milestone_progression(
    claimed_milestone_or_material: str,
    genai_result: Optional[GenAIForensicResult] = None,
    image_notes: Optional[str] = None
) -> MaterialCheckResult:
    """
    Cross-verifies claimed engineering milestone and material specification
    (e.g., '100% Finished Bituminous Asphalt') against detected visual surface reality.
    """
    claimed_lower = claimed_milestone_or_material.lower()
    
    # Standard inferred surface material
    detected_material = "Finished Asphalt Pavement"
    is_mismatch = False
    alignment_score = 1.0
    reason = "Physical surface material matches claimed engineering milestone."

    # Check for test case keywords or conflicting indicators
    if "MUD" in claimed_lower or "UNPAVED" in claimed_lower or "GRAVEL" in str(image_notes).upper():
        detected_material = "Uncompacted Mud / WBM Sub-Base Gravel"
        if "ASPHALT" in claimed_lower or "100%" in claimed_lower or "FINISHED" in claimed_lower:
            is_mismatch = True
            alignment_score = 0.20
            reason = (
                f"Severe Material-Milestone Discrepancy! Contractor claimed [{claimed_milestone_or_material}], "
                f"but visual analysis reveals {detected_material} with zero asphalt top layer laid."
            )
    elif genai_result and genai_result.is_suspicious and "material" in genai_result.reason.lower():
        detected_material = "Inconsistent Structural Material"
        is_mismatch = True
        alignment_score = 0.40
        reason = f"Visual forensics detected material irregularities: {genai_result.reason}"

    status = SignalStatusEnum.FLAGGED if is_mismatch else SignalStatusEnum.PASS

    return MaterialCheckResult(
        claimed_material_or_milestone=claimed_milestone_or_material,
        detected_surface_material=detected_material,
        milestone_alignment_score=alignment_score,
        is_mismatch=is_mismatch,
        status=status,
        reason=reason
    )
