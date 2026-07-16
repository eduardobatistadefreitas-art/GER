"""
============================================================
RSG
S28-E3.1
Fundamental Geometric Axes
============================================================

Objective
---------
Identify which Geometric Signatures are most strongly aligned
with the principal geometric axis of the current Relational
Signature Space.

Computed quantities

    • Principal geometric axis
    • Alignment of each signature
    • Positive and negative extremes
    • Orthogonal signatures

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
    print("S28-E3.1")
    print("Fundamental Geometric Axes")
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

    print("Reference Signature Space")
    print("-" * 60)
    print(df)
    print()

    # --------------------------------------------------------
    # Centroid
    # --------------------------------------------------------

    centroid = X.mean(axis=0)

    Xc = X - centroid

    # --------------------------------------------------------
    # Principal axis
    # --------------------------------------------------------

    covariance = np.cov(
        Xc,
        rowvar=False,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)

    order = np.argsort(eigenvalues)[::-1]

    principal_axis = eigenvectors[:, order][:, 0]

    # --------------------------------------------------------
    # Alignments
    # --------------------------------------------------------

    alignments = []

    for label, vec in zip(labels, Xc):

        u = vec / np.linalg.norm(vec)

        alignment = float(np.dot(u, principal_axis))

        alignments.append(
            (
                label,
                alignment,
            )
        )

    alignments.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    print("Principal Geometric Axis")
    print("-" * 60)
    print(
        f"["
        f"{principal_axis[0]: .6f}, "
        f"{principal_axis[1]: .6f}, "
        f"{principal_axis[2]: .6f}"
        f"]"
    )
    print()

    print("Axis Alignment")
    print("-" * 60)

    for label, value in alignments:

        print(f"{label:20s} {value: .6f}")

    print()

    positive = alignments[0]
    negative = alignments[-1]

    orthogonal = min(
        alignments,
        key=lambda x: abs(x[1]),
    )

    print("Geometric Interpretation")
    print("-" * 60)

    print(
        f"Positive extreme      : "
        f"{positive[0]}"
    )

    print(
        f"Negative extreme      : "
        f"{negative[0]}"
    )

    print(
        f"Most orthogonal       : "
        f"{orthogonal[0]}"
    )

    print()

    print("=" * 60)
    print("STATUS : FUNDAMENTAL AXES IDENTIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
