"""
=========================================================
GER CORE

experiment_pipeline.py

=========================================================

Official Experimental Pipeline

This module defines the official entry point for every
experiment that produces a Geometric Signature.

The pipeline performs no scientific computation.

Its responsibility is only to orchestrate the official
CORE components.

Pipeline

    Signature Generation
            ↓
    Structural Certificate
            ↓
    Validated Result

Future experimental series (S29, S30, S31, ...)
should use this module instead of calling the internal
components directly.
"""

from __future__ import annotations

from GER.CORE.signature_api import (
    generate_signature,
)

from GER.CORE.ger_structural_certificate import (
    structural_certificate,
)

# =========================================================
# Public API
# =========================================================

__all__ = [
    "run_signature_pipeline",
]

# =========================================================
# Version
# =========================================================

EXPERIMENT_PIPELINE_VERSION = "1.0"


# =========================================================
# Official Pipeline
# =========================================================

def run_signature_pipeline(
    *args,
    **kwargs,
):
    """
    Executes the official RSG Signature Pipeline.

    Parameters
    ----------
    *args
        Forwarded to the registered SignatureProvider.

    **kwargs
        Forwarded to the registered SignatureProvider.

    Returns
    -------
    dict

        {
            "signature": Signature,
            "certificate": dict,
        }
    """

    signature = generate_signature(
        *args,
        **kwargs,
    )

    certificate = structural_certificate(
        signature,
    )

    return {

        "signature": signature,

        "certificate": certificate,

    }
