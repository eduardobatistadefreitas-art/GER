"""
============================================================
GER
S29
E6.2
Statistical Observatory
Outlier Detection
============================================================

Detects statistically rare signatures in the
Relational Signature Space.

Outliers are identified using the estimated local
density together with a robust IQR criterion.

Author
------
GER Project
"""

from __future__ import annotations

import pandas as pd

from .density import compute_density
from .io import load_signatures

# ============================================================
# Version
# ============================================================

OUTLIER_VERSION = "1.0"

# ============================================================
# Public API
# ============================================================

__all__ = [
    "detect_outliers",
    "outlier_summary",
    "compute_outliers",
]

# ============================================================
# Detection
# ============================================================

def detect_outliers(
    density_table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect density outliers using the IQR rule.
    """

    table = density_table.copy()

    q1 = table["Density"].quantile(0.25)
    q3 = table["Density"].quantile(0.75)

    iqr = q3 - q1

    threshold = q1 - 1.5 * iqr

    table["Outlier"] = (
        table["Density"] < threshold
    )

    return table


# ============================================================
# Summary
# ============================================================

def outlier_summary(
    table: pd.DataFrame,
) -> dict:
    """
    Summarize detected outliers.
    """

    total = len(table)

    outliers = int(table["Outlier"].sum())

    return {

        "total_points": total,

        "outliers": outliers,

        "normal_points": total - outliers,

        "outlier_fraction":
            outliers / total if total else 0.0,
    }


# ============================================================
# High-Level API
# ============================================================

def compute_outliers(
    signatures: pd.DataFrame,
):
    """
    Complete outlier analysis.
    """

    density = compute_density(signatures)

    table = detect_outliers(
        density["table"]
    )

    summary = outlier_summary(table)

    return {

        "table": table,

        "summary": summary,
    }


# ============================================================
# Printing
# ============================================================

def _print_summary(summary):

    print("=" * 60)
    print("GER Statistical Observatory")
    print("Outlier Detection")
    print("=" * 60)
    print()

    for key, value in summary.items():

        print(f"{key:20s}: {value}")

    print()


# ============================================================
# Self Test
# ============================================================

def main():

    print("=" * 60)
    print("GER S29 E6.2")
    print("Outlier Module")
    print("=" * 60)
    print()

    signatures = load_signatures()

    results = compute_outliers(
        signatures
    )

    _print_summary(
        results["summary"]
    )

    print("Detected Outliers")
    print("-----------------")

    print(
        results["table"]
        .loc[
            results["table"]["Outlier"]
        ]
    )

    print()


if __name__ == "__main__":
    main()
