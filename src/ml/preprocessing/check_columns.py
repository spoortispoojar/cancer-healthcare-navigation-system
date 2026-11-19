import pandas as pd

df = pd.read_csv(
    "src/ml/data/processed/patient_engineered_features_v2.csv"
)

print("Dataset shape:", df.shape)
print("\nDoes selected_symptoms still exist?")
print("selected_symptoms" in df.columns)

print("\nAll columns:")
print(df.columns.tolist())