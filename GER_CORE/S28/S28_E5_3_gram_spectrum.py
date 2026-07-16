"""
============================================================
RSG
S28-E5.3
Gram Spectrum
============================================================

Objective
---------
Investigate the spectral structure of the Gram operator of the
current Relational Signature Space.

Computed quantities

    • Gram eigenvalues
    • Spectral energy distribution
    • Cumulative energy
    • Spectral entropy
    • Effective rank

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
    print("S28-E5.3")
    print("Gram Spectrum")
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

    cumulative = np.cumsum(energy)

    entropy = -np.sum(
        energy * np.log(energy)
    )

    effective_rank = np.exp(entropy)

    print("Gram Eigenvalues")
    print("-" * 60)

    for i, value in enumerate(positive, start=1):
        print(f"λ{i:<2} : {value:.6f}")

    print()

    print("Spectral Energy")
    print("-" * 60)

    for i, value in enumerate(energy, start=1):
        print(f"Mode {i:<2}: {100*value:.3f}%")

    print()

    print("Cumulative Energy")
    print("-" * 60)

    for i, value in enumerate(cumulative, start=1):
        print(f"Mode {i:<2}: {100*value:.3f}%")

    print()

    print("Spectral Summary")
    print("-" * 60)

    print(f"Spectral entropy     : {entropy:.6f}")
    print(f"Effective rank       : {effective_rank:.6f}")

    dominance = energy[0]

    print(f"Dominant mode        : {100*dominance:.3f}%")

    print()

    if dominance > 0.90:
        interpretation = "Highly concentrated spectrum"

    elif dominance > 0.70:
        interpretation = "Moderately concentrated spectrum"

    else:
        interpretation = "Distributed spectrum"

    print("Interpretation")
    print("-" * 60)
    print(interpretation)

    print()
    print("=" * 60)
    print("STATUS : GRAM SPECTRUM COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
