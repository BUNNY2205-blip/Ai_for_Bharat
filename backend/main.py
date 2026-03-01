"""FastAPI application entrypoint for MindLearn AI backend."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from backend.routes.prediction_routes import router as prediction_router
from backend.schemas.prediction_schema import HealthResponse
from backend.services.ai_service import AIService

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

ai_service = AIService(
    weakness_model_path=MODEL_DIR / "weakness_model.pkl",
    burnout_model_path=MODEL_DIR / "burnout_model.pkl",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Load models at app startup and release resources at shutdown."""
    ai_service.load_models()
    yield


app = FastAPI(
    title="MindLearn AI Backend",
    description="Backend API for concept weakness and burnout risk prediction.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(prediction_router)


@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    """Root endpoint with quick API navigation hints."""
    return {
        "message": "MindLearn AI Backend is running",
        "health": "/health",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    """Health endpoint for uptime checks."""
    return HealthResponse(status="running")
