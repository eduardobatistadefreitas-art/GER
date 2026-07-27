"""
GER - Geometria Espectral Relacional
S29 - E7.5

Geometric Representation

Defines the possible geometric representations of a
DynamicRegime and the data structures used during the
representation analysis.

This module contains no scientific decision logic.
It only defines the domain model used by the analyzer.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ============================================================
# Representation Types
# ============================================================

class RepresentationType(Enum):

    POINT = "POINT"

    REGION = "REGION"

    TRAJECTORY = "TRAJECTORY"

    SET = "SET"

    CENTROID = "CENTROID"

    MANIFOLD = "MANIFOLD"

    UNKNOWN = "UNKNOWN"


# ============================================================
# Evidence
# ============================================================

@dataclass(frozen=True)
class RepresentationEvidence:

    hypothesis: RepresentationType

    supported: bool

    confidence: float

    reason: str


# ============================================================
# Analysis
# ============================================================

@dataclass
class RepresentationAnalysis:

    evidences: List[
        RepresentationEvidence
    ] = field(
        default_factory=list
    )

    recommended: RepresentationType = (
        RepresentationType.UNKNOWN
    )

    completed: bool = False
