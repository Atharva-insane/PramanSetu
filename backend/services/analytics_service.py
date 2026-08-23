from typing import Dict, Any, List
import json
from database import get_db_analytics_summary


def get_geo_heatmap_data() -> Dict[str, Any]:
    """
    Returns geographical distribution of monitored infrastructure projects
    combining live persistent SQLite audit records with the 2 signature baseline corridors.
    """
    db_summary = get_db_analytics_summary()
    live_geo_audits = db_summary.get("geo_audits", [])

    live_projects = []
    for a in live_geo_audits:
        live_projects.append({
            "id": a.get("dossier_id") or f"PROJ-LIVE-{a.get('id')}",
            "name": a.get("project_name") or "Infrastructure Project",
            "scheme": a.get("scheme") or "PMGSY",
            "contractor": a.get("contractor_name") or "Registered Contractor",
            "latitude": float(a.get("claimed_latitude", 25.3176)),
            "longitude": float(a.get("claimed_longitude", 82.9739)),
            "location_name": f"{a.get('scheme', 'Public Work')} Site",
            "risk_score": int(a.get("risk_score", 0)),
            "status": a.get("verdict", "CLEAR"),
            "claim_amount": a.get("claim_amount", "₹0"),
            "protected_amount": a.get("claim_amount", "₹0") if a.get("verdict") == "FLAGGED" else "₹0",
            "discrepancy": a.get("decision_reason") or "Audit milestone evaluated."
        })

    # The 2 Signature Baseline Corridors (Demo 1 & Demo 2)
    baseline_projects = [
        {
            "id": "PROJ-UP-VAR-01",
            "name": "PMGSY Rural Bituminous Road - Sector 4",
            "scheme": "PMGSY 2024",
            "contractor": "Varanasi Highway Developers Ltd.",
            "latitude": 25.3176,
            "longitude": 82.9739,
            "location_name": "Varanasi, Uttar Pradesh",
            "risk_score": 5,
            "status": "CLEAR",
            "claim_amount": "₹50,00,000",
            "protected_amount": "₹0",
            "discrepancy": "All 10 forensic vectors clear. Hardware EXIF GPS & muster roll verified."
        },
        {
            "id": "PROJ-UP-PRY-02",
            "name": "Prayagraj Rural Drinking Water Pipeline & Embankment",
            "scheme": "Jal Jeevan Mission 2024",
            "contractor": "M/s Apex Civil Constructions Ltd.",
            "latitude": 25.4358,
            "longitude": 81.8463,
            "location_name": "Prayagraj, Uttar Pradesh",
            "risk_score": 92,
            "status": "FLAGGED",
            "claim_amount": "₹45,00,000",
            "protected_amount": "₹45,00,000",
            "discrepancy": "Multi-Vector Fraud: Reused 2023 asset (pHash match), ghost labor leakage & satellite anomaly."
        }
    ]

    all_projects = live_projects + baseline_projects

    return {
        "total_monitored_projects": len(all_projects),
        "flagged_count": len([p for p in all_projects if p["status"] == "FLAGGED"]),
        "review_count": len([p for p in all_projects if p["status"] == "REVIEW"]),
        "clear_count": len([p for p in all_projects if p["status"] == "CLEAR"]),
        "total_protected_funds": "₹45,00,000",
        "projects": all_projects
    }


