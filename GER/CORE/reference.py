"""
=========================================================
GER CORE

reference.py

=========================================================

Reference Universe Loader

This module provides the official interface for loading
frozen Reference Universes used by experimental series.

The loader performs no validation or interpretation.

It simply reads a persisted reference and returns its
contents.

Future baselines (S29, S30, ...) may be added without
changing the public API.
"""

from __future__ import annotations

import json
from pathlib import Path

# =========================================================
# Public API
# =========================================================

__all__ = [
    "load_reference",
]

# =========================================================
# Version
# =========================================================

REFERENCE_MODULE_VERSION = "1.0"

# =========================================================
# Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIRECTORY = PROJECT_ROOT / "DATA"

# =========================================================
# Public Loader
# =========================================================

def load_reference(name):
    """
    Loads a frozen Reference Universe.

    Parameters
    ----------
    name : str

        Reference name without extension.

        Example
        -------
        "S28_REFERENCE"

    Returns
    -------
    dict
        Parsed JSON reference.
    """

    filename = DATA_DIRECTORY / f"{name}.json"

    if not filename.exists():

        raise FileNotFoundError(

            f"Reference '{name}' not found:\n"

            f"{filename}"

        )

    with filename.open(

        "r",

        encoding="utf-8",

    ) as file:

        return json.load(file)
