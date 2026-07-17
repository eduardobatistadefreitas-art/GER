"""
=========================================================
GER CORE
Arquivo : bootstrap.py
=========================================================

Official bootstrap of the Relational Spectral Geometry
framework.

Usage

    python bootstrap.py

or

    from GER.CORE.bootstrap import initialize

    initialize()

Responsibilities

- Registers the official Signature Provider
- Validates the CORE
- Leaves the framework ready for experiments
"""

from __future__ import annotations


# =========================================================
# CORE Imports
# =========================================================

from GER.CORE.default_signature_provider import (
    DefaultSignatureProvider,
)

from GER.CORE.signature_api import (
    register_signature_provider,
)

from GER.CORE.ger_validation import (
    validate_GER_CORE,
)


# =========================================================
# Initialization
# =========================================================

def initialize():
    """
    Initializes the official RSG CORE.
    """

    print("=" * 40)
    print(" INITIALIZING RSG CORE")
    print("=" * 40)

    # -----------------------------------------------------
    # Register official Signature Provider
    # -----------------------------------------------------

    register_signature_provider(
        DefaultSignatureProvider()
    )

    # -----------------------------------------------------
    # Validate CORE
    # -----------------------------------------------------

    validate_GER_CORE()

    print()

    print("Official Signature Provider : Registered")
    print("GER CORE ready for experiments.")

    print("=" * 40)

    return True


# =========================================================
# Direct execution
# =========================================================

if __name__ == "__main__":

    initialize()