def get_collusion_network_data() -> Dict[str, Any]:
    """
    Returns node-link graph showing contractor syndicates and joint bidding networks.
    """
    nodes = [
        {"id": "c1", "label": "M/s Apex Civil Constructions Ltd.", "type": "contractor", "risk": "high", "flagged_claims": 2},
        {"id": "c2", "label": "Varanasi Highway Developers Ltd.", "type": "contractor", "risk": "low", "flagged_claims": 0},
        {"id": "t1", "label": "Tender JJM-PRY-2024", "type": "tender", "amount": "₹45.0L"},
        {"id": "t2", "label": "Tender PMGSY-VAR-2024", "type": "tender", "amount": "₹50.0L"},
        {"id": "h1", "label": "Reused Asset Hash [c46e6ec4...]", "type": "shared_asset", "details": "Photo submitted across 2 distinct fiscal milestone vouchers"}
    ]

    links = [
        {"source": "c1", "target": "t1", "relation": "claimed_milestone", "type": "bid"},
        {"source": "c2", "target": "t2", "relation": "claimed_milestone", "type": "bid"},
        {"source": "c1", "target": "h1", "relation": "submitted_reused_photo", "type": "fraud_link"}
    ]

    return {
        "syndicates_detected": 1,
        "cross_tender_photo_links": 1,
        "nodes": nodes,
        "links": links
    }


def get_temporal_trends_data() -> Dict[str, Any]:
    """
    Returns monthly disbursement volume vs intercepted fraudulent claims,
    highlighting the annual Q4 / March-Rush anomaly spike.
    """
    monthly_data = [
        {"month": "Oct 2023", "claimed_cr": 2.4, "approved_cr": 2.3, "intercepted_cr": 0.1, "is_march_rush": False},
        {"month": "Nov 2023", "claimed_cr": 3.1, "approved_cr": 2.9, "intercepted_cr": 0.2, "is_march_rush": False},
        {"month": "Dec 2023", "claimed_cr": 4.0, "approved_cr": 3.6, "intercepted_cr": 0.4, "is_march_rush": False},
        {"month": "Jan 2024", "claimed_cr": 3.8, "approved_cr": 3.4, "intercepted_cr": 0.4, "is_march_rush": False},
        {"month": "Feb 2024", "claimed_cr": 5.2, "approved_cr": 4.1, "intercepted_cr": 1.1, "is_march_rush": False},
        {"month": "Mar 2024 (March Rush)", "claimed_cr": 14.8, "approved_cr": 9.4, "intercepted_cr": 5.42, "is_march_rush": True},
        {"month": "Apr 2024", "claimed_cr": 2.8, "approved_cr": 2.6, "intercepted_cr": 0.2, "is_march_rush": False},
        {"month": "May 2024", "claimed_cr": 3.5, "approved_cr": 3.2, "intercepted_cr": 0.3, "is_march_rush": False},
        {"month": "Jun 2024", "claimed_cr": 4.2, "approved_cr": 3.7, "intercepted_cr": 0.5, "is_march_rush": False},
        {"month": "Jul 2024", "claimed_cr": 5.0, "approved_cr": 4.1, "intercepted_cr": 0.9, "is_march_rush": False}
    ]

    return {
        "cumulative_protected_cr": 9.52,
        "march_rush_anomaly_ratio": "3.8x baseline volume",
        "trend_summary": "Pre-approval interception prevented ₹5.42 Cr in fraudulent disbursements during the FY2023-24 March expenditure rush.",
        "monthly_series": monthly_data
    }


def get_enforcement_pipeline_data() -> Dict[str, Any]:
    """
    Returns legal enforcement pipeline tracking proceedings from Show-Cause
    to Performance Bank Guarantee (PBG) forfeiture and GeM blacklisting.
    """
    cases = [
        {
            "case_id": "CASE-2024-UP-001",
            "contractor": "M/s Apex Civil Constructions Ltd.",
            "scheme": "Jal Jeevan Mission",
            "disputed_amount": "₹45,00,000",
            "infraction": "Past Asset Recycling (pHash 0), Ghost Labor (₹3.15L) & Satellite Anomaly",
            "current_stage": "PBG Encashment Initiated",
            "stage_step": 3,
            "days_elapsed": 5,
            "cvo_reference": "CVO/JJM/2024/089",
            "pbg_status": "₹4.50 Lakhs Bank Guarantee Seized",
            "gem_debarment": "In Progress (7-Day Notice Expiring)"
        }
    ]

    return {
        "active_cases": len(cases),
        "total_pbg_seized": "₹4,50,000",
        "debarred_contractors_count": 0,
        "cases": cases
    }
