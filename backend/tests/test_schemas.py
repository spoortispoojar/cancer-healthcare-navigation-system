
import pytest
from pydantic import ValidationError

from app.schemas import PatientMLInput


@pytest.fixture
def valid_patient_data():
    return {
        "cancer_type": "Breast Cancer",
        "age_years": 55,
        "cancer_stage": "Stage II",
        "current_treatment": "Chemotherapy",
        "symptom_severity": "Moderate",
        "symptom_duration": "1-4 weeks",
        "symptom_frequency": "Daily",
        "needs_caregiver_support": "Sometimes",
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


def test_valid_patient_data_is_accepted(valid_patient_data):
    patient = PatientMLInput(**valid_patient_data)
    assert patient.cancer_type == "Breast Cancer"


def test_exactly_35_features_are_present(valid_patient_data):
    patient = PatientMLInput(**valid_patient_data)
    assert len(patient.model_dump(by_alias=True)) == 35


def test_ml_feature_names_are_preserved(valid_patient_data):
    patient = PatientMLInput(**valid_patient_data)
    result = patient.model_dump(by_alias=True)

    assert "Shortness of breath" in result
    assert "Arm swelling (lymphedema)" in result
    assert "Tingling or numbness in hands/feet" in result


def test_missing_feature_is_rejected(valid_patient_data):
    valid_patient_data.pop("Fatigue")

    with pytest.raises(ValidationError):
        PatientMLInput(**valid_patient_data)


def test_unexpected_feature_is_rejected(valid_patient_data):
    valid_patient_data["unexpected_feature"] = 1

    with pytest.raises(ValidationError):
        PatientMLInput(**valid_patient_data)


def test_invalid_cancer_type_is_rejected(valid_patient_data):
    valid_patient_data["cancer_type"] = "Other Cancer"

    with pytest.raises(ValidationError):
        PatientMLInput(**valid_patient_data)


def test_invalid_symptom_value_is_rejected(valid_patient_data):
    valid_patient_data["Fatigue"] = 2

    with pytest.raises(ValidationError):
        PatientMLInput(**valid_patient_data)


def test_boolean_age_is_rejected(valid_patient_data):
    valid_patient_data["age_years"] = True

    with pytest.raises(ValidationError):
        PatientMLInput(**valid_patient_data)

