"""
============================================================
GER
Descriptive Statistics Utilities
============================================================

Reusable descriptive statistics for the GER observatories.

Functions
---------
compute_basic_statistics(values)
compute_entropy(values)
compute_gini(values)
============================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats


# ============================================================
# ENTROPY
# ============================================================

def compute_entropy(values, base="e"):

    values = np.asarray(values, dtype=float)

    total = values.sum()

    if total == 0:
        return 0.0

    p = values / total

    p = p[p > 0]

    if base in ("e", "natural", None):

        return float(-np.sum(p * np.log(p)))

    if base in (2, "2", "bits"):

        return float(-np.sum(p * np.log2(p)))

    if base in (10, "10"):

        return float(-np.sum(p * np.log10(p)))

    raise ValueError(f"Unsupported entropy base: {base}")


# ============================================================
# GINI
# ============================================================

def compute_gini(values):

    values = np.asarray(values, dtype=float)

    if len(values) == 0:
        return 0.0

    if np.min(values) < 0:
        values = values - np.min(values)

    values = np.sort(values)

    n = len(values)

    total = values.sum()

    if total == 0:
        return 0.0

    index = np.arange(1, n + 1)

    gini = (
        np.sum((2 * index - n - 1) * values)
        / (n * total)
    )

    return float(gini)


# ============================================================
# BASIC STATISTICS
# ============================================================

def compute_basic_statistics(values):

    values = np.asarray(values, dtype=float)

    if len(values) == 0:

        return {
            "count": 0,
        }

    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)

    statistics = {

        "count": int(len(values)),

        "mean": float(np.mean(values)),

        "median": float(np.median(values)),

        "variance": float(np.var(values)),

        "std": float(np.std(values)),

        "minimum": float(np.min(values)),

        "maximum": float(np.max(values)),

        "range": float(np.max(values) - np.min(values)),

        "q1": float(q1),

        "q3": float(q3),

        "iqr": float(q3 - q1),

        "cv": float(
            np.std(values) / np.mean(values)
        )
        if np.mean(values) != 0
        else 0.0,

        "skewness": float(
            stats.skew(values)
        ),

        "kurtosis": float(
            stats.kurtosis(values)
        ),

        "entropy": compute_entropy(values),

        "gini": compute_gini(values),

    }

    return statistics
