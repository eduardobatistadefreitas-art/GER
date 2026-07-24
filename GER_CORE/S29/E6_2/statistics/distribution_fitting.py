"""
============================================================
GER
Distribution Fitting Utilities
============================================================

Reusable probability distribution fitting utilities.

This module centralizes statistical distribution
analysis for the GER framework.

Existing public functions remain fully compatible
with previous versions.

Functions
---------
fit_distribution(...)
fit_all_distributions(...)
best_distribution(...)
accepted_distributions(...)
rejected_distributions(...)

Additional utilities
--------------------
clean_numeric(...)
compute_kde(...)
evaluate_kde(...)
density_grid(...)
density_peak(...)
effective_support(...)
============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy import stats
from scipy.stats import gaussian_kde


# ============================================================
# Version
# ============================================================

DISTRIBUTION_VERSION = "2.0"


# ============================================================
# Constants
# ============================================================

EPSILON = 1e-12

DEFAULT_GRID_SIZE = 512

DEFAULT_BANDWIDTH = None


# ============================================================
# Default Distributions
# ============================================================

DEFAULT_DISTRIBUTIONS = [

    stats.norm,

    stats.expon,

    stats.gamma,

    stats.lognorm,

    stats.weibull_min,

]


# ============================================================
# Public API
# ============================================================

__all__ = [

    "fit_distribution",

    "fit_all_distributions",

    "best_distribution",

    "accepted_distributions",

    "rejected_distributions",

    "clean_numeric",

    "compute_kde",

    "evaluate_kde",

    "density_grid",

    "density_peak",

    "effective_support",

]


# ============================================================
# Internal utilities
# ============================================================

def clean_numeric(values):

    """
    Convert an iterable into a clean numeric array.

    NaN and infinite values are removed.
    """

    values = np.asarray(

        values,

        dtype=float,

    )

    return values[

        np.isfinite(values)

    ]


# ============================================================
# KDE
# ============================================================

def compute_kde(

    values,

    bandwidth=DEFAULT_BANDWIDTH,

):

    """
    Build a Gaussian Kernel Density Estimator.
    """

    values = clean_numeric(values)

    if len(values) < 2:

        raise ValueError(

            "At least two observations are required."

        )

    kde = gaussian_kde(

        values,

        bw_method=bandwidth,

    )

    return kde


# ============================================================
# Evaluate KDE
# ============================================================

def evaluate_kde(

    kde,

    points,

):

    """
    Evaluate a KDE over arbitrary points.
    """

    points = np.asarray(

        points,

        dtype=float,

    )

    return kde(points)


# ============================================================
# Density Grid
# ============================================================

def density_grid(

    values,

    bandwidth=DEFAULT_BANDWIDTH,

    grid_size=DEFAULT_GRID_SIZE,

):

    """
    Compute a regular density grid.
    """

    values = clean_numeric(values)

    kde = compute_kde(

        values,

        bandwidth,

    )

    xmin = values.min()

    xmax = values.max()

    grid = np.linspace(

        xmin,

        xmax,

        grid_size,

    )

    density = kde(grid)

    return pd.DataFrame(

        {

            "Value": grid,

            "Density": density,

        }

    )


# ============================================================
# Density Peak
# ============================================================

def density_peak(

    values,

    bandwidth=DEFAULT_BANDWIDTH,

):

    """
    Locate the maximum KDE density.
    """

    table = density_grid(

        values,

        bandwidth,

    )

    peak = table.loc[

        table["Density"].idxmax()

    ]

    return {

        "value": float(

            peak["Value"]

        ),

        "density": float(

            peak["Density"]

        ),

    }


# ============================================================
# Effective Support
# ============================================================

def effective_support(values):

    """
    Compute the effective support interval.
    """

    values = clean_numeric(values)

    if len(values) == 0:

        return {

            "minimum": None,

            "maximum": None,

            "range": None,

        }

    minimum = float(

        values.min()

    )

    maximum = float(

        values.max()

    )

    return {

        "minimum": minimum,

        "maximum": maximum,

        "range": maximum - minimum,

    }


# ============================================================
# FIT SINGLE DISTRIBUTION
# ============================================================

def fit_distribution(

    values,

    distribution,

):

    """
    Fit a single probability distribution.
    """

    values = clean_numeric(values)

    if len(values) < 2:

        raise ValueError(

            "At least two observations are required."

        )

    params = distribution.fit(

        values,

    )

    loglikelihood = np.sum(

        distribution.logpdf(

            values,

            *params,

        )

    )

    k = len(params)

    n = len(values)

    aic = 2 * k - 2 * loglikelihood

    bic = np.log(n) * k - 2 * loglikelihood

    ks, pvalue = stats.kstest(

        values,

        distribution.name,

        args=params,

    )

    return {

        "Distribution":

            distribution.name,

        "AIC":

            float(aic),

        "BIC":

            float(bic),

        "KS":

            float(ks),

        "KS p-value":

            float(pvalue),

        "Accepted":

            bool(

                pvalue >= 0.05

            ),

        "LogLikelihood":

            float(loglikelihood),

        "Parameters":

            params,

    }

# ============================================================
# FIT MULTIPLE DISTRIBUTIONS
# ============================================================

def fit_all_distributions(

    values,

    distributions=None,

):

    """
    Fit multiple probability distributions and
    rank them according to AIC.
    """

    values = clean_numeric(values)

    if distributions is None:

        distributions = DEFAULT_DISTRIBUTIONS

    results = []

    for distribution in distributions:

        try:

            results.append(

                fit_distribution(

                    values,

                    distribution,

                )

            )

        except Exception:

            continue

    if len(results) == 0:

        return pd.DataFrame()

    return (

        pd.DataFrame(results)

        .sort_values(

            "AIC",

            ascending=True,

        )

        .reset_index(drop=True)

    )


# ============================================================
# BEST MODEL
# ============================================================

def best_distribution(results):

    """
    Return the best fitted model.
    """

    if len(results) == 0:

        return None

    return results.iloc[0].to_dict()


# ============================================================
# ACCEPTED MODELS
# ============================================================

def accepted_distributions(results):

    """
    Return accepted models according to the
    Kolmogorov-Smirnov test.
    """

    if len(results) == 0:

        return results

    return (

        results

        .loc[

            results["Accepted"]

        ]

        .reset_index(drop=True)

    )


# ============================================================
# REJECTED MODELS
# ============================================================

def rejected_distributions(results):

    """
    Return rejected models.
    """

    if len(results) == 0:

        return results

    return (

        results

        .loc[

            ~results["Accepted"]

        ]

        .reset_index(drop=True)

    )


# ============================================================
# MODEL COMPARISON
# ============================================================

def compare_models(results):

    """
    Compare fitted models.
    """

    if len(results) == 0:

        return pd.DataFrame()

    columns = [

        "Distribution",

        "AIC",

        "BIC",

        "KS",

        "KS p-value",

        "Accepted",

    ]

    return (

        results

        .loc[:, columns]

        .copy()

    )


# ============================================================
# DISTRIBUTION SUMMARY
# ============================================================

def distribution_summary(results):

    """
    Produce a compact summary of the fitted models.
    """

    if len(results) == 0:

        return {

            "tested_models": 0,

            "accepted_models": 0,

            "rejected_models": 0,

            "best_model": None,

        }

    best = best_distribution(results)

    accepted = accepted_distributions(results)

    rejected = rejected_distributions(results)

    return {

        "tested_models":

            int(len(results)),

        "accepted_models":

            int(len(accepted)),

        "rejected_models":

            int(len(rejected)),

        "best_model":

            best["Distribution"],

        "best_aic":

            float(best["AIC"]),

        "best_bic":

            float(best["BIC"]),

        "best_ks":

            float(best["KS"]),

        "best_pvalue":

            float(best["KS p-value"]),

    }


# ============================================================
# SAMPLE FROM DISTRIBUTION
# ============================================================

def sample_distribution(

    distribution,

    parameters,

    size=1000,

    random_state=None,

):

    """
    Draw random samples from a fitted distribution.
    """

    rng = np.random.default_rng(

        random_state

    )

    np.random.seed(

        rng.integers(

            0,

            2**32 - 1,

        )

    )

    return distribution.rvs(

        *parameters,

        size=size,

    )


# ============================================================
# GOODNESS OF FIT TABLE
# ============================================================

def goodness_of_fit_table(results):

    """
    Alias maintained for readability in the
    observatories.
    """

    return compare_models(results)


# ============================================================
# Self Test
# ============================================================

def _print_summary(results):

    print("=" * 60)

    print("GER")

    print("Distribution Fitting")

    print("=" * 60)

    print()

    summary = distribution_summary(

        results

    )

    for key, value in summary.items():

        print(

            f"{key:20s}: {value}"

        )

    print()

    if len(results):

        print(results)


def main():

    np.random.seed(42)

    values = np.random.normal(

        loc=0,

        scale=1,

        size=5000,

    )

    results = fit_all_distributions(

        values

    )

    _print_summary(

        results

    )

    print()

    print("Density Peak")

    print(

        density_peak(values)

    )

    print()

    print("Support")

    print(

        effective_support(values)

    )


if __name__ == "__main__":

    main()
