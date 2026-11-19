
import pandas as pd
from pathlib import Path

# 1. Paths
ML_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ML_DIR / "data" / "processed" /
    "patient_features_v2.csv"
)

OUTPUT_DIR = ML_DIR / "data" / "processed"

OUTPUT_PATH = (
    OUTPUT_DIR / "patient_engineered_features_v2.csv"
)

# 2. Load dataset
df = pd.read_csv(DATA_PATH)

# 3. Define the 26 symptoms found during inspection
symptom_list = [
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

# 4. Convert symptom strings into binary columns
for symptom in symptom_list:
    df[symptom] = df["selected_symptoms"].apply(
        lambda value: int(
            symptom in [
                item.strip()
                for item in value.split(";")
            ]
        )
        if value != "No symptoms reported"
        else 0
    )

# 5. Remove original combined symptom column
df = df.drop(columns=["selected_symptoms"])

# 6. Save engineered dataset
df.to_csv(OUTPUT_PATH, index=False)

# 7. Verification
print("\n========== FEATURE ENGINEERING ==========")

print("\nDataset shape:")
print(df.shape)

print("\nNumber of symptom features:")
print(len(symptom_list))

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nSample symptom features:")
print(df[symptom_list].head())

print("\nTotal symptom selections:")
print(df[symptom_list].sum().sum())

print("\nSaved to:")
print(OUTPUT_PATH)

print("\n========== COMPLETED ==========")
