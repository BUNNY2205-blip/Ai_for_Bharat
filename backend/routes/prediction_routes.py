"""Prediction endpoints for weakness and burnout risk."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.schemas.prediction_schema import (
    BurnoutPredictionRequest,
    BurnoutPredictionResponse,
    WeaknessPredictionRequest,
    WeaknessPredictionResponse,
)
from backend.services.ai_service import AIService

router = APIRouter(prefix="/predict", tags=["prediction"])


def get_ai_service() -> AIService:
    """Dependency that returns the initialized AI service."""
    from backend.main import ai_service

    return ai_service


@router.post("/weakness", response_model=WeaknessPredictionResponse)
def predict_weakness(
    request: WeaknessPredictionRequest,
    service: AIService = Depends(get_ai_service),
) -> WeaknessPredictionResponse:
    """Predict concept weakness level for a student."""
    concept_level = service.predict_weakness(request.model_dump())
    return WeaknessPredictionResponse(concept_level=concept_level)


@router.post("/burnout", response_model=BurnoutPredictionResponse)
def predict_burnout(
    request: BurnoutPredictionRequest,
    service: AIService = Depends(get_ai_service),
) -> BurnoutPredictionResponse:
    """Predict burnout risk level for a student."""
    burnout_risk = service.predict_burnout(request.model_dump())
    return BurnoutPredictionResponse(burnout_risk=burnout_risk)
