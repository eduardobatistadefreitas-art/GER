"""
============================================================
GER
Distribution Comparison
============================================================

Reusable statistical routines for pairwise comparison
between marginal distributions.

Implemented metrics
-------------------

- Wasserstein Distance
- Kolmogorov-Smirnov Distance
- Jensen-Shannon Distance
- Overlap Coefficient

Version
-------
2.0

Improvements
------------

- KDE cache (computed once per variable)
- Common support construction
- Shared evaluation grid
- Reusable density evaluation

============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from itertools import combinations

from scipy.stats import (

    wasserstein_distance,

    ks_2samp,

    gaussian_kde,

)

from scipy.spatial.distance import (

    jensenshannon,

)

GRID_POINTS = 512

EPSILON = 1e-12


# ============================================================
# INTERNAL
# ============================================================


def _numeric_columns(
    df: pd.DataFrame,
):

    return [

        c

        for c in df.columns

        if pd.api.types.is_numeric_dtype(
            df[c]
        )

    ]


def _empty_matrix(
    variables,
):

    return pd.DataFrame(

        np.zeros(

            (

                len(variables),

                len(variables),

            )

        ),

        index=variables,

        columns=variables,

    )


# ============================================================
# KDE CACHE
# ============================================================


def _build_kde_cache(
    df: pd.DataFrame,
):

    cache = {}

    variables = _numeric_columns(
        df
    )

    for variable in variables:

        values = (

            df[variable]

            .dropna()

            .to_numpy()

        )

        cache[variable] = {

            "values": values,

            "minimum": float(
                values.min()
            ),

            "maximum": float(
                values.max()
            ),

            "kde": gaussian_kde(
                values
            ),

        }

    return cache


# ============================================================
# COMMON SUPPORT
# ============================================================


def _common_grid(
    cache,
    a,
    b,
    grid_points=GRID_POINTS,
):

    xmin = min(

        cache[a]["minimum"],

        cache[b]["minimum"],

    )

    xmax = max(

        cache[a]["maximum"],

        cache[b]["maximum"],

    )

    grid = np.linspace(

        xmin,

        xmax,

        grid_points,

    )

    return grid


# ============================================================
# SHARED DENSITIES
# ============================================================


def _pair_densities(
    cache,
    a,
    b,
    grid_points=GRID_POINTS,
):

    grid = _common_grid(

        cache,

        a,

        b,

        grid_points,

    )

    pdf_a = cache[a]["kde"](
        grid
    )

    pdf_b = cache[b]["kde"](
        grid
    )

    pdf_a = np.maximum(
        pdf_a,
        EPSILON,
    )

    pdf_b = np.maximum(
        pdf_b,
        EPSILON,
    )

    pdf_a /= np.trapz(
        pdf_a,
        grid,
    )

    pdf_b /= np.trapz(
        pdf_b,
        grid,
    )

    return (

        grid,

        pdf_a,

        pdf_b,

    )

# ============================================================
# WASSERSTEIN
# ============================================================


def pairwise_wasserstein(
    df: pd.DataFrame,
):

    variables = _numeric_columns(df)

    matrix = _empty_matrix(
        variables
    )

    for a, b in combinations(
        variables,
        2,
    ):

        d = wasserstein_distance(

            df[a].dropna(),

            df[b].dropna(),

        )

        matrix.loc[a, b] = d
        matrix.loc[b, a] = d

    return matrix


# ============================================================
# KOLMOGOROV-SMIRNOV
# ============================================================


def pairwise_ks(
    df: pd.DataFrame,
):

    variables = _numeric_columns(df)

    distance = _empty_matrix(
        variables
    )

    pvalue = _empty_matrix(
        variables
    )

    np.fill_diagonal(
        pvalue.values,
        1.0,
    )

    for a, b in combinations(
        variables,
        2,
    ):

        result = ks_2samp(

            df[a].dropna(),

            df[b].dropna(),

        )

        distance.loc[a, b] = result.statistic
        distance.loc[b, a] = result.statistic

        pvalue.loc[a, b] = result.pvalue
        pvalue.loc[b, a] = result.pvalue

    return distance, pvalue


# ============================================================
# JENSEN-SHANNON
# ============================================================


def pairwise_js(
    df: pd.DataFrame,
):

    variables = _numeric_columns(
        df
    )

    cache = _build_kde_cache(
        df
    )

    matrix = _empty_matrix(
        variables
    )

    for a, b in combinations(
        variables,
        2,
    ):

        _, pa, pb = _pair_densities(

            cache,

            a,

            b,

        )

        d = jensenshannon(

            pa,

            pb,

        )

        matrix.loc[a, b] = d
        matrix.loc[b, a] = d

    return matrix


# ============================================================
# OVERLAP
# ============================================================


def pairwise_overlap(
    df: pd.DataFrame,
):

    variables = _numeric_columns(
        df
    )

    cache = _build_kde_cache(
        df
    )

    matrix = _empty_matrix(
        variables
    )

    np.fill_diagonal(
        matrix.values,
        1.0,
    )

    for a, b in combinations(
        variables,
        2,
    ):

        grid, da, db = _pair_densities(

            cache,

            a,

            b,

        )

        overlap = np.trapz(

            np.minimum(

                da,

                db,

            ),

            grid,

        )

        matrix.loc[a, b] = overlap
        matrix.loc[b, a] = overlap

    return matrix


# ============================================================
# SUMMARY
# ============================================================


def summary_statistics(
    matrix: pd.DataFrame,
):

    values = []

    pairs = []

    variables = list(
        matrix.columns
    )

    for a, b in combinations(
        variables,
        2,
    ):

        value = float(
            matrix.loc[a, b]
        )

        values.append(
            value
        )

        pairs.append(
            (
                a,
                b,
                value,
            )
        )

    minimum = min(
        pairs,
        key=lambda x: x[2],
    )

    maximum = max(
        pairs,
        key=lambda x: x[2],
    )

    return {

        "variables":
            len(variables),

        "comparisons":
            len(values),

        "minimum":
            minimum,

        "maximum":
            maximum,

        "mean":
            float(
                np.mean(values)
            ),

    }
