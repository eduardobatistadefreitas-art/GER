"""
============================================================
GER
S29
E6.2
Statistical Observatory
Stability Analysis
============================================================

Evaluates the statistical stability of the
Relational Signature Space through repeated
random resampling.

Author
------
GER Project
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .io import load_signatures

# ============================================================
# Version
# ============================================================

STABILITY_VERSION = "1.0"

DEFAULT_ITERATIONS = 100
DEFAULT_FRACTION = 0.80

# ============================================================
# Public API
# ============================================================

__all__ = [
    "bootstrap_statistics",
    "stability_summary",
    "compute_stability",
]

# ============================================================
# Bootstrap
# ============================================================

def bootstrap_statistics(
    signatures: pd.DataFrame,
    iterations: int = DEFAULT_ITERATIONS,
    fraction: float = DEFAULT_FRACTION,
):
    """
    Bootstrap estimation of statistical stability.
    """

    records = []

    sample_size = max(
        2,
        int(len(signatures) * fraction),
    )

    for _ in range(iterations):

        sample = signatures.sample(
            n=sample_size,
            replace=True,
        )

        row = {}

        for column in sample.columns:

            row[f"{column}_mean"] = sample[column].mean()
            row[f"{column}_std"] = sample[column].std()

        records.append(row)

    return pd.DataFrame(records)


# ============================================================
# Summary
# ============================================================

def stability_summary(
    bootstrap: pd.DataFrame,
):
    """
    Summarize bootstrap variability.
    """

    summary = {}

    for column in bootstrap.columns:

        summary[column] = {

            "mean": float(
                bootstrap[column].mean()
            ),

            "std": float(
                bootstrap[column].std()
            ),

            "minimum": float(
                bootstrap[column].min()
            ),

            "maximum": float(
                bootstrap[column].max()
            ),
        }

    return summary


# ============================================================
# High-Level API
# ============================================================

def compute_stability(
    signatures: pd.DataFrame,
    iterations: int = DEFAULT_ITERATIONS,
    fraction: float = DEFAULT_FRACTION,
):
    """
    Complete stability analysis.
    """

    bootstrap = bootstrap_statistics(
        signatures,
        iterations,
        fraction,
    )

    summary = stability_summary(
        bootstrap
    )

    return {

        "bootstrap": bootstrap,

        "summary": summary,
    }


# ============================================================
# Printing
# ============================================================

def _print_summary(summary):

    print("=" * 60)
    print("GER Statistical Observatory")
    print("Stability")
    print("=" * 60)
    print()

    for variable, values in summary.items():

        print(variable)

        print(
            f"  mean : {values['mean']:.6f}"
        )

        print(
            f"  std  : {values['std']:.6f}"
        )

        print()


# ============================================================
# Self Test
# ============================================================

def main():

    print("=" * 60)
    print("GER S29 E6.2")
    print("Stability Module")
    print("=" * 60)
    print()

    signatures = load_signatures()

    results = compute_stability(
        signatures
    )

    _print_summary(
        results["summary"]
    )


if __name__ == "__main__":
    main()
