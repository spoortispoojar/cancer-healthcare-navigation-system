
import pandas as pd
from pathlib import Path

# 1. Locate processed dataset
ML_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ML_DIR / "data" / "processed" /
    "patient_dataset_v2.csv"
)

# 2. Load dataset
df = pd.read_csv(DATA_PATH)

print("\n========== REVISED DATASET CHECK ==========")

# 3. Dataset dimensions
print("\nDataset shape:")
print(df.shape)

# 4. Missing values
print("\nMissing values:")
print(df.isnull().sum())

# 5. Target distribution
print("\nRevised target distribution:")
print(df["support_requirement_label_v2"].value_counts())

print("\nTarget distribution percentages:")
print(
    df["support_requirement_label_v2"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# 6. Check insurance column
print("\nInsurance column present:")
print("has_health_insurance_or_scheme" in df.columns)

# 7. Check duplicate records
print("\nDuplicate records:")
print(df.duplicated().sum())

print("\n========== CHECK COMPLETED ==========")
