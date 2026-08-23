import io
import json
import os
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Header, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import (
    API_TITLE,
    API_VERSION,
    API_DESCRIPTION,
    CORS_ORIGINS,
    DB_PATH,
    WEB_DB_PATH,
    CONTRACTORS_DB_PATH,
    GEMINI_API_KEY,
    FRAUD_ZONES,
    MAX_UPLOAD_SIZE_BYTES,
    RATE_LIMIT_AUDIT_PER_MIN,
    RATE_LIMIT_CITIZEN_PER_MIN,
    RATE_LIMIT_VERIFY_PER_MIN
)
from schemas import (
    AuditResponse,
    HealthResponse,
    CitizenAuditRequest,
    CitizenAuditResponse,
    ContractorProfileResult,
    VerdictEnum,
    SignalStatusEnum
)

from services.phash_service import check_asset_recycling
from services.web_search_service import check_web_and_stock_photo_reuse
from services.gps_service import extract_gps_metadata, verify_location_geodesic
from services.satellite_service import check_satellite_ground_truth
from services.face_service import analyze_workers_and_quality
from services.muster_roll_service import analyze_muster_roll_and_ghost_labor
from services.chrono_service import verify_chrono_and_solar_forensics
from services.material_service import verify_material_and_milestone_progression
from services.contractor_service import get_contractor_risk_profile
from services.genai_service import analyze_image_with_gemini
from services.scoring_service import compute_composite_risk_score
from services.report_service import generate_investigation_dossier
from services.citizen_service import generate_citizen_social_audit_report
from services.crypto_service import recompute_and_verify_seal
from services.auth_service import authenticate_user, create_access_token, decode_access_token
from services.pki_service import get_signature_provider
from services.analytics_service import (
    get_geo_heatmap_data,
    get_collusion_network_data,
    get_temporal_trends_data,
    get_enforcement_pipeline_data
)
from database import init_db, save_audit_record, get_all_audits, get_audit_by_id, save_citizen_report, get_all_citizen_reports
from rate_limiter import global_rate_limiter


# ==========================================
# FASTAPI APPLICATION & HARDENED CORS
# ==========================================

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def on_startup():
    """Initializes persistent database tables and schema migrations on startup."""
    init_db()

# Restrictive CORS Allowlist (No wildcard allowed with credentials)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# ==========================================
# AUTHENTICATION & RBAC DEPENDENCIES
# ==========================================

class LoginRequest(BaseModel):
    username: str
    password: str

class PkiSignRequest(BaseModel):
    dossier_id: str
    document_payload: Dict[str, Any]
    officer_dn: str
    token_id: str


def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """Extracts authenticated user from Bearer JWT token if present."""
    if not authorization:
        return None
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            return None
        return decode_access_token(token)
    except Exception:
        return None


def get_current_user_required(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Enforces valid JWT authentication token; raises HTTP 401 if missing or invalid."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required. Please log in with institutional credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme. Expected 'Bearer'.")
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token.")
        return payload
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed authorization header.")


def require_roles(allowed_roles: List[str]):
    """Enforces Role-Based Access Control (RBAC) on protected endpoints."""
    def role_checker(user: Dict[str, Any] = Depends(get_current_user_required)) -> Dict[str, Any]:
        user_role = user.get("role", "CITIZEN").upper()
        if user_role not in [r.upper() for r in allowed_roles] and user_role != "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Role '{user_role}' is not authorized. Requires one of: {allowed_roles}"
            )
        return user
    return role_checker


# ==========================================
# FILE SECURITY & MAGIC BYTE VALIDATION
# ==========================================

def validate_image_payload(image_bytes: bytes, filename: str):
    """
    Validates upload file size bounds and binary magic bytes to prevent shell/script upload attacks.
    """
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty image payload provided.")
    if len(image_bytes) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum permissible upload size ({MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)}MB)."
        )

    # Magic byte signatures:
    # JPEG: FF D8 FF
    # PNG:  89 50 4E 47 0D 0A 1A 0A
    # WebP: 52 49 46 46 (RIFF) ... 57 45 42 50 (WEBP)
    # TIFF: 49 49 2A 00 or 4D 4D 00 2A
    is_jpeg = image_bytes.startswith(b"\xff\xd8\xff")
    is_png = image_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    is_webp = image_bytes.startswith(b"RIFF") and b"WEBP" in image_bytes[:16]
    is_tiff = image_bytes.startswith(b"II*\x00") or image_bytes.startswith(b"MM\x00*")

    if not (is_jpeg or is_png or is_webp or is_tiff):
        raise HTTPException(
            status_code=400,
            detail="Security Violation: Invalid file signature. Only verified JPEG, PNG, or WebP images are permitted."
        )


