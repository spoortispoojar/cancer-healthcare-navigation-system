
import pandas as pd
import re
from pathlib import Path

# 1. Paths
ML_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ML_DIR / "data" / "raw" /
    "patient_form_training_dataset_7000_clean.csv"
)

OUTPUT_DIR = ML_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "patient_dataset_v2.csv"

# 2. Load original dataset
df = pd.read_csv(DATA_PATH)

# 3. Extract original score and insurance contribution
def extract_value(text, key):
    match = re.search(rf"{key}=(\d+)", text)
    return int(match.group(1)) if match else None

df["original_score"] = df["label_basis"].apply(
    lambda x: extract_value(x, "score")
)

df["insurance_contribution"] = df["label_basis"].apply(
    lambda x: extract_value(x, "no_insurance")
)

# 4. Calculate revised score without insurance
df["revised_score"] = (
    df["original_score"] - df["insurance_contribution"]
)

# 5. Assign revised labels
def assign_label(score):
    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Moderate"
    else:
        return "High"

df["support_requirement_label_v2"] = (
    df["revised_score"].apply(assign_label)
)

# 6. Save processed dataset
df.to_csv(OUTPUT_PATH, index=False)

# 7. Display results
print("\n========== REVISED LABEL GENERATION ==========")

print("\nOriginal label distribution:")
print(df["support_requirement_label"].value_counts())

print("\nRevised label distribution:")
print(df["support_requirement_label_v2"].value_counts())

print("\nNumber of labels changed:")
print(
    (df["support_requirement_label"] !=
     df["support_requirement_label_v2"]).sum()
)

print("\nSaved dataset to:")
print(OUTPUT_PATH)

print("\n========== COMPLETED ==========")
