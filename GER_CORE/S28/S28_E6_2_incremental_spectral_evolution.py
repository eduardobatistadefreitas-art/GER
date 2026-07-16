"""
============================================================
RSG
S28-E6.2
Incremental Spectral Evolution
============================================================

Objective
---------
Investigate how the spectral properties of the Relational
Signature Space evolve as new signatures are progressively
incorporated into the Reference Universe.

Computed quantities

    • Spectral Concentration Index (SCI)
    • Effective Rank
    • Spectral Entropy

for every incremental universe.

============================================================
"""

import numpy as np

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
    print("S28-E6.2")
    print("Incremental Spectral Evolution")
    print("=" * 60)
    print()


def spectrum_statistics(X):

    centroid = X.mean(axis=0)
    Xc = X - centroid

    G = Xc @ Xc.T

    eig = np.linalg.eigvalsh(G)
    eig = np.sort(eig)[::-1]

    eig = eig[eig > 1e-12]

    energy = eig / eig.sum()

    sci = energy[0]

    entropy = -np.sum(
        energy * np.log(energy)
    )

    effective_rank = np.exp(entropy)

    return sci, entropy, effective_rank


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    labels = names()
    X = vectors()

    print("Incremental Evolution")
    print("-" * 60)

    print(
        f"{'Universe':<12}"
        f"{'SCI':>12}"
        f"{'Entropy':>14}"
        f"{'Eff.Rank':>14}"
    )

    print("-" * 60)

    for n in range(2, len(labels)+1):

        sci, entropy, rank = spectrum_statistics(
            X[:n]
        )

        print(
            f"{n:<12}"
            f"{sci:>12.6f}"
            f"{entropy:>14.6f}"
            f"{rank:>14.6f}"
        )

    print()

    print("=" * 60)
    print("STATUS : SPECTRAL EVOLUTION COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
