"""
============================================================
GER
Descriptive Statistics Utilities
============================================================

Reusable descriptive statistics for the GER observatories.

This module centralizes descriptive statistical
computations used throughout the GER framework.

Existing public functions remain fully compatible
with previous versions.

Functions
---------
compute_basic_statistics(values)
compute_entropy(values)
compute_gini(values)

Additional utilities
--------------------
clean_numeric(values)
compute_percentiles(values)
compute_moments(values)
compute_dispersion(values)
============================================================
"""

from __future__ import annotations

from typing import Iterable

import numpy as np

from scipy import stats


# ============================================================
# Version
# ============================================================

DESCRIPTIVE_VERSION = "2.0"


# ============================================================
# Constants
# ============================================================

EPSILON = 1e-12

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


# ============================================================
# Public API
# ============================================================

__all__ = [

    "compute_basic_statistics",

    "compute_entropy",

    "compute_gini",

    "clean_numeric",

    "compute_percentiles",

    "compute_moments",

    "compute_dispersion",

]


# ============================================================
# Internal utilities
# ============================================================

def clean_numeric(values):

    """
    Convert any iterable into a clean numeric numpy array.

    NaN and infinite values are removed.
    """

    values = np.asarray(
        values,
        dtype=float,
    )

    mask = np.isfinite(values)

    return values[mask]


# ============================================================
# ENTROPY
# ============================================================

def compute_entropy(values, base="e"):

    values = clean_numeric(values)

    if len(values) == 0:

        return 0.0

    total = values.sum()

    if abs(total) < EPSILON:

        return 0.0

    p = values / total

    p = p[p > 0]

    if len(p) == 0:

        return 0.0

    if base in ("e", "natural", None):

        return float(

            -np.sum(

                p * np.log(p)

            )

        )

    if base in (2, "2", "bits"):

        return float(

            -np.sum(

                p * np.log2(p)

            )

        )

    if base in (10, "10"):

        return float(

            -np.sum(

                p * np.log10(p)

            )

        )

    raise ValueError(

        f"Unsupported entropy base: {base}"

    )


# ============================================================
# GINI
# ============================================================

def compute_gini(values):

    values = clean_numeric(values)

    if len(values) == 0:

        return 0.0

    if np.min(values) < 0:

        values = values - np.min(values)

    values = np.sort(values)

    total = values.sum()

    if abs(total) < EPSILON:

        return 0.0

    n = len(values)

    index = np.arange(

        1,

        n + 1,

    )

    gini = (

        np.sum(

            (2 * index - n - 1)

            * values

        )

        /

        (n * total)

    )

    return float(gini)


# ============================================================
# Percentiles
# ============================================================

def compute_percentiles(

    values,

    percentiles=DEFAULT_PERCENTILES,

):

    values = clean_numeric(values)

    if len(values) == 0:

        return {}

    return {

        f"p{p}":

        float(

            np.percentile(

                values,

                p,

            )

        )

        for p in percentiles

    }


# ============================================================
# Moments
# ============================================================

def compute_moments(values):

    values = clean_numeric(values)

    if len(values) == 0:

        return {}

    return {

        "mean":

            float(

                np.mean(values)

            ),

        "variance":

            float(

                np.var(values)

            ),

        "std":

            float(

                np.std(values)

            ),

        "skewness":

            float(

                stats.skew(values)

            ),

        "kurtosis":

            float(

                stats.kurtosis(values)

            ),

    }


# ============================================================
# Dispersion
# ============================================================

def compute_dispersion(values):

    values = clean_numeric(values)

    if len(values) == 0:

        return {}

    mean = np.mean(values)

    q1 = np.percentile(values, 25)

    q3 = np.percentile(values, 75)

    return {

        "minimum":

            float(np.min(values)),

        "maximum":

            float(np.max(values)),

        "range":

            float(

                np.max(values)

                -

                np.min(values)

            ),

        "q1":

            float(q1),

        "median":

            float(

                np.median(values)

            ),

        "q3":

            float(q3),

        "iqr":

            float(q3 - q1),

        "cv":

            float(

                np.std(values)

                /

                mean

            )

            if abs(mean) > EPSILON

            else 0.0,

    }

# ============================================================
# BASIC STATISTICS
# ============================================================

def compute_basic_statistics(values):

    """
    Compute the complete descriptive statistics summary.

    This function preserves full backward compatibility
    with previous GER versions while internally relying
    on reusable utilities implemented in this module.
    """

    values = clean_numeric(values)

    if len(values) == 0:

        return {
            "count": 0,
        }

    statistics = {

        "count": int(len(values)),

    }

    # --------------------------------------------------------
    # Central moments
    # --------------------------------------------------------

    statistics.update(

        compute_moments(values)

    )

    # --------------------------------------------------------
    # Dispersion
    # --------------------------------------------------------

    statistics.update(

        compute_dispersion(values)

    )

    # --------------------------------------------------------
    # Information measures
    # --------------------------------------------------------

    statistics["entropy"] = compute_entropy(

        values

    )

    statistics["gini"] = compute_gini(

        values

    )

    return statistics


# ============================================================
# COMPLETE SUMMARY
# ============================================================

def descriptive_summary(values):

    """
    Extended descriptive summary.

    This helper is intended for newer observatories.
    Existing code can continue using
    compute_basic_statistics().
    """

    values = clean_numeric(values)

    if len(values) == 0:

        return {
            "count": 0,
        }

    summary = compute_basic_statistics(values)

    summary.update(

        compute_percentiles(values)

    )

    return summary


# ============================================================
# Self Test
# ============================================================

def _print_summary(summary):

    print("=" * 60)

    print("GER")

    print("Descriptive Statistics")

    print("=" * 60)

    print()

    for key, value in summary.items():

        print(

            f"{key:20s}: {value}"

        )

    print()


def main():

    np.random.seed(42)

    values = np.random.normal(

        loc=0.0,

        scale=1.0,

        size=1000,

    )

    summary = descriptive_summary(

        values

    )

    _print_summary(summary)


if __name__ == "__main__":

    main()
