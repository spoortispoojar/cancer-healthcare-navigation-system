
from pathlib import Path
import math

import joblib
import pandas as pd


# --------------------------------------------------
# 1. PROJECT AND MODEL PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "src"
    / "ml"
    / "saved_models"
    / "logistic_regression_pipeline.joblib"
)


# --------------------------------------------------
# 2. EXPECTED MODEL FEATURES
# --------------------------------------------------

FEATURE_COLUMNS = [
    "cancer_type",
    "age_years",
    "cancer_stage",
    "current_treatment",
    "symptom_severity",
    "symptom_duration",
    "symptom_frequency",
    "needs_caregiver_support",
    "has_transport_to_hospital",
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

BINARY_FEATURES = FEATURE_COLUMNS[9:]


# --------------------------------------------------
# 3. LOAD TRAINED MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained model not found at: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# 4. PREDICTION FUNCTION
# --------------------------------------------------

def predict_support_requirement(patient_data: dict) -> dict:

    if not isinstance(patient_data, dict):
        raise TypeError("Patient data must be a dictionary.")

    # Check missing features
    missing_features = [
        feature for feature in FEATURE_COLUMNS
        if feature not in patient_data
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Check unexpected features
    unexpected_features = [
        feature for feature in patient_data
        if feature not in FEATURE_COLUMNS
    ]

    if unexpected_features:
        raise ValueError(
            f"Unexpected features: {unexpected_features}"
        )

    # Check null values
    for feature in FEATURE_COLUMNS:
        value = patient_data[feature]

        if pd.isna(value):
            raise ValueError(
                f"Feature '{feature}' cannot be empty."
            )

    # Validate age
    age = patient_data["age_years"]

    if isinstance(age, bool):
        raise ValueError("Age must be a valid positive number.")

    try:
        age = float(age)
    except (TypeError, ValueError):
        raise ValueError("Age must be a valid positive number.")

    if not math.isfinite(age) or age <= 0:
        raise ValueError("Age must be a valid positive number.")

    # Validate binary symptom features
    for feature in BINARY_FEATURES:
        value = patient_data[feature]

        if value not in (0, 1, False, True):
            raise ValueError(
                f"Feature '{feature}' must be either 0 or 1."
            )

    # Arrange features in the exact training order
    input_data = pd.DataFrame(
        [[patient_data[feature] for feature in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    # Generate prediction using the complete saved pipeline
    prediction = model.predict(input_data)[0]

    return {
        "support_requirement": str(prediction)
    }
