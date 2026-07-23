"""
============================================================
GER
Hypothesis Tests Utilities
============================================================

Reusable statistical hypothesis tests.

Functions
---------
kolmogorov_smirnov(...)
shapiro_wilk(...)
anderson_darling(...)
normality_report(...)
============================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats


# ============================================================
# KOLMOGOROV-SMIRNOV
# ============================================================

def kolmogorov_smirnov(
    values,
    distribution,
    params,
):

    values = np.asarray(values, dtype=float)

    statistic, pvalue = stats.kstest(
        values,
        distribution.name,
        args=params,
    )

    return {

        "test": "Kolmogorov-Smirnov",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= 0.05),

    }


# ============================================================
# SHAPIRO-WILK
# ============================================================

def shapiro_wilk(values):

    values = np.asarray(values, dtype=float)

    statistic, pvalue = stats.shapiro(values)

    return {

        "test": "Shapiro-Wilk",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= 0.05),

    }


# ============================================================
# ANDERSON-DARLING
# ============================================================

def anderson_darling(
    values,
    distribution="norm",
):

    values = np.asarray(values, dtype=float)

    result = stats.anderson(
        values,
        dist=distribution,
    )

    return {

        "test": "Anderson-Darling",

        "statistic": float(result.statistic),

        "critical_values": result.critical_values.tolist(),

        "significance_levels": result.significance_level.tolist(),

    }


# ============================================================
# NORMALITY REPORT
# ============================================================

def normality_report(values):

    shapiro = shapiro_wilk(values)

    anderson = anderson_darling(values)

    return {

        "shapiro": shapiro,

        "anderson": anderson,

    }
