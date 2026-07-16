"""
============================================================
RSG
S28-E1.1
Metric Properties of the Relational Signature Space
============================================================

Objective
---------
Investigate the basic metric properties of the Relational Signature Space.

Given the current Reference Signature Space, this experiment computes:

    • Pairwise Euclidean distances
    • Metric diameter
    • Metric radius
    • Metric center
    • Eccentricity of every signature
    • Peripheral set

No new dynamical systems are generated.

============================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


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
# Header
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E1.1")
    print("Metric Properties of the Relational Signature Space")
    print("=" * 60)
    print()


# ============================================================
# Dataset
# ============================================================

def build_dataframe():

    names = list(SIGNATURES.keys())

    data = np.array(list(SIGNATURES.values()))

    return pd.DataFrame(
        data,
        index=names,
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

    distance_matrix = cdist(X, X, metric="euclidean")

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

    center = ecc[ecc == radius].index.tolist()

    peripheral = ecc[ecc == diameter].index.tolist()

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

    results = Path("RESULTS")
    results.mkdir(exist_ok=True)

    distance_df.to_csv(
        results / "S28_E1_1_metric_distance_matrix.csv"
    )

    ecc.to_csv(
        results / "S28_E1_1_eccentricities.csv"
    )

    print()
    print("Generated files")
    print("-" * 60)
    print("RESULTS/S28_E1_1_metric_distance_matrix.csv")
    print("RESULTS/S28_E1_1_eccentricities.csv")

    print()
    print("=" * 60)
    print("STATUS : METRIC PROPERTIES COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
