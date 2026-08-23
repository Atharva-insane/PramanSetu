from typing import List, Tuple
from config import RISK_WEIGHTS, SCORE_CLEAR_MAX, SCORE_REVIEW_MAX
from schemas import (
    DuplicateCheckResult,
    WebSearchCheckResult,
    LocationCheckResult,
    SatelliteCheckResult,
    GenAIForensicResult,
    GPSExtractionResult,
    GhostWorkerResult,
    MusterRollCheckResult,
    ChronoCheckResult,
    MaterialCheckResult,
    RiskAssessment,
    TriggeredSignalDetail,
    VerdictEnum,
    SignalStatusEnum
)


def compute_composite_risk_score(
    duplicate_res: DuplicateCheckResult,
    web_res: WebSearchCheckResult,
    location_res: LocationCheckResult,
    satellite_res: SatelliteCheckResult,
    genai_res: GenAIForensicResult,
    gps_res: GPSExtractionResult,
    ghost_worker_res: GhostWorkerResult,
    muster_res: MusterRollCheckResult,
    chrono_res: ChronoCheckResult,
    material_res: MaterialCheckResult
) -> RiskAssessment:
    """
    Computes a transparent, calibrated composite risk score (0-100) based on all 10 multi-vector forensic signals.
    Formula: Risk Score = min(100, sum(W_i * S_i))
    """
    breakdown: List[TriggeredSignalDetail] = []
    total_score = 0

    # 1. Past Asset Recycling / Duplicate Check (Weight: 40)
    dup_triggered = duplicate_res.match_found
    dup_weight = RISK_WEIGHTS.get("duplicate_asset", 40)
    if dup_triggered:
        total_score += dup_weight
        reason = f"Historical asset recycling detected: Match in claims database (Hamming distance: {duplicate_res.hamming_distance})"
    else:
        reason = "No historical asset recycling found in government claims database."
    breakdown.append(TriggeredSignalDetail(
        signal_id="duplicate_asset",
        label="Past Asset Recycling",
        weight=dup_weight,
        triggered=dup_triggered,
        reason=reason
    ))

    # 2. Public Web / Stock Photo Reuse (Weight: 40)
    web_triggered = web_res.match_found
    web_weight = RISK_WEIGHTS.get("web_asset_reuse", 40)
    if web_triggered:
        total_score += web_weight
        reason = f"Public web/stock image reuse detected: Stolen from {web_res.domain} (Confidence: {int(web_res.confidence * 100)}%)"
    else:
        reason = "No matching public stock photos or web assets found. Image is an original capture."
    breakdown.append(TriggeredSignalDetail(
        signal_id="web_asset_reuse",
        label="Web Reverse Search & Stock Photo Intelligence",
        weight=web_weight,
        triggered=web_triggered,
        reason=reason
    ))

    # 3. Location Mismatch Check (Weight: 35)
    loc_triggered = location_res.status == SignalStatusEnum.MISMATCH
    loc_weight = RISK_WEIGHTS.get("location_mismatch", 35)
    if loc_triggered:
        total_score += loc_weight
        reason = f"Geographic discrepancy: Photo taken {location_res.distance_metres}m away from claimed site coordinates."
    else:
        reason = "Photo GPS matches claimed project site within acceptable 500m tolerance."
    breakdown.append(TriggeredSignalDetail(
        signal_id="location_mismatch",
        label="Geodesic Site Verification",
        weight=loc_weight,
        triggered=loc_triggered,
        reason=reason
    ))

    # 4. Ground-Truth Satellite Check (Weight: 30)
    sat_triggered = satellite_res.status == SignalStatusEnum.ANOMALY
    sat_weight = RISK_WEIGHTS.get("ground_truth_anomaly", 30)
    if sat_triggered:
        total_score += sat_weight
        reason = f"Earth observation anomaly detected: Site intersects '{satellite_res.zone}' with zero verified construction."
    else:
        reason = "Earth observation cross-verification indicates plausible site progress."
    breakdown.append(TriggeredSignalDetail(
        signal_id="ground_truth_anomaly",
        label="Satellite Earth-Observation",
        weight=sat_weight,
        triggered=sat_triggered,
        reason=reason
    ))

    # 5. Labor Muster Roll & Ghost Labor Check (Weight: 30)
    muster_triggered = muster_res.status == SignalStatusEnum.FLAGGED
    muster_weight = RISK_WEIGHTS.get("ghost_worker_muster_roll", 30)
    if muster_triggered:
        total_score += muster_weight
        reason = f"Ghost labor anomaly: {muster_res.flagged_workers_count} phantom worker discrepancies. Suspected leakage: ₹{muster_res.suspected_ghost_wage_leakage:,.0f}"
    else:
        reason = "Muster roll verified against photographic labor density. No phantom labor patterns detected."
    breakdown.append(TriggeredSignalDetail(
        signal_id="ghost_worker_muster_roll",
        label="Muster Roll & Ghost Labor Intelligence",
        weight=muster_weight,
        triggered=muster_triggered,
        reason=reason
    ))

    # 6. Material & Milestone Alignment Check (Weight: 25)
    mat_triggered = material_res.is_mismatch
    mat_weight = RISK_WEIGHTS.get("material_milestone_mismatch", 25)
    if mat_triggered:
        total_score += mat_weight
        reason = material_res.reason
    else:
        reason = "Physical surface material matches claimed engineering milestone."
    breakdown.append(TriggeredSignalDetail(
        signal_id="material_milestone_mismatch",
        label="Material & Milestone Progression",
        weight=mat_weight,
        triggered=mat_triggered,
        reason=reason
    ))

    # 7. Gemini 2.0 Flash Visual AI / Manipulation Check (Weight: 20)
    genai_triggered = genai_res.is_suspicious and genai_res.confidence >= 0.70
    genai_weight = RISK_WEIGHTS.get("visual_ai_tampering", 20)
    if genai_triggered:
        total_score += genai_weight
        reason = f"Visual forensics flagged manipulation cues: {genai_res.reason}"
    else:
        reason = "Visual forensic scan found no synthetic AI or digital tampering."
    breakdown.append(TriggeredSignalDetail(
        signal_id="visual_ai_tampering",
        label="Visual Forensics & AI Synthesis",
        weight=genai_weight,
        triggered=genai_triggered,
        reason=reason
    ))

    # 8. Chrono-Forensics & Solar/Weather Check (Weight: 15)
    chrono_triggered = chrono_res.status == SignalStatusEnum.FLAGGED
    chrono_weight = RISK_WEIGHTS.get("chrono_weather_mismatch", 15)
    if chrono_triggered:
        total_score += chrono_weight
        reason = chrono_res.message
    else:
        reason = "Chrono-forensic check passed: Solar angle and weather metrics consistent."
    breakdown.append(TriggeredSignalDetail(
        signal_id="chrono_weather_mismatch",
        label="Weather & Chrono-Forensics",
        weight=chrono_weight,
        triggered=chrono_triggered,
        reason=reason
    ))

    # 9. Missing / Unverifiable GPS (Weight: 10)
    gps_missing_triggered = not gps_res.gps_found
    gps_weight = RISK_WEIGHTS.get("unverifiable_gps", 10)
    if gps_missing_triggered:
        total_score += gps_weight
        reason = "Image EXIF GPS tags are stripped or unavailable. Manual geo-tagged recapture recommended."
    else:
        reason = f"Valid EXIF GPS metadata present ({gps_res.latitude}, {gps_res.longitude})."
    breakdown.append(TriggeredSignalDetail(
        signal_id="unverifiable_gps",
        label="EXIF Hardware Tag Integrity",
        weight=gps_weight,
        triggered=gps_missing_triggered,
        reason=reason
    ))

    # 10. File Quality Outlier Check (Weight: 5)
    quality_triggered = ghost_worker_res.quality_check.get("status") == "REVIEW"
    quality_weight = RISK_WEIGHTS.get("file_quality_outlier", 5)
    if quality_triggered:
        total_score += quality_weight
        reason = "Image payload is unusually degraded (<5KB) or exhibits extreme compression noise."
    else:
        reason = "Image resolution and file size meet engineering audit standards."
    breakdown.append(TriggeredSignalDetail(
        signal_id="file_quality_outlier",
        label="Image Payload Quality Standard",
        weight=quality_weight,
        triggered=quality_triggered,
        reason=reason
    ))

    # Clamp Score between 0 and 100
    final_score = min(100, max(0, total_score))

    # Determine Verdict and Recommended Action
    if final_score <= SCORE_CLEAR_MAX:
        verdict = VerdictEnum.CLEAR
        decision_reason = "No critical forensic anomalies detected across multi-modal evidence vectors."
        recommended_action = "Proceed with routine administrative approval and milestone payment disbursement."
    elif final_score <= SCORE_REVIEW_MAX:
        verdict = VerdictEnum.REVIEW
        decision_reason = "Moderate risk signals detected. Requires human verification before payment release."
        recommended_action = "Place milestone payment on provisional hold pending physical site inspection or geo-tagged recapture."
    else:
        verdict = VerdictEnum.FLAGGED
        decision_reason = "High-confidence procurement fraud risk: Severe visual, spatial, labor, or asset reuse anomalies detected."
        recommended_action = "Immediate pre-disbursement payment freeze. Issue Show-Cause Notice and escalate to Chief Vigilance Officer."

    return RiskAssessment(
        risk_score=final_score,
        verdict=verdict,
        decision_reason=decision_reason,
        recommended_action=recommended_action,
        breakdown=breakdown
    )
