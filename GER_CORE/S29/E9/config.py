"""
=============================================================
S29_E9/config.py
=============================================================

Trajectory Relaxation Analysis

Central configuration file.

=============================================================
"""

from __future__ import annotations

# ============================================================
# Experiment
# ============================================================

EXPERIMENT_NAME = "S29_E9"

EXPERIMENT_TITLE = "Trajectory Relaxation Analysis"

VERSION = "1.1"

STATUS = "Prototype"


# ============================================================
# Observables
# ============================================================

AVAILABLE_OBSERVABLES = [

    "delta_sigma",

    "path_length",

    "velocity",

    "acceleration",

    "second_difference",

    "second_difference_rate",

]


# ============================================================
# Mathematical Models
# ============================================================

ENABLED_MODELS = [

    "linear",

    "quadratic",

    "exponential",

    "power",

    "logarithmic",

    "inverse",

    "exp_saturation",

    "michaelis_menten",

    "logistic",

]


# ============================================================
# Fitting
# ============================================================

MAX_FIT_ITERATIONS = 10000

FIT_TOLERANCE = 1e-10

ALLOW_NEGATIVE_PARAMETERS = True


# ============================================================
# Model Selection
# ============================================================

MODEL_SELECTION_POLICY = "balanced"

PRIMARY_SELECTION_METRIC = "aic"

SECONDARY_SELECTION_METRIC = "bic"

TERTIARY_SELECTION_METRIC = "r2"


# ============================================================
# Balanced Policy
# ============================================================

#
# Future configurable score:
#
# score =
#     w1*AIC_norm +
#     w2*BIC_norm -
#     w3*R2_norm
#

BALANCED_SCORE_ENABLED = False

BALANCED_AIC_WEIGHT = 1.0

BALANCED_BIC_WEIGHT = 1.0

BALANCED_R2_WEIGHT = 1.0


# ============================================================
# Acceptance Thresholds
# ============================================================

MIN_R2_ACCEPTABLE = 0.80

MAX_RMSE_ACCEPTABLE = None

MAX_MAE_ACCEPTABLE = None


# ============================================================
# Residual Statistics
# ============================================================

RESIDUAL_DDOF = 1

RESIDUAL_NORMALITY_TEST = True

RESIDUAL_AUTOCORRELATION = True


# ============================================================
# Confidence Levels
# ============================================================

HIGH_CONFIDENCE_R2 = 0.98

MEDIUM_CONFIDENCE_R2 = 0.95

LOW_CONFIDENCE_R2 = 0.90

# ============================================================
# Report
# ============================================================

REPORT_WIDTH = 80

REPORT_DECIMAL_PRECISION = 6

REPORT_SEPARATOR = "="

REPORT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

REPORT_INCLUDE_PARAMETERS = True

REPORT_INCLUDE_RESIDUALS = True

REPORT_INCLUDE_RANKING = True

REPORT_INCLUDE_CERTIFICATE = True


# ============================================================
# Dashboard
# ============================================================

DASHBOARD_INCLUDE_METADATA = True

DASHBOARD_INCLUDE_SELECTION = True

DASHBOARD_INCLUDE_PARAMETERS = True

DASHBOARD_INCLUDE_RESIDUALS = True

DASHBOARD_INCLUDE_RANKING = True

DASHBOARD_INCLUDE_CERTIFICATE = True


# ============================================================
# Output Files
# ============================================================

OUTPUT_REPORT_FILENAME = "report.txt"

OUTPUT_DASHBOARD_FILENAME = "dashboard.json"

OUTPUT_SUMMARY_FILENAME = "summary.json"

OUTPUT_STATISTICS_FILENAME = "statistics.json"

OUTPUT_CERTIFICATE_FILENAME = "certificate.json"


# ============================================================
# Output Options
# ============================================================

EXPORT_JSON = True

EXPORT_TEXT = True

EXPORT_CSV = False


# ============================================================
# Public API
# ============================================================

def available_models():
    """
    Return enabled models.
    """

    return list(

        ENABLED_MODELS

    )


def available_observables():
    """
    Return available observables.
    """

    return list(

        AVAILABLE_OBSERVABLES

    )


def output_files():
    """
    Return output file names.
    """

    return {

        "report":

            OUTPUT_REPORT_FILENAME,

        "dashboard":

            OUTPUT_DASHBOARD_FILENAME,

        "summary":

            OUTPUT_SUMMARY_FILENAME,

        "statistics":

            OUTPUT_STATISTICS_FILENAME,

        "certificate":

            OUTPUT_CERTIFICATE_FILENAME,

    }


__all__ = [

    "EXPERIMENT_NAME",
    "EXPERIMENT_TITLE",
    "VERSION",
    "STATUS",

    "AVAILABLE_OBSERVABLES",

    "ENABLED_MODELS",

    "MAX_FIT_ITERATIONS",
    "FIT_TOLERANCE",
    "ALLOW_NEGATIVE_PARAMETERS",

    "MODEL_SELECTION_POLICY",
    "PRIMARY_SELECTION_METRIC",
    "SECONDARY_SELECTION_METRIC",
    "TERTIARY_SELECTION_METRIC",

    "BALANCED_SCORE_ENABLED",
    "BALANCED_AIC_WEIGHT",
    "BALANCED_BIC_WEIGHT",
    "BALANCED_R2_WEIGHT",

    "MIN_R2_ACCEPTABLE",
    "MAX_RMSE_ACCEPTABLE",
    "MAX_MAE_ACCEPTABLE",

    "RESIDUAL_DDOF",
    "RESIDUAL_NORMALITY_TEST",
    "RESIDUAL_AUTOCORRELATION",

    "HIGH_CONFIDENCE_R2",
    "MEDIUM_CONFIDENCE_R2",
    "LOW_CONFIDENCE_R2",

    "REPORT_WIDTH",
    "REPORT_DECIMAL_PRECISION",
    "REPORT_SEPARATOR",
    "REPORT_TIMESTAMP_FORMAT",
    "REPORT_INCLUDE_PARAMETERS",
    "REPORT_INCLUDE_RESIDUALS",
    "REPORT_INCLUDE_RANKING",
    "REPORT_INCLUDE_CERTIFICATE",

    "DASHBOARD_INCLUDE_METADATA",
    "DASHBOARD_INCLUDE_SELECTION",
    "DASHBOARD_INCLUDE_PARAMETERS",
    "DASHBOARD_INCLUDE_RESIDUALS",
    "DASHBOARD_INCLUDE_RANKING",
    "DASHBOARD_INCLUDE_CERTIFICATE",

    "OUTPUT_REPORT_FILENAME",
    "OUTPUT_DASHBOARD_FILENAME",
    "OUTPUT_SUMMARY_FILENAME",
    "OUTPUT_STATISTICS_FILENAME",
    "OUTPUT_CERTIFICATE_FILENAME",

    "EXPORT_JSON",
    "EXPORT_TEXT",
    "EXPORT_CSV",

    "available_models",
    "available_observables",
    "output_files",

]
