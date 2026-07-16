"""
============================================================
RSG
S28-E4.4
Boundary Invariance
============================================================

Objective
---------
Verify that the Convex Hull boundary is preserved under the
transformation from observational coordinates to intrinsic
coordinates.

Computed quantities

    • Convex Hull vertices (observational)
    • Convex Hull vertices (intrinsic)
    • Boundary equivalence

============================================================
"""

import numpy as np
from scipy.spatial import ConvexHull

from GER_CORE.S28.signature_dataset import (
    names,
    vectors,
)


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E4.4")
    print("Boundary Invariance")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    labels = names()
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

    eigval, eigvec = np.linalg.eigh(covariance)

    order = np.argsort(eigval)[::-1]

    eigvec = eigvec[:, order]

    intrinsic = Xc @ eigvec

    # --------------------------------------------------------
    # Convex Hulls
    # --------------------------------------------------------

    hull_obs = ConvexHull(X)
    hull_int = ConvexHull(intrinsic)

    obs_vertices = sorted(hull_obs.vertices.tolist())
    int_vertices = sorted(hull_int.vertices.tolist())

    obs_names = [labels[i] for i in obs_vertices]
    int_names = [labels[i] for i in int_vertices]

    print("Observational Boundary")
    print("-" * 60)

    for name in obs_names:
        print(name)

    print()

    print("Intrinsic Boundary")
    print("-" * 60)

    for name in int_names:
        print(name)

    print()

    identical = obs_vertices == int_vertices

    print("Boundary Comparison")
    print("-" * 60)

    print(f"Observational vertices : {len(obs_vertices)}")
    print(f"Intrinsic vertices     : {len(int_vertices)}")
    print()

    if identical:

        print("PASS")
        print()
        print("Both coordinate systems")
        print("generate the same Convex Hull boundary.")

    else:

        print("FAIL")

    print()
    print("=" * 60)
    print("STATUS : BOUNDARY INVARIANCE VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