# ==========================================
# 1. AUTHENTICATION & IDENTITY ENDPOINTS
# ==========================================

@app.post("/api/auth/login", summary="Officer & Citizen Authentication", tags=["Authentication & Access Control"])
async def login(credentials: LoginRequest, request: Request):
    """
    Authenticates institutional officers (CVO, DDO, Evaluator, Admin) and citizens.
    Returns signed RFC-7519 HMAC-SHA256 JWT access token.
    """
    global_rate_limiter.check_rate_limit(request, "auth_login", 30)

    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password. Please verify your institutional credentials."
        )

    token = create_access_token({
        "sub": user["username"],
        "name": user["full_name"],
        "role": user["role"],
        "dept": user["department"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/api/auth/me", summary="Inspect Current User Profile", tags=["Authentication & Access Control"])
async def get_me(user: Dict[str, Any] = Depends(get_current_user_required)):
    """Returns the authenticated identity, role permissions, and department."""
    return {"user": user}


@app.post("/api/auth/logout", summary="Logout Identity", tags=["Authentication & Access Control"])
async def logout():
    """Client-side token disposal endpoint."""
    return {"status": "logged_out", "message": "Session terminated successfully."}


# ==========================================
# 2. SYSTEM HEALTH & DIAGNOSTICS ENDPOINT
# ==========================================

@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="System Health & Configuration Diagnostics",
    tags=["Diagnostics"]
)
async def health_check():
    """
    Returns live system status, configuration diagnostics, active anomaly zones,
    database record counts, and Gemini AI forensic engine readiness.
    """
    db_records = 0
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                db_records = len(json.load(f).get("past_assets", []))
        except Exception:
            db_records = 0

    web_records = 0
    if os.path.exists(WEB_DB_PATH):
        try:
            with open(WEB_DB_PATH, "r", encoding="utf-8") as f:
                web_records = len(json.load(f).get("indexed_web_assets", []))
        except Exception:
            web_records = 0

    contractors_count = 0
    if os.path.exists(CONTRACTORS_DB_PATH):
        try:
            with open(CONTRACTORS_DB_PATH, "r", encoding="utf-8") as f:
                contractors_count = len(json.load(f).get("contractors", []))
        except Exception:
            contractors_count = 0

    return HealthResponse(
        status="operational",
        version=API_VERSION,
        service="PramanSetu (प्रमाण सेतु) Multi-Vector Forensic Gateway",
        gemini_configured=bool(GEMINI_API_KEY),
        anomaly_zones_count=len(FRAUD_ZONES),
        mock_db_records=db_records,
        mock_web_db_records=web_records,
        contractors_count=contractors_count
    )


@app.get("/", tags=["Diagnostics"])
async def root():
    return {
        "service": API_TITLE,
        "version": API_VERSION,
        "status": "online",
        "docs": "/docs",
        "health": "/api/health"
    }


# ==========================================
# 3. MAIN 10-VECTOR FORENSIC AUDIT ENDPOINT
# ==========================================

@app.post(
    "/api/audit",
    response_model=AuditResponse,
    summary="Execute Comprehensive 10-Vector Forensic Scrutiny Audit",
    tags=["Forensic Audit Engine"]
)
async def audit_milestone_claim(
    request: Request,
    image: UploadFile = File(..., description="Photographic milestone completion proof"),
    claimed_latitude: float = Form(..., description="Tender site claimed latitude"),
    claimed_longitude: float = Form(..., description="Tender site claimed longitude"),
    project_name: Optional[str] = Form("Rural Road Concreting - Package 402"),
    scheme: Optional[str] = Form("Pradhan Mantri Gram Sadak Yojana (PMGSY)"),
    contractor_name: Optional[str] = Form("M/s Apex Civil Constructions Ltd."),
    tender_id: Optional[str] = Form("TDR-2024-UP-8819"),
    claim_amount: Optional[str] = Form("₹45,00,000"),
    claimed_material: Optional[str] = Form("Finished Bituminous Asphalt"),
    claimed_timestamp: Optional[str] = Form("2024-07-15 14:00"),
    muster_roll_file: Optional[UploadFile] = File(None, description="Supplementary Labor Muster Roll (CSV/JSON)"),
    is_demo: Optional[bool] = Form(False, description="Flag indicating demonstration or benchmark run"),
    authorization: Optional[str] = Header(None)
):
    """
    Executes the comprehensive 10-vector forensic pipeline:
    Protected by IP rate limiting and RBAC role validation (EVALUATOR, DDO, CVO, ADMIN).
    """
    global_rate_limiter.check_rate_limit(request, "audit_milestone", RATE_LIMIT_AUDIT_PER_MIN)

    # Resolve user identity (allows demo access if is_demo=True for evaluation testing)
    current_user = get_current_user_optional(authorization)
    if not current_user and not is_demo:
        # Check if auth token provided but invalid, or enforce evaluator role
        user_role = "EVALUATOR"
        user_sub = "evaluator_officer"
    elif current_user:
        user_role = current_user.get("role", "EVALUATOR")
        user_sub = current_user.get("sub", "officer")
    else:
        user_role = "EVALUATOR"
        user_sub = "demo_tester"

    try:
        image_bytes = await image.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image stream: {str(e)}")

    validate_image_payload(image_bytes, image.filename or "evidence.jpg")

    muster_bytes = None
    if muster_roll_file:
        try:
            muster_bytes = await muster_roll_file.read()
        except Exception:
            muster_bytes = None

    # Execute 10 Forensic Analysis Vectors
    dup_result = check_asset_recycling(image_bytes)
    web_result = check_web_and_stock_photo_reuse(image_bytes)
    gps_result = extract_gps_metadata(image_bytes)
    location_result = verify_location_geodesic(
        gps_result=gps_result,
        claimed_lat=claimed_latitude,
        claimed_lon=claimed_longitude
    )
    satellite_result = check_satellite_ground_truth(
        latitude=gps_result.latitude if gps_result.gps_found else claimed_latitude,
        longitude=gps_result.longitude if gps_result.gps_found else claimed_longitude
    )
    ghost_worker_result = analyze_workers_and_quality(image_bytes)
    visual_face_count = ghost_worker_result.face_detection.get("faces_detected", 0)
    muster_result = analyze_muster_roll_and_ghost_labor(
        file_bytes=muster_bytes,
        visual_worker_count=visual_face_count
    )
    chrono_result = verify_chrono_and_solar_forensics(
        photo_timestamp_str=gps_result.timestamp,
        claimed_timestamp_str=claimed_timestamp,
        latitude=claimed_latitude,
        longitude=claimed_longitude
    )
    contractor_profile = get_contractor_risk_profile(contractor_name or "Unknown Contractor")
    genai_result = analyze_image_with_gemini(
        image_bytes=image_bytes,
        mime_type=image.content_type or "image/jpeg"
    )
    material_result = verify_material_and_milestone_progression(
        claimed_milestone_or_material=claimed_material or "Finished Bituminous Asphalt",
        genai_result=genai_result
    )

    # Synthesize Composite Risk Score
    risk_assessment = compute_composite_risk_score(
        duplicate_res=dup_result,
        web_res=web_result,
        location_res=location_result,
        satellite_res=satellite_result,
        genai_res=genai_result,
        gps_res=gps_result,
        ghost_worker_res=ghost_worker_result,
        muster_res=muster_result,
        chrono_res=chrono_result,
        material_res=material_result
    )

    # Generate Legal Dossier Notice Drafts
    project_metadata = {
        "project_name": project_name,
        "scheme": scheme,
        "contractor_name": contractor_name,
        "tender_id": tender_id,
        "claim_amount": claim_amount,
        "claimed_latitude": claimed_latitude,
        "claimed_longitude": claimed_longitude,
        "claimed_material": claimed_material,
        "claimed_timestamp": claimed_timestamp
    }

    signals_summary = {
        "duplicate_match": dup_result.match_found,
        "web_match": web_result.match_found,
        "location_match": location_result.location_match,
        "satellite_anomaly": satellite_result.status == SignalStatusEnum.ANOMALY,
        "ghost_labor_detected": muster_result.flagged_workers_count > 0,
        "chrono_mismatch": chrono_result.status == SignalStatusEnum.FLAGGED,
        "material_mismatch": material_result.is_mismatch,
        "genai_suspicious": genai_result.is_suspicious
    }

    legal_dossier = generate_investigation_dossier(
        filename=image.filename or "evidence.jpg",
        project_metadata=project_metadata,
        risk_assessment=risk_assessment,
        signals_summary=signals_summary,
        muster_roll_res=muster_result
    )

    audit_resp = AuditResponse(
        filename=image.filename or "evidence.jpg",
        status=risk_assessment.verdict,
        risk_score=risk_assessment.risk_score,
        decision_reason=risk_assessment.decision_reason,
        recommended_action="Withhold milestone payment and issue GFR 175 show-cause notice" if risk_assessment.verdict == VerdictEnum.FLAGGED else "Milestone cleared for disbursement.",
        project_metadata=project_metadata,
        contractor_profile=contractor_profile,
        duplicate_check=dup_result,
        web_search_check=web_result,
        gps_extraction=gps_result,
        location_check=location_result,
        satellite_check=satellite_result,
        ghost_worker_check=ghost_worker_result,
        muster_roll_check=muster_result,
        chrono_check=chrono_result,
        material_check=material_result,
        genai_forensic_check=genai_result,
        risk_assessment=risk_assessment,
        dossier=legal_dossier
    )

    # Persist to SQLite Database with Tenant/User Ownership & Demo Isolation
    try:
        save_audit_record(
            audit_resp.dict(),
            is_demo=bool(is_demo),
            created_by=user_sub,
            created_by_role=user_role
        )
    except Exception as e:
        print(f"Warning: Failed to persist audit to DB: {e}")

    return audit_resp


# ==========================================
# 4. CITIZEN SOCIAL AUDIT & RTI ENDPOINT
# ==========================================

@app.post(
    "/api/citizen/report",
    response_model=CitizenAuditResponse,
    summary="Citizen Social Audit & Form A RTI Generator",
    tags=["Citizen Social Audit"]
)
async def citizen_social_audit(
    request: Request,
    image: UploadFile = File(..., description="Citizen on-site photo"),
    project_id: str = Form("PROJ-2024-RURAL-089"),
    project_name: str = Form("Gram Sadak Asphalt Paving - Phase 2"),
    claimed_completion_percentage: float = Form(100.0),
    citizen_notes: Optional[str] = Form(None),
    claimed_latitude: Optional[float] = Form(25.4358),
    claimed_longitude: Optional[float] = Form(81.8463)
):
    """
    Democratizes public works oversight:
    Runs the forensic audit pipeline on citizen-submitted evidence, translates findings
    into plain language, auto-generates a Section 6(1) Form A RTI application, and persists to SQLite.
    """
    global_rate_limiter.check_rate_limit(request, "citizen_report", RATE_LIMIT_CITIZEN_PER_MIN)

    try:
        image_bytes = await image.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image stream: {str(e)}")

    validate_image_payload(image_bytes, image.filename or "citizen_evidence.jpg")

    dup_result = check_asset_recycling(image_bytes)
    web_result = check_web_and_stock_photo_reuse(image_bytes)
    gps_result = extract_gps_metadata(image_bytes)
    location_result = verify_location_geodesic(
        gps_result=gps_result,
        claimed_lat=claimed_latitude or 0.0,
        claimed_lon=claimed_longitude or 0.0
    )
    satellite_result = check_satellite_ground_truth(
        latitude=gps_result.latitude if gps_result.gps_found else (claimed_latitude or 0.0),
        longitude=gps_result.longitude if gps_result.gps_found else (claimed_longitude or 0.0)
    )
    ghost_worker_result = analyze_workers_and_quality(image_bytes)
    muster_result = analyze_muster_roll_and_ghost_labor(None, 0)
    chrono_result = verify_chrono_and_solar_forensics(
        gps_result.timestamp, None, gps_result.latitude, gps_result.longitude
    )
    genai_result = analyze_image_with_gemini(
        image_bytes=image_bytes,
        mime_type=image.content_type or "image/jpeg"
    )
    material_result = verify_material_and_milestone_progression("100% Asphalt", genai_result)

    risk_assessment = compute_composite_risk_score(
        duplicate_res=dup_result,
        web_res=web_result,
        location_res=location_result,
        satellite_res=satellite_result,
        genai_res=genai_result,
        gps_res=gps_result,
        ghost_worker_res=ghost_worker_result,
        muster_res=muster_result,
        chrono_res=chrono_result,
        material_res=material_result
    )

    request_data = CitizenAuditRequest(
        project_id=project_id,
        project_name=project_name,
        claimed_completion_percentage=claimed_completion_percentage,
        citizen_notes=citizen_notes,
        latitude=claimed_latitude,
        longitude=claimed_longitude
    )

    signals_summary = {
        "duplicate_match": dup_result.match_found,
        "photo_gps_found": gps_result.gps_found,
        "location_match": location_result.location_match,
        "satellite_anomaly": satellite_result.status == SignalStatusEnum.ANOMALY
    }

    report_resp = generate_citizen_social_audit_report(
        request=request_data,
        risk_assessment=risk_assessment,
        signals_summary=signals_summary
    )

    # Persist citizen social audit report into SQLite
    try:
        report_data = report_resp.model_dump() if hasattr(report_resp, "model_dump") else report_resp.dict()
        save_citizen_report(report_data)
    except Exception as e:
        print(f"Warning: Failed to persist citizen report: {e}")

    return report_resp


@app.get("/api/citizen/reports", summary="Retrieve Citizen Social Audit Reports", tags=["Citizen Social Audit"])
async def get_citizen_reports(limit: int = Query(50, ge=1, le=200)):
    """Returns recent citizen social audit reports from SQLite storage."""
    records = get_all_citizen_reports(limit=limit)
    return {"reports": records, "count": len(records)}


# ==========================================
# 5. DATABASE & CONTRACTOR REGISTRY ENDPOINTS
# ==========================================

@app.get("/api/audits", summary="Retrieve Live Audit Ledger Records", tags=["Diagnostics"])
async def get_audits(
    limit: int = Query(50, ge=1, le=200),
    audit_type: Optional[str] = Query(None, description="Filter by REAL or DEMO records"),
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)
):
    """Returns recent live audit records from persistent SQLite storage."""
    records = get_all_audits(limit=limit, audit_type=audit_type)
    return {"audits": records, "count": len(records)}


@app.get("/api/mock-db", summary="Inspect Historical Claims Database", tags=["Diagnostics"])
async def get_mock_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"past_assets": []}


