"""
GER - Geometria Espectral Relacional
S29 - E7

model.py

Scientific domain model for Dynamic Regimes.

This module defines the canonical data structures used by the
E7 experimental series. The classes declared here are passive
containers and do not implement loading, validation or analysis.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Configuration:
    """
    Numerical configuration used during the GER simulation.
    """

    beta: float
    sigma: float
    potential: str
    timesteps: int
    dt: float


# ---------------------------------------------------------------------
# Geometric Signature
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class GeometricSignature:
    """
    Canonical geometric signature produced by S26.
    """

    diameter: float
    convergence: float
    recurrence: float
    drift: float


# ---------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Classification:
    """
    Dynamic regime assigned by the classifier.
    """

    regime: str
    persistence_score: float
    persistence_variance: float


# ---------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Audit:
    """
    Optional audit information produced by the classifier audit.

    The structure is intentionally flexible because future versions
    of S26 may extend the audit without changing the E7 interface.
    """

    data: Dict[str, Any]


# ---------------------------------------------------------------------
# Dynamic Regime
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class DynamicRegime:
    """
    Canonical scientific object manipulated by S29-E7.

    This object integrates the public outputs produced by S26
    into a single domain representation.

    The Builder is responsible for constructing instances.
    """

    configuration: Configuration

    signature: GeometricSignature

    classification: Classification

    audit: Optional[Audit] = None
