"""
GER - Geometria Espectral Relacional
S29 - E7

E7_builder.py

DynamicRegime Builder.

This module assembles the public outputs produced by S26 into
the canonical DynamicRegime object used throughout the E7 series.

Responsibilities
----------------
- Load public S26 artifacts.
- Validate public S26 artifacts.
- Build a DynamicRegime instance.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""

from __future__ import annotations

from pathlib import Path

from .loader import load
from .validator import validate

from .model import (
    Audit,
    Classification,
    Configuration,
    DynamicRegime,
    GeometricSignature,
)


class DynamicRegimeBuilder:
    """
    Builder for DynamicRegime objects.
    """

    @staticmethod
    def build(
        stationary_scan_path: str | Path,
        classifier_path: str | Path,
        classifier_audit_path: str | Path,
    ) -> DynamicRegime:
        """
        Build a DynamicRegime from the public outputs of S26.

        Parameters
        ----------
        stationary_scan_path
            Path to stationary_scan.json

        classifier_path
            Path to classifier.json

        classifier_audit_path
            Path to classifier_audit.json

        Returns
        -------
        DynamicRegime
        """

        (
            stationary_scan,
            classifier,
            classifier_audit,
        ) = load(
            stationary_scan_path,
            classifier_path,
            classifier_audit_path,
        )

        validate(
            stationary_scan,
            classifier,
            classifier_audit,
        )

        configuration = Configuration(
            beta=stationary_scan["configuration"]["beta"],
            sigma=stationary_scan["configuration"]["sigma"],
            potential=stationary_scan["configuration"]["potential"],
            timesteps=stationary_scan["configuration"]["timesteps"],
            dt=stationary_scan["configuration"]["dt"],
        )

        signature = GeometricSignature(
            diameter=stationary_scan["signature"]["diameter"],
            convergence=stationary_scan["signature"]["convergence"],
            recurrence=stationary_scan["signature"]["recurrence"],
            drift=stationary_scan["signature"]["drift"],
        )

        classification = Classification(
            regime=classifier["classification"]["regime"],
            persistence_score=classifier["classification"]["persistence_score"],
            persistence_variance=classifier["classification"]["persistence_variance"],
        )

        audit = Audit(
            data=classifier_audit
        )

        return DynamicRegime(
            configuration=configuration,
            signature=signature,
            classification=classification,
            audit=audit,
        )
