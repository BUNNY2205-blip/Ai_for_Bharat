"""Service layer for loading and running AI model predictions."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import HTTPException

from backend.core.constants import (
    BURNOUT_LABELS,
    BURNOUT_STABILITY_MAP,
    CONCEPT_LABELS,
    CONCEPT_SCORE_MAP,
    READINESS_BAND_RULES,
)
from backend.core.enums import BurnoutRisk, ConceptLevel, ReadinessBand

logger = logging.getLogger(__name__)


class AIService:
    """Encapsulates model loading and inference for the API."""

    def __init__(self, weakness_model_path: Path, burnout_model_path: Path) -> None:
        self.weakness_model_path = weakness_model_path
        self.burnout_model_path = burnout_model_path
        self._weakness_model: Any | None = None
        self._burnout_model: Any | None = None

    def load_models(self) -> None:
        """Load trained models into memory once at startup."""
        try:
            if not self.weakness_model_path.exists():
                raise HTTPException(
                    status_code=500,
                    detail=f"Weakness model not found: {self.weakness_model_path}",
                )
            if not self.burnout_model_path.exists():
                raise HTTPException(
                    status_code=500,
                    detail=f"Burnout model not found: {self.burnout_model_path}",
                )

            self._weakness_model = joblib.load(self.weakness_model_path)
            self._burnout_model = joblib.load(self.burnout_model_path)
        except HTTPException:
            raise
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Failed to load AI models") from exc

    def predict_weakness(self, payload: dict[str, float]) -> ConceptLevel:
        """Predict concept level from academic performance features."""
        concept_level, _ = self.predict_weakness_with_confidence(payload)
        return concept_level

    def predict_weakness_with_confidence(
        self, payload: dict[str, float]
    ) -> tuple[ConceptLevel, float]:
        """Predict concept level and confidence from academic performance features."""
        if self._weakness_model is None:
            raise HTTPException(status_code=503, detail="Weakness model is not loaded")

        input_df = pd.DataFrame([payload])
        try:
            prediction = int(self._weakness_model.predict(input_df)[0])
            confidence = round(float(self._weakness_model.predict_proba(input_df).max() * 100), 2)
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Weakness prediction failed") from exc

        concept_level = CONCEPT_LABELS.get(prediction)
        if concept_level is None:
            raise HTTPException(status_code=500, detail="Unknown weakness class predicted")
        logger.info("Weakness Prediction: %s (%.2f%%)", concept_level.value, confidence)
        return concept_level, confidence

    def predict_burnout(self, payload: dict[str, float]) -> BurnoutRisk:
        """Predict burnout risk from performance trend features."""
        burnout_risk, _ = self.predict_burnout_with_confidence(payload)
        return burnout_risk

    def predict_burnout_with_confidence(
        self, payload: dict[str, float]
    ) -> tuple[BurnoutRisk, float]:
        """Predict burnout risk and confidence from performance trend features."""
        if self._burnout_model is None:
            raise HTTPException(status_code=503, detail="Burnout model is not loaded")

        input_df = pd.DataFrame([payload])
        try:
            prediction = int(self._burnout_model.predict(input_df)[0])
            confidence = round(float(self._burnout_model.predict_proba(input_df).max() * 100), 2)
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Burnout prediction failed") from exc

        burnout_risk = BURNOUT_LABELS.get(prediction)
        if burnout_risk is None:
            raise HTTPException(status_code=500, detail="Unknown burnout class predicted")
        logger.info("Burnout Prediction: %s (%.2f%%)", burnout_risk.value, confidence)
        return burnout_risk, confidence

    @staticmethod
    def compute_readiness(
        concept_level: ConceptLevel, burnout_risk: BurnoutRisk
    ) -> tuple[int, ReadinessBand]:
        """Compute readiness score and band from concept and burnout outcomes."""
        concept_score = CONCEPT_SCORE_MAP[concept_level]
        burnout_stability_score = BURNOUT_STABILITY_MAP[burnout_risk]
        readiness_score = int(round((0.6 * concept_score) + (0.4 * burnout_stability_score)))

        readiness_band = ReadinessBand.AT_RISK
        for threshold, band in READINESS_BAND_RULES:
            if readiness_score >= threshold:
                readiness_band = band
                break

        return readiness_score, readiness_band

    @staticmethod
    def build_recommendations(
        concept_level: ConceptLevel, burnout_risk: BurnoutRisk
    ) -> dict[str, Any]:
        """Build personalized recommendations from concept and burnout risk."""
        study_plan = [
            "Complete 1 timed mixed-topic quiz daily.",
            "Review mistakes within 24 hours and note correction patterns.",
        ]
        focus_area = "Maintain balanced revision across all subjects."
        rest_advice = "Take short 5-10 minute breaks every 50 minutes."

        if concept_level == ConceptLevel.WEAK:
            study_plan = [
                "Practice Set: Algebra Q1, Physics Q3, Chemistry Q2.",
                "Revision Plan: 45 min concept recap + 30 min question drill.",
                "Error Log: Track repeated errors and revisit weak topics every 2 days.",
            ]
            focus_area = "Focus Areas: Core fundamentals, formula application, and error-prone topics."
        elif concept_level == ConceptLevel.MODERATE:
            study_plan.append("Add 2 targeted weak-topic practice sets per week.")
            focus_area = "Focus Areas: Medium-difficulty problem solving and speed accuracy."

        if burnout_risk == BurnoutRisk.HIGH:
            study_plan.append("Reduced Study Load: Limit intense sessions to 2 per day this week.")
            rest_advice = (
                "Rest Tips: Sleep 7-8 hours, add one full recovery block daily, and avoid late-night cramming. "
                "Mindfulness Suggestions: 10 minutes of breathing or guided meditation after study sessions."
            )
        elif burnout_risk == BurnoutRisk.MEDIUM:
            rest_advice = (
                "Stabilize workload with one light day per week and add 5 minutes of breathing exercises daily."
            )

        return {
            "study_plan": study_plan,
            "focus_area": focus_area,
            "rest_advice": rest_advice,
        }

    @staticmethod
    def build_risk_reasoning(payload: dict[str, float]) -> list[str]:
        """Generate explainable reasoning statements from analysis input features."""
        reasons: list[str] = []

        if payload["accuracy"] < 50:
            reasons.append("Low accuracy detected")
        if payload["repeated_errors"] > 3:
            reasons.append("High repeated mistake frequency")
        if payload["avg_time"] > 40:
            reasons.append("Slow response time pattern")

        if payload["accuracy_trend"] < -8:
            reasons.append("Significant performance decline")
        if payload["time_increase"] > 10:
            reasons.append("Response time increasing")
        if payload["study_hours"] > 9:
            reasons.append("Potential overwork detected")

        return reasons

    def predict_analysis(self, payload: dict[str, float]) -> dict[str, Any]:
        """Run unified analysis: predictions, readiness score, and recommendations."""
        weakness_payload = {
            "accuracy": payload["accuracy"],
            "attempts": payload["attempts"],
            "avg_time": payload["avg_time"],
            "difficulty": payload["difficulty"],
            "repeated_errors": payload["repeated_errors"],
        }
        burnout_payload = {
            "accuracy_trend": payload["accuracy_trend"],
            "time_increase": payload["time_increase"],
            "consistency": payload["consistency"],
            "study_hours": payload["study_hours"],
        }

        concept_level, concept_confidence = self.predict_weakness_with_confidence(
            weakness_payload
        )
        burnout_risk, burnout_confidence = self.predict_burnout_with_confidence(
            burnout_payload
        )
        readiness_score, readiness_band = self.compute_readiness(concept_level, burnout_risk)
        risk_reasoning = self.build_risk_reasoning(payload)
        recommendations = self.build_recommendations(concept_level, burnout_risk)

        logger.info(
            "Unified analysis completed: concept_level=%s, concept_confidence=%.2f, "
            "burnout_risk=%s, burnout_confidence=%.2f, readiness_score=%s, readiness_band=%s",
            concept_level.value,
            concept_confidence,
            burnout_risk.value,
            burnout_confidence,
            readiness_score,
            readiness_band.value,
        )

        return {
            "concept_level": concept_level,
            "concept_confidence": concept_confidence,
            "burnout_risk": burnout_risk,
            "burnout_confidence": burnout_confidence,
            "readiness_score": readiness_score,
            "readiness_band": readiness_band,
            "risk_reasoning": risk_reasoning,
            "recommendations": recommendations,
        }
