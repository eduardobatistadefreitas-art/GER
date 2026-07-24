"""
============================================================
GER
S29
E6.2
Statistical Observatory
Configuration
============================================================

Global configuration for the Statistical Observatory.

Responsibilities
----------------
- Centralize experiment constants.
- Define default paths.
- Configure numerical parameters.
- Configure export behavior.
- Configure dashboard behavior.

This module intentionally contains no scientific algorithms.

Author
------
GER Project
"""

from __future__ import annotations

from pathlib import Path

# ============================================================
# Version
# ============================================================

CONFIG_VERSION = "1.0"

# ============================================================
# Experiment Identification
# ============================================================

FRAMEWORK = "GER"

SERIES = "S29"

EXPERIMENT = "E6.2"

EXPERIMENT_NAME = "Statistical Observatory"

FULL_NAME = f"{FRAMEWORK} {SERIES} {EXPERIMENT}"

# ============================================================
# Repository
# ============================================================

PROJECT_ROOT = Path("/content/GER")

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS"
)

EXPERIMENT_RESULTS = RESULTS_ROOT / "S29_E6_2"

# ============================================================
# Output folders
# ============================================================

OUTPUT_FOLDERS = (
    "statistics",
    "occupancy",
    "density",
    "concentration",
    "stability",
    "outliers",
    "certificates",
    "reports",
)

# ============================================================
# Export configuration
# ============================================================

EXPORT_CSV = True

EXPORT_JSON = True

EXPORT_TXT = True

EXPORT_PARQUET = False

EXPORT_PNG = False

# ============================================================
# Numerical parameters
# ============================================================

DEFAULT_RANDOM_SEED = 42

DEFAULT_HISTOGRAM_BINS = 50

DEFAULT_PERCENTILES = (
    1,
    5,
    10,
    25,
    50,
    75,
    90,
    95,
    99,
)

EPS = 1e-12

# ============================================================
# Dashboard
# ============================================================

DASHBOARD_TITLE = (
    "GER\n"
    "S29-E6.2\n"
    "Statistical Observatory"
)

DASHBOARD_UPDATE_INTERVAL = 2.0

# ============================================================
# Reports
# ============================================================

REPORT_FILENAME = "statistical_report"

CERTIFICATE_FILENAME = "statistical_certificate"

SUMMARY_FILENAME = "summary"

# ============================================================
# Data
# ============================================================

SUPPORTED_INPUT_FORMATS = (
    ".csv",
    ".json",
    ".parquet",
)

# ============================================================
# Public API
# ============================================================

__all__ = [

    # Version
    "CONFIG_VERSION",

    # Experiment
    "FRAMEWORK",
    "SERIES",
    "EXPERIMENT",
    "EXPERIMENT_NAME",
    "FULL_NAME",

    # Repository
    "PROJECT_ROOT",
    "RESULTS_ROOT",
    "EXPERIMENT_RESULTS",

    # Output
    "OUTPUT_FOLDERS",

    # Export
    "EXPORT_CSV",
    "EXPORT_JSON",
    "EXPORT_TXT",
    "EXPORT_PARQUET",
    "EXPORT_PNG",

    # Numerical
    "DEFAULT_RANDOM_SEED",
    "DEFAULT_HISTOGRAM_BINS",
    "DEFAULT_PERCENTILES",
    "EPS",

    # Dashboard
    "DASHBOARD_TITLE",
    "DASHBOARD_UPDATE_INTERVAL",

    # Reports
    "REPORT_FILENAME",
    "CERTIFICATE_FILENAME",
    "SUMMARY_FILENAME",

    # Data
    "SUPPORTED_INPUT_FORMATS",
]

# ============================================================
# Self Test
# ============================================================

def main():

    print("=" * 60)
    print(FULL_NAME)
    print("Configuration")
    print("=" * 60)
    print()

    print(f"Results Root : {EXPERIMENT_RESULTS}")
    print(f"Histogram Bins : {DEFAULT_HISTOGRAM_BINS}")
    print(f"Export CSV : {EXPORT_CSV}")
    print(f"Export JSON : {EXPORT_JSON}")
    print(f"Export TXT : {EXPORT_TXT}")
    print()

    print("=" * 60)
    print("Configuration loaded successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
