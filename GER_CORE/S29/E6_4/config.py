"""
============================================================
GER
S29-E6.4
Configuration Module
============================================================

Centralized configuration for S29-E6.2.

This module contains ONLY experiment parameters.

Directory creation, persistence and export are delegated
to the GER CORE infrastructure.

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

# ============================================================
# Experiment Metadata
# ============================================================

EXPERIMENT_ID = "S29-E6.2"

EXPERIMENT_NAME = (
    "Existence of the Relational Signature Space"
)

VERSION = "1.0"

AUTHOR = "Eduardo Batista de Freitas"

FRAMEWORK = "GER"

DESCRIPTION = (
    "Intrinsic geometric characterization of the "
    "Relational Signature Space."
)

# ============================================================
# Signature Provider
# ============================================================

#
# The experiment must NEVER instantiate signatures directly.
#

SIGNATURE_PROVIDER_MODULE = (
    "GER.CORE.signature_api"
)

# ============================================================
# Metric Configuration
# ============================================================

METRIC = "euclidean"

NORMALIZE_SIGNATURES = True

# ============================================================
# Graph Construction
# ============================================================

#
# Available modes
#
# "knn"
# "radius"
#

GRAPH_MODE = "knn"

GRAPH_K = 8

GRAPH_RADIUS = None

# ============================================================
# Numerical Precision
# ============================================================

FLOAT_PRECISION = 10

EPSILON = 1e-12

# ============================================================
# Runtime
# ============================================================

VERBOSE = True

# ============================================================
# Metadata helper
# ============================================================

def experiment_metadata() -> dict:
    """
    Returns experiment metadata.
    """

    return {

        "experiment": EXPERIMENT_ID,

        "name": EXPERIMENT_NAME,

        "framework": FRAMEWORK,

        "version": VERSION,

        "author": AUTHOR,

        "description": DESCRIPTION,

        "metric": METRIC,

        "normalize_signatures": NORMALIZE_SIGNATURES,

        "graph_mode": GRAPH_MODE,

        "k_neighbors": K_NEIGHBORS,

        "radius": RADIUS,

    }


# ============================================================
# Console helper
# ============================================================

def print_configuration() -> None:

    print("=" * 60)

    print(FRAMEWORK)

    print(EXPERIMENT_ID)

    print(EXPERIMENT_NAME)

    print("=" * 60)

    print(f"Version       : {VERSION}")

    print(f"Metric        : {METRIC}")

    print(f"Normalize     : {NORMALIZE_SIGNATURES}")

    print(f"Graph Mode    : {GRAPH_MODE}")

    print(f"K Neighbors   : {K_NEIGHBORS}")

    print("=" * 60)
