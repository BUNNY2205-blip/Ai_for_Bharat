"""Service layer for loading and running AI model predictions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import HTTPException


WEAKNESS_LABELS = {0: "Strong", 1: "Moderate", 2: "Weak"}
BURNOUT_LABELS = {0: "Low", 1: "Medium", 2: "High"}


class AIService:
    """Encapsulates model loading and inference for the API."""

    def __init__(self, weakness_model_path: Path, burnout_model_path: Path) -> None:
        self.weakness_model_path = weakness_model_path
        self.burnout_model_path = burnout_model_path
        self._weakness_model: Any | None = None
        self._burnout_model: Any | None = None

    def load_models(self) -> None:
        """Load trained models into memory once at startup."""
        if not self.weakness_model_path.exists():
            raise FileNotFoundError(f"Weakness model not found: {self.weakness_model_path}")
        if not self.burnout_model_path.exists():
            raise FileNotFoundError(f"Burnout model not found: {self.burnout_model_path}")

        self._weakness_model = joblib.load(self.weakness_model_path)
        self._burnout_model = joblib.load(self.burnout_model_path)

    def predict_weakness(self, payload: dict[str, float]) -> str:
        """Predict concept level from academic performance features."""
        if self._weakness_model is None:
            raise HTTPException(status_code=503, detail="Weakness model is not loaded")

        input_df = pd.DataFrame([payload])
        try:
            prediction = int(self._weakness_model.predict(input_df)[0])
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Weakness prediction failed") from exc

        return WEAKNESS_LABELS.get(prediction, "Unknown")

    def predict_burnout(self, payload: dict[str, float]) -> str:
        """Predict burnout risk from performance trend features."""
        if self._burnout_model is None:
            raise HTTPException(status_code=503, detail="Burnout model is not loaded")

        input_df = pd.DataFrame([payload])
        try:
            prediction = int(self._burnout_model.predict(input_df)[0])
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Burnout prediction failed") from exc

        return BURNOUT_LABELS.get(prediction, "Unknown")
