
"""
Requirement mapping for the cancer healthcare navigation system.

This module maps a patient's stated current treatment to a
corresponding service category. It does not diagnose or prescribe care.
"""

TREATMENT_SERVICE_MAP = {
    "chemo": "TEST_CHEMO",
    "chemotherapy": "TEST_CHEMO",
    "radiation": "TEST_RADIATION",
    "radiation therapy": "TEST_RADIATION",
    "radiotherapy": "TEST_RADIATION",
    "surgery": "TEST_SURGERY",
    "immunotherapy": "TEST_IMMUNOTHERAPY",
}


def map_requirements(patient_profile):
    """
    Return required service codes based on the stated treatment.

    Expected input example:
    {
        "cancer_type": "Breast",
        "current_treatment": "Chemo",
        "symptoms": ["fatigue"],
        "severity": "moderate",
        "duration": "2 weeks",
        "city": "Bengaluru",
        "support_level": "Moderate"
    }

    These rules are for software testing, not clinical decision-making.
    """
    treatment = patient_profile.get("current_treatment", "")
    treatment = treatment.strip().lower()

    service_code = TREATMENT_SERVICE_MAP.get(treatment)

    if service_code is None:
        return {
            "required_services": [],
            "message": (
                "No service mapping is configured for this treatment. "
                "Further review or an approved mapping rule is needed."
            ),
        }

    return {
        "required_services": [service_code],
        "message": (
            "Service mapped from the patient's stated current treatment. "
            "This is a test rule, not a clinical recommendation."
        ),
    }

# Production mapping using service codes from the facility research CSV.
# Keep this separate from the TEST_* mapping above.

PRODUCTION_TREATMENT_SERVICE_MAP = {
    "chemo": "CHEMOTHERAPY",
    "chemotherapy": "CHEMOTHERAPY",
    "radiation": "RADIATION",
    "radiation therapy": "RADIATION",
    "radiotherapy": "RADIATION",
    "surgery": "SURGICAL_ONCOLOGY",
    "immunotherapy": "IMMUNOTHERAPY",
}


def map_production_requirements(patient_profile):
    """
    Map the patient's stated current treatment to a production
    healthcare service code.

    This supports facility navigation only. It does not diagnose
    or prescribe treatment.
    """
    treatment = patient_profile.get("current_treatment", "")
    treatment = treatment.strip().lower()

    service_code = PRODUCTION_TREATMENT_SERVICE_MAP.get(treatment)

    if service_code is None:
        return {
            "required_services": [],
            "message": (
                "No production service mapping is configured "
                "for this treatment. Further review is required."
            ),
        }

    return {
        "required_services": [service_code],
        "message": (
            "Service mapped from the patient's stated current treatment. "
            "This mapping supports healthcare facility navigation only."
        ),
    }


if __name__ == "__main__":
    sample_profile = {
        "cancer_type": "Breast",
        "current_treatment": "Chemo",
        "symptoms": ["fatigue"],
        "severity": "moderate",
        "duration": "2 weeks",
        "city": "Bengaluru",
        "support_level": "Moderate",
    }

    result = map_requirements(sample_profile)

    print("Sample patient profile:", sample_profile)
    print("Mapping result:", result)
