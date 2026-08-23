import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from schemas import (
    RiskAssessment,
    VerdictEnum,
    InvestigationDossier,
    HoldAlert,
    ShowCauseNotice,
    VigilanceMemo,
    AnnexureBLaborRoll,
    MusterRollCheckResult,
    CryptoVerificationSeal
)
from services.crypto_service import generate_sha256_seal, generate_verification_qr_data


def generate_investigation_dossier(
    filename: str,
    project_metadata: Dict[str, Any],
    risk_assessment: RiskAssessment,
    signals_summary: Dict[str, Any],
    muster_roll_res: Optional[MusterRollCheckResult] = None
) -> InvestigationDossier:
    """
    Generates official administrative drafts and investigation dossiers
    for Drawing & Disbursing Officers (DDO) and Chief Vigilance Officers (CVO).
    """
    dossier_id = f"DOSSIER-{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    project_name = project_metadata.get("project_name", "Rural Infrastructure Package #402")
    scheme = project_metadata.get("scheme", "Pradhan Mantri Gram Sadak Yojana (PMGSY)")
    contractor = project_metadata.get("contractor_name", "M/s Apex Civil Constructions Ltd.")
    claim_amount = project_metadata.get("claim_amount", "₹42,50,000")
    tender_id = project_metadata.get("tender_id", "TDR-2024-UP-9921")

    # Generate Hold Alert
    hold_directive = (
        f"URGENT: Place immediate pre-disbursement payment freeze on Claim Voucher for "
        f"Tender [{tender_id}] ({contractor}) in the amount of {claim_amount}. "
        f"PramanSetu (प्रमाण सेतु) risk score: {risk_assessment.risk_score}/100 ({risk_assessment.verdict.value}). "
        f"Do not release funds via PFMS/Treasury until physical vigilance clearance is recorded."
    )
    pbg_action = "Mark Performance Bank Guarantee (PBG) as under administrative vigilance hold."
    hold_alert = HoldAlert(directive=hold_directive, pbg_action=pbg_action)

    # Generate Show-Cause Notice
    triggered_reasons = "\n".join([
        f"- [VIOLATION {i+1}] {item.label}: {item.reason}"
        for i, item in enumerate(risk_assessment.breakdown) if item.triggered
    ])

    if not triggered_reasons:
        triggered_reasons = "- General verification of milestone documentation required."

    show_cause_text = f"""
GOVERNMENT OF INDIA / STATE INFRASTRUCTURE CELL
OFFICE OF THE EXECUTIVE ENGINEER & TENDER APPROVAL AUTHORITY

MEMORANDUM / SHOW-CAUSE NOTICE
Ref: GFR-2017/Rule-175/VIG/{dossier_id}
Date: {datetime.now().strftime('%d %B %Y')}

To:
Authorized Representative,
{contractor}

Subject: SHOW-CAUSE NOTICE FOR IRREGULARITIES IN MILESTONE DISBURSEMENT CLAIM (Tender: {tender_id})

1. WHEREAS you submitted photographic evidence and a milestone fund disbursement claim of {claim_amount} for project "{project_name}" under scheme "{scheme}".

2. AND WHEREAS an automated pre-approval forensic audit by PramanSetu (प्रमाण सेतु) has identified critical integrity violations in the submitted evidence (Risk Score: {risk_assessment.risk_score}/100):

{triggered_reasons}

3. NOW THEREFORE, pursuant to Rule 175 of the General Financial Rules (GFR 2017) and Clause 59 of the Standard Conditions of Contract, you are hereby directed to SHOW CAUSE in writing within SEVEN (7) DAYS of receipt of this notice as to why:
   (a) The milestone disbursement voucher should not be cancelled;
   (b) The Performance Bank Guarantee (PBG) deposited by your firm should not be forfeited; and
   (c) Proceedings for debarment/blacklisting from government e-Marketplace (GeM) should not be initiated.

Issued under the direction of the Vigilance & Audit Authority.
[AI-GENERATED DRAFT — REQUIRES AUTHORIZED HUMAN REVIEW AND SIGNATURE]
""".strip()

    show_cause_notice = ShowCauseNotice(notice_text=show_cause_text)

    # Generate Vigilance Escalation Memo
    vigilance_memo_text = f"""
CONFIDENTIAL VIGILANCE ESCALATION MEMORANDUM
To: Chief Vigilance Officer (CVO) / Anti-Corruption Bureau Liaison
From: Automated Evidence Intelligence Unit (PramanSetu)
Dossier ID: {dossier_id} | Risk Rating: {risk_assessment.verdict.value} ({risk_assessment.risk_score}/100)

SUMMARY OF FINDINGS:
- Project: {project_name} | Tender ID: {tender_id}
- Contractor: {contractor} | Disputed Claim: {claim_amount}
- Submitted Evidence File: {filename}

RECOMMENDED ADMINISTRATIVE ACTIONS:
1. Issue formal blacklisting notice on Government e-Marketplace (GeM) and State Procurement Portals.
2. Direct Treasury Officer to withhold disbursement indefinitely.
3. Order independent total-station physical survey and core sample lab testing.
4. Prepare Annexure A & Annexure B evidence packet for referral to Lokayukta / Anti-Corruption Branch.
""".strip()

    vigilance_memo = VigilanceMemo(
        cvo_recommendation="Immediate debarment recommendation and contract suspension pending inquiry.",
        gem_blacklisting_recommended=True,
        memo_text=vigilance_memo_text
    )

    # Generate Annexure B for Labor Muster Roll if discrepancies exist
    annexure_b = None
    if muster_roll_res and muster_roll_res.flagged_workers_count > 0:
        annexure_b = AnnexureBLaborRoll(
            total_suspected_leakage=f"₹{muster_roll_res.suspected_ghost_wage_leakage:,.2f}",
            flagged_workers=muster_roll_res.discrepancies
        )

    # Generate Cryptographic Verification Seal & QR Data
    audit_summary_for_crypto = {
        "dossier_id": dossier_id,
        "risk_score": risk_assessment.risk_score,
        "status": risk_assessment.verdict.value,
        "timestamp": timestamp_str,
        "contractor_name": contractor,
        "tender_id": tender_id,
        "duplicate_check": signals_summary.get("duplicate_check", {}),
        "location_check": signals_summary.get("location_check", {}),
        "muster_roll_check": signals_summary.get("muster_roll_check", {})
    }
    sha_seal = generate_sha256_seal(audit_summary_for_crypto)
    qr_data = generate_verification_qr_data(dossier_id, sha_seal, risk_assessment.risk_score, risk_assessment.verdict.value)

    crypto_seal_obj = CryptoVerificationSeal(
        sha256_seal=sha_seal,
        verification_url=qr_data["verification_url"],
        blockchain_ledger_ref=qr_data["blockchain_ledger_ref"],
        timestamp_utc=qr_data["timestamp_utc"]
    )

    return InvestigationDossier(
        watermark="AI-GENERATED DRAFT — REQUIRES AUTHORIZED HUMAN REVIEW",
        dossier_id=dossier_id,
        generated_at=timestamp_str,
        hold_alert=hold_alert if risk_assessment.verdict in [VerdictEnum.FLAGGED, VerdictEnum.REVIEW] else None,
        show_cause_notice=show_cause_notice if risk_assessment.verdict == VerdictEnum.FLAGGED else None,
        vigilance_memo=vigilance_memo if risk_assessment.verdict == VerdictEnum.FLAGGED else None,
        annexure_b_labor_muster=annexure_b,
        crypto_verification=crypto_seal_obj,
        evidence_summary=signals_summary
    )
