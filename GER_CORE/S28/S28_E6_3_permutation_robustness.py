"""
============================================================
RSG
S28-E6.3
Permutation Robustness
============================================================

Objective
---------
Investigate whether the spectral evolution of the Reference
Universe depends on the order in which signatures are added.

For many random permutations of the current Reference
Universe, compute the Spectral Concentration Index (SCI)
during incremental growth.

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
    print("S28-E6.3")
    print("Permutation Robustness")
    print("=" * 60)
    print()


def spectral_concentration(X):

    centroid = X.mean(axis=0)

    Xc = X - centroid

    G = Xc @ Xc.T

    eig = np.linalg.eigvalsh(G)

    eig = np.sort(eig)[::-1]

    eig = eig[eig > 1e-12]

    energy = eig / eig.sum()

    return energy[0]


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    X = vectors()

    rng = np.random.default_rng(seed=42)

    permutations = 1000

    sizes = range(2, len(X) + 1)

    print("Running permutations...")
    print()

    results = {}

    for n in sizes:

        sci = []

        for _ in range(permutations):

            idx = rng.permutation(len(X))

            subset = X[idx[:n]]

            sci.append(
                spectral_concentration(subset)
            )

        results[n] = np.array(sci)

    print("Spectral Concentration Statistics")
    print("-" * 60)

    print(
        f"{'N':<6}"
        f"{'Mean SCI':>12}"
        f"{'Std':>12}"
        f"{'Minimum':>12}"
        f"{'Maximum':>12}"
    )

    print("-" * 60)

    for n in sizes:

        r = results[n]

        print(
            f"{n:<6}"
            f"{r.mean():>12.6f}"
            f"{r.std():>12.6f}"
            f"{r.min():>12.6f}"
            f"{r.max():>12.6f}"
        )

    print()

    print("=" * 60)
    print("STATUS : PERMUTATION ROBUSTNESS COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
