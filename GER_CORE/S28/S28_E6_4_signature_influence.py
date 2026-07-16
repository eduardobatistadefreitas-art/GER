"""
============================================================
RSG
S28-E6.4
Signature Influence Analysis
============================================================

Objective
---------
Quantify the influence of each signature on the global
spectral geometry of the current Reference Universe.

For each signature, remove it from the universe and
recompute the main spectral observables.

Computed quantities

    • Spectral Concentration Index (SCI)
    • Spectral Entropy
    • Effective Rank

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
    print("S28-E6.4")
    print("Signature Influence Analysis")
    print("=" * 60)
    print()


def spectral_statistics(X):

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

    sci0, ent0, rank0 = spectral_statistics(X)

    print("Reference Universe")
    print("-" * 60)
    print(f"SCI             : {sci0:.6f}")
    print(f"Entropy         : {ent0:.6f}")
    print(f"Effective Rank  : {rank0:.6f}")
    print()

    print("Leave-One-Out Analysis")
    print("-" * 60)

    print(
        f"{'Removed':<20}"
        f"{'SCI':>10}"
        f"{'ΔSCI':>12}"
        f"{'Eff.Rank':>14}"
    )

    print("-" * 60)

    influence = []

    for i, label in enumerate(labels):

        subset = np.delete(X, i, axis=0)

        sci, ent, rank = spectral_statistics(subset)

        delta = sci - sci0

        influence.append((label, abs(delta)))

        print(
            f"{label:<20}"
            f"{sci:>10.6f}"
            f"{delta:>12.6f}"
            f"{rank:>14.6f}"
        )

    print()

    influence.sort(key=lambda x: x[1], reverse=True)

    print("Influence Ranking")
    print("-" * 60)

    for i, (label, value) in enumerate(influence, start=1):

        print(
            f"{i:2d}. "
            f"{label:<20}"
            f"{value:.6f}"
        )

    print()

    print("=" * 60)
    print("STATUS : SIGNATURE INFLUENCE COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
