"""Central constants and mappings for service-layer model outputs."""

from __future__ import annotations

from backend.core.enums import BurnoutRisk, ConceptLevel, ReadinessBand

CONCEPT_LABELS = {
    0: ConceptLevel.STRONG,
    1: ConceptLevel.MODERATE,
    2: ConceptLevel.WEAK,
}

BURNOUT_LABELS = {
    0: BurnoutRisk.LOW,
    1: BurnoutRisk.MEDIUM,
    2: BurnoutRisk.HIGH,
}

CONCEPT_SCORE_MAP = {
    ConceptLevel.STRONG: 100,
    ConceptLevel.MODERATE: 60,
    ConceptLevel.WEAK: 30,
}

BURNOUT_STABILITY_MAP = {
    BurnoutRisk.LOW: 100,
    BurnoutRisk.MEDIUM: 70,
    BurnoutRisk.HIGH: 40,
}

READINESS_BAND_RULES = [
    (80, ReadinessBand.EXCELLENT),
    (60, ReadinessBand.GOOD),
    (40, ReadinessBand.MODERATE),
    (0, ReadinessBand.AT_RISK),
]
