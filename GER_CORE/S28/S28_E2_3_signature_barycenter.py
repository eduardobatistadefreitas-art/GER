"""
============================================================
RSG
S28-E2.3
Signature Barycenter
============================================================

Objective
---------
Compute the geometric barycenter (centroid) of the current
Relational Signature Space and characterize the relative
position of every Geometric Signature.

Computed quantities

    • Signature barycenter
    • Distance of every signature to the barycenter
    • Nearest signature
    • Farthest signature
    • Mean radius

============================================================
"""

import numpy as np

from GER_CORE.S28.signature_dataset import (
    dataframe,
    names,
    vectors,
)


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E2.3")
    print("Signature Barycenter")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    df = dataframe()
    labels = names()
    X = vectors()

    centroid = X.mean(axis=0)

    distances = np.linalg.norm(
        X - centroid,
        axis=1,
    )

    ranking = sorted(
        zip(labels, distances),
        key=lambda x: x[1],
    )

    print("Reference Signature Space")
    print("-" * 60)
    print(df)
    print()

    print("Signature Barycenter")
    print("-" * 60)
    print(f"Diameter             : {centroid[0]:.6f}")
    print(f"Convergence          : {centroid[1]:.6f}")
    print(f"Recurrence           : {centroid[2]:.6f}")
    print()

    print("Distances to Barycenter")
    print("-" * 60)

    for name, distance in ranking:
        print(f"{name:20s} {distance:.6f}")

    nearest = ranking[0]
    farthest = ranking[-1]

    print()

    print("Nearest Signature")
    print("-" * 60)
    print(f"{nearest[0]} ({nearest[1]:.6f})")

    print()

    print("Farthest Signature")
    print("-" * 60)
    print(f"{farthest[0]} ({farthest[1]:.6f})")

    print()

    print("Mean Radius")
    print("-" * 60)
    print(f"{distances.mean():.6f}")

    print()

    print("=" * 60)
    print("STATUS : SIGNATURE BARYCENTER COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
