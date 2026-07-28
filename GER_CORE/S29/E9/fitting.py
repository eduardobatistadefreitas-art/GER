"""
=============================================================
S29_E9/fitting.py
=============================================================

Trajectory Relaxation Analysis

Numerical fitting engine.

This module is responsible ONLY for fitting candidate
models and computing statistical metrics.

Model selection is performed in selection.py.

=============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from scipy.optimize import curve_fit

from .models import (
    get_model,
    get_initial_parameters,
)


# ============================================================
# Fit Result
# ============================================================

@dataclass
class FitResult:
    """
    Standard result returned by every fitted model.
    """

    model: str

    success: bool

    parameters: tuple

    covariance: np.ndarray | None

    y_fit: np.ndarray

    residuals: np.ndarray

    r2: float

    rmse: float

    mae: float

    aic: float

    bic: float

    rss: float

    n_parameters: int

    n_samples: int

    message: str = ""


# ============================================================
# Metrics
# ============================================================

def compute_rss(
    y,
    y_fit,
):
    """
    Residual Sum of Squares.
    """

    return np.sum(

        (y - y_fit) ** 2

    )


def compute_r2(
    y,
    y_fit,
):
    """
    Coefficient of determination.
    """

    ss_res = compute_rss(

        y,

        y_fit,

    )

    ss_tot = np.sum(

        (y - np.mean(y)) ** 2

    )

    if ss_tot == 0:

        return 1.0

    return 1.0 - ss_res / ss_tot


def compute_rmse(
    y,
    y_fit,
):
    """
    Root Mean Squared Error.
    """

    return np.sqrt(

        np.mean(

            (y - y_fit) ** 2

        )

    )


def compute_mae(
    y,
    y_fit,
):
    """
    Mean Absolute Error.
    """

    return np.mean(

        np.abs(

            y - y_fit

        )

    )


def compute_aic(
    rss,
    n,
    k,
):
    """
    Akaike Information Criterion.
    """

    rss = max(

        rss,

        1e-300,

    )

    return (

        n * np.log(

            rss / n

        )

        + 2 * k

    )


def compute_bic(
    rss,
    n,
    k,
):
    """
    Bayesian Information Criterion.
    """

    rss = max(

        rss,

        1e-300,

    )

    return (

        n * np.log(

            rss / n

        )

        + k * np.log(n)

    )


# ============================================================
# Curve Fit Wrapper
# ============================================================

def safe_curve_fit(
    model,
    x,
    y,
    p0,
):
    """
    Wrapper around scipy.optimize.curve_fit.
    """

    return curve_fit(

        model,

        x,

        y,

        p0=p0,

        maxfev=100000,

    )


# ============================================================
# Fit Single Model
# ============================================================

def fit_model(
    model_name,
    x,
    y,
):
    """
    Fit one candidate model.
    """

    model = get_model(

        model_name

    )

    p0 = get_initial_parameters(

        model_name

    )

    try:

        params, covariance = safe_curve_fit(

            model,

            x,

            y,

            p0,

        )

        y_fit = model(

            x,

            *params,

        )

        residuals = y - y_fit

        rss = compute_rss(

            y,

            y_fit,

        )

        n = len(y)

        k = len(params)

        return FitResult(

            model=model_name,

            success=True,

            parameters=tuple(params),

            covariance=covariance,

            y_fit=y_fit,

            residuals=residuals,

            r2=compute_r2(

                y,

                y_fit,

            ),

            rmse=compute_rmse(

                y,

                y_fit,

            ),

            mae=compute_mae(

                y,

                y_fit,

            ),

            aic=compute_aic(

                rss,

                n,

                k,

            ),

            bic=compute_bic(

                rss,

                n,

                k,

            ),

            rss=rss,

            n_parameters=k,

            n_samples=n,

            message="OK",

        )

    except Exception as exc:

        n = len(y)

        nan = np.full(

            n,

            np.nan,

        )

        return FitResult(

            model=model_name,

            success=False,

            parameters=tuple(),

            covariance=None,

            y_fit=nan,

            residuals=nan,

            r2=np.nan,

            rmse=np.nan,

            mae=np.nan,

            aic=np.nan,

            bic=np.nan,

            rss=np.nan,

            n_parameters=0,

            n_samples=n,

            message=str(exc),

        )

# ============================================================
# Fit Multiple Models
# ============================================================

def fit_all_models(
    x,
    y,
    model_names,
):
    """
    Fit every candidate model.

    Parameters
    ----------
    x : ndarray
        Independent variable.

    y : ndarray
        Observed data.

    model_names : iterable[str]
        Candidate model names.

    Returns
    -------
    list[FitResult]
    """

    results = []

    for model_name in model_names:

        result = fit_model(

            model_name,

            x,

            y,

        )

        results.append(

            result

        )

    return results


# ============================================================
# Successful Fits
# ============================================================

def successful_results(
    results,
):
    """
    Return only successful fits.
    """

    return [

        result

        for result in results

        if result.success

    ]


# ============================================================
# Summary Table
# ============================================================

def summary_table(
    results,
):
    """
    Convert results into dictionaries suitable
    for CSV/JSON export.
    """

    rows = []

    for result in results:

        rows.append(

            {

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

                "n_parameters":
                    result.n_parameters,

                "n_samples":
                    result.n_samples,

                "parameters":
                    list(result.parameters),

                "message":
                    result.message,

            }

        )

    return rows


# ============================================================
# Public API
# ============================================================

__all__ = [

    "FitResult",

    "fit_model",

    "fit_all_models",

    "successful_results",

    "summary_table",

]