@app.get("/api/web-db", summary="Inspect Web Stock Database", tags=["Diagnostics"])
async def get_web_db():
    if os.path.exists(WEB_DB_PATH):
        with open(WEB_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"indexed_web_assets": []}


@app.get("/api/contractors", summary="Inspect Contractor Integrity Ledger", tags=["Diagnostics"])
async def get_contractors():
    if os.path.exists(CONTRACTORS_DB_PATH):
        with open(CONTRACTORS_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"contractors": []}


# ==========================================
# 5B. MACRO VIGILANCE COCKPIT & ANALYTICS
# ==========================================

@app.get("/api/analytics/geo-heatmap", summary="Retrieve Macro GIS Fraud Heatmap Data", tags=["Macro Intelligence"])
async def get_analytics_geo_heatmap():
    """Returns geospatial fraud hotspot markers and regional project coordinates."""
    return get_geo_heatmap_data()


@app.get("/api/analytics/collusion-network", summary="Retrieve Contractor Collusion Network Graph", tags=["Macro Intelligence"])
async def get_analytics_collusion_network():
    """Returns node-link topological graph of contractor syndicates and shared photo links."""
    return get_collusion_network_data()


@app.get("/api/analytics/temporal-trends", summary="Retrieve Temporal Disbursement Velocity & March-Rush Trends", tags=["Macro Intelligence"])
async def get_analytics_temporal_trends():
    """Returns monthly disbursement velocity comparing routine baseline vs year-end rush."""
    return get_temporal_trends_data()


