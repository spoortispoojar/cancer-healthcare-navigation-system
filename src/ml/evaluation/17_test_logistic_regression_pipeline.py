
from pathlib import Path

import joblib
import pandas as pd


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "src" / "ml" / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "src" / "ml" / "saved_models"

MODEL_PATH = MODEL_DIR / "logistic_regression_pipeline.joblib"


# ==========================================
# 2. LOAD MODEL
# ==========================================

print("Loading Logistic Regression pipeline...")

pipeline = joblib.load(MODEL_PATH)

print("Model loaded successfully!")
print("Model type:", type(pipeline).__name__)


# ==========================================
# 3. LOAD TEST DATA
# ==========================================

X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze("columns")

print("\nTest data loaded.")
print("X_test shape:", X_test.shape)


# ==========================================
# 4. GENERATE PREDICTIONS
# ==========================================

predictions = pipeline.predict(X_test)

print("\nPredictions generated successfully!")


# ==========================================
# 5. COMPARE ACTUAL AND PREDICTED VALUES
# ==========================================

comparison = pd.DataFrame({
    "Actual": y_test,
    "Predicted": predictions
})

print("\nFirst 15 predictions:")
print(comparison.head(15).to_string(index=False))


# ==========================================
# 6. VERIFY PREDICTION OUTPUT
# ==========================================

print("\nPrediction distribution:")
print(pd.Series(predictions).value_counts())

print("\nPrediction test completed successfully!")
