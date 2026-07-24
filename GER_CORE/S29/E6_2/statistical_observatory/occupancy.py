"""
============================================================
GER
S29
E6.2
Statistical Observatory
Occupancy Analysis
============================================================

Measures how the Relational Signature Space is occupied.

The occupancy analysis is intentionally independent from
density estimation. It answers questions such as:

• Which signatures are unique?
• How many repeated signatures exist?
• How much of the generated universe occupies the same
  signature?
• What is the effective occupation of the Signature Space?

Author
------
GER Project
"""

from __future__ import annotations

import pandas as pd

from .io import load_signatures

# ============================================================
# Version
# ============================================================

OCCUPANCY_VERSION = "1.0"

# ============================================================
# Public API
# ============================================================

__all__ = [
    "occupancy_table",
    "occupancy_summary",
    "compute_occupancy",
]

# ============================================================
# Occupancy
# ============================================================

def occupancy_table(
    signatures: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count identical signatures.

    Returns
    -------
    DataFrame

        diameter
        convergence
        recurrence
        drift
        Count
    """

    table = (
        signatures
        .value_counts()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return table


# ============================================================
# Summary
# ============================================================

def occupancy_summary(
    occupancy: pd.DataFrame,
) -> dict:
    """
    Compute global occupancy indicators.
    """

    total = int(occupancy["Count"].sum())

    unique = int(len(occupancy))

    repeated = int((occupancy["Count"] > 1).sum())

    maximum = int(occupancy["Count"].max())

    mean = float(occupancy["Count"].mean())

    return {

        "total_samples": total,

        "unique_signatures": unique,

        "repeated_signatures": repeated,

        "maximum_occupancy": maximum,

        "mean_occupancy": mean,

        "occupation_ratio": unique / total,
    }


# ============================================================
# High-Level API
# ============================================================

def compute_occupancy(
    signatures: pd.DataFrame,
) -> dict:
    """
    Complete occupancy analysis.
    """

    table = occupancy_table(signatures)

    summary = occupancy_summary(table)

    return {

        "table": table,

        "summary": summary,
    }


# ============================================================
# Printing
# ============================================================

def _print_summary(summary: dict):

    print("=" * 60)
    print("GER Statistical Observatory")
    print("Occupancy")
    print("=" * 60)
    print()

    for key, value in summary.items():

        print(f"{key:25s}: {value}")

    print()


# ============================================================
# Self Test
# ============================================================

def main():

    print("=" * 60)
    print("GER S29 E6.2")
    print("Occupancy Module")
    print("=" * 60)
    print()

    signatures = load_signatures()

    results = compute_occupancy(signatures)

    _print_summary(results["summary"])

    print("Most occupied signatures")
    print("------------------------")

    print(
        results["table"].head(10)
    )

    print()


if __name__ == "__main__":
    main()
