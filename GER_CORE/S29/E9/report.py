"""
=============================================================
S29_E9/report.py
=============================================================

Trajectory Relaxation Analysis

Report Generation Module

This module converts numerical results into a human-readable
scientific report.

=============================================================
"""

from __future__ import annotations

from datetime import datetime

from .config import (
    EXPERIMENT_NAME,
    EXPERIMENT_TITLE,
    VERSION,
    REPORT_WIDTH,
    REPORT_DECIMAL_PRECISION,
    REPORT_TIMESTAMP_FORMAT,
    REPORT_SEPARATOR,
    REPORT_INCLUDE_PARAMETERS,
    REPORT_INCLUDE_RESIDUALS,
    REPORT_INCLUDE_RANKING,
    REPORT_INCLUDE_CERTIFICATE,
)

from .selection import (
    selection_summary,
)

from .statistics import (
    analyze_fit,
)

from .fitting import (
    FitResult,
)


# ============================================================
# Formatting
# ============================================================

def line(
    char=REPORT_SEPARATOR,
):
    """
    Horizontal separator.
    """

    return char * REPORT_WIDTH


def center(
    text: str,
):
    """
    Center text.
    """

    return text.center(
        REPORT_WIDTH
    )


def format_float(
    value,
):
    """
    Float formatter.
    """

    if value is None:

        return "N/A"

    try:

        return (

            f"{value:.{REPORT_DECIMAL_PRECISION}f}"

        )

    except Exception:

        return str(value)


def section(
    title: str,
):
    """
    Section title.
    """

    return (

        "\n"

        + line()

        + "\n"

        + title

        + "\n"

        + line()

        + "\n"

    )


# ============================================================
# Header
# ============================================================

def report_header():
    """
    Report header.
    """

    now = datetime.now()

    return (

        line()

        + "\n"

        + center(EXPERIMENT_NAME)

        + "\n"

        + center(EXPERIMENT_TITLE)

        + "\n"

        + line()

        + "\n"

        + f"Version   : {VERSION}\n"

        + f"Generated : {now.strftime(REPORT_TIMESTAMP_FORMAT)}\n"

    )


# ============================================================
# Experiment Information
# ============================================================

def experiment_section(
    summary,
):
    """
    General experiment information.
    """

    text = section(

        "Experiment"

    )

    text += (

        f"Selection Policy : "

        f"{summary['policy']}\n"

    )

    text += (

        f"Primary Metric   : "

        f"{summary['primary_metric']}\n"

    )

    text += (

        f"Secondary Metric : "

        f"{summary['secondary_metric']}\n"

    )

    text += (

        f"Tertiary Metric  : "

        f"{summary['tertiary_metric']}\n"

    )

    text += (

        f"Models Tested    : "

        f"{summary['n_models']}\n"

    )

    text += (

        f"Valid Models     : "

        f"{summary['n_valid_models']}\n"

    )

    text += (

        f"Accepted Models  : "

        f"{summary['n_acceptable_models']}\n"

    )

    return text


# ============================================================
# Best Model
# ============================================================

def best_model_section(
    result: FitResult,
):
    """
    Selected model.
    """

    text = section(

        "Selected Model"

    )

    if result is None:

        text += (

            "No acceptable model found.\n"

        )

        return text

    text += (

        f"Model : "

        f"{result.model}\n"

    )

    text += (

        f"R²    : "

        f"{format_float(result.r2)}\n"

    )

    text += (

        f"RMSE  : "

        f"{format_float(result.rmse)}\n"

    )

    text += (

        f"MAE   : "

        f"{format_float(result.mae)}\n"

    )

    text += (

        f"RSS   : "

        f"{format_float(result.rss)}\n"

    )

    text += (

        f"AIC   : "

        f"{format_float(result.aic)}\n"

    )

    text += (

        f"BIC   : "

        f"{format_float(result.bic)}\n"

    )

    return text


# ============================================================
# Parameters
# ============================================================

def parameter_section(
    result: FitResult,
):
    """
    Estimated parameters.
    """

    text = section(

        "Estimated Parameters"

    )

    if result is None:

        text += (

            "No parameters available.\n"

        )

        return text

    for i, value in enumerate(

        result.parameters

    ):

        text += (

            f"p{i + 1:<2} : "

            f"{format_float(value)}\n"

        )

    return text

# ============================================================
# Residual Statistics
# ============================================================

def residual_section(
    result: FitResult,
):
    """
    Residual statistical analysis.
    """

    text = section(

        "Residual Analysis"

    )

    if result is None:

        text += (

            "No residual statistics available.\n"

        )

        return text

    analysis = analyze_fit(

        result

    )

    residuals = analysis["residuals"]

    for key, value in residuals.items():

        text += (

            f"{key:<20}"

            f": "

            f"{format_float(value)}\n"

        )

    autocorr = analysis.get(

        "autocorrelation"

    )

    if autocorr is not None:

        text += (

            f"\nAutocorrelation : "

            f"{format_float(autocorr)}\n"

        )

    normality = analysis.get(

        "normality"

    )

    if normality is not None:

        text += (

            f"Normality p-value : "

            f"{format_float(normality['pvalue'])}\n"

        )

        text += (

            f"Gaussian Residuals: "

            f"{normality['normal']}\n"

        )

    return text


# ============================================================
# Certificate
# ============================================================

def certificate_section(
    summary,
):
    """
    Scientific certificate.
    """

    text = section(

        "Scientific Certificate"

    )

    certificate = summary.get(

        "certificate",

        None,

    )

    if certificate is None:

        text += (

            "No certificate available.\n"

        )

        return text

    for key, value in certificate.items():

        if isinstance(

            value,

            float,

        ):

            value = format_float(

                value

            )

        text += (

            f"{key:<20}: "

            f"{value}\n"

        )

    return text


# ============================================================
# Ranking
# ============================================================

def ranking_section(
    results,
):
    """
    Model ranking.
    """

    text = section(

        "Model Ranking"

    )

    ordered = sorted(

        results,

        key=lambda r: (

            float("inf")

            if r.aic is None

            else r.aic

        )

    )

    for i, result in enumerate(

        ordered,

        start=1,

    ):

        text += (

            f"{i:>2}. "

            f"{result.model:<24}"

            f"R²={format_float(result.r2)}   "

            f"AIC={format_float(result.aic)}   "

            f"BIC={format_float(result.bic)}\n"

        )

    return text


# ============================================================
# Complete Report
# ============================================================

def build_report(
    results,
):
    """
    Build complete report.
    """

    summary = selection_summary(

        results

    )

    best = summary.get(

        "best_model"

    )

    report = ""

    report += report_header()

    report += experiment_section(

        summary

    )

    report += best_model_section(

        best

    )

    if REPORT_INCLUDE_PARAMETERS:

        report += parameter_section(

            best

        )

    if REPORT_INCLUDE_RESIDUALS:

        report += residual_section(

            best

        )

    if REPORT_INCLUDE_CERTIFICATE:

        report += certificate_section(

            summary

        )

    if REPORT_INCLUDE_RANKING:

        report += ranking_section(

            results

        )

    return report


# ============================================================
# Save
# ============================================================
def save_report(
    report: str,
    filename,
):
    """
    Save report to disk.
    """

    with open(

        filename,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            report

        )


# ============================================================
# Public API
# ============================================================

__all__ = [

    "line",

    "center",

    "format_float",

    "section",

    "report_header",

    "experiment_section",

    "best_model_section",

    "parameter_section",

    "residual_section",

    "certificate_section",

    "ranking_section",

    "build_report",

    "save_report",

]