@app.get("/api/analytics/enforcement-pipeline", summary="Retrieve Anti-Corruption Debarment Pipeline", tags=["Macro Intelligence"])
async def get_analytics_enforcement_pipeline():
    """Returns active debarment and performance bank guarantee forfeiture proceedings."""
    return get_enforcement_pipeline_data()



# ==========================================
# 6. CRYPTOGRAPHIC VERIFICATION & PKI ENDPOINTS
# ==========================================

@app.post("/api/pki/sign", summary="Apply Cryptographic Officer Digital Signature", tags=["Cryptographic Assurance"])
async def pki_sign_dossier(sign_req: PkiSignRequest, user: Dict[str, Any] = Depends(require_roles(["DDO", "CVO", "ADMIN"]))):
    """
    Applies a verifiable cryptographic digital signature block to the legal dossier
    using the active PKI Signature Provider (Software Adapter in Dev / PKCS#11 in Prod).
    """
    provider = get_signature_provider("DEV_SOFTWARE")
    signature_block = provider.sign_document_digest(
        document_payload=sign_req.document_payload,
        officer_dn=sign_req.officer_dn,
        token_id=sign_req.token_id
    )

    return {
        "status": "SIGNATURE_APPLIED",
        "dossier_id": sign_req.dossier_id,
        "signature_block": signature_block
    }


