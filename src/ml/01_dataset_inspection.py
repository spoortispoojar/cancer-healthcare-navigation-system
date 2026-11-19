
import pandas as pd
from pathlib import Path

# ----------------------------------
# 1. SET PROJECT PATHS
# ----------------------------------

ML_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    ML_DIR / "data" / "raw" /
    "patient_form_training_dataset_7000_clean.csv"
)

# ----------------------------------
# 2. LOAD DATASET
# ----------------------------------

df = pd.read_csv(DATA_PATH)

print("\n========== DATASET INSPECTION ==========\n")

# ----------------------------------
# 3. DATASET DIMENSIONS
# ----------------------------------

print("Dataset Shape:")
print(df.shape)

print("\nNumber of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])

# ----------------------------------
# 4. COLUMN NAMES
# ----------------------------------

print("\nColumn Names:")
print(df.columns.tolist())

# ----------------------------------
# 5. DATA TYPES
# ----------------------------------

print("\nData Types:")
print(df.dtypes)

# ----------------------------------
# 6. MISSING VALUES
# ----------------------------------

print("\nMissing Values:")
print(df.isnull().sum())

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

# ----------------------------------
# 7. DUPLICATE RECORDS
# ----------------------------------

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nDuplicate Patient IDs:")
print(df["patient_record_id"].duplicated().sum())

# ----------------------------------
# 8. UNIQUE VALUES
# ----------------------------------

print("\nUnique Values in Each Column:")

for column in df.columns:
    print(f"\n{column}:")
    print(df[column].nunique())

# ----------------------------------
# 9. TARGET VARIABLE DISTRIBUTION
# ----------------------------------

target = "support_requirement_label"

print("\nTarget Variable Distribution:")
print(df[target].value_counts())

print("\nTarget Distribution (%):")
print(
    df[target]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# ----------------------------------
# 10. CANCER TYPE DISTRIBUTION
# ----------------------------------

print("\nCancer Type Distribution:")
print(df["cancer_type"].value_counts())

# ----------------------------------
# 11. DATASET SUMMARY
# ----------------------------------

print("\nDataset Statistical Summary:")
print(df.describe(include="all").T)

print("\n========== INSPECTION COMPLETED ==========")


# ----------------------------------
# 12. INVESTIGATE MISSING SYMPTOMS
# ----------------------------------

print("\n========== MISSING VALUE INVESTIGATION ==========")

missing_rows = df[
    df["selected_symptoms"].isna() |
    df["symptom_severity"].isna()
]

print("\nNumber of affected records:")
print(len(missing_rows))

print("\nMissing symptom combinations:")
print(
    missing_rows[
        ["selected_symptoms", "symptom_severity"]
    ].value_counts(dropna=False)
)

print("\nSample affected records:")

print(
    missing_rows[
        [
            "cancer_type",
            "cancer_stage",
            "current_treatment",
            "selected_symptoms",
            "symptom_severity",
            "symptom_duration",
            "symptom_frequency",
            "support_requirement_label"
        ]
    ].head(15).to_string(index=False)
)

print("\n========== INVESTIGATION COMPLETED ==========")

print("\nUnique symptom severity values:")
print(df["symptom_severity"].value_counts(dropna=False))

print("\nUnique symptom duration values:")
print(df["symptom_duration"].value_counts(dropna=False))

print("\nUnique symptom frequency values:")
print(df["symptom_frequency"].value_counts(dropna=False))

print("\nTreatment categories:")
print(df["current_treatment"].value_counts())


# ----------------------------------
# 13. INVESTIGATE LABEL GENERATION
# ----------------------------------

print("\n========== LABEL GENERATION ANALYSIS ==========")

print("\nSample label_basis values:")

for value in df["label_basis"].drop_duplicates().head(20):
    print(value)

print("\nLabel distribution for records with no symptoms:")

no_symptoms = df["selected_symptoms"].isna()

print(
    df.loc[no_symptoms, "support_requirement_label"]
    .value_counts()
)

print("\nLabel distribution for records with symptoms:")

print(
    df.loc[~no_symptoms, "support_requirement_label"]
    .value_counts()
)

print("\n========== LABEL ANALYSIS COMPLETED ==========")

