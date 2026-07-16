"""
============================================================
RSG
S28-E3.2
Intrinsic Coordinate System
============================================================

Objective
---------
Express every Geometric Signature in the intrinsic coordinate
system induced by the principal geometric axes of the current
Relational Signature Space.

Computed quantities

    • Principal geometric basis
    • Intrinsic coordinates
    • Coordinate ranges
    • Coordinate variances

============================================================
"""

import numpy as np
import pandas as pd

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
    print("S28-E3.2")
    print("Intrinsic Coordinate System")
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

    # --------------------------------------------------------
    # Center the data
    # --------------------------------------------------------

    centroid = X.mean(axis=0)
    Xc = X - centroid

    # --------------------------------------------------------
    # Intrinsic basis
    # --------------------------------------------------------

    covariance = np.cov(
        Xc,
        rowvar=False,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)

    order = np.argsort(eigenvalues)[::-1]

    eigenvectors = eigenvectors[:, order]

    # --------------------------------------------------------
    # Projection
    # --------------------------------------------------------

    coordinates = Xc @ eigenvectors

    coord_df = pd.DataFrame(
        coordinates,
        index=labels,
        columns=[
            "Alpha1",
            "Alpha2",
            "Alpha3",
        ],
    )

    print("Intrinsic Coordinates")
    print("-" * 60)
    print(coord_df.round(6))
    print()

    print("Coordinate Statistics")
    print("-" * 60)

    for column in coord_df.columns:

        values = coord_df[column]

        print(f"{column}")
        print(f"    Mean      : {values.mean(): .6f}")
        print(f"    Variance  : {values.var(): .6f}")
        print(f"    Minimum   : {values.min(): .6f}")
        print(f"    Maximum   : {values.max(): .6f}")
        print()

    print("Intrinsic Basis")
    print("-" * 60)

    for i in range(3):

        v = eigenvectors[:, i]

        print(
            f"v{i+1} = "
            f"[{v[0]: .6f}, "
            f"{v[1]: .6f}, "
            f"{v[2]: .6f}]"
        )

    print()

    print("=" * 60)
    print("STATUS : INTRINSIC COORDINATE SYSTEM COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
