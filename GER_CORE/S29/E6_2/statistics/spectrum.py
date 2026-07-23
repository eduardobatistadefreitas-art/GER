"""
============================================================
GER
Frequency Spectrum Utilities
============================================================

Reusable utilities for analysing signature frequency spectra.

Functions
---------
compute_frequency_table(...)
compute_cumulative_coverage(...)
compute_long_tail(...)
compute_spectrum_summary(...)
============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ============================================================
# FREQUENCY TABLE
# ============================================================

def compute_frequency_table(df):

    frequency = (

        df
        .groupby(list(df.columns))
        .size()
        .reset_index(name="Frequency")

    )

    frequency = (

        frequency

        .sort_values(
            "Frequency",
            ascending=False,
        )

        .reset_index(drop=True)

    )

    frequency["Rank"] = np.arange(

        1,

        len(frequency) + 1,

    )

    return frequency


# ============================================================
# CUMULATIVE COVERAGE
# ============================================================

def compute_cumulative_coverage(frequency_table):

    table = frequency_table.copy()

    total = table["Frequency"].sum()

    table["Cumulative"] = table[
        "Frequency"
    ].cumsum()

    table["Coverage"] = (

        table["Cumulative"]

        / total

    )

    return table


# ============================================================
# LONG TAIL
# ============================================================

def compute_long_tail(

    frequency_table,

    threshold=0.01,

):

    total = frequency_table[
        "Frequency"
    ].sum()

    relative = (

        frequency_table["Frequency"]

        / total

    )

    return (

        frequency_table.loc[
            relative < threshold
        ]

        .reset_index(drop=True)

    )


# ============================================================
# SUMMARY
# ============================================================

def compute_spectrum_summary(

    frequency_table,

):

    frequencies = frequency_table[
        "Frequency"
    ].values

    coverage = compute_cumulative_coverage(
        frequency_table
    )

    return {

        "unique_signatures": int(

            len(frequency_table)

        ),

        "total_occurrences": int(

            frequencies.sum()

        ),

        "maximum_frequency": int(

            frequencies.max()

        ),

        "minimum_frequency": int(

            frequencies.min()

        ),

        "mean_frequency": float(

            np.mean(frequencies)

        ),

        "median_frequency": float(

            np.median(frequencies)

        ),

        "std_frequency": float(

            np.std(frequencies)

        ),

        "coverage_50_percent": int(

            (coverage["Coverage"] < 0.50).sum()

            + 1

        ),

        "coverage_90_percent": int(

            (coverage["Coverage"] < 0.90).sum()

            + 1

        ),

        "coverage_99_percent": int(

            (coverage["Coverage"] < 0.99).sum()

            + 1

        ),

    }
