
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# ==========================================
# 1. PROJECT PATHS
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT_DIR / "src" / "ml" / "data" / "raw" /
    "patient_form_training_dataset_7000_clean.csv"
)

OUTPUT_DIR = ROOT_DIR / "reports" / "eda"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD DATASET
# ==========================================

df = pd.read_csv(DATA_PATH)

sns.set_theme(style="whitegrid")

print("\n========== EXPLORATORY DATA ANALYSIS ==========")

# ==========================================
# 3. TARGET VARIABLE DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="support_requirement_label",
    order=["Low", "Moderate", "High"]
)

plt.title("Support Requirement Distribution")
plt.xlabel("Support Requirement")
plt.ylabel("Number of Patients")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_target_distribution.png")
plt.close()

# ==========================================
# 4. CANCER TYPE VS SUPPORT REQUIREMENT
# ==========================================

plt.figure(figsize=(9, 5))

sns.countplot(
    data=df,
    x="cancer_type",
    hue="support_requirement_label",
    hue_order=["Low", "Moderate", "High"]
)

plt.title("Cancer Type vs Support Requirement")
plt.xlabel("Cancer Type")
plt.ylabel("Number of Patients")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_cancer_vs_support.png")
plt.close()

# ==========================================
# 5. AGE DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="age_years",
    bins=20,
    kde=True
)

plt.title("Patient Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Patients")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_age_distribution.png")
plt.close()

# ==========================================
# 6. CANCER STAGE VS SUPPORT
# ==========================================

stage_order = [
    "Stage I",
    "Stage II",
    "Stage III",
    "Stage IV",
    "Not sure"
]

stage_table = pd.crosstab(
    df["cancer_stage"],
    df["support_requirement_label"],
    normalize="index"
)

stage_table = stage_table.reindex(
    columns=["Low", "Moderate", "High"],
    fill_value=0
)

stage_table.plot(
    kind="bar",
    stacked=True,
    figsize=(10, 6)
)

plt.title("Cancer Stage vs Support Requirement")
plt.xlabel("Cancer Stage")
plt.ylabel("Proportion of Patients")
plt.legend(title="Support Requirement")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_stage_vs_support.png")
plt.close()

# ==========================================
# 7. TREATMENT VS SUPPORT
# ==========================================

treatment_counts = df["current_treatment"].value_counts()

plt.figure(figsize=(11, 7))

sns.barplot(
    x=treatment_counts.values,
    y=treatment_counts.index
)

plt.title("Distribution of Treatment Categories")
plt.xlabel("Number of Patients")
plt.ylabel("Treatment")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_treatment_distribution.png")
plt.close()

# ==========================================
# 8. SYMPTOM FREQUENCY
# ==========================================

symptoms = (
    df["selected_symptoms"]
    .dropna()
    .str.split(";")
    .explode()
    .str.strip()
)

symptom_counts = symptoms.value_counts().head(15)

plt.figure(figsize=(11, 7))

sns.barplot(
    x=symptom_counts.values,
    y=symptom_counts.index
)

plt.title("Top 15 Selected Symptoms")
plt.xlabel("Number of Occurrences")
plt.ylabel("Symptoms")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_symptom_distribution.png")
plt.close()

# ==========================================
# 9. SUPPORT FACTORS
# ==========================================

support_columns = [
    "needs_caregiver_support",
    "has_transport_to_hospital",
    "has_health_insurance_or_scheme"
]

for column in support_columns:

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x=column
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column.replace("_", " ").title())
    plt.ylabel("Number of Patients")

    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"07_{column}.png"
    )

    plt.close()

# ==========================================
# 10. SAVE EDA SUMMARY
# ==========================================

print("\nTarget distribution:")
print(df["support_requirement_label"].value_counts())

print("\nCancer type distribution:")
print(df["cancer_type"].value_counts())

print("\nAverage age:")
print(df["age_years"].mean())

print("\nStage vs support:")
print(pd.crosstab(
    df["cancer_stage"],
    df["support_requirement_label"]
))

print("\nEDA charts saved to:")
print(OUTPUT_DIR)

print("\n========== EDA COMPLETED ==========")


# ==========================================
# FINAL EDA: INPUT FEATURES VS TARGET
# ==========================================

target = "support_requirement_label"

# 1. Cancer type vs support requirement
print("\n1. CANCER TYPE VS SUPPORT REQUIREMENT")

print(pd.crosstab(
    df["cancer_type"],
    df[target],
    normalize="index"
).mul(100).round(2))


# 2. Cancer stage vs support requirement
print("\n2. CANCER STAGE VS SUPPORT REQUIREMENT")

print(pd.crosstab(
    df["cancer_stage"],
    df[target],
    normalize="index"
).mul(100).round(2))


# 3. Treatment vs support requirement
print("\n3. TREATMENT VS SUPPORT REQUIREMENT")

print(pd.crosstab(
    df["current_treatment"],
    df[target],
    normalize="index"
).mul(100).round(2))


# 4. Caregiver support vs support requirement
print("\n4. CAREGIVER SUPPORT VS TARGET")

print(pd.crosstab(
    df["needs_caregiver_support"],
    df[target],
    normalize="index"
).mul(100).round(2))


# 5. Transport availability vs support requirement
print("\n5. TRANSPORT AVAILABILITY VS TARGET")

print(pd.crosstab(
    df["has_transport_to_hospital"],
    df[target],
    normalize="index"
).mul(100).round(2))


# 6. Age group vs support requirement
df["age_group"] = pd.cut(
    df["age_years"],
    bins=[0, 40, 50, 60, 70, 100],
    labels=["Below 40", "40-49", "50-59", "60-69", "70+"]
)

print("\n6. AGE GROUP VS SUPPORT REQUIREMENT")

print(pd.crosstab(
    df["age_group"],
    df[target],
    normalize="index"
).mul(100).round(2))


# 7. Symptom severity vs support requirement
print("\n7. SYMPTOM SEVERITY VS SUPPORT REQUIREMENT")

print(pd.crosstab(
    df["symptom_severity"].fillna("None reported"),
    df[target],
    normalize="index"
).mul(100).round(2))


# 8. Symptom presence vs support requirement
df["has_reported_symptoms"] = (
    df["selected_symptoms"].notna()
)

print("\n8. SYMPTOM PRESENCE VS SUPPORT REQUIREMENT")

print(pd.crosstab(
    df["has_reported_symptoms"],
    df[target],
    normalize="index"
).mul(100).round(2))


print("\n========== FINAL EDA COMPLETED ==========")
