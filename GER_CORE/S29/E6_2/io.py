"""
============================================================
GER
S29-E6.2
Input / Output Module
============================================================

Responsibilities
----------------

• Load signatures from the public Signature Provider.

• Validate loaded signatures.

This module NEVER creates signatures manually.

Persistence and result export are delegated to the
GER CORE infrastructure.

Author
------
Eduardo Batista de Freitas

Framework
---------
GER — Geometria Espectral Relacional

Version
-------
1.0
"""

from __future__ import annotations

import importlib

from .config import SIGNATURE_PROVIDER_MODULE


# ============================================================
# Dynamic Signature Provider
# ============================================================

def load_signature_provider():
    """
    Loads the public Signature Provider.
    """

    return importlib.import_module(
        SIGNATURE_PROVIDER_MODULE
    )


# ============================================================
# Signature Loading
# ============================================================

def load_signatures():
    """
    Loads every available signature using the public API.

    Returns
    -------
    SignatureCollection
    """

    provider = load_signature_provider()

    collection = provider.load_signatures()

    validate_signatures(collection)

    return collection


# ============================================================
# Validation
# ============================================================

def validate_signatures(collection):
    """
    Basic structural validation.
    """

    if collection is None:

        raise RuntimeError(
            "Signature Provider returned None."
        )

    if len(collection) == 0:

        raise RuntimeError(
            "No signatures were loaded."
        )

    dimension = len(collection[0])

    for index, signature in enumerate(collection):

        if len(signature) != dimension:

            raise ValueError(
                "Signature dimension mismatch "
                f"at index {index}."
            )


# ============================================================
# Convenience Helpers
# ============================================================

def number_of_signatures(collection):
    """
    Returns the number of signatures.
    """

    return len(collection)


def signature_dimension(collection):
    """
    Returns the signature dimension.
    """

    return len(collection[0])


# ============================================================
# Public Symbols
# ============================================================

__all__ = [
    "load_signatures",
    "validate_signatures",
    "number_of_signatures",
    "signature_dimension",
]
