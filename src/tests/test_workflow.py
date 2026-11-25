from src.requirement_mapping import (
    map_requirements,
    map_production_requirements,
)


def test_chemo_maps_to_test_service():
    profile = {
        "cancer_type": "Breast",
        "current_treatment": "Chemo",
        "symptoms": ["fatigue"],
        "severity": "moderate",
        "duration": "2 weeks",
        "city": "Bengaluru",
        "support_level": "Moderate",
    }

    result = map_requirements(profile)

    assert result["required_services"] == ["TEST_CHEMO"]


def test_radiation_maps_to_test_service():
    profile = {
        "cancer_type": "Lung",
        "current_treatment": "Radiation",
        "symptoms": [],
        "severity": "moderate",
        "duration": "1 week",
        "city": "Bengaluru",
        "support_level": "Moderate",
    }

    result = map_requirements(profile)

    assert result["required_services"] == ["TEST_RADIATION"]


def test_unknown_treatment_returns_no_service():
    profile = {
        "cancer_type": "Breast",
        "current_treatment": "Unknown treatment",
        "symptoms": [],
        "severity": "moderate",
        "duration": "1 week",
        "city": "Bengaluru",
        "support_level": "Moderate",
    }

    result = map_requirements(profile)

    assert result["required_services"] == []
    assert "No service mapping" in result["message"]

def test_production_chemo_mapping():
    profile = {"current_treatment": "Chemotherapy"}

    result = map_production_requirements(profile)

    assert result["required_services"] == ["CHEMOTHERAPY"]


def test_production_radiation_mapping():
    profile = {"current_treatment": "Radiation"}

    result = map_production_requirements(profile)

    assert result["required_services"] == ["RADIATION"]


def test_production_surgery_mapping():
    profile = {"current_treatment": "Surgery"}

    result = map_production_requirements(profile)

    assert result["required_services"] == ["SURGICAL_ONCOLOGY"]


def test_production_immunotherapy_mapping():
    profile = {"current_treatment": "Immunotherapy"}

    result = map_production_requirements(profile)

    assert result["required_services"] == ["IMMUNOTHERAPY"]


def test_production_unknown_treatment():
    profile = {"current_treatment": "Unknown treatment"}

    result = map_production_requirements(profile)

    assert result["required_services"] == []
    assert "No production service mapping" in result["message"]
