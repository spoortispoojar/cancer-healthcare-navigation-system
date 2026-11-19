
"""
Rule-based healthcare support service mapping.

This module is separate from ML prediction.
It identifies relevant navigation and support services
using patient-reported information and the predicted
support requirement level.
"""

SUPPORT_LEVELS = {"Low", "Moderate", "High"}

SYMPTOM_FEATURES = [
    "Fatigue",
    "Shortness of breath",
    "Nausea",
    "Bone pain",
    "Weight loss",
    "Anxiety or low mood",
    "Loss of appetite",
    "Persistent cough",
    "Sleep difficulty",
    "Breast lump",
    "Breast pain",
    "Chest pain",
    "Tingling or numbness in hands/feet",
    "Shoulder stiffness",
    "Arm swelling (lymphedema)",
    "Skin changes or redness",
    "Hair loss",
    "Coughing up blood",
    "Wheezing",
    "Recurrent chest infections",
    "Hot flashes",
    "Hoarseness",
    "Difficulty swallowing",
    "Skin rash",
    "Nipple discharge",
    "Joint or muscle pain"
]


def map_support_services(
    patient_data: dict,
    support_requirement: str
) -> dict:
    """
    Map patient information to relevant support services.

    Args:
        patient_data: Validated patient information using
                      the original ML feature names.
        support_requirement: Low, Moderate, or High.

    Returns:
        A dictionary containing the support level,
        navigation guidance, and recommended services.
    """

    if support_requirement not in SUPPORT_LEVELS:
        raise ValueError(
            "Support requirement must be Low, Moderate, or High."
        )

    if not isinstance(patient_data, dict):
        raise TypeError("Patient data must be a dictionary.")

    required_features = [
        "Anxiety or low mood",
        "Loss of appetite",
        "Weight loss",
        "Fatigue",
        "Shoulder stiffness",
        "Arm swelling (lymphedema)",
        "Tingling or numbness in hands/feet",
        "needs_caregiver_support",
        "has_transport_to_hospital"
    ] + SYMPTOM_FEATURES

    missing_features = [
        feature
        for feature in required_features
        if feature not in patient_data
    ]

    if missing_features:
        raise ValueError(
            f"Missing service mapping features: {missing_features}"
        )

    services = []

    # 1. Psychological support
    if patient_data["Anxiety or low mood"] == 1:
        services.append({
            "service": "Psychological support",
            "reason": (
                "Anxiety or low mood was reported. "
                "Psychological support resources may be relevant."
            )
        })

    # 2. Nutrition support
    if (
        patient_data["Loss of appetite"] == 1
        or patient_data["Weight loss"] == 1
    ):
        services.append({
            "service": "Nutrition support",
            "reason": (
                "Loss of appetite or weight loss was reported. "
                "Nutrition support resources may be relevant."
            )
        })

    # 3. Rehabilitation support
    rehabilitation_symptoms = [
        "Fatigue",
        "Shoulder stiffness",
        "Arm swelling (lymphedema)",
        "Tingling or numbness in hands/feet"
    ]

    if any(
        patient_data[symptom] == 1
        for symptom in rehabilitation_symptoms
    ):
        services.append({
            "service": "Rehabilitation support",
            "reason": (
                "One or more symptoms associated with "
                "physical or functional support were reported."
            )
        })

    # 4. Transportation assistance
    if patient_data["has_transport_to_hospital"] in [
        "No",
        "Sometimes"
    ]:
        services.append({
            "service": "Transportation assistance",
            "reason": (
                "The patient reported that transport to the "
                "hospital is unavailable or only sometimes available."
            )
        })

    # 5. Caregiver support
    if patient_data["needs_caregiver_support"] in [
        "Yes",
        "Sometimes"
    ]:
        services.append({
            "service": "Caregiver support",
            "reason": (
                "The patient reported needing caregiver "
                "support either regularly or sometimes."
            )
        })

    # 6. Symptom-management support
    reported_symptoms = [
        symptom
        for symptom in SYMPTOM_FEATURES
        if patient_data[symptom] == 1
    ]

    if reported_symptoms:
        services.append({
            "service": "Symptom-management support",
            "reason": (
                "The patient reported one or more symptoms. "
                "Information about symptom-support services "
                "may be useful."
            )
        })

    # Navigation guidance based on ML support requirement
    coordination_guidance = {
        "Low": (
            "Provide general information about relevant "
            "healthcare support services and facilities."
        ),
        "Moderate": (
            "Provide additional assistance coordinating access "
            "to relevant healthcare support services and facilities."
        ),
        "High": (
            "Provide more comprehensive and coordinated "
            "healthcare navigation across relevant support services "
            "and facilities."
        )
    }

    return {
        "support_requirement": support_requirement,
        "coordination_guidance": coordination_guidance[
            support_requirement
        ],
        "services": services,
        "disclaimer": (
            "These are healthcare navigation suggestions, "
            "not medical diagnoses, treatment recommendations, "
            "or emergency triage decisions."
        )
    }