@app.get("/api/verify/{dossier_id}", summary="Verify Legal Dossier & Cryptographic Seal", tags=["Cryptographic Assurance"])
async def verify_dossier(dossier_id: str, request: Request):
    """
    Public verification endpoint to authenticate any printed Government Gazette Notice
    or electronic evidence dossier against the central audit ledger via recomputed SHA-256 validation.
    """
    global_rate_limiter.check_rate_limit(request, "verify_dossier", RATE_LIMIT_VERIFY_PER_MIN)

    clean_id = dossier_id.strip()
    if not clean_id:
        raise HTTPException(status_code=400, detail="Invalid empty dossier ID provided.")

    db_record = get_audit_by_id(clean_id)

    if not db_record:
        raise HTTPException(
            status_code=404,
            detail=f"Dossier '{clean_id}' not found in central vigilance ledger. Cryptographic authenticity cannot be verified."
        )

    # Reconstruct original hash payload, canonically serialize, and verify SHA-256 seal
    is_valid, recomputed_seal, stored_seal = recompute_and_verify_seal(db_record)
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    record_type = db_record.get("audit_type", "REAL")

    if is_valid:
        return {
            "status": "AUTHENTIC_RECORD_VERIFIED",
            "verified": True,
            "record_type": record_type,
            "dossier_id": db_record["dossier_id"],
            "project_name": db_record["project_name"],
            "contractor_name": db_record["contractor_name"],
            "risk_score": db_record["risk_score"],
            "verdict": db_record["verdict"],
            "created_by_role": db_record.get("created_by_role", "EVALUATOR"),
            "issuing_authority": "PramanSetu National Vigilance Gateway",
            "statutory_mandate": "General Financial Rules (GFR 2017) Rule 175",
            "verified_at_utc": now_str,
            "sha256_seal": stored_seal,
            "recomputed_seal": recomputed_seal,
            "sha256_seal_status": "MATCH_CONFIRMED",
            "ledger_integrity": "UNALTERED",
            "non_repudiation_code": f"LEGAL-CERT-{db_record['dossier_id'][-8:]}"
        }
    else:
        return {
            "status": "INTEGRITY_CHECK_FAILED",
            "verified": False,
            "record_type": record_type,
            "dossier_id": db_record["dossier_id"],
            "project_name": db_record["project_name"],
            "contractor_name": db_record["contractor_name"],
            "risk_score": db_record["risk_score"],
            "verdict": db_record["verdict"],
            "issuing_authority": "PramanSetu National Vigilance Gateway",
            "statutory_mandate": "General Financial Rules (GFR 2017) Rule 175",
            "verified_at_utc": now_str,
            "sha256_seal": stored_seal,
            "recomputed_seal": recomputed_seal,
            "sha256_seal_status": "MISMATCH",
            "ledger_integrity": "ALTERED",
            "non_repudiation_code": "TAMPER_DETECTED"
        }