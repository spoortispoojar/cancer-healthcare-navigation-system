
import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


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

X_train = pd.read_csv(DATA_PATH)

print("========== TRAINING DATA LOADED ==========")
print("Training dataset shape:", X_train.shape)


# --------------------------------------------------
# 3. Define feature groups
# --------------------------------------------------

NUMERICAL_FEATURES = [
    "age_years"
]

CATEGORICAL_FEATURES = [
    "cancer_type",
    "cancer_stage",
    "current_treatment",
    "symptom_severity",
    "symptom_duration",
    "symptom_frequency",
    "needs_caregiver_support",
    "has_transport_to_hospital"
]

BINARY_FEATURES = [
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


# --------------------------------------------------
# 4. Verify feature groups
# --------------------------------------------------

ALL_FEATURES = (
    NUMERICAL_FEATURES
    + CATEGORICAL_FEATURES
    + BINARY_FEATURES
)

if len(ALL_FEATURES) != len(set(ALL_FEATURES)):
    raise ValueError("Duplicate features found in feature groups.")

if set(ALL_FEATURES) != set(X_train.columns):
    missing = set(X_train.columns) - set(ALL_FEATURES)
    extra = set(ALL_FEATURES) - set(X_train.columns)

    raise ValueError(
        f"Feature mismatch detected.\n"
        f"Missing from feature groups: {missing}\n"
        f"Not present in dataset: {extra}"
    )

print("\n========== FEATURE GROUPS ==========")
print("Numerical features:", len(NUMERICAL_FEATURES))
print("Categorical features:", len(CATEGORICAL_FEATURES))
print("Binary features:", len(BINARY_FEATURES))
print("Total features:", len(ALL_FEATURES))


# --------------------------------------------------
# 5. Create categorical encoder
# --------------------------------------------------

categorical_encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)


# --------------------------------------------------
# 6. Preprocessing for Logistic Regression
# --------------------------------------------------

logistic_preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            NUMERICAL_FEATURES
        ),
        (
            "categorical",
            categorical_encoder,
            CATEGORICAL_FEATURES
        ),
        (
            "binary",
            "passthrough",
            BINARY_FEATURES
        )
    ],
    remainder="drop"
)


# --------------------------------------------------
# 7. Preprocessing for tree-based algorithms
# --------------------------------------------------

tree_preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            "passthrough",
            NUMERICAL_FEATURES
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            CATEGORICAL_FEATURES
        ),
        (
            "binary",
            "passthrough",
            BINARY_FEATURES
        )
    ],
    remainder="drop"
)


# --------------------------------------------------
# 8. Fit and transform training data
# --------------------------------------------------

print("\n========== LOGISTIC REGRESSION PREPROCESSING ==========")

X_train_logistic = logistic_preprocessor.fit_transform(X_train)

print("Transformed training shape:", X_train_logistic.shape)

print("\n========== TREE-BASED PREPROCESSING ==========")

X_train_tree = tree_preprocessor.fit_transform(X_train)

print("Transformed training shape:", X_train_tree.shape)


# --------------------------------------------------
# 9. Inspect transformed feature names
# --------------------------------------------------

print("\n========== TRANSFORMED FEATURES ==========")

feature_names = tree_preprocessor.get_feature_names_out()

print("Total transformed features:", len(feature_names))

print("\nFeature names:")
for feature in feature_names:
    print(feature)


# --------------------------------------------------
# 10. Final verification
# --------------------------------------------------

if X_train_logistic.shape[0] != len(X_train):
    raise ValueError("Logistic Regression row count mismatch.")

if X_train_tree.shape[0] != len(X_train):
    raise ValueError("Tree-based model row count mismatch.")

if X_train_logistic.shape[1] != X_train_tree.shape[1]:
    raise ValueError("Preprocessing output dimensions do not match.")

if pd.isna(X_train_logistic).any():
    raise ValueError("Missing values found after Logistic Regression preprocessing.")

if pd.isna(X_train_tree).any():
    raise ValueError("Missing values found after tree preprocessing.")

print("\n========== PREPROCESSING VERIFICATION ==========")
print("Logistic Regression preprocessing: Successful")
print("Tree-based preprocessing: Successful")
print("Training records preserved: Yes")
print("Missing values after transformation: 0")

print("\nPreprocessing pipeline verification completed.")
