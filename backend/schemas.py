from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class VerdictEnum(str, Enum):
    CLEAR = "CLEAR"
    REVIEW = "REVIEW"
    FLAGGED = "FLAGGED"
    ERROR = "ERROR"


class SignalStatusEnum(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FLAGGED = "FLAGGED"
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    ANOMALY = "ANOMALY"
    UNVERIFIABLE = "UNVERIFIABLE"
    FAIL = "FAIL"


# ==========================================
# 1. CORE FORENSIC SIGNAL SCHEMAS
# ==========================================

class DuplicateCheckResult(BaseModel):
    match_found: bool = False
    closest_match: Optional[Dict[str, Any]] = None
    hamming_distance: Optional[int] = None
    status: SignalStatusEnum = SignalStatusEnum.PASS
    message: str = "Structurally unique image"


class WebSearchCheckResult(BaseModel):
    match_found: bool = False
    matched_asset_id: Optional[str] = None
    title: Optional[str] = None
    source_type: Optional[str] = None
    domain: Optional[str] = None
    source_url: Optional[str] = None
    hamming_distance: Optional[int] = None
    confidence: float = 0.0
    status: SignalStatusEnum = SignalStatusEnum.PASS
    message: str = "No public stock photo or web duplicate match found"


class GPSExtractionResult(BaseModel):
    gps_found: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    timestamp: Optional[str] = None
    device_make: Optional[str] = None
    device_model: Optional[str] = None
    message: str = "GPS metadata parsed"


class LocationCheckResult(BaseModel):
    photo_gps_found: bool = False
    claimed_latitude: float
    claimed_longitude: float
    photo_latitude: Optional[float] = None
    photo_longitude: Optional[float] = None
    distance_metres: Optional[float] = None
    location_match: Optional[bool] = None
    status: SignalStatusEnum = SignalStatusEnum.UNVERIFIABLE
    message: str = "Location evaluation complete"


class SatelliteCheckResult(BaseModel):
    status: SignalStatusEnum = SignalStatusEnum.PASS
    construction_found: Optional[bool] = True
    message: str = "No anomaly found by earth-observation prototype"
    zone: Optional[str] = None
    distance_from_anomaly_zone_metres: Optional[float] = None


class GhostWorkerResult(BaseModel):
    image_analysis: Dict[str, Any] = Field(default_factory=dict)
    face_detection: Dict[str, Any] = Field(default_factory=dict)
    quality_check: Dict[str, Any] = Field(default_factory=dict)


class GenAIForensicResult(BaseModel):
    status: SignalStatusEnum = SignalStatusEnum.PASS
    is_suspicious: bool = False
    confidence: float = 0.0
    reason: str = "No synthetic or digital manipulation artifacts detected"


# ==========================================
# 2. EXTENDED FORENSIC SIGNAL SCHEMAS (PHASE 2)
# ==========================================

class LaborDiscrepancyEntry(BaseModel):
    worker_id: str
    worker_name: str
    trade: str
    days_claimed: int
    daily_wage: float
    claimed_wage_total: float
    discrepancy_reason: str
    risk_level: str = "FLAGGED"

MusterDiscrepancyItem = LaborDiscrepancyEntry


class MusterRollCheckResult(BaseModel):
    muster_roll_provided: bool = False
    total_workers_listed: int = 0
    total_man_days_claimed: int = 0
    total_claimed_labor_wages: float = 0.0
    detected_workers_in_photo: int = 0
    labor_density_ratio: Optional[float] = None
    flagged_workers_count: int = 0
    suspected_ghost_wage_leakage: float = 0.0
    discrepancies: List[LaborDiscrepancyEntry] = Field(default_factory=list)
    status: SignalStatusEnum = SignalStatusEnum.PASS
    message: str = "Labor muster roll evaluation complete"


class ChronoCheckResult(BaseModel):
    timestamp_verified: bool = True
    claimed_timestamp: Optional[str] = None
    extracted_timestamp: Optional[str] = None
    historical_weather_summary: Optional[str] = None
    solar_azimuth_degrees: Optional[float] = None
    shadow_inconsistency_detected: bool = False
    weather_inconsistency_detected: bool = False
    status: SignalStatusEnum = SignalStatusEnum.PASS
    message: str = "Chrono-forensic and solar vector check passed"


class MaterialCheckResult(BaseModel):
    claimed_material_or_milestone: str
    detected_surface_material: str
    milestone_alignment_score: float = 1.0  # 0.0 to 1.0
    is_mismatch: bool = False
    status: SignalStatusEnum = SignalStatusEnum.PASS
    reason: str = "Physical surface material matches claimed engineering milestone."


class ContractorProfileResult(BaseModel):
    contractor_id: str = "UNKNOWN"
    contractor_name: str
    integrity_score: int = 80  # 0 to 100
    star_rating: float = 4.0   # 1.0 to 5.0
    risk_tier: str = "LOW_RISK"
    total_flags: int = 0
    is_repeat_offender: bool = False
    cvo_alert: Optional[str] = None


# ==========================================
# 3. RISK SCORING & EXPLAINABILITY SCHEMAS
# ==========================================

class TriggeredSignalDetail(BaseModel):
    signal_id: str
    label: str
    weight: int
    triggered: bool
    reason: str


class RiskAssessment(BaseModel):
    risk_score: int = Field(ge=0, le=100, description="Calibrated Risk Score (0-100)")
    verdict: VerdictEnum
    decision_reason: str
    recommended_action: str
    breakdown: List[TriggeredSignalDetail] = Field(default_factory=list)


# ==========================================
# 4. ACCOUNTABILITY DOSSIER & LEGAL NOTICES
# ==========================================

class HoldAlert(BaseModel):
    title: str = "PRE-DISBURSEMENT PAYMENT HOLD DIRECTIVE"
    recipient: str = "Drawing & Disbursing Officer (DDO)"
    directive: str
    pbg_action: str


class ShowCauseNotice(BaseModel):
    title: str = "DRAFT SHOW-CAUSE NOTICE (PROCUREMENT FRAUD MITIGATION)"
    legal_reference: str = "General Financial Rules (GFR 2017) Rule 175 & Works Procurement Manual"
    statutory_window_days: int = 7
    notice_text: str


class VigilanceMemo(BaseModel):
    title: str = "VIGILANCE ESCALATION & DEBARMENT RECOMMENDATION"
    cvo_recommendation: str
    gem_blacklisting_recommended: bool = True
    memo_text: str


class AnnexureBLaborRoll(BaseModel):
    title: str = "ANNEXURE B: AUDIT DISPUTED LABOR MUSTER ROLL & WAGE LEAKAGE"
    total_suspected_leakage: str
    flagged_workers: List[LaborDiscrepancyEntry] = Field(default_factory=list)


class CryptoVerificationSeal(BaseModel):
    sha256_seal: str
    verification_url: str
    blockchain_ledger_ref: str
    timestamp_utc: str


class InvestigationDossier(BaseModel):
    watermark: str = "AI-GENERATED DRAFT — REQUIRES AUTHORIZED HUMAN REVIEW"
    dossier_id: str
    generated_at: str
    hold_alert: Optional[HoldAlert] = None
    show_cause_notice: Optional[ShowCauseNotice] = None
    vigilance_memo: Optional[VigilanceMemo] = None
    annexure_b_labor_muster: Optional[AnnexureBLaborRoll] = None
    crypto_verification: Optional[CryptoVerificationSeal] = None
    evidence_summary: Dict[str, Any] = Field(default_factory=dict)


# ==========================================
# 5. COMPLETE AUDIT RESPONSE SCHEMA
# ==========================================

class AuditResponse(BaseModel):
    status: VerdictEnum
    risk_score: int
    decision_reason: str
    recommended_action: str
    filename: str
    project_metadata: Dict[str, Any] = Field(default_factory=dict)
    contractor_profile: ContractorProfileResult
    duplicate_check: DuplicateCheckResult
    web_search_check: WebSearchCheckResult
    gps_extraction: GPSExtractionResult
    location_check: LocationCheckResult
    satellite_check: SatelliteCheckResult
    ghost_worker_check: GhostWorkerResult
    muster_roll_check: MusterRollCheckResult
    chrono_check: ChronoCheckResult
    material_check: MaterialCheckResult
    genai_forensic_check: GenAIForensicResult
    risk_assessment: RiskAssessment
    dossier: InvestigationDossier


# ==========================================
# 6. CITIZEN SOCIAL AUDIT & RTI SCHEMAS
# ==========================================

class CitizenAuditRequest(BaseModel):
    project_id: str = "PROJ-2024-RURAL-089"
    project_name: str = "Gram Sadak Asphalt Paving - Phase 2"
    claimed_completion_percentage: float = 100.0
    citizen_notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FormARTIDraft(BaseModel):
    title: str = "APPLICATION FOR INFORMATION UNDER SECTION 6(1) OF THE RTI ACT, 2005"
    section: str = "Right to Information Act, 2005 - Section 6(1)"
    pio_authority: str = "Public Information Officer (PIO), Rural Works Department"
    demanded_documents: List[str]
    application_body: str
    statutory_reply_window_days: int = 30


class CitizenAuditResponse(BaseModel):
    audit_id: str
    project_id: str = "PROJ-UNKNOWN"
    project_name: str
    citizen_notes: Optional[str] = None
    verdict: VerdictEnum
    risk_score: int
    plain_language_summary: str
    grievance_text: str
    form_a_rti: FormARTIDraft
    statutory_countdown_days: int = 30
    first_appeal_date: str


# ==========================================
# 7. SYSTEM HEALTH & DIAGNOSTICS SCHEMA
# ==========================================

class HealthResponse(BaseModel):
    status: str = "operational"
    version: str = "2.0.0"
    service: str = "PramanSetu (प्रमाण सेतु) Multi-Vector Forensic Gateway"
    gemini_configured: bool
    anomaly_zones_count: int
    mock_db_records: int
    mock_web_db_records: int
    contractors_count: int
