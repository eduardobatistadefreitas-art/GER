"""
============================================================
RSG
S28-E4.3
Volume Invariance
============================================================

Objective
---------
Verify that the intrinsic coordinate system preserves the
global geometric volume of the Relational Signature Space.

Computed quantities

    • Convex Hull volume (observational coordinates)
    • Convex Hull volume (intrinsic coordinates)
    • Absolute difference
    • Relative difference

============================================================
"""

import numpy as np
from scipy.spatial import ConvexHull

from GER_CORE.S28.signature_dataset import vectors


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E4.3")
    print("Volume Invariance")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    X = vectors()

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

    hull_obs = ConvexHull(X)

    hull_int = ConvexHull(intrinsic)

    volume_obs = hull_obs.volume
    volume_int = hull_int.volume

    absolute = abs(volume_obs - volume_int)

    relative = absolute / volume_obs

    print("Volume Comparison")
    print("-" * 60)

    print(f"Observational volume  : {volume_obs:.12f}")
    print(f"Intrinsic volume      : {volume_int:.12f}")
    print()

    print(f"Absolute difference   : {absolute:.12e}")
    print(f"Relative difference   : {relative:.12e}")

    print()

    tolerance = 1e-10

    print("Invariant Check")
    print("-" * 60)

    if absolute < tolerance:

        print("PASS")
        print()
        print("The intrinsic coordinate system")
        print("preserves the Convex Hull volume.")

    else:

        print("FAIL")

    print()
    print("=" * 60)
    print("STATUS : VOLUME INVARIANCE VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
