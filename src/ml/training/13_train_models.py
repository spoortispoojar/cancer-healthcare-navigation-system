
from pathlib import Path
import time

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "src" / "ml" / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "src" / "ml" / "saved_models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. LOAD TRAINING DATA
# ==========================================

X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze("columns")

print("Training data loaded successfully.")
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)


# ==========================================
# 3. IDENTIFY FEATURE TYPES
# ==========================================

NUMERIC_FEATURES = ["age_years"]

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
    column for column in X_train.columns
    if column not in NUMERIC_FEATURES + CATEGORICAL_FEATURES
]

# Validate the expected columns
expected_features = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
    + BINARY_FEATURES
)

if set(expected_features) != set(X_train.columns):
    raise ValueError("Feature column mismatch detected.")

if X_train[expected_features].isnull().any().any():
    raise ValueError("Missing values detected in training features.")

for column in BINARY_FEATURES:
    if not set(X_train[column].dropna().unique()).issubset({0, 1}):
        raise ValueError(
            f"Feature '{column}' is not binary."
        )

print("\nFeature information:")
print("Numerical features:", len(NUMERIC_FEATURES))
print("Categorical features:", len(CATEGORICAL_FEATURES))
print("Binary features:", len(BINARY_FEATURES))
print("Total features:", len(expected_features))


# ==========================================
# 4. CREATE PREPROCESSING PIPELINES
# ==========================================

# Used by Logistic Regression, SVM and KNN
scaled_preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUMERIC_FEATURES),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            CATEGORICAL_FEATURES
        ),
        ("binary", "passthrough", BINARY_FEATURES)
    ]
)

# Used by Decision Tree
tree_preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", NUMERIC_FEATURES),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            CATEGORICAL_FEATURES
        ),
        ("binary", "passthrough", BINARY_FEATURES)
    ]
)


# ==========================================
# 5. DEFINE FOUR CLASSIFICATION MODELS
# ==========================================

models = {
    "Logistic Regression": Pipeline([
        ("preprocessor", scaled_preprocessor),
        ("classifier", LogisticRegression(
            max_iter=2000,
            random_state=42
        ))
    ]),

    "Decision Tree": Pipeline([
        ("preprocessor", tree_preprocessor),
        ("classifier", DecisionTreeClassifier(
            max_depth=10,
            random_state=42
        ))
    ]),

    "SVM": Pipeline([
        ("preprocessor", scaled_preprocessor),
        ("classifier", SVC(
            kernel="rbf",
            C=1.0,
            random_state=42
        ))
    ]),

    "KNN": Pipeline([
        ("preprocessor", scaled_preprocessor),
        ("classifier", KNeighborsClassifier(
            n_neighbors=5,
            weights="uniform",
            metric="minkowski",
            p=2,
            n_jobs=-1
        ))
    ])
}


# ==========================================
# 6. TRAIN AND SAVE MODELS
# ==========================================

print("\n========== MODEL TRAINING STARTED ==========\n")

for model_name, pipeline in models.items():

    print(f"Training {model_name}...")

    start_time = time.time()

    pipeline.fit(X_train, y_train)

    training_time = time.time() - start_time

    file_name = (
        model_name.lower()
        .replace(" ", "_")
        + "_pipeline.joblib"
    )

    model_path = MODEL_DIR / file_name

    joblib.dump(pipeline, model_path)

    print(f"{model_name} trained successfully.")
    print(f"Training time: {training_time:.2f} seconds")
    print(f"Saved to: {model_path}\n")


print("========== MODEL TRAINING COMPLETED ==========")
print("All four models have been saved successfully.")
