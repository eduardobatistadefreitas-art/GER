"""
GER - Geometria Espectral Relacional
S29 - E7

loader.py

Load public S26 artifacts required by the DynamicRegimeBuilder.

Responsibilities
----------------
- Locate JSON files.
- Load JSON files.
- Return Python dictionaries.

This module performs no validation and no scientific processing.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""

from __future__ import annotations

import json
from pathlib import Path

from .exceptions import (
    MissingStationaryScanError,
    MissingClassifierError,
    MissingClassifierAuditError,
)


# ---------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------

def _load_json(path: Path) -> dict:
    """
    Load a JSON file.

    Parameters
    ----------
    path
        JSON file.

    Returns
    -------
    dict
    """

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def load_stationary_scan(path: str | Path) -> dict:
    """
    Load stationary_scan.json.
    """

    path = Path(path)

    if not path.exists():
        raise MissingStationaryScanError(str(path))

    return _load_json(path)


def load_classifier(path: str | Path) -> dict:
    """
    Load classifier.json.
    """

    path = Path(path)

    if not path.exists():
        raise MissingClassifierError(str(path))

    return _load_json(path)


def load_classifier_audit(path: str | Path) -> dict:
    """
    Load classifier_audit.json.
    """

    path = Path(path)

    if not path.exists():
        raise MissingClassifierAuditError(str(path))

    return _load_json(path)


def load(
    stationary_scan_path: str | Path,
    classifier_path: str | Path,
    classifier_audit_path: str | Path,
) -> tuple[dict, dict, dict]:
    """
    Load every public S26 artifact required by E7.

    Returns
    -------
    tuple
        (
            stationary_scan,
            classifier,
            classifier_audit
        )
    """

    stationary_scan = load_stationary_scan(
        stationary_scan_path
    )

    classifier = load_classifier(
        classifier_path
    )

    classifier_audit = load_classifier_audit(
        classifier_audit_path
    )

    return (
        stationary_scan,
        classifier,
        classifier_audit,
    )
