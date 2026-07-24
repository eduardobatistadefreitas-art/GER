"""
============================================================
GER
Frequency Spectrum Utilities
============================================================

Reusable utilities for analysing signature frequency
spectra.

Existing public functions remain fully compatible.

Functions
---------
compute_frequency_table(...)
compute_cumulative_coverage(...)
compute_long_tail(...)
compute_spectrum_summary(...)

Additional utilities
--------------------
validate_frequency_table(...)
relative_frequency(...)
rank_frequency_curve(...)
frequency_histogram(...)
frequency_percentiles(...)
============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ============================================================
# Version
# ============================================================

SPECTRUM_VERSION = "2.0"


# ============================================================
# Constants
# ============================================================

DEFAULT_LONG_TAIL_THRESHOLD = 0.01

DEFAULT_HISTOGRAM_BINS = 20


# ============================================================
# Public API
# ============================================================

__all__ = [

    "compute_frequency_table",

    "compute_cumulative_coverage",

    "compute_long_tail",

    "compute_spectrum_summary",

    "validate_frequency_table",

    "relative_frequency",

    "rank_frequency_curve",

    "frequency_histogram",

    "frequency_percentiles",

]


# ============================================================
# Validation
# ============================================================

def validate_frequency_table(

    frequency_table,

):
    """
    Validate a GER frequency table.
    """

    if "Frequency" not in frequency_table.columns:

        raise ValueError(

            "Frequency column not found."

        )

    return frequency_table


# ============================================================
# FREQUENCY TABLE
# ============================================================

def compute_frequency_table(

    df,

):
    """
    Build a frequency table from signatures.
    """

    frequency = (

        df

        .groupby(

            list(df.columns)

        )

        .size()

        .reset_index(

            name="Frequency"

        )

    )

    frequency = (

        frequency

        .sort_values(

            "Frequency",

            ascending=False,

        )

        .reset_index(

            drop=True,

        )

    )

    frequency["Rank"] = np.arange(

        1,

        len(frequency) + 1,

    )

    return frequency


# ============================================================
# RELATIVE FREQUENCY
# ============================================================

def relative_frequency(

    frequency_table,

):
    """
    Add relative frequencies.
    """

    table = validate_frequency_table(

        frequency_table,

    ).copy()

    total = table["Frequency"].sum()

    if total == 0:

        table["Relative"] = 0.0

    else:

        table["Relative"] = (

            table["Frequency"]

            / total

        )

    return table


# ============================================================
# RANK-FREQUENCY CURVE
# ============================================================

def rank_frequency_curve(

    frequency_table,

):
    """
    Return rank-frequency representation.
    """

    table = validate_frequency_table(

        frequency_table,

    )

    return table.loc[

        :,

        [

            "Rank",

            "Frequency",

        ],

    ].copy()


# ============================================================
# HISTOGRAM
# ============================================================

def frequency_histogram(

    frequency_table,

    bins=DEFAULT_HISTOGRAM_BINS,

):
    """
    Histogram of frequencies.
    """

    table = validate_frequency_table(

        frequency_table,

    )

    hist, edges = np.histogram(

        table["Frequency"],

        bins=bins,

    )

    return pd.DataFrame(

        {

            "Left": edges[:-1],

            "Right": edges[1:],

            "Count": hist,

        }

    )


# ============================================================
# FREQUENCY PERCENTILES
# ============================================================

def frequency_percentiles(

    frequency_table,

    percentiles=(

        5,

        25,

        50,

        75,

        95,

    ),

):
    """
    Compute frequency percentiles.
    """

    table = validate_frequency_table(

        frequency_table,

    )

    values = table["Frequency"]

    return {

        int(p):

        float(

            np.percentile(

                values,

                p,

            )

        )

        for p in percentiles

    }


# ============================================================
# CUMULATIVE COVERAGE
# ============================================================

def compute_cumulative_coverage(

    frequency_table,

):
    """
    Compute cumulative coverage.
    """

    table = relative_frequency(

        frequency_table,

    )

    table["Cumulative"] = (

        table["Frequency"]

        .cumsum()

    )

    table["Coverage"] = (

        table["Relative"]

        .cumsum()

    )

    return table


# ============================================================
# LONG TAIL
# ============================================================

def compute_long_tail(

    frequency_table,

    threshold=DEFAULT_LONG_TAIL_THRESHOLD,

):
    """
    Extract the long tail.
    """

    table = relative_frequency(

        frequency_table,

    )

    return (

        table

        .loc[

            table["Relative"] < threshold

        ]

        .reset_index(

            drop=True,

        )

    )

# ============================================================
# RICHNESS
# ============================================================

def richness(

    frequency_table,

):
    """
    Number of unique signatures.
    """

    table = validate_frequency_table(

        frequency_table,

    )

    return int(

        len(table)

    )


# ============================================================
# DOMINANCE
# ============================================================

def dominance(

    frequency_table,

):
    """
    Relative frequency of the most common signature.
    """

    table = relative_frequency(

        frequency_table,

    )

    if len(table) == 0:

        return 0.0

    return float(

        table["Relative"].max()

    )


# ============================================================
# SINGLETON FRACTION
# ============================================================

def singleton_fraction(

    frequency_table,

):
    """
    Fraction of signatures observed once.
    """

    table = validate_frequency_table(

        frequency_table,

    )

    if len(table) == 0:

        return 0.0

    return float(

        (table["Frequency"] == 1).mean()

    )


# ============================================================
# DOUBLETON FRACTION
# ============================================================

def doubleton_fraction(

    frequency_table,

):
    """
    Fraction of signatures observed twice.
    """

    table = validate_frequency_table(

        frequency_table,

    )

    if len(table) == 0:

        return 0.0

    return float(

        (table["Frequency"] == 2).mean()

    )


# ============================================================
# HEAD MASS
# ============================================================

def head_mass(

    frequency_table,

    threshold=DEFAULT_LONG_TAIL_THRESHOLD,

):
    """
    Relative mass outside the long tail.
    """

    return float(

        1.0

        -

        compute_long_tail(

            frequency_table,

            threshold,

        )["Relative"].sum()

    )


# ============================================================
# TAIL MASS
# ============================================================

def tail_mass(

    frequency_table,

    threshold=DEFAULT_LONG_TAIL_THRESHOLD,

):
    """
    Relative mass contained in the long tail.
    """

    tail = compute_long_tail(

        frequency_table,

        threshold,

    )

    return float(

        tail["Relative"].sum()

    )


# ============================================================
# COVERAGE AT RANK
# ============================================================

def coverage_at_rank(

    frequency_table,

    rank,

):
    """
    Coverage achieved up to a given rank.
    """

    table = compute_cumulative_coverage(

        frequency_table,

    )

    rank = max(

        1,

        min(

            int(rank),

            len(table),

        ),

    )

    return float(

        table.iloc[

            rank - 1

        ]["Coverage"]

    )


# ============================================================
# RANK FOR COVERAGE
# ============================================================

def rank_for_coverage(

    frequency_table,

    target,

):
    """
    Minimum rank required to achieve a target coverage.
    """

    table = compute_cumulative_coverage(

        frequency_table,

    )

    mask = table["Coverage"] >= target

    if not np.any(mask):

        return len(table)

    return int(

        table.loc[

            mask,

            "Rank",

        ].iloc[0]

    )


# ============================================================
# SPECTRAL BALANCE
# ============================================================

def spectral_balance(

    frequency_table,

    threshold=DEFAULT_LONG_TAIL_THRESHOLD,

):
    """
    Head/Tail balance.
    """

    head = head_mass(

        frequency_table,

        threshold,

    )

    tail = tail_mass(

        frequency_table,

        threshold,

    )

    return {

        "head": head,

        "tail": tail,

        "difference": head - tail,

        "ratio": (

            np.inf

            if tail == 0

            else head / tail

        ),

    }


# ============================================================
# SPECTRUM SUMMARY
# ============================================================

def compute_spectrum_summary(

    frequency_table,

):
    """
    Compute descriptive statistics of the
    frequency spectrum.
    """

    table = compute_cumulative_coverage(

        frequency_table,

    )

    frequencies = table["Frequency"].to_numpy()

    return {

        "unique_signatures": richness(table),

        "total_occurrences": int(frequencies.sum()),

        "maximum_frequency": int(frequencies.max()),

        "minimum_frequency": int(frequencies.min()),

        "mean_frequency": float(np.mean(frequencies)),

        "median_frequency": float(np.median(frequencies)),

        "std_frequency": float(np.std(frequencies)),

        "dominance": dominance(table),

        "singleton_fraction": singleton_fraction(table),

        "doubleton_fraction": doubleton_fraction(table),

        "tail_mass": tail_mass(table),

        "head_mass": head_mass(table),

        "coverage_50_percent": rank_for_coverage(table, 0.50),

        "coverage_90_percent": rank_for_coverage(table, 0.90),

        "coverage_99_percent": rank_for_coverage(table, 0.99),

    }


# ============================================================
# SELF TEST
# ============================================================

def main():

    df = pd.DataFrame(

        {

            "Signature": np.random.choice(

                list("ABCDEFGHIJ"),

                size=1000,

                p=[

                    0.30,

                    0.20,

                    0.15,

                    0.10,

                    0.08,

                    0.06,

                    0.04,

                    0.03,

                    0.02,

                    0.02,

                ],

            )

        }

    )

    spectrum = compute_frequency_table(df)

    summary = compute_spectrum_summary(

        spectrum

    )

    print("=" * 60)

    print("GER")

    print("Frequency Spectrum")

    print("=" * 60)

    print()

    for key, value in summary.items():

        print(

            f"{key:25s}: {value}"

        )


if __name__ == "__main__":

    main()
