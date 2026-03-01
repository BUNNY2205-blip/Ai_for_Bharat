"""Run sample predictions for MindLearn AI models."""

from __future__ import annotations

from pathlib import Path
import warnings

warnings.filterwarnings(
    "ignore",
    message=".*joblib will operate in serial mode.*",
    category=UserWarning,
)
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"
WEAKNESS_MODEL_PATH = MODEL_DIR / "weakness_model.pkl"
BURNOUT_MODEL_PATH = MODEL_DIR / "burnout_model.pkl"

WEAKNESS_LABELS = {0: "Strong", 1: "Moderate", 2: "Weak"}
BURNOUT_LABELS = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}


def load_model(path: Path):
    """Load serialized sklearn pipeline."""
    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found at {path}. Train the model before prediction."
        )
    return joblib.load(path)


def predict_weakness(model) -> str:
    """Predict concept strength level from sample student data."""
    sample_academic = pd.DataFrame(
        [
            {
                "accuracy": 58.0,
                "attempts": 12,
                "avg_time": 41.0,
                "difficulty": 2,
                "repeated_errors": 3,
            }
        ]
    )
    prediction = int(model.predict(sample_academic)[0])
    return WEAKNESS_LABELS[prediction]


def predict_burnout(model) -> str:
    """Predict burnout risk level from sample performance trend data."""
    sample_burnout = pd.DataFrame(
        [
            {
                "accuracy_trend": -11.5,
                "time_increase": 14.0,
                "consistency": 0.33,
                "study_hours": 9.0,
            }
        ]
    )
    prediction = int(model.predict(sample_burnout)[0])
    return BURNOUT_LABELS[prediction]


def main() -> None:
    """Load models and print readable predictions."""
    weakness_model = load_model(WEAKNESS_MODEL_PATH)
    burnout_model = load_model(BURNOUT_MODEL_PATH)

    concept_level = predict_weakness(weakness_model)
    burnout_level = predict_burnout(burnout_model)

    print(f"Concept Strength Level: {concept_level}")
    print(f"Burnout Risk Level: {burnout_level}")


if __name__ == "__main__":
    main()
