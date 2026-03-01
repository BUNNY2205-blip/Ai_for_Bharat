"""Application configuration for logging and CORS."""

from __future__ import annotations

import logging

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

CORS_ALLOW_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]


def configure_logging() -> None:
    """Initialize application-wide logging config once at startup."""
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
