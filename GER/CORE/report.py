"""
=========================================================
GER CORE

report.py

=========================================================

Experiment Report

Immutable report returned by the experimental audit.

This object contains the official outcome of one
Reference Universe experiment.

It performs no computation.

Future versions may add export methods (JSON, LaTeX,
console) without changing the experimental interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# =========================================================
# Public API
# =========================================================

__all__ = [
    "ExperimentReport",
]

# =========================================================
# Version
# =========================================================

REPORT_MODULE_VERSION = "1.0"


# =========================================================
# Experiment Report
# =========================================================

@dataclass(frozen=True)
class ExperimentReport:
    """
    Immutable report describing the outcome of one
    Reference Universe experiment.
    """

    signature_generated: bool

    certificate_passed: bool

    reference_universe_updated: bool

    geometry_changed: bool

    new_intrinsic_direction: bool

    reference_universe_coherent: bool

    updated_observables: dict[str, Any] = field(
        default_factory=dict
    )

    comments: str = ""
