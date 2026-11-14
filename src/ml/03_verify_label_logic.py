
import pandas as pd
import re
from pathlib import Path

# 1. Load dataset
ML_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    ML_DIR / "data" / "raw" /
    "patient_form_training_dataset_7000_clean.csv"
)

df = pd.read_csv(DATA_PATH)

# 2. Components used in original scoring
components = [
    "stage",
    "severity",
    "symptoms3plus",
    "freq_daily_or_constant",
    "caregiver",
    "no_transport",
    "no_insurance",
    "treatment_intensity",
    "age70plus"
]

# 3. Extract scores and component values
def extract_value(text, key):
    match = re.search(rf"{key}=(\d+)", text)
    return int(match.group(1)) if match else None

df["extracted_score"] = df["label_basis"].apply(
    lambda x: extract_value(x, "score")
)

for component in components:
    df[component] = df["label_basis"].apply(
        lambda x: extract_value(x, component)
    )

# 4. Calculate score from components
df["calculated_score"] = df[components].sum(axis=1)

# 5. Check whether all component values were extracted
missing_components = df[components].isnull().sum().sum()

# 6. Compare calculated score with original score
df["score_matches"] = (
    df["calculated_score"] == df["extracted_score"]
)

# 7. Verify original label thresholds
def assign_label(score):
    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Moderate"
    else:
        return "High"

df["reconstructed_label"] = df["extracted_score"].apply(
    assign_label
)

df["label_matches"] = (
    df["reconstructed_label"] ==
    df["support_requirement_label"]
)

# 8. Print verification results
print("\n========== LABEL LOGIC VERIFICATION ==========")

print("\nTotal records:", len(df))

print("\nMissing extracted component values:", missing_components)

print("\nScore matches:")
print(df["score_matches"].value_counts())

print("\nOriginal label matches:")
print(df["label_matches"].value_counts())

print("\nScore mismatches:")
print(
    df.loc[
        ~df["score_matches"],
        ["label_basis", "extracted_score", "calculated_score"]
    ].head(10).to_string(index=False)
)

print("\nLabel mismatches:")
print(
    df.loc[
        ~df["label_matches"],
        ["extracted_score", "support_requirement_label",
         "reconstructed_label"]
    ].head(10).to_string(index=False)
)

print("\n========== VERIFICATION COMPLETED ==========")
