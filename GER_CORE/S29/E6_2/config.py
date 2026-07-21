"""
============================================================
GER
S29-E6.2
Configuration Module
============================================================

Experiment
----------
Existence of the Relational Signature Space

This module centralizes every configuration parameter used
throughout S29-E6.2.

No other module should contain hard-coded paths, filenames
or experiment constants.

Author
------
Eduardo Batista de Freitas

Framework
---------
GER — Geometria Espectral Relacional

Version
-------
1.0
============================================================
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

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
# E6.2 never reads observables directly.
# Every signature must be obtained through the public
# Signature Provider API.
#

SIGNATURE_PROVIDER_MODULE = (
    "GER.CORE.signature_api"
)

# ============================================================
# Metric Configuration
# ============================================================

#
# Future-proof.
# Even if only one metric exists today,
# experiments should always reference this constant.
#

METRIC = "euclidean"

NORMALIZE_SIGNATURES = True

# ============================================================
# Graph Construction
# ============================================================

#
# Two supported modes:
#
#   "knn"
#   "radius"
#

GRAPH_MODE = "knn"

K_NEIGHBORS = 8

RADIUS = None

# ============================================================
# Numerical Precision
# ============================================================

FLOAT_PRECISION = 10

EPSILON = 1e-12

# ============================================================
# Result Directories
# ============================================================

RESULT_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E6_2"
)

TIMESTAMP = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

RESULT_DIR = RESULT_ROOT / TIMESTAMP

LOG_DIR = RESULT_DIR / "logs"

TABLE_DIR = RESULT_DIR / "tables"

GRAPH_DIR = RESULT_DIR / "graphs"

EXPORT_DIR = RESULT_DIR / "exports"

# ============================================================
# Output Files
# ============================================================

FILES = {

    "summary":
        "experiment_summary.json",

    "metrics":
        "signature_metrics.csv",

    "statistics":
        "space_statistics.csv",

    "distance_matrix":
        "distance_matrix.parquet",

    "graph":
        "signature_graph.graphml",

    "components":
        "connected_components.csv",

    "centrality":
        "centrality_metrics.csv",

    "degree":
        "degree_distribution.csv",

    "log":
        "execution_log.txt",

}

# ============================================================
# Runtime
# ============================================================

VERBOSE = True

SAVE_PARQUET = True

SAVE_JSON = True

SAVE_CSV = True

SAVE_TXT = True

# ============================================================
# Helper Functions
# ============================================================

def initialize_result_directory() -> Path:
    """
    Creates the complete experiment directory tree.

    Returns
    -------
    Path
        Root directory of the current execution.
    """

    RESULT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    LOG_DIR.mkdir(
        exist_ok=True,
    )

    TABLE_DIR.mkdir(
        exist_ok=True,
    )

    GRAPH_DIR.mkdir(
        exist_ok=True,
    )

    EXPORT_DIR.mkdir(
        exist_ok=True,
    )

    return RESULT_DIR


def experiment_metadata() -> dict:
    """
    Returns experiment metadata.

    Returns
    -------
    dict
    """

    return {

        "experiment":

            EXPERIMENT_ID,

        "name":

            EXPERIMENT_NAME,

        "framework":

            FRAMEWORK,

        "version":

            VERSION,

        "author":

            AUTHOR,

        "description":

            DESCRIPTION,

        "timestamp":

            TIMESTAMP,

        "metric":

            METRIC,

        "normalize_signatures":

            NORMALIZE_SIGNATURES,

        "graph_mode":

            GRAPH_MODE,

        "k_neighbors":

            K_NEIGHBORS,

        "radius":

            RADIUS,

    }


def print_configuration() -> None:
    """
    Prints the current experiment configuration.
    """

    print("=" * 60)
    print(FRAMEWORK)
    print(EXPERIMENT_ID)
    print(EXPERIMENT_NAME)
    print("=" * 60)

    print(f"Version      : {VERSION}")
    print(f"Metric       : {METRIC}")
    print(f"Normalize    : {NORMALIZE_SIGNATURES}")
    print(f"Graph Mode   : {GRAPH_MODE}")
    print(f"K Neighbors  : {K_NEIGHBORS}")
    print(f"Result Folder: {RESULT_DIR}")

    print("=" * 60)
