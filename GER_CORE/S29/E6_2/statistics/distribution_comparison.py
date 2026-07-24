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
    bins=100,
):

    variables = _numeric_columns(df)

    matrix = _empty_matrix(
        variables
    )

    for a, b in combinations(
        variables,
        2,
    ):

        xa = df[a].dropna()

        xb = df[b].dropna()

        minimum = min(
            xa.min(),
            xb.min(),
        )

        maximum = max(
            xa.max(),
            xb.max(),
        )

        pa, _ = np.histogram(

            xa,

            bins=bins,

            range=(minimum, maximum),

            density=True,

        )

        pb, _ = np.histogram(

            xb,

            bins=bins,

            range=(minimum, maximum),

            density=True,

        )

        pa += 1e-12
        pb += 1e-12

        pa /= pa.sum()
        pb /= pb.sum()

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
    grid_points=512,
):

    variables = _numeric_columns(df)

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

        xa = df[a].dropna().to_numpy()

        xb = df[b].dropna().to_numpy()

        xmin = min(
            xa.min(),
            xb.min(),
        )

        xmax = max(
            xa.max(),
            xb.max(),
        )

        grid = np.linspace(

            xmin,

            xmax,

            grid_points,

        )

        da = gaussian_kde(
            xa
        )(grid)

        db = gaussian_kde(
            xb
        )(grid)

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
