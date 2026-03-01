"""Pydantic schemas for prediction requests and responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WeaknessPredictionRequest(BaseModel):
    """Incoming payload for concept weakness prediction."""

    accuracy: float = Field(..., ge=0, le=100, description="Accuracy percentage")
    attempts: int = Field(..., ge=0, description="Number of attempted questions")
    avg_time: float = Field(..., ge=0, description="Average response time in seconds")
    difficulty: int = Field(..., ge=1, le=3, description="Difficulty level: 1, 2, 3")
    repeated_errors: int = Field(..., ge=0, description="Repeated error count")


class WeaknessPredictionResponse(BaseModel):
    """Response payload for concept weakness prediction."""

    concept_level: str


class BurnoutPredictionRequest(BaseModel):
    """Incoming payload for burnout risk prediction."""

    accuracy_trend: float = Field(..., description="Change in performance trend")
    time_increase: float = Field(..., ge=0, description="Increase in response time")
    consistency: float = Field(..., ge=0, le=1, description="Consistency score between 0 and 1")
    study_hours: float = Field(..., ge=0, description="Daily study hours")


class BurnoutPredictionResponse(BaseModel):
    """Response payload for burnout risk prediction."""

    burnout_risk: str


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
