"""
============================================================
GER
Information Criteria Utilities
============================================================

Reusable information criteria for statistical model selection.

Functions
---------
log_likelihood(...)
aic(...)
bic(...)
aicc(...)
============================================================
"""

from __future__ import annotations

import numpy as np


# ============================================================
# LOG-LIKELIHOOD
# ============================================================

def log_likelihood(logpdf_values):

    """
    Computes the total log-likelihood from log-PDF values.
    """

    return float(np.sum(logpdf_values))


# ============================================================
# AIC
# ============================================================

def aic(k, loglikelihood):

    """
    Akaike Information Criterion.
    """

    return float(2 * k - 2 * loglikelihood)


# ============================================================
# BIC
# ============================================================

def bic(n, k, loglikelihood):

    """
    Bayesian Information Criterion.
    """

    return float(np.log(n) * k - 2 * loglikelihood)


# ============================================================
# AICc
# ============================================================

def aicc(n, k, loglikelihood):

    """
    Small-sample corrected Akaike Information Criterion.
    """

    base = aic(k, loglikelihood)

    if n <= k + 1:
        return float("inf")

    correction = (2 * k * (k + 1)) / (n - k - 1)

    return float(base + correction)


# ============================================================
# MODEL SUMMARY
# ============================================================

def information_summary(
    n,
    k,
    loglikelihood,
):

    """
    Returns all supported information criteria.
    """

    return {

        "loglikelihood": float(loglikelihood),

        "AIC": aic(k, loglikelihood),

        "AICc": aicc(n, k, loglikelihood),

        "BIC": bic(n, k, loglikelihood),

    }
