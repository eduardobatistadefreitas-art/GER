"""
============================================================
GER
Correlation Utilities
============================================================

Reusable correlation analysis utilities for the
GER framework.

This module centralizes correlation computations
used throughout the GER observatories.

Existing public functions remain fully compatible
with future versions.

Functions
---------
pearson_matrix(...)
spearman_matrix(...)
kendall_matrix(...)
correlation_matrix(...)

Additional utilities
--------------------
clean_dataframe(...)
correlation_table(...)
flatten_correlations(...)
rank_correlations(...)
correlation_summary(...)

============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# ============================================================
# Version
# ============================================================

CORRELATION_VERSION = "1.0"

# ============================================================
# Constants
# ============================================================

SUPPORTED_METHODS = (
    "pearson",
    "spearman",
    "kendall",
)

# ============================================================
# Public API
# ============================================================

__all__ = [

    "clean_dataframe",

    "pearson_matrix",
    "spearman_matrix",
    "kendall_matrix",

    "correlation_matrix",

    "correlation_table",
    "flatten_correlations",
    "rank_correlations",

    "correlation_summary",

]

# ============================================================
# Utilities
# ============================================================

def clean_dataframe(df):
    """
    Keep only numeric columns and remove rows
    containing missing values.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    numeric = df.select_dtypes(
        include=[np.number]
    )

    numeric = numeric.dropna()

    if numeric.shape[1] < 2:
        raise ValueError(
            "At least two numeric columns are required."
        )

    return numeric


# ============================================================
# Pearson
# ============================================================

def pearson_matrix(df):
    """
    Pearson correlation matrix.
    """

    df = clean_dataframe(df)

    return df.corr(
        method="pearson"
    )


# ============================================================
# Spearman
# ============================================================

def spearman_matrix(df):
    """
    Spearman rank correlation matrix.
    """

    df = clean_dataframe(df)

    return df.corr(
        method="spearman"
    )


# ============================================================
# Kendall
# ============================================================

def kendall_matrix(df):
    """
    Kendall rank correlation matrix.
    """

    df = clean_dataframe(df)

    return df.corr(
        method="kendall"
    )


# ============================================================
# Generic Interface
# ============================================================

def correlation_matrix(
    df,
    method="pearson",
):
    """
    Generic correlation interface.
    """

    method = method.lower()

    if method not in SUPPORTED_METHODS:

        raise ValueError(
            f"Unsupported method: {method}"
        )

    if method == "pearson":
        return pearson_matrix(df)

    if method == "spearman":
        return spearman_matrix(df)

    return kendall_matrix(df)

# ============================================================
# Correlation Table
# ============================================================

def correlation_table(matrix):
    """
    Convert a correlation matrix into a tidy table.

    Duplicate pairs and diagonal elements are removed.
    """

    if not isinstance(matrix, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    records = []

    columns = list(matrix.columns)

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            records.append({

                "Variable_1":
                    columns[i],

                "Variable_2":
                    columns[j],

                "Correlation":
                    float(
                        matrix.iloc[i, j]
                    ),

            })

    return pd.DataFrame(records)


# ============================================================
# Flatten Correlations
# ============================================================

def flatten_correlations(matrix):
    """
    Convert a correlation matrix into a list of
    dictionaries.
    """

    return correlation_table(
        matrix
    ).to_dict(
        orient="records"
    )


# ============================================================
# Rank Correlations
# ============================================================

def rank_correlations(
    matrix,
    absolute=True,
):
    """
    Rank correlation pairs.

    Parameters
    ----------
    absolute : bool
        If True, ranking is performed using
        absolute correlation values.
    """

    table = correlation_table(
        matrix
    ).copy()

    if absolute:

        table["Score"] = (
            table["Correlation"]
            .abs()
        )

    else:

        table["Score"] = (
            table["Correlation"]
        )

    table = (
        table
        .sort_values(
            "Score",
            ascending=False,
        )
        .drop(
            columns="Score"
        )
        .reset_index(
            drop=True
        )
    )

    return table


# ============================================================
# Correlation Summary
# ============================================================

def correlation_summary(matrix):
    """
    Compute descriptive statistics for a
    correlation matrix.
    """

    table = correlation_table(
        matrix
    )

    if len(table) == 0:

        return {

            "variables": 0,

            "pairs": 0,

        }

    values = (
        table["Correlation"]
        .to_numpy()
    )

    absolute = np.abs(
        values
    )

    return {

        "variables":
            int(
                matrix.shape[0]
            ),

        "pairs":
            int(
                len(values)
            ),

        "maximum":
            float(
                values.max()
            ),

        "minimum":
            float(
                values.min()
            ),

        "mean":
            float(
                values.mean()
            ),

        "mean_absolute":
            float(
                absolute.mean()
            ),

        "median_absolute":
            float(
                np.median(
                    absolute
                )
            ),

        "std_absolute":
            float(
                absolute.std()
            ),

        "strong_positive":
            int(
                np.sum(
                    values >= 0.70
                )
            ),

        "strong_negative":
            int(
                np.sum(
                    values <= -0.70
                )
            ),

        "very_strong":
            int(
                np.sum(
                    absolute >= 0.90
                )
            ),

    }


# ============================================================
# Self Test
# ============================================================

def main():

    np.random.seed(42)

    data = pd.DataFrame({

        "A":
            np.random.normal(
                size=1000,
            ),

        "B":
            np.random.normal(
                size=1000,
            ),

        "C":
            np.random.normal(
                size=1000,
            ),

        "D":
            np.random.normal(
                size=1000,
            ),

    })

    matrix = correlation_matrix(
        data,
        method="pearson",
    )

    print("=" * 60)
    print("GER")
    print("Correlation Utilities")
    print("=" * 60)
    print()

    print("Correlation Matrix")
    print(matrix)

    print()

    print("Correlation Ranking")
    print(
        rank_correlations(
            matrix
        )
    )

    print()

    print("Summary")

    summary = correlation_summary(
        matrix
    )

    for key, value in summary.items():

        print(
            f"{key:20s}: {value}"
        )


if __name__ == "__main__":

    main()
