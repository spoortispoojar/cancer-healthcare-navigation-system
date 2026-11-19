
import pandas as pd
from pathlib import Path

ML_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ML_DIR / "data" / "processed" /
    "patient_features_v2.csv"
)

df = pd.read_csv(DATA_PATH)

# Extract individual symptoms
symptoms = (
    df.loc[
        df["selected_symptoms"] != "No symptoms reported",
        "selected_symptoms"
    ]
    .dropna()
    .str.split(";")
    .explode()
    .str.strip()
)

# Count occurrences
symptom_counts = symptoms.value_counts()

print("\n========== SYMPTOM VOCABULARY ==========")

print("\nNumber of unique symptoms:")
print(symptom_counts.shape[0])

print("\nAll individual symptoms and their frequencies:")

print(symptom_counts.to_string())

print("\n========== COMPLETED ==========")
