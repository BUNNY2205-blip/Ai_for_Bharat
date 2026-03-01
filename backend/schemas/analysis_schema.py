"""Pydantic schemas for unified AI analysis endpoint."""

from __future__ import annotations

from pydantic import BaseModel, Field

from backend.core.enums import BurnoutRisk, ConceptLevel, ReadinessBand


class AnalysisRequest(BaseModel):
    """Input payload that combines weakness and burnout features."""

    accuracy: float = Field(..., ge=0, le=100, description="Accuracy percentage")
    attempts: int = Field(..., ge=0, description="Number of attempted questions")
    avg_time: float = Field(..., ge=0, description="Average response time in seconds")
    difficulty: int = Field(..., ge=1, le=3, description="Difficulty level: 1, 2, 3")
    repeated_errors: int = Field(..., ge=0, description="Repeated error count")
    accuracy_trend: float = Field(..., description="Change in performance trend")
    time_increase: float = Field(..., ge=0, description="Increase in response time")
    consistency: float = Field(..., ge=0, le=1, description="Consistency score between 0 and 1")
    study_hours: float = Field(..., ge=0, description="Daily study hours")


class Recommendations(BaseModel):
    """Personalized recommendation payload."""

    study_plan: list[str]
    focus_area: str
    rest_advice: str


class AnalysisResponse(BaseModel):
    """Unified prediction and intervention response."""

    concept_level: ConceptLevel
    concept_confidence: float
    burnout_risk: BurnoutRisk
    burnout_confidence: float
    readiness_score: int
    readiness_band: ReadinessBand
    risk_reasoning: list[str]
    recommendations: Recommendations
