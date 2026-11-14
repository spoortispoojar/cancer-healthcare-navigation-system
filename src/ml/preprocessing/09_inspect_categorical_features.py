
import pandas as pd
from pathlib import Path

ML_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ML_DIR / "data" / "processed" /
    "patient_engineered_features_v2.csv"
)

df = pd.read_csv(DATA_PATH)

# Identify categorical columns
categorical_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

print("\n========== CATEGORICAL FEATURE INSPECTION ==========")

for column in categorical_columns:
    print(f"\n{column}")
    print("Unique values:", df[column].nunique())
    print(df[column].value_counts().to_string())

print("\nTotal categorical columns:", len(categorical_columns))

print("\nDataset shape:", df.shape)

print("\n========== COMPLETED ==========")
