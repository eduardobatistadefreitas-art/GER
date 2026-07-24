"""
============================================================
GER
S29
E6.2
Statistical Observatory
Concentration Analysis
============================================================

Measures how concentrated or dispersed the
Relational Signature Space is.

This module operates on the density estimates
computed by density.py.

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

CONCENTRATION_VERSION = "1.0"

# ============================================================
# Public API
# ============================================================

__all__ = [
    "concentration_summary",
    "compute_concentration",
]

# ============================================================
# Concentration Metrics
# ============================================================

def concentration_summary(
    density_table: pd.DataFrame,
) -> dict:
    """
    Compute global concentration indicators.
    """

    values = density_table["Density"]

    q25 = float(values.quantile(0.25))
    q50 = float(values.quantile(0.50))
    q75 = float(values.quantile(0.75))

    high = int((values >= q75).sum())
    medium = int(((values >= q25) & (values < q75)).sum())
    low = int((values < q25).sum())

    return {

        "minimum": float(values.min()),

        "maximum": float(values.max()),

        "mean": float(values.mean()),

        "median": float(values.median()),

        "standard_deviation": float(values.std()),

        "coefficient_of_variation":
            float(values.std() / abs(values.mean()))
            if values.mean() != 0 else 0.0,

        "q25": q25,

        "q50": q50,

        "q75": q75,

        "high_concentration_points": high,

        "medium_concentration_points": medium,

        "low_concentration_points": low,

        "dynamic_range":
            float(values.max() - values.min()),
    }


# ============================================================
# High-Level API
# ============================================================

def compute_concentration(
    signatures: pd.DataFrame,
) -> dict:
    """
    Complete concentration analysis.
    """

    density = compute_density(signatures)

    summary = concentration_summary(
        density["table"]
    )

    return {

        "density": density,

        "summary": summary,
    }


# ============================================================
# Printing
# ============================================================

def _print_summary(summary):

    print("=" * 60)
    print("GER Statistical Observatory")
    print("Concentration")
    print("=" * 60)
    print()

    for key, value in summary.items():

        print(f"{key:30s}: {value}")

    print()


# ============================================================
# Self Test
# ============================================================

def main():

    print("=" * 60)
    print("GER S29 E6.2")
    print("Concentration Module")
    print("=" * 60)
    print()

    signatures = load_signatures()

    results = compute_concentration(
        signatures
    )

    _print_summary(
        results["summary"]
    )


if __name__ == "__main__":
    main()
