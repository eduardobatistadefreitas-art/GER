"""
============================================================
RSG
S28-E6.1
Spectral Concentration
============================================================

Objective
---------
Characterize the concentration of the Gram spectrum of the
current Relational Signature Space.

Computed quantities

    • Spectral Concentration Index (SCI)
    • Relative eigenvalue ratios
    • Effective rank
    • Spectral entropy

============================================================
"""

import numpy as np

from GER_CORE.S28.signature_dataset import vectors


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E6.1")
    print("Spectral Concentration")
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

    G = Xc @ Xc.T

    eigenvalues = np.linalg.eigvalsh(G)
    eigenvalues = np.sort(eigenvalues)[::-1]

    positive = eigenvalues[eigenvalues > 1e-12]

    energy = positive / positive.sum()

    sci = energy[0]

    ratio21 = positive[1] / positive[0]
    ratio31 = positive[2] / positive[0]

    entropy = -np.sum(
        energy * np.log(energy)
    )

    effective_rank = np.exp(entropy)

    print("Spectral Concentration")
    print("-" * 60)

    print(f"SCI                 : {sci:.6f}")
    print(f"λ2 / λ1             : {ratio21:.6f}")
    print(f"λ3 / λ1             : {ratio31:.6f}")
    print()

    print("Spectral Complexity")
    print("-" * 60)

    print(f"Spectral entropy    : {entropy:.6f}")
    print(f"Effective rank      : {effective_rank:.6f}")

    print()

    print("Interpretation")
    print("-" * 60)

    if sci >= 0.90:
        print("Strongly concentrated spectrum")

    elif sci >= 0.80:
        print("Moderately concentrated spectrum")

    elif sci >= 0.60:
        print("Weakly concentrated spectrum")

    else:
        print("Distributed spectrum")

    print()

    print("=" * 60)
    print("STATUS : SPECTRAL CONCENTRATION COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
