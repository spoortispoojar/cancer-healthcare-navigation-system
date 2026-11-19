
import pytest

from app.service_mapping import map_support_services, SYMPTOM_FEATURES


@pytest.fixture
def valid_patient_data():
    """Create a complete patient profile with no reported symptoms."""

    data = {
        "cancer_type": "Breast Cancer",
        "age_years": 45,
        "cancer_stage": "Stage II",
        "current_treatment": "Chemotherapy",
        "symptom_severity": "Mild",
        "symptom_duration": "1-4 weeks",
        "symptom_frequency": "Occasionally",
        "needs_caregiver_support": "No",
        "has_transport_to_hospital": "Yes",
    }

    # All 26 symptoms are initially absent.
    for symptom in SYMPTOM_FEATURES:
        data[symptom] = 0

    return data


def get_service_names(result):
    """Extract service names from the mapping response."""
    return [
        service["service"]
        for service in result["services"]
    ]


def test_no_specific_support_services(valid_patient_data):
    result = map_support_services(
        valid_patient_data,
        "Low"
    )

    assert result["support_requirement"] == "Low"
    assert result["services"] == []
    assert "coordination_guidance" in result


def test_psychological_support_mapping(valid_patient_data):
    valid_patient_data["Anxiety or low mood"] = 1

    result = map_support_services(
        valid_patient_data,
        "Moderate"
    )

    assert "Psychological support" in get_service_names(result)


def test_nutrition_support_mapping(valid_patient_data):
    valid_patient_data["Weight loss"] = 1

    result = map_support_services(
        valid_patient_data,
        "Moderate"
    )

    assert "Nutrition support" in get_service_names(result)


def test_transportation_support_mapping(valid_patient_data):
    valid_patient_data["has_transport_to_hospital"] = "No"

    result = map_support_services(
        valid_patient_data,
        "Low"
    )

    assert "Transportation assistance" in get_service_names(result)


def test_caregiver_support_mapping(valid_patient_data):
    valid_patient_data["needs_caregiver_support"] = "Sometimes"

    result = map_support_services(
        valid_patient_data,
        "High"
    )

    assert "Caregiver support" in get_service_names(result)


def test_symptom_management_mapping(valid_patient_data):
    valid_patient_data["Persistent cough"] = 1

    result = map_support_services(
        valid_patient_data,
        "Moderate"
    )

    assert "Symptom-management support" in get_service_names(result)


def test_rehabilitation_support_mapping(valid_patient_data):
    valid_patient_data["Fatigue"] = 1

    result = map_support_services(
        valid_patient_data,
        "Moderate"
    )

    assert "Rehabilitation support" in get_service_names(result)


def test_multiple_services_can_be_returned(valid_patient_data):
    valid_patient_data["Anxiety or low mood"] = 1
    valid_patient_data["Loss of appetite"] = 1
    valid_patient_data["has_transport_to_hospital"] = "No"
    valid_patient_data["needs_caregiver_support"] = "Yes"

    result = map_support_services(
        valid_patient_data,
        "High"
    )

    services = get_service_names(result)

    assert "Psychological support" in services
    assert "Nutrition support" in services
    assert "Transportation assistance" in services
    assert "Caregiver support" in services


def test_invalid_support_requirement(valid_patient_data):
    with pytest.raises(ValueError):
        map_support_services(
            valid_patient_data,
            "Very High"
        )


def test_missing_mapping_feature(valid_patient_data):
    del valid_patient_data["Fatigue"]

    with pytest.raises(ValueError):
        map_support_services(
            valid_patient_data,
            "Low"
        )


def test_disclaimer_is_returned(valid_patient_data):
    result = map_support_services(
        valid_patient_data,
        "Low"
    )

    assert "not medical diagnoses" in result["disclaimer"]

