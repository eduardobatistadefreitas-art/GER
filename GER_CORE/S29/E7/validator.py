"""
GER - Geometria Espectral Relacional
S29 - E7

validator.py

Validation routines for DynamicRegime construction.

This module validates the public outputs produced by S26 before
they are assembled into a DynamicRegime.

The validator never modifies data.
It only verifies consistency.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""

from __future__ import annotations

from .exceptions import (
    InvalidStationaryScanError,
    InvalidClassifierError,
    InvalidClassifierAuditError,
)


# ---------------------------------------------------------------------
# Required Fields
# ---------------------------------------------------------------------

_REQUIRED_SIGNATURE = (
    "diameter",
    "convergence",
    "recurrence",
    "drift",
)

_REQUIRED_CONFIGURATION = (
    "beta",
    "sigma",
    "potential",
    "timesteps",
    "dt",
)

_REQUIRED_CLASSIFICATION = (
    "regime",
    "persistence_score",
    "persistence_variance",
)


# ---------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------

def _require(container: dict, fields: tuple[str, ...], exception):
    """
    Ensure that every required field exists.
    """

    missing = [field for field in fields if field not in container]

    if missing:
        raise exception(
            f"Missing required fields: {', '.join(missing)}"
        )


# ---------------------------------------------------------------------
# Stationary Scan
# ---------------------------------------------------------------------

def validate_stationary_scan(data: dict) -> None:
    """
    Validate stationary_scan.json.
    """

    if not isinstance(data, dict):
        raise InvalidStationaryScanError(
            "stationary_scan.json must contain a dictionary."
        )

    if "configuration" not in data:
        raise InvalidStationaryScanError(
            "Missing 'configuration' section."
        )

    if "signature" not in data:
        raise InvalidStationaryScanError(
            "Missing 'signature' section."
        )

    _require(
        data["configuration"],
        _REQUIRED_CONFIGURATION,
        InvalidStationaryScanError,
    )

    _require(
        data["signature"],
        _REQUIRED_SIGNATURE,
        InvalidStationaryScanError,
    )


# ---------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------

def validate_classifier(data: dict) -> None:
    """
    Validate classifier.json.
    """

    if not isinstance(data, dict):
        raise InvalidClassifierError(
            "classifier.json must contain a dictionary."
        )

    if "classification" not in data:
        raise InvalidClassifierError(
            "Missing 'classification' section."
        )

    _require(
        data["classification"],
        _REQUIRED_CLASSIFICATION,
        InvalidClassifierError,
    )


# ---------------------------------------------------------------------
# Classifier Audit
# ---------------------------------------------------------------------

def validate_classifier_audit(data: dict) -> None:
    """
    Validate classifier_audit.json.

    The audit structure is intentionally flexible.
    Only the top-level object is required.
    """

    if not isinstance(data, dict):
        raise InvalidClassifierAuditError(
            "classifier_audit.json must contain a dictionary."
        )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def validate(
    stationary_scan: dict,
    classifier: dict,
    classifier_audit: dict,
) -> None:
    """
    Validate all public S26 products required by E7.
    """

    validate_stationary_scan(stationary_scan)
    validate_classifier(classifier)
    validate_classifier_audit(classifier_audit)
