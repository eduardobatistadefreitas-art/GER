"""
============================================================
RSG
S28-E4.2
Angle Invariance
============================================================

Objective
---------
Verify that the intrinsic coordinate system preserves the
angles between displacement vectors in the current
Relational Signature Space.

Computed quantities

    • Pairwise angles (observational coordinates)
    • Pairwise angles (intrinsic coordinates)
    • Maximum angular difference
    • Mean angular difference

============================================================
"""

import numpy as np
from itertools import combinations

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
    print("S28-E4.2")
    print("Angle Invariance")
    print("=" * 60)
    print()


def angle(u, v):

    c = np.dot(u, v)

    c /= np.linalg.norm(u)

    c /= np.linalg.norm(v)

    c = np.clip(c, -1.0, 1.0)

    return np.degrees(np.arccos(c))


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    labels = names()
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

    errors = []

    print("Angle Comparison")
    print("-" * 60)

    for i, j in combinations(range(len(labels)), 2):

        a1 = angle(Xc[i], Xc[j])

        a2 = angle(intrinsic[i], intrinsic[j])

        diff = abs(a1 - a2)

        errors.append(diff)

        print(
            f"{labels[i]:18s}"
            f"{labels[j]:18s}"
            f"{diff:.12e}"
        )

    print()

    print("Summary")
    print("-" * 60)

    print(f"Maximum difference    : {max(errors):.12e}")

    print(f"Mean difference       : {np.mean(errors):.12e}")

    print()

    tolerance = 1e-10

    if max(errors) < tolerance:

        print("Invariant Check")
        print("-" * 60)
        print("PASS")
        print()
        print("The intrinsic coordinate system")
        print("preserves all pairwise angles.")

    else:

        print("Invariant Check")
        print("-" * 60)
        print("FAIL")

    print()
    print("=" * 60)
    print("STATUS : ANGLE INVARIANCE VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
