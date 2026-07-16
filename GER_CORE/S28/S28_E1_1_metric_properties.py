"""
============================================================
RSG
S28-E1.1
Metric Properties of the Relational Signature Space
============================================================

Objective
---------
Investigate the basic metric properties of the Relational
Signature Space.

Computed quantities

    • Pairwise Euclidean Distance Matrix
    • Eccentricities
    • Metric Diameter
    • Metric Radius
    • Metric Center
    • Peripheral Set

The object of study is the Relational Signature Space itself.

============================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


# ============================================================
# Project directories
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS = PROJECT_ROOT / "RESULTS"
RESULTS.mkdir(parents=True, exist_ok=True)


# ============================================================
# Reference Signature Space
# ============================================================

SIGNATURES = {
    "Harmonic": (1.992115, 0.083005, 0.022109),
    "Damped": (1.999804, 0.618431, 0.027211),
    "Van der Pol": (1.560891, 0.291408, 0.035714),
    "Logistic": (0.010717, 0.003313, 1.000000),
    "Lorenz": (0.419313, 0.079386, 0.137755),
    "Double Pendulum": (1.301499, 0.388995, 0.069728),
}


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E1.1")
    print("Metric Properties of the Relational Signature Space")
    print("=" * 60)
    print()


def build_dataframe():

    return pd.DataFrame(
        list(SIGNATURES.values()),
        index=list(SIGNATURES.keys()),
        columns=[
            "Diameter",
            "Convergence",
            "Recurrence",
        ],
    )


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    df = build_dataframe()

    print("Reference Signature Space")
    print("-" * 60)
    print(df)
    print()

    X = df.values

    distance_matrix = cdist(
        X,
        X,
        metric="euclidean",
    )

    distance_df = pd.DataFrame(
        distance_matrix,
        index=df.index,
        columns=df.index,
    )

    print("Metric Distance Matrix")
    print("-" * 60)
    print(distance_df.round(6))
    print()

    eccentricities = distance_matrix.max(axis=1)

    ecc = pd.Series(
        eccentricities,
        index=df.index,
        name="Eccentricity",
    )

    diameter = float(ecc.max())
    radius = float(ecc.min())

    tol = 1e-12

    center = ecc[
        np.isclose(
            ecc,
            radius,
            atol=tol,
        )
    ].index.tolist()

    peripheral = ecc[
        np.isclose(
            ecc,
            diameter,
            atol=tol,
        )
    ].index.tolist()

    print("Metric Properties")
    print("-" * 60)

    print(f"Number of signatures : {len(df)}")
    print(f"Metric diameter      : {diameter:.6f}")
    print(f"Metric radius        : {radius:.6f}")
    print()
    print("Metric Center")
    print("-" * 60)

    for c in center:
        print(c)

    print()

    print("Eccentricities")
    print("-" * 60)

    for name, value in ecc.items():
        print(f"{name:20s} {value:.6f}")

    print()

    print("Peripheral Set")
    print("-" * 60)

    for p in peripheral:
        print(p)

    print()

    distance_file = (
        RESULTS /
        "S28_E1_1_metric_distance_matrix.csv"
    )

    ecc_file = (
        RESULTS /
        "S28_E1_1_eccentricities.csv"
    )

    distance_df.to_csv(distance_file)

    ecc.to_csv(ecc_file)

    print("Generated files")
    print("-" * 60)
    print(distance_file)
    print(ecc_file)

    print()
    print("=" * 60)
    print("STATUS : METRIC PROPERTIES COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
