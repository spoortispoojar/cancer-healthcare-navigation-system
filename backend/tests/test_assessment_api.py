
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes import get_support_predictor


@pytest.fixture
def valid_assessment_payload():
    patient = {
        "cancer_type": "Breast Cancer",
        "age_years": 55,
        "cancer_stage": "Stage II",
        "current_treatment": "Chemotherapy",
        "symptom_severity": "Moderate",
        "symptom_duration": "1-4 weeks",
        "symptom_frequency": "Daily",
        "needs_caregiver_support": "No",
        "has_transport_to_hospital": "Yes",
        "Fatigue": 0,
        "Shortness of breath": 0,
        "Nausea": 0,
        "Bone pain": 0,
        "Weight loss": 0,
        "Anxiety or low mood": 0,
        "Loss of appetite": 0,
        "Persistent cough": 0,
        "Sleep difficulty": 0,
        "Breast lump": 0,
        "Breast pain": 0,
        "Chest pain": 0,
        "Tingling or numbness in hands/feet": 0,
        "Shoulder stiffness": 0,
        "Arm swelling (lymphedema)": 0,
        "Skin changes or redness": 0,
        "Hair loss": 0,
        "Coughing up blood": 0,
        "Wheezing": 0,
        "Recurrent chest infections": 0,
        "Hot flashes": 0,
        "Hoarseness": 0,
        "Difficulty swallowing": 0,
        "Skin rash": 0,
        "Nipple discharge": 0,
        "Joint or muscle pain": 0,
    }

    return {
        "city": "Bengaluru",
        "patient": patient
    }

def test_assessment_uses_real_ml_predictor(
    valid_assessment_payload
):
    with TestClient(app) as client:
        response = client.post(
            "/assessment",
            json=valid_assessment_payload
        )

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "success"
    assert result["support_requirement"] in {
        "Low", "Moderate", "High"
    }
    assert isinstance(result["support_services"], list)
    assert isinstance(result["recommended_facilities"], list)

def test_assessment_rejects_invalid_patient_input(
    valid_assessment_payload
):
    valid_assessment_payload["patient"]["Fatigue"] = 2

    with TestClient(app) as client:
        response = client.post(
            "/assessment",
            json=valid_assessment_payload
        )

    assert response.status_code == 422


def test_assessment_workflow_with_test_predictor(
    valid_assessment_payload
):
    def test_predictor(patient_data):
        assert len(patient_data) == 35

        return {
            "support_requirement": "Low"
        }

    app.dependency_overrides[get_support_predictor] = (
        lambda: test_predictor
    )

    try:
        with TestClient(app) as client:
            response = client.post(
                "/assessment",
                json=valid_assessment_payload
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "success"
    assert result["support_requirement"] == "Low"
    assert result["patient_summary"]["city"] == "Bengaluru"
    assert isinstance(result["support_services"], list)
    assert isinstance(result["recommended_facilities"], list)
    assert len(result["recommended_facilities"]) == 1
    assert (
        result["recommended_facilities"][0]["facility_name"]
        == "Sample Cancer Care Centre"
    )

