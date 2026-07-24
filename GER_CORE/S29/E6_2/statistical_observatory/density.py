"""
============================================================
GER
S29
E6.2
Statistical Observatory
Density Analysis
============================================================

Estimates the density distribution over the
Relational Signature Space.

Unlike occupancy, density measures the local
concentration of neighbouring signatures.

Author
------
GER Project
"""

from __future__ import annotations

import pandas as pd

from sklearn.neighbors import KernelDensity

from .io import load_signatures

# ============================================================
# Version
# ============================================================

DENSITY_VERSION = "1.0"

# ============================================================
# Defaults
# ============================================================

DEFAULT_BANDWIDTH = 0.05

# ============================================================
# Public API
# ============================================================

__all__ = [
    "estimate_density",
    "density_summary",
    "compute_density",
]

# ============================================================
# Density Estimation
# ============================================================

def estimate_density(
    signatures: pd.DataFrame,
    bandwidth: float = DEFAULT_BANDWIDTH,
) -> pd.DataFrame:
    """
    Estimate local density using Kernel Density Estimation.
    """

    kde = KernelDensity(
        kernel="gaussian",
        bandwidth=bandwidth,
    )

    kde.fit(signatures)

    density = kde.score_samples(signatures)

    result = signatures.copy()

    result["Density"] = density

    return result


# ============================================================
# Summary
# ============================================================

def density_summary(
    density: pd.DataFrame,
) -> dict:
    """
    Compute density indicators.
    """

    values = density["Density"]

    return {

        "minimum_density": float(values.min()),

        "maximum_density": float(values.max()),

        "mean_density": float(values.mean()),

        "median_density": float(values.median()),

        "std_density": float(values.std()),

        "high_density_points": int(
            (values > values.mean()).sum()
        ),

        "low_density_points": int(
            (values <= values.mean()).sum()
        ),
    }


# ============================================================
# High-Level API
# ============================================================

def compute_density(
    signatures: pd.DataFrame,
    bandwidth: float = DEFAULT_BANDWIDTH,
) -> dict:
    """
    Complete density analysis.
    """

    table = estimate_density(
        signatures,
        bandwidth,
    )

    summary = density_summary(
        table,
    )

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
    print("Density")
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
    print("Density Module")
    print("=" * 60)
    print()

    signatures = load_signatures()

    results = compute_density(signatures)

    _print_summary(results["summary"])

    print("Highest Density Regions")
    print("-----------------------")

    print(
        results["table"]
        .sort_values(
            "Density",
            ascending=False,
        )
        .head(10)
    )

    print()


if __name__ == "__main__":
    main()
