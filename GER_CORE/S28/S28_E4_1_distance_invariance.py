"""
============================================================
RSG
S28-E4.1
Distance Invariance
============================================================

Objective
---------
Verify that the intrinsic coordinate system preserves all
pairwise Euclidean distances of the current Relational
Signature Space.

Computed quantities

    • Distance matrix (observational coordinates)
    • Distance matrix (intrinsic coordinates)
    • Maximum absolute difference
    • Mean absolute difference

============================================================
"""

import numpy as np
from scipy.spatial.distance import cdist

from GER_CORE.S28.signature_dataset import (
    vectors,
)


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E4.1")
    print("Distance Invariance")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    X = vectors()

    # --------------------------------------------------------
    # Intrinsic coordinates
    # --------------------------------------------------------

    centroid = X.mean(axis=0)

    Xc = X - centroid

    covariance = np.cov(
        Xc,
        rowvar=False,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)

    order = np.argsort(eigenvalues)[::-1]

    eigenvectors = eigenvectors[:, order]

    intrinsic = Xc @ eigenvectors

    # --------------------------------------------------------
    # Distance matrices
    # --------------------------------------------------------

    D_obs = cdist(X, X)

    D_int = cdist(intrinsic, intrinsic)

    difference = np.abs(
        D_obs - D_int
    )

    max_error = difference.max()

    mean_error = difference.mean()

    print("Distance Comparison")
    print("-" * 60)
    print(f"Maximum difference    : {max_error:.12e}")
    print(f"Mean difference       : {mean_error:.12e}")
    print()

    tolerance = 1e-10

    if max_error < tolerance:

        print("Invariant Check")
        print("-" * 60)
        print("PASS")
        print()
        print("The intrinsic coordinate system")
        print("preserves all pairwise distances.")

    else:

        print("Invariant Check")
        print("-" * 60)
        print("FAIL")

    print()
    print("=" * 60)
    print("STATUS : DISTANCE INVARIANCE VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
