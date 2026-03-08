"""Application configuration for logging and CORS."""

from __future__ import annotations

import logging
import os

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

DEFAULT_CORS_ORIGINS = (
    "http://aiforbharat-frontend.s3-website-us-east-1.amazonaws.com,"
    "http://localhost:5173"
)

CORS_ALLOW_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type"]


def configure_logging() -> None:
    """Initialize application-wide logging config once at startup."""
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
