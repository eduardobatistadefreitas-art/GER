"""
=============================================================
S29_E9/selection.py
=============================================================

Trajectory Relaxation Analysis

Model Selection Engine

This module is responsible for selecting the best model
according to the configured policy.

=============================================================
"""

from __future__ import annotations

from typing import List

from .config import (
    MODEL_SELECTION_POLICY,
    PRIMARY_SELECTION_METRIC,
    SECONDARY_SELECTION_METRIC,
    TERTIARY_SELECTION_METRIC,
    MIN_R2_ACCEPTABLE,
)

from .fitting import FitResult


# ============================================================
# Validation
# ============================================================

def valid_results(
    results: List[FitResult],
) -> List[FitResult]:
    """
    Keep only successful fits.
    """

    return [

        result

        for result in results

        if result.success

    ]


def acceptable_results(
    results: List[FitResult],
) -> List[FitResult]:
    """
    Remove poor fits.
    """

    return [

        result

        for result in valid_results(results)

        if result.r2 >= MIN_R2_ACCEPTABLE

    ]


# ============================================================
# Ranking
# ============================================================

def rank_by_metric(
    results: List[FitResult],
    metric: str,
):
    """
    Rank according to one metric.
    """

    reverse = (

        metric.lower() == "r2"

    )

    return sorted(

        results,

        key=lambda r: getattr(

            r,

            metric,

        ),

        reverse=reverse,

    )


# ============================================================
# Policies
# ============================================================

def select_by_aic(
    results,
):

    ranking = rank_by_metric(

        acceptable_results(results),

        "aic",

    )

    if len(ranking) == 0:

        return None

    return ranking[0]


def select_by_bic(
    results,
):

    ranking = rank_by_metric(

        acceptable_results(results),

        "bic",

    )

    if len(ranking) == 0:

        return None

    return ranking[0]


def select_by_r2(
    results,
):

    ranking = rank_by_metric(

        acceptable_results(results),

        "r2",

    )

    if len(ranking) == 0:

        return None

    return ranking[0]


# ============================================================
# Balanced Policy
# ============================================================

def balanced_selection(
    results,
):
    """
    AIC
        ↓
    BIC
        ↓
    R²
    """

    ranking = acceptable_results(

        results

    )

    if len(ranking) == 0:

        return None

    ranking = sorted(

        ranking,

        key=lambda r: (

            r.aic,

            r.bic,

            -r.r2,

        ),

    )

    return ranking[0]


# ============================================================
# Generic Policy
# ============================================================

def apply_policy(
    results,
):
    """
    Apply configured policy.
    """

    policy = MODEL_SELECTION_POLICY.lower()

    if policy == "aic":

        return select_by_aic(

            results

        )

    if policy == "bic":

        return select_by_bic(

            results

        )

    if policy == "r2":

        return select_by_r2(

            results

        )

    if policy == "balanced":

        return balanced_selection(

            results

        )

    raise ValueError(

        f"Unknown selection policy: {policy}"

    )

# ============================================================
# Selection Interface
# ============================================================

def select_best_model(
    results,
):
    """
    Public interface for model selection.

    Parameters
    ----------
    results : list[FitResult]

    Returns
    -------
    FitResult | None
    """

    return apply_policy(

        results

    )


# ============================================================
# Certificate
# ============================================================

def generate_certificate(
    result,
):
    """
    Generate a scientific certificate describing
    the selected model.
    """

    if result is None:

        return {

            "status": "FAILED",

            "reason": "No acceptable model found.",

        }

    if result.r2 >= 0.995:

        confidence = "HIGH"

    elif result.r2 >= 0.980:

        confidence = "MEDIUM"

    elif result.r2 >= 0.950:

        confidence = "LOW"

    else:

        confidence = "POOR"

    return {

        "status":
            "SUCCESS",

        "selection_policy":
            MODEL_SELECTION_POLICY,

        "selected_model":
            result.model,

        "confidence":
            confidence,

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

        "parameters":
            list(result.parameters),

        "n_parameters":
            result.n_parameters,

        "n_samples":
            result.n_samples,

    }


# ============================================================
# Selection Summary
# ============================================================

def selection_summary(
    results,
):
    """
    Build a compact summary of the model selection.
    """

    best = select_best_model(

        results

    )

    certificate = generate_certificate(

        best

    )

    return {

        "policy":
            MODEL_SELECTION_POLICY,

        "primary_metric":
            PRIMARY_SELECTION_METRIC,

        "secondary_metric":
            SECONDARY_SELECTION_METRIC,

        "tertiary_metric":
            TERTIARY_SELECTION_METRIC,

        "n_models":
            len(results),

        "n_valid_models":
            len(valid_results(results)),

        "n_acceptable_models":
            len(acceptable_results(results)),

        "best_model":

            None if best is None

            else best.model,

        "certificate":

            certificate,

    }


# ============================================================
# Public API
# ============================================================

__all__ = [

    "valid_results",

    "acceptable_results",

    "rank_by_metric",

    "select_by_aic",

    "select_by_bic",

    "select_by_r2",

    "balanced_selection",

    "apply_policy",

    "select_best_model",

    "generate_certificate",

    "selection_summary",

]
