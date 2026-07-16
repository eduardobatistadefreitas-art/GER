"""
============================================================
RSG
S28-E5.2
Gram Structure
============================================================

Objective
---------
Construct the Gram matrix of the centered Relational
Signature Space and investigate its algebraic structure.

Computed quantities

    • Gram matrix
    • Symmetry check
    • Matrix rank
    • Eigenvalues
    • Trace
    • Frobenius norm

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
    print("S28-E5.2")
    print("Gram Structure")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    print("Reference Signature Space")
    print("-" * 60)
    print(dataframe())
    print()

    X = vectors()

    centroid = X.mean(axis=0)

    Xc = X - centroid

    # --------------------------------------------------------
    # Gram matrix
    # --------------------------------------------------------

    G = Xc @ Xc.T

    print("Gram Matrix")
    print("-" * 60)
    print(np.round(G, 6))
    print()

    # --------------------------------------------------------
    # Properties
    # --------------------------------------------------------

    symmetric = np.allclose(G, G.T)

    rank = np.linalg.matrix_rank(G)

    eigenvalues = np.linalg.eigvalsh(G)
    eigenvalues = np.sort(eigenvalues)[::-1]

    trace = np.trace(G)

    frobenius = np.linalg.norm(G, ord="fro")

    print("Properties")
    print("-" * 60)

    print(f"Symmetric           : {symmetric}")
    print(f"Rank                : {rank}")
    print(f"Trace               : {trace:.6f}")
    print(f"Frobenius norm      : {frobenius:.6f}")

    print()

    print("Eigenvalues")
    print("-" * 60)

    for i, value in enumerate(eigenvalues, start=1):
        print(f"λ{i} = {value:.6f}")

    print()

    print("=" * 60)
    print("STATUS : GRAM STRUCTURE COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
