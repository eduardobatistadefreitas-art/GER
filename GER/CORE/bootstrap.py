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

- Validates the CORE
- Leaves the framework ready for experiments

NOTE

The official SignatureProvider registration will be
enabled after the complete migration of the geometric
operators to the CORE.
"""

from __future__ import annotations


# =========================================================
# CORE Imports
# =========================================================

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
    # Validate CORE
    # -----------------------------------------------------

    validate_GER_CORE()

    print()

    print("GER CORE ready for experiments.")

    print("=" * 40)

    return True


# =========================================================
# Direct execution
# =========================================================

if __name__ == "__main__":

    initialize()
