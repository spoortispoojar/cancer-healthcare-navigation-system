
import pandas as pd
from pathlib import Path

# 1. Paths
ML_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ML_DIR / "data" / "processed" /
    "patient_dataset_v2.csv"
)

OUTPUT_DIR = ML_DIR / "data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "patient_features_v2.csv"

# 2. Load revised dataset
df = pd.read_csv(DATA_PATH)

# 3. Select only approved ML inputs
feature_columns = [
    "cancer_type",
    "age_years",
    "cancer_stage",
    "current_treatment",
    "selected_symptoms",
    "symptom_severity",
    "symptom_duration",
    "symptom_frequency",
    "needs_caregiver_support",
    "has_transport_to_hospital"
]

target_column = "support_requirement_label_v2"

# 4. Create feature dataset
X = df[feature_columns].copy()
y = df[target_column].copy()

# 5. Preserve missing symptom information
X["selected_symptoms"] = (
    X["selected_symptoms"].fillna("No symptoms reported")
)

X["symptom_severity"] = (
    X["symptom_severity"].fillna("None reported")
)

# 6. Combine features and target
prepared_df = X.copy()
prepared_df[target_column] = y

# 7. Save
prepared_df.to_csv(OUTPUT_PATH, index=False)

# 8. Verify
print("\n========== FEATURE DATASET ==========")

print("\nShape:", prepared_df.shape)

print("\nColumns:")
print(prepared_df.columns.tolist())

print("\nMissing values:")
print(prepared_df.isnull().sum())

print("\nTarget distribution:")
print(prepared_df[target_column].value_counts())

print("\nInsurance column included:")
print("has_health_insurance_or_scheme" in prepared_df.columns)

print("\nSaved to:")
print(OUTPUT_PATH)

print("\n========== COMPLETED ==========")
