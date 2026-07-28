"""
=============================================================
S29_E9/statistics.py
=============================================================

Trajectory Relaxation Analysis

Statistical analysis of fitted models.

This module performs statistical analyses on the residuals
produced by fitting.py.

=============================================================
"""

from __future__ import annotations

import numpy as np

from scipy.stats import (
    skew,
    kurtosis,
)

from .fitting import FitResult


# ============================================================
# Residual Statistics
# ============================================================

def residual_mean(
    residuals,
):
    """
    Mean residual.
    """

    return float(

        np.mean(

            residuals

        )

    )


def residual_variance(
    residuals,
):
    """
    Residual variance.
    """

    return float(

        np.var(

            residuals,

            ddof=1,

        )

    )


def residual_std(
    residuals,
):
    """
    Residual standard deviation.
    """

    return float(

        np.std(

            residuals,

            ddof=1,

        )

    )


def residual_min(
    residuals,
):
    """
    Minimum residual.
    """

    return float(

        np.min(

            residuals

        )

    )


def residual_max(
    residuals,
):
    """
    Maximum residual.
    """

    return float(

        np.max(

            residuals

        )

    )


def residual_range(
    residuals,
):
    """
    Residual amplitude.
    """

    return (

        residual_max(

            residuals

        )

        -

        residual_min(

            residuals

        )

    )


# ============================================================
# Distribution Shape
# ============================================================

def residual_skewness(
    residuals,
):
    """
    Residual skewness.
    """

    return float(

        skew(

            residuals,

            bias=False,

        )

    )


def residual_kurtosis(
    residuals,
):
    """
    Residual kurtosis (excess).
    """

    return float(

        kurtosis(

            residuals,

            fisher=True,

            bias=False,

        )

    )


# ============================================================
# Absolute Errors
# ============================================================

def mean_absolute_residual(
    residuals,
):
    """
    Mean absolute residual.
    """

    return float(

        np.mean(

            np.abs(

                residuals

            )

        )

    )


def median_absolute_residual(
    residuals,
):
    """
    Median absolute residual.
    """

    return float(

        np.median(

            np.abs(

                residuals

            )

        )

    )


def max_absolute_residual(
    residuals,
):
    """
    Maximum absolute residual.
    """

    return float(

        np.max(

            np.abs(

                residuals

            )

        )

    )


# ============================================================
# Summary
# ============================================================

def residual_summary(
    residuals,
):
    """
    Complete descriptive statistics for residuals.
    """

    return {

        "mean":

            residual_mean(

                residuals

            ),

        "variance":

            residual_variance(

                residuals

            ),

        "std":

            residual_std(

                residuals

            ),

        "minimum":

            residual_min(

                residuals

            ),

        "maximum":

            residual_max(

                residuals

            ),

        "range":

            residual_range(

                residuals

            ),

        "mean_absolute":

            mean_absolute_residual(

                residuals

            ),

        "median_absolute":

            median_absolute_residual(

                residuals

            ),

        "maximum_absolute":

            max_absolute_residual(

                residuals

            ),

        "skewness":

            residual_skewness(

                residuals

            ),

        "kurtosis":

            residual_kurtosis(

                residuals

            ),

    }

# ============================================================
# Residual Diagnostics
# ============================================================

def residual_autocorrelation(
    residuals,
):
    """
    Lag-1 residual autocorrelation.
    """

    residuals = np.asarray(

        residuals,

        dtype=float,

    )

    if len(residuals) < 2:

        return None

    x = residuals[:-1]

    y = residuals[1:]

    if np.std(x) == 0 or np.std(y) == 0:

        return None

    return float(

        np.corrcoef(

            x,

            y,

        )[0, 1]

    )


def residual_normality(
    residuals,
):
    """
    Jarque-Bera normality test.
    """

    try:

        from scipy.stats import jarque_bera

        statistic, pvalue = jarque_bera(

            residuals

        )

        return {

            "statistic": float(statistic),

            "pvalue": float(pvalue),

            "normal": bool(pvalue >= 0.05),

        }

    except Exception:

        return None


# ============================================================
# Fit Analysis
# ============================================================

def analyze_fit(
    result: FitResult,
):
    """
    Complete statistical analysis of one fitted model.
    """

    if result is None:

        return None

    residuals = result.residuals

    analysis = {

        "model":

            result.model,

        "success":

            result.success,

        "r2":

            result.r2,

        "rmse":

            result.rmse,

        "mae":

            result.mae,

        "rss":

            result.rss,

        "aic":

            result.aic,

        "bic":

            result.bic,

        "residuals":

            residual_summary(

                residuals

            ),

        "autocorrelation":

            residual_autocorrelation(

                residuals

            ),

        "normality":

            residual_normality(

                residuals

            ),

    }

    return analysis


# ============================================================
# Batch Analysis
# ============================================================

def analyze_all_models(
    results,
):
    """
    Analyze every fitted model.
    """

    analyses = []

    for result in results:

        analyses.append(

            analyze_fit(

                result

            )

        )

    return analyses


# ============================================================
# Statistical Summary
# ============================================================

def statistical_summary(
    analyses,
):
    """
    Overall statistical summary.
    """

    valid = [

        a

        for a in analyses

        if a is not None

    ]

    return {

        "n_models":

            len(analyses),

        "n_valid":

            len(valid),

        "successful":

            sum(

                a["success"]

                for a in valid

            ),

    }


# ============================================================
# Public API
# ============================================================

__all__ = [

    "residual_mean",

    "residual_variance",

    "residual_std",

    "residual_min",

    "residual_max",

    "residual_range",

    "residual_skewness",

    "residual_kurtosis",

    "mean_absolute_residual",

    "median_absolute_residual",

    "max_absolute_residual",

    "residual_summary",

    "residual_autocorrelation",

    "residual_normality",

    "analyze_fit",

    "analyze_all_models",

    "statistical_summary",

]
