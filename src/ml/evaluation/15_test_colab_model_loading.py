
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = PROJECT_ROOT / "src" / "ml" / "saved_models"

model_files = [
    "random_forest_model.joblib",
    "gradient_boosting_model.joblib"
]

for filename in model_files:
    model_path = MODEL_DIR / filename

    print("\n" + "=" * 50)
    print("Testing:", filename)

    if not model_path.exists():
        print("FILE NOT FOUND:", model_path)
        continue

    try:
        model = joblib.load(model_path)
        print("SUCCESS: Model loaded!")
        print("Model type:", type(model).__name__)

    except Exception as error:
        print("FAILED TO LOAD")
        print("Error:", type(error).__name__, error)
