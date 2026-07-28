"""
=============================================================
S29_E9/config.py
=============================================================

Configuration file for S29-E9

Trajectory Relaxation Analysis

This module centralizes every configurable parameter used by
the experiment.

Changing this file should never require modifications in any
other module.

=============================================================
"""

from __future__ import annotations

from pathlib import Path


# ============================================================
# Experiment Metadata
# ============================================================

EXPERIMENT_NAME = "S29_E9"

EXPERIMENT_TITLE = (
    "Trajectory Relaxation Analysis"
)

VERSION = "1.0"


# ============================================================
# Input
# ============================================================

INPUT_FILENAME = "trajectory.csv"


# ============================================================
# Observable Columns
# ============================================================

OBSERVABLES = [

    "delta_sigma",

    "path_length",

    "velocity",

    "acceleration",

    "second_difference",

    "second_difference_rate",

]


# ============================================================
# Candidate Models
# ============================================================

MODELS = [

    "linear",

    "quadratic",

    "exponential",

    "power",

    "logarithmic",

    "inverse",

    "exp_saturation",

]


# ============================================================
# Numerical Settings
# ============================================================

EPSILON = 1e-12

MAX_ITERATIONS = 10000


# ============================================================
# Statistical Metrics
# ============================================================

METRICS = [

    "r2",

    "rmse",

    "mae",

    "aic",

    "bic",

]


# ============================================================
# Output Files
# ============================================================

FIT_SUMMARY_CSV = "E9_fit_summary.csv"

BEST_MODELS_CSV = "E9_best_models.csv"

MODEL_PARAMETERS_CSV = "E9_model_parameters.csv"

STATISTICS_JSON = "E9_statistics.json"

REPORT_TXT = "E9_report.txt"


# ============================================================
# Dashboard
# ============================================================

GENERATE_DASHBOARD = True


# ============================================================
# Report
# ============================================================

REPORT_PRECISION = 6

REPORT_WIDTH = 80


# ============================================================
# Validation
# ============================================================

MIN_REQUIRED_POINTS = 20


# ============================================================
# Helper
# ============================================================

def get_output_files() -> list[str]:
    """
    Returns every output filename produced by E9.
    """

    return [

        FIT_SUMMARY_CSV,

        BEST_MODELS_CSV,

        MODEL_PARAMETERS_CSV,

        STATISTICS_JSON,

        REPORT_TXT,

    ]
