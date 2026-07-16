"""
============================================================
RSG
S28-E5.1
Reflection Symmetry
============================================================

Objective
---------
Investigate whether the current Relational Signature Space
exhibits approximate reflection symmetry with respect to its
geometric barycenter.

For every signature Si, the experiment searches for the
signature Sj that best approximates the reflected point

    2G - Si

where G is the geometric barycenter.

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
    print("S28-E5.1")
    print("Reflection Symmetry")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    labels = names()
    X = vectors()

    print("Reference Signature Space")
    print("-" * 60)
    print(dataframe())
    print()

    centroid = X.mean(axis=0)

    print("Reflection Pairs")
    print("-" * 60)

    residuals = []

    for i, label in enumerate(labels):

        reflected = 2 * centroid - X[i]

        distances = np.linalg.norm(
            X - reflected,
            axis=1,
        )

        distances[i] = np.inf

        j = np.argmin(distances)

        residual = distances[j]

        residuals.append(residual)

        print(
            f"{label:20s}"
            f"<-> "
            f"{labels[j]:20s}"
            f"{residual:.6f}"
        )

    print()

    print("Symmetry Summary")
    print("-" * 60)

    print(f"Mean residual        : {np.mean(residuals):.6f}")
    print(f"Minimum residual     : {np.min(residuals):.6f}")
    print(f"Maximum residual     : {np.max(residuals):.6f}")

    print()

    if np.mean(residuals) < 0.25:

        interpretation = (
            "Strong approximate reflection symmetry"
        )

    elif np.mean(residuals) < 0.75:

        interpretation = (
            "Moderate reflection symmetry"
        )

    else:

        interpretation = (
            "No significant reflection symmetry"
        )

    print("Interpretation")
    print("-" * 60)
    print(interpretation)

    print()
    print("=" * 60)
    print("STATUS : REFLECTION SYMMETRY ANALYZED")
    print("=" * 60)


if __name__ == "__main__":
    main()
