"""Enum contracts for MindLearn AI API responses."""

from __future__ import annotations

from enum import Enum


class ConceptLevel(str, Enum):
    """Concept proficiency labels returned by the weakness model."""

    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"


class BurnoutRisk(str, Enum):
    """Burnout risk labels returned by the burnout model."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ReadinessBand(str, Enum):
    """Student readiness band derived from unified analysis."""

    EXCELLENT = "Excellent"
    GOOD = "Good"
    MODERATE = "Moderate"
    AT_RISK = "At-Risk"
