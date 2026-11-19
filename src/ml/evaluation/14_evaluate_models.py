
from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "src" / "ml" / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "src" / "ml" / "saved_models"

REPORT_DIR = PROJECT_ROOT / "reports" / "model_evaluation"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. LOAD TEST DATA
# ==========================================

X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze("columns")

print("Test data loaded successfully.")
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)


# ==========================================
# 3. DEFINE SAVED MODELS
# ==========================================

model_files = {
    "Logistic Regression": "logistic_regression_pipeline.joblib",
    "Decision Tree": "decision_tree_pipeline.joblib",
    "SVM": "svm_pipeline.joblib",
    "KNN": "knn_pipeline.joblib"
}


# ==========================================
# 4. EVALUATE EACH MODEL
# ==========================================

results = []

print("\n========== MODEL EVALUATION STARTED ==========\n")

for model_name, file_name in model_files.items():

    print(f"Evaluating {model_name}...")

    model_path = MODEL_DIR / file_name

    pipeline = joblib.load(model_path)

    # Generate predictions using the complete pipeline
    y_pred = pipeline.predict(X_test)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test, y_pred,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_test, y_pred,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_test, y_pred,
        average="macro",
        zero_division=0
    )

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision_Macro": precision,
        "Recall_Macro": recall,
        "F1_Macro": f1
    })

    # Detailed classification report
    report = classification_report(
        y_test,
        y_pred,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report).transpose()

    report_path = REPORT_DIR / (
        model_name.lower().replace(" ", "_")
        + "_classification_report.csv"
    )

    report_df.to_csv(report_path)

    # Confusion matrix
    class_labels = pipeline.classes_

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=class_labels
    )

    cm_df = pd.DataFrame(
        cm,
        index=class_labels,
        columns=class_labels
    )

    cm_df.index.name = "Actual"
    cm_df.columns.name = "Predicted"

    cm_path = REPORT_DIR / (
        model_name.lower().replace(" ", "_")
        + "_confusion_matrix.csv"
    )

    cm_df.to_csv(cm_path)

    print(f"{model_name} evaluation completed.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision (Macro): {precision:.4f}")
    print(f"Recall (Macro): {recall:.4f}")
    print(f"F1-score (Macro): {f1:.4f}")
    print()


# ==========================================
# 5. CREATE MODEL COMPARISON TABLE
# ==========================================

comparison_df = pd.DataFrame(results)

comparison_df = comparison_df.sort_values(
    by="F1_Macro",
    ascending=False
)

comparison_path = REPORT_DIR / "model_comparison.csv"

comparison_df.to_csv(comparison_path, index=False)


# ==========================================
# 6. DISPLAY FINAL RESULTS
# ==========================================

print("\n========== MODEL COMPARISON ==========\n")

print(
    comparison_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision_Macro": "{:.4f}".format,
            "Recall_Macro": "{:.4f}".format,
            "F1_Macro": "{:.4f}".format
        }
    )
)

print("\nBest model by macro F1-score:")
print(comparison_df.iloc[0]["Model"])

print("\nEvaluation reports saved in:")
print(REPORT_DIR)

print("\n========== EVALUATION COMPLETED ==========")
