import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from schemas import (
    CitizenAuditRequest,
    CitizenAuditResponse,
    FormARTIDraft,
    VerdictEnum,
    RiskAssessment
)


def generate_citizen_social_audit_report(
    request: CitizenAuditRequest,
    risk_assessment: RiskAssessment,
    signals_summary: Dict[str, Any]
) -> CitizenAuditResponse:
    """
    Translates technical forensic telemetry into plain-language civic intelligence
    and generates an automated Section 6(1) Form A RTI petition and CPGRAMS grievance draft.
    """
    audit_id = f"RTI-{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    today = datetime.now()
    first_appeal_date = (today + timedelta(days=30)).strftime("%d %B %Y")

    # Plain Language Summary Generation
    if risk_assessment.verdict == VerdictEnum.FLAGGED:
        plain_summary = (
            f"DISCREPANCY DETECTED: The contractor claimed '{request.project_name}' is "
            f"{request.claimed_completion_percentage}% physically completed. However, multi-vector forensic "
            f"analysis indicates severe irregularities (Risk Score: {risk_assessment.risk_score}/100). "
            f"The primary reason identified is: {risk_assessment.decision_reason}. "
            f"This suggests the ground reality differs significantly from the government disbursement record."
        )
    elif risk_assessment.verdict == VerdictEnum.REVIEW:
        plain_summary = (
            f"FURTHER VERIFICATION NEEDED: The photographic evidence for '{request.project_name}' "
            f"shows moderate anomalies (Risk Score: {risk_assessment.risk_score}/100). "
            f"Details: {risk_assessment.decision_reason}. A formal RTI inspection request is recommended."
        )
    else:
        plain_summary = (
            f"CLEAR RECORD: Photographic and spatial evidence for '{request.project_name}' appears consistent "
            f"with claimed physical progress (Risk Score: {risk_assessment.risk_score}/100)."
        )

    # CPGRAMS Grievance Text
    grievance_text = f"""
PUBLIC INFRASTRUCTURE GRIEVANCE PETITION (CPGRAMS / STATE PORTAL)
Project: {request.project_name} (ID: {request.project_id})
Date: {today.strftime('%d/%m/%Y')}
Grievance Description:
I am submitting a citizen social audit regarding public works at {request.project_name}. 
Official records claim {request.claimed_completion_percentage}% physical milestone completion. 
Independent photographic and spatial analysis via CivicAudit AI reveals potential irregularities:
"{plain_summary}"
Citizen Site Notes: {request.citizen_notes or 'No additional citizen notes provided.'}
Prayer:
Kindly order an urgent on-site joint inspection by the Superintending Engineer and place a temporary hold on further payment releases until physical verification is submitted.
""".strip()

    # Form A RTI Application Demanded Documents
    demanded_docs = [
        "Certified copies of all Measurement Book (MB) entries recorded for this project from commencement to date.",
        "Certified copies of Contractor Labor Muster Rolls and machinery deployment logs.",
        "Certified copies of laboratory material quality testing reports (compressive strength, asphalt grading, water potability).",
        "Certified copies of all Milestone Disbursement Vouchers and Treasury Sanction Orders issued to the contractor."
    ]

    docs_formatted = "\n".join([f"{i+1}. {doc}" for i, doc in enumerate(demanded_docs)])

    rti_body = f"""
FORM 'A' - APPLICATION FOR INFORMATION UNDER SECTION 6(1) OF THE RTI ACT, 2005

To,
The Public Information Officer (PIO) / Executive Engineer,
Department of Rural Works / Public Works Department,
Government of Uttar Pradesh / India.

1. Full Name of Applicant: [Citizen Social Auditor / Applicant Name]
2. Address: [Applicant Local Address]
3. Particulars of Information Required:
   Concerning Public Infrastructure Project: "{request.project_name}" (Project ID: {request.project_id})
   
   Please provide certified true copies of the following official public records under RTI Act Section 2(j):
{docs_formatted}

4. Period to which the information relates: Financial Years 2023-2024 & 2024-2025.
5. Mode of Receipt: Registered Speed Post / Certified Physical Copy.
6. Application Fee: ₹10 (Postal Order / Court Fee Stamp enclosed herewith).

Declaration:
I state that I am a citizen of India and the requested information falls within the scope of public interest and transparent governance.

Date: {today.strftime('%d %B %Y')}
Place: [Applicant District]
Signature of Applicant: _______________________
""".strip()

    form_a_rti = FormARTIDraft(
        title="APPLICATION FOR INFORMATION UNDER SECTION 6(1) OF THE RTI ACT, 2005",
        section="Right to Information Act, 2005 - Section 6(1)",
        pio_authority="Public Information Officer (PIO), Public Works & Infrastructure Department",
        demanded_documents=demanded_docs,
        application_body=rti_body,
        statutory_reply_window_days=30
    )

    return CitizenAuditResponse(
        audit_id=audit_id,
        project_id=request.project_id,
        project_name=request.project_name,
        citizen_notes=request.citizen_notes,
        verdict=risk_assessment.verdict,
        risk_score=risk_assessment.risk_score,
        plain_language_summary=plain_summary,
        grievance_text=grievance_text,
        form_a_rti=form_a_rti,
        statutory_countdown_days=30,
        first_appeal_date=first_appeal_date
    )
