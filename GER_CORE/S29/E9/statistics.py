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

