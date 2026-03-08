"""FastAPI application entrypoint for MindLearn AI backend."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import (
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_HEADERS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_ORIGINS,
    configure_logging,
)
from backend.routes.analysis_routes import router as analysis_router
from backend.routes.prediction_routes import router as prediction_router
from backend.schemas.prediction_schema import HealthResponse
from backend.services.ai_service import AIService

configure_logging()

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Go up to /home/bunny/Documents/Ai_for_bharat
MODEL_DIR = BASE_DIR / "models"

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(prediction_router)
api_router.include_router(analysis_router)


@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    """Root endpoint with quick API navigation hints."""
    return {
        "message": "MindLearn AI Backend is running",
        "health": "/api/v1/health",
        "api_base": "/api/v1",
        "docs": "/docs",
    }


@api_router.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    """Health endpoint for uptime checks."""
    return HealthResponse(status="running")


app.include_router(api_router)
