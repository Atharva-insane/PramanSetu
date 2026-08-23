import sys
from pathlib import Path
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app

client = TestClient(app)
SAMPLE_DIR = BACKEND_DIR / "data" / "sample_images"


def test_e2e_clean_road_audit():
    with open(SAMPLE_DIR / "case1_clean_road.jpg", "rb") as img:
        response = client.post(
            "/api/audit",
            files={"image": ("case1_clean_road.jpg", img, "image/jpeg")},
            data={
                "claimed_latitude": 25.3176,
                "claimed_longitude": 82.9739,
                "project_name": "Rural Varanasi Road Package 01",
                "contractor_name": "Varanasi Highway Developers Ltd.",
                "claim_amount": "₹50,00,000"
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["CLEAR", "REVIEW"]
    assert data["risk_score"] < 40
    assert data["location_check"]["location_match"] is True


def test_e2e_duplicate_pipeline_audit():
    with open(SAMPLE_DIR / "case2_duplicate_pipeline.jpg", "rb") as img:
        response = client.post(
            "/api/audit",
            files={"image": ("case2_duplicate_pipeline.jpg", img, "image/jpeg")},
            data={
                "claimed_latitude": 25.3176,
                "claimed_longitude": 82.9739,
                "project_name": "New Water Scheme 2024",
                "contractor_name": "M/s Apex Civil Constructions Ltd.",
                "claim_amount": "₹42,50,000"
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert data["duplicate_check"]["match_found"] is True
    assert data["status"] in ["REVIEW", "FLAGGED"]
    assert data["risk_score"] >= 40


def test_e2e_web_stock_photo_audit():
    with open(SAMPLE_DIR / "case4_web_stock_photo.jpg", "rb") as img:
        response = client.post(
            "/api/audit",
            files={"image": ("case4_web_stock_photo.jpg", img, "image/jpeg")},
            data={
                "claimed_latitude": 25.3176,
                "claimed_longitude": 82.9739,
                "project_name": "Stock Photo Highway Claim",
                "contractor_name": "M/s Apex Civil Constructions Ltd."
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert data["web_search_check"]["match_found"] is True
    assert data["web_search_check"]["domain"] == "shutterstock.com"


def test_e2e_ghost_labor_muster_roll_audit():
    with open(SAMPLE_DIR / "case5_ghost_muster_roll.jpg", "rb") as img, \
         open(SAMPLE_DIR / "case5_muster_roll.csv", "rb") as csv_file:
        response = client.post(
            "/api/audit",
            files={
                "image": ("case5_ghost_muster_roll.jpg", img, "image/jpeg"),
                "muster_roll_file": ("case5_muster_roll.csv", csv_file, "text/csv")
            },
            data={
                "claimed_latitude": 25.3176,
                "claimed_longitude": 82.9739,
                "project_name": "Ghost Labor Claim Case",
                "contractor_name": "M/s Apex Civil Constructions Ltd."
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert data["muster_roll_check"]["muster_roll_provided"] is True
    assert data["muster_roll_check"]["flagged_workers_count"] > 0
    assert data["muster_roll_check"]["suspected_ghost_wage_leakage"] > 0
    assert data["dossier"]["annexure_b_labor_muster"] is not None


def test_e2e_citizen_social_audit():
    with open(SAMPLE_DIR / "case1_clean_road.jpg", "rb") as img:
        response = client.post(
            "/api/citizen/report",
            files={"image": ("citizen_photo.jpg", img, "image/jpeg")},
            data={
                "project_id": "PROJ-VNS-2024",
                "project_name": "Varanasi Gram Sadak",
                "claimed_completion_percentage": "100.0",
                "citizen_notes": "Road looks authentic from local inspection."
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert "form_a_rti" in data
    assert len(data["form_a_rti"]["demanded_documents"]) >= 4
    assert data["statutory_countdown_days"] == 30
