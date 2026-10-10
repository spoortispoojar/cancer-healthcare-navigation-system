
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_assessment_profile():
    payload = {
        "cancer_type": "Breast",
        "current_treatment": "Chemotherapy",
        "symptoms": ["Fatigue", "Weakness"],
        "severity": "Moderate",
        "duration_days": 4,
        "city": "  Bengaluru  ",
    }

    response = client.post("/assessment/profile", json=payload)

    assert response.status_code == 200
    assert response.json()["city"] == "Bengaluru"


def test_invalid_cancer_type():
    payload = {
        "cancer_type": "Stomach",
        "current_treatment": "Chemotherapy",
        "symptoms": ["Fatigue"],
        "severity": "Moderate",
        "duration_days": 4,
        "city": "Bengaluru",
    }

    response = client.post("/assessment/profile", json=payload)

    assert response.status_code == 422


def test_negative_duration():
    payload = {
        "cancer_type": "Breast",
        "current_treatment": "Chemotherapy",
        "symptoms": ["Fatigue"],
        "severity": "Moderate",
        "duration_days": -2,
        "city": "Bengaluru",
    }

    response = client.post("/assessment/profile", json=payload)

    assert response.status_code == 422


def test_facility_search():
    response = client.get(
        "/facilities",
        params={
            "city": "Bengaluru",
            "cancer_type": "Breast",
            "current_treatment": "Chemotherapy",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "facilities" in data
    assert "count" in data


def test_assessment_recommendations():
    payload = {
        "cancer_type": "Breast",
        "current_treatment": "Chemotherapy",
        "symptoms": ["Fatigue", "Weakness"],
        "severity": "Moderate",
        "duration_days": 4,
        "city": "Bengaluru",
    }

    response = client.post(
        "/assessment/recommendations",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()
    assert "patient_profile" in data
    assert "facilities" in data
    assert "facility_count" in data
