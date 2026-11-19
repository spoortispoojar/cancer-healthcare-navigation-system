
from pathlib import Path
import pandas as pd


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REPORT_DIR = PROJECT_ROOT / "reports" / "model_evaluation"

LOCAL_RESULTS = REPORT_DIR / "model_comparison.csv"

COLAB_RESULTS = REPORT_DIR / "colab_model_results.csv"

OUTPUT_FILE = REPORT_DIR / "all_models_comparison.csv"


# ==========================================
# 2. LOAD RESULTS
# ==========================================

local_df = pd.read_csv(LOCAL_RESULTS)
colab_df = pd.read_csv(COLAB_RESULTS)

print("Local model results loaded:", len(local_df))
print("Colab model results loaded:", len(colab_df))


# ==========================================
# 3. STANDARDIZE COLUMN NAMES
# ==========================================

local_df = local_df.rename(columns={
    "Precision_Macro": "Precision",
    "Recall_Macro": "Recall",
    "F1_Macro": "Macro_F1"
})

colab_df = colab_df.rename(columns={
    "Macro F1": "Macro_F1"
})


# ==========================================
# 4. SELECT COMMON METRICS
# ==========================================

metrics = [
    "Model",
    "Accuracy",
    "Precision",
    "Recall",
    "Macro_F1"
]

local_df = local_df[metrics]
colab_df = colab_df[metrics]


# ==========================================
# 5. COMBINE RESULTS
# ==========================================

comparison_df = pd.concat(
    [local_df, colab_df],
    ignore_index=True
)

comparison_df = comparison_df.sort_values(
    by="Macro_F1",
    ascending=False
).reset_index(drop=True)


# ==========================================
# 6. SAVE FINAL COMPARISON
# ==========================================

comparison_df.to_csv(OUTPUT_FILE, index=False)


# ==========================================
# 7. DISPLAY RESULTS
# ==========================================

print("\n========== SIX-MODEL COMPARISON ==========\n")

print(
    comparison_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "Macro_F1": "{:.4f}".format
        }
    )
)

print("\nBest model by Macro F1:")
print(comparison_df.iloc[0]["Model"])

print("\nSaved comparison to:")
print(OUTPUT_FILE)
