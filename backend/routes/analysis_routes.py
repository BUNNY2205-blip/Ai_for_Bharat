"""Unified analysis endpoint combining prediction and recommendation outputs."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.routes.prediction_routes import get_ai_service
from backend.schemas.analysis_schema import AnalysisRequest, AnalysisResponse
from backend.services.ai_service import AIService

router = APIRouter(prefix="/predict", tags=["analysis"])


@router.post("/analysis", response_model=AnalysisResponse)
def predict_analysis(
    request: AnalysisRequest,
    service: AIService = Depends(get_ai_service),
) -> AnalysisResponse:
    """Run unified analysis for concept level, burnout risk, readiness, and recommendations."""
    result = service.predict_analysis(request.model_dump())
    return AnalysisResponse(**result)
