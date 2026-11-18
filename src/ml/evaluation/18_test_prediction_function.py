
# ==================================================
# 18. TEST REUSABLE PREDICTION FUNCTION
# ==================================================

import sys
from pathlib import Path

import joblib
import pandas as pd


# ==================================================
# 1. SET PROJECT ROOT AND IMPORT PATH
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==================================================
# 2. IMPORT REUSABLE PREDICTION FUNCTION
# ==================================================

from src.ml.predict_support import (
    predict_support_requirement,
    FEATURE_COLUMNS
)


# ==================================================
# 3. DEFINE FILE PATHS
# ==================================================

DATA_PATH = (
    PROJECT_ROOT
    / "src"
    / "ml"
    / "data"
    / "processed"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "src"
    / "ml"
    / "saved_models"
    / "logistic_regression_pipeline.joblib"
)


# ==================================================
# 4. LOAD TEST DATA
# ==================================================

X_test = pd.read_csv(DATA_PATH / "X_test.csv")
y_test = pd.read_csv(DATA_PATH / "y_test.csv")

print("\n========== TEST DATA LOADED ==========")
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)


# ==================================================
# 5. VERIFY FEATURE COLUMNS
# ==================================================

if list(X_test.columns) != FEATURE_COLUMNS:
    raise ValueError(
        "Test dataset columns do not match "
        "the expected model feature columns."
    )

print("\nFeature columns verified successfully.")
print("Number of features:", len(FEATURE_COLUMNS))


# ==================================================
# 6. SELECT ONE TEST PATIENT
# ==================================================

patient_data = X_test.iloc[0].to_dict()

print("\n========== TEST PATIENT ==========")
print("Number of input features:", len(patient_data))


# ==================================================
# 7. PREDICT USING REUSABLE FUNCTION
# ==================================================

function_result = predict_support_requirement(patient_data)

print("\n========== REUSABLE FUNCTION RESULT ==========")
print(function_result)


# ==================================================
# 8. PREDICT DIRECTLY USING SAVED MODEL
# ==================================================

model = joblib.load(MODEL_PATH)

direct_prediction = model.predict(
    X_test.iloc[[0]]
)[0]

print("\n========== DIRECT MODEL RESULT ==========")
print("Direct prediction:", direct_prediction)


# ==================================================
# 9. GET ACTUAL TEST LABEL
# ==================================================

actual_label = y_test.iloc[0, 0]

print("\n========== ACTUAL TEST LABEL ==========")
print("Actual label:", actual_label)


# ==================================================
# 10. COMPARE PREDICTIONS
# ==================================================

function_prediction = function_result["support_requirement"]

if function_prediction == direct_prediction:

    print("\nSUCCESS: Both predictions match.")

else:

    raise AssertionError(
        "Reusable function prediction does not "
        "match the direct model prediction."
    )


# ==================================================
# 11. CHECK ACTUAL CLASSIFICATION
# ==================================================

if function_prediction == actual_label:
    print("The prediction matches the actual test label.")
else:
    print("The prediction differs from the actual test label.")

print("\n========== TEST COMPLETED ==========")


# ==================================================
# 12. INPUT VALIDATION TESTS
# ==================================================

print("\n========== INPUT VALIDATION TESTS ==========")


def check_invalid_input(test_name, test_data, expected_error):

    try:
        predict_support_requirement(test_data)

    except expected_error as error:
        print(f"PASSED: {test_name}")
        print("Error:", error)

    except Exception as error:
        raise AssertionError(
            f"{test_name} raised an unexpected error: {error}"
        )

    else:
        raise AssertionError(
            f"{test_name} failed: Invalid input was accepted."
        )


# Test 1: Missing feature
invalid_data = patient_data.copy()
invalid_data.pop("cancer_type")

check_invalid_input(
    "Missing feature",
    invalid_data,
    ValueError
)


# Test 2: Unexpected feature
invalid_data = patient_data.copy()
invalid_data["unknown_feature"] = 1

check_invalid_input(
    "Unexpected feature",
    invalid_data,
    ValueError
)


# Test 3: Null value
invalid_data = patient_data.copy()
invalid_data["age_years"] = None

check_invalid_input(
    "Null value",
    invalid_data,
    ValueError
)


# Test 4: Invalid age
invalid_data = patient_data.copy()
invalid_data["age_years"] = -10

check_invalid_input(
    "Invalid age",
    invalid_data,
    ValueError
)


# Test 5: Invalid binary symptom value
invalid_data = patient_data.copy()
invalid_data["Fatigue"] = 5

check_invalid_input(
    "Invalid binary symptom value",
    invalid_data,
    ValueError
)


print("\n========== ALL VALIDATION TESTS COMPLETED ==========")


# ==================================================
# 13. TEST ALL 1400 TEST RECORDS
# ==================================================

print("\n========== FULL TEST DATASET VALIDATION ==========")

# Generate predictions directly using the saved model
direct_predictions = model.predict(X_test)

# Generate predictions using the reusable function
function_predictions = []

for index in range(len(X_test)):

    patient_data = X_test.iloc[index].to_dict()

    result = predict_support_requirement(patient_data)

    function_predictions.append(
        result["support_requirement"]
    )

# Compare both prediction lists
matching_predictions = sum(
    function_predictions[i] == direct_predictions[i]
    for i in range(len(X_test))
)

total_records = len(X_test)

print("Total records tested:", total_records)
print("Matching predictions:", matching_predictions)
print("Mismatching predictions:", total_records - matching_predictions)

if matching_predictions == total_records:
    print("\nSUCCESS: All reusable function predictions match the saved model.")
else:
    raise AssertionError(
        "Some reusable function predictions do not match "
        "the saved model predictions."
    )

print("\n========== FULL DATASET VALIDATION COMPLETED ==========")

