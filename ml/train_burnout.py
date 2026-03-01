"""Train burnout risk classifier for MindLearn AI."""

from __future__ import annotations

from pathlib import Path
import warnings

warnings.filterwarnings(
    "ignore",
    message=".*joblib will operate in serial mode.*",
    category=UserWarning,
)
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight

RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
FEATURES = ["accuracy_trend", "time_increase", "consistency", "study_hours"]
TARGET = "label"
DATA_PATH = Path(__file__).resolve().parent.parent / "dataset" / "burnout_data.csv"
MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = MODEL_DIR / "burnout_model.pkl"
LABEL_NAMES = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}


def load_dataset(path: Path) -> pd.DataFrame:
    """Load and validate training dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run `python ml/generate_dataset.py` first."
        )

    data = pd.read_csv(path)
    required_cols = set(FEATURES + [TARGET])
    missing = required_cols.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns in dataset: {sorted(missing)}")

    return data[FEATURES + [TARGET]].copy()


def compute_balanced_class_weights(y: pd.Series) -> dict[int, float]:
    """Compute balanced class weights from labels."""
    classes = np.sort(y.unique())
    weights = compute_class_weight(class_weight="balanced", classes=classes, y=y)
    return {int(cls): float(weight) for cls, weight in zip(classes, weights)}


def build_pipeline(class_weights: dict[int, float]) -> Pipeline:
    """Create model pipeline with scaling and class-balanced RandomForest."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=10,
                    min_samples_leaf=2,
                    random_state=RANDOM_STATE,
                    class_weight=class_weights,
                    n_jobs=1,
                ),
            ),
        ]
    )


def print_feature_importance(pipeline: Pipeline, feature_names: list[str]) -> None:
    """Print feature importance ranking."""
    classifier = pipeline.named_steps["classifier"]
    importances = classifier.feature_importances_
    ranking = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    print("\nFeature Importance:")
    print(ranking.to_string(index=False))


def train() -> None:
    """Train, evaluate, and persist burnout risk model pipeline."""
    data = load_dataset(DATA_PATH)
    X = data[FEATURES]
    y = data[TARGET].astype(int)

    class_weights = compute_balanced_class_weights(y)
    pipeline = build_pipeline(class_weights=class_weights)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        scoring="f1_weighted",
        cv=cv,
        n_jobs=1,
    )
    print(
        f"Cross-validation (weighted F1, {CV_FOLDS} folds): "
        f"{cv_scores.mean():.4f} +/- {cv_scores.std():.4f}"
    )

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    print("\nBurnout Risk Classification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1, 2],
            target_names=[LABEL_NAMES[i] for i in [0, 1, 2]],
            zero_division=0,
        )
    )
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions, labels=[0, 1, 2]))

    print_feature_importance(pipeline, FEATURES)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nSaved pipeline to: {MODEL_PATH}")


if __name__ == "__main__":
    train()
