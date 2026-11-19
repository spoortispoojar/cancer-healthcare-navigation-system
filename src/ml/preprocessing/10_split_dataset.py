
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parents[3]

DATASET_PATH = (
    PROJECT_ROOT
    / "src"
    / "ml"
    / "data"
    / "processed"
    / "patient_engineered_features_v2.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "src" / "ml" / "data" / "processed"


# --------------------------------------------------
# 2. Load the engineered dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print("========== DATASET LOADED ==========")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 3. Separate input features and target
# --------------------------------------------------

TARGET_COLUMN = "support_requirement_label_v2"

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

print("\n========== FEATURES AND TARGET ==========")
print("Input features shape:", X.shape)
print("Target shape:", y.shape)


# --------------------------------------------------
# 4. Perform stratified train/test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 5. Display split information
# --------------------------------------------------

print("\n========== SPLIT INFORMATION ==========")

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining target distribution:")
print(y_train.value_counts())
print("\nTraining target percentages:")
print(
    (y_train.value_counts(normalize=True) * 100).round(2)
)

print("\nTesting target distribution:")
print(y_test.value_counts())
print("\nTesting target percentages:")
print(
    (y_test.value_counts(normalize=True) * 100).round(2)
)


# --------------------------------------------------
# 6. Save training and testing datasets
# --------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

X_train.to_csv(OUTPUT_DIR / "X_train.csv", index=False)
X_test.to_csv(OUTPUT_DIR / "X_test.csv", index=False)

y_train.to_frame().to_csv(
    OUTPUT_DIR / "y_train.csv",
    index=False
)

y_test.to_frame().to_csv(
    OUTPUT_DIR / "y_test.csv",
    index=False
)


# --------------------------------------------------
# 7. Completion message
# --------------------------------------------------

print("\n========== TRAIN/TEST SPLIT COMPLETED ==========")
print("All four datasets have been saved successfully.")
