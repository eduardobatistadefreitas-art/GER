"""
============================================================
RSG
S28-E2.1
Intrinsic Dimension
============================================================

Objective
---------
Determine the intrinsic linear dimension of the current
Relational Signature Space.

Computed quantities

    • Matrix rank
    • Centered matrix rank
    • Singular values
    • Condition number
    • Observed intrinsic dimension

============================================================
"""

import numpy as np

from GER_CORE.S28.signature_dataset import (
    dataframe,
    vectors,
)


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E2.1")
    print("Intrinsic Dimension")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    df = dataframe()

    X = vectors()

    print("Signature Matrix")
    print("-" * 60)
    print(df)
    print()

    print("Matrix Dimensions")
    print("-" * 60)
    print(f"Samples              : {X.shape[0]}")
    print(f"Coordinates          : {X.shape[1]}")
    print()

    rank_raw = np.linalg.matrix_rank(X)

    X_centered = X - X.mean(axis=0)

    rank_centered = np.linalg.matrix_rank(X_centered)

    singular_values = np.linalg.svd(
        X_centered,
        compute_uv=False,
    )

    condition = np.linalg.cond(X_centered)

    print("Linear Structure")
    print("-" * 60)
    print(f"Raw rank             : {rank_raw}")
    print(f"Centered rank        : {rank_centered}")
    print()

    print("Singular Values")
    print("-" * 60)

    for i, value in enumerate(singular_values, start=1):
        print(f"s{i}                   : {value:.6f}")

    print()

    print("Condition Number")
    print("-" * 60)
    print(f"{condition:.6f}")
    print()

    print("Conclusion")
    print("-" * 60)
    print(f"Observed intrinsic dimension : {rank_centered}")

    print()
    print("=" * 60)
    print("STATUS : INTRINSIC DIMENSION COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
