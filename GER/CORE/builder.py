"""
=========================================================
GER CORE

builder.py

=========================================================

Reference Universe Builder

This module is responsible for creating temporary
Reference Universes during experimental campaigns.

The original reference is never modified.

The builder performs no validation and no scientific
interpretation.

Its only responsibility is to extend a frozen Reference
Universe with one additional Geometric Signature.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict

# =========================================================
# Public API
# =========================================================

__all__ = [
    "extend_reference_universe",
]

# =========================================================
# Version
# =========================================================

BUILDER_MODULE_VERSION = "1.0"


# =========================================================
# Utilities
# =========================================================

def _signature_to_dict(signature):

    if hasattr(signature, "__dataclass_fields__"):
        return asdict(signature)

    return dict(signature)


# =========================================================
# Public Builder
# =========================================================

def extend_reference_universe(
    reference,
    signature,
    *,
    system_name="Candidate",
):
    """
    Creates a temporary Reference Universe by extending
    a frozen baseline with one additional Signature.

    Parameters
    ----------
    reference : dict
        Frozen Reference Universe.

    signature : Signature or dict
        Candidate Geometric Signature.

    system_name : str
        Identifier of the candidate system.

    Returns
    -------
    dict
        Independent temporary Reference Universe.
    """

    temporary = deepcopy(reference)

    signature = _signature_to_dict(signature)

    if "reference_universe" not in temporary:

        temporary["reference_universe"] = []

    temporary["reference_universe"].append({

        "system": system_name,

        "signature": signature,

    })

    return temporary
