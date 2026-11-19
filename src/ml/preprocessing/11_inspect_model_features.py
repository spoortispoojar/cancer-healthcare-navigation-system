
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[3]

DATA_PATH = (
    PROJECT_ROOT
    / "src"
    / "ml"
    / "data"
    / "processed"
    / "X_train.csv"
)


# --------------------------------------------------
# 2. Load training features
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("========== TRAINING FEATURES ==========")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 3. Inspect column names and data types
# --------------------------------------------------

print("\n========== COLUMN DATA TYPES ==========")

print(df.dtypes)


# --------------------------------------------------
# 4. Identify feature categories
# --------------------------------------------------

binary_features = []
numerical_features = []
categorical_features = []

for column in df.columns:

    if pd.api.types.is_numeric_dtype(df[column]):

        unique_values = set(df[column].dropna().unique())

        if unique_values.issubset({0, 1}):
            binary_features.append(column)

        else:
            numerical_features.append(column)

    else:
        categorical_features.append(column)


# --------------------------------------------------
# 5. Display identified feature groups
# --------------------------------------------------

print("\n========== FEATURE CLASSIFICATION ==========")

print("\nBinary Features:")
print(binary_features)
print("Total binary features:", len(binary_features))

print("\nNumerical Features:")
print(numerical_features)
print("Total numerical features:", len(numerical_features))

print("\nCategorical Features:")
print(categorical_features)
print("Total categorical features:", len(categorical_features))


# --------------------------------------------------
# 6. Inspect unique values of categorical features
# --------------------------------------------------

print("\n========== CATEGORICAL FEATURE VALUES ==========")

for column in categorical_features:

    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False))


# --------------------------------------------------
# 7. Check missing values
# --------------------------------------------------

print("\n========== MISSING VALUE CHECK ==========")

print(df.isnull().sum().sum())


# --------------------------------------------------
# 8. Final summary
# --------------------------------------------------

print("\n========== FEATURE INSPECTION SUMMARY ==========")

print("Total features:", len(df.columns))
print("Binary features:", len(binary_features))
print("Numerical features:", len(numerical_features))
print("Categorical features:", len(categorical_features))

print("\nFeature inspection completed successfully.")
