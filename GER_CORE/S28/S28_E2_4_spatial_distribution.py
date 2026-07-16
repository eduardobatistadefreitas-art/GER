"""
============================================================
RSG
S28-E2.4
Spatial Distribution
============================================================

Objective
---------
Characterize the spatial distribution of the current
Relational Signature Space.

Computed quantities

    • Covariance matrix
    • Eigenvalues
    • Eigenvectors
    • Anisotropy ratio
    • Principal geometric directions

============================================================
"""

import numpy as np

from GER_CORE.S28.signature_dataset import dataframe, vectors


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E2.4")
    print("Spatial Distribution")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    df = dataframe()
    X = vectors()

    print("Reference Signature Space")
    print("-" * 60)
    print(df)
    print()

    Xc = X - X.mean(axis=0)

    covariance = np.cov(
        Xc,
        rowvar=False,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)

    order = np.argsort(eigenvalues)[::-1]

    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    anisotropy = eigenvalues[0] / eigenvalues[-1]

    print("Covariance Matrix")
    print("-" * 60)
    print(np.round(covariance, 6))
    print()

    print("Eigenvalues")
    print("-" * 60)

    for i, value in enumerate(eigenvalues, start=1):
        print(f"λ{i} = {value:.6f}")

    print()

    print("Principal Directions")
    print("-" * 60)

    for i in range(eigenvectors.shape[1]):

        v = eigenvectors[:, i]

        print(
            f"v{i+1} = "
            f"[{v[0]: .6f}, "
            f"{v[1]: .6f}, "
            f"{v[2]: .6f}]"
        )

    print()

    print("Distribution Summary")
    print("-" * 60)
    print(f"Anisotropy ratio      : {anisotropy:.6f}")

    if anisotropy < 2:
        interpretation = "Approximately isotropic"

    elif anisotropy < 5:
        interpretation = "Moderately anisotropic"

    else:
        interpretation = "Strongly anisotropic"

    print(f"Observed distribution : {interpretation}")

    print()
    print("=" * 60)
    print("STATUS : SPATIAL DISTRIBUTION COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
