"""
============================================================
RSG
S28-E6.5
Geometric Influence Network
============================================================

Objective
---------
Construct the Geometric Influence Network of the current
Reference Universe.

Each node represents one Geometric Signature.

The node influence is measured through the variation of the
Spectral Concentration Index (SCI) after removing that
signature from the universe.

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
    print("S28-E6.5")
    print("Geometric Influence Network")
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

    labels = names()
    X = vectors()

    sci_reference = spectral_concentration(X)

    influence = []

    for i, label in enumerate(labels):

        subset = np.delete(
            X,
            i,
            axis=0,
        )

        sci = spectral_concentration(subset)

        delta = sci - sci_reference

        influence.append(
            (
                label,
                delta,
            )
        )

    influence.sort(
        key=lambda x: abs(x[1]),
        reverse=True,
    )

    total = sum(abs(v) for _, v in influence)

    print("Influence Network")
    print("-" * 60)

    print(
        f"{'Signature':20s}"
        f"{'ΔSCI':>12}"
        f"{'Contribution':>16}"
    )

    print("-" * 60)

    for label, delta in influence:

        contribution = abs(delta) / total

        print(
            f"{label:20s}"
            f"{delta:12.6f}"
            f"{100*contribution:15.2f}%"
        )

    print()

    print("Global Summary")
    print("-" * 60)

    print(f"Reference SCI      : {sci_reference:.6f}")

    print(f"Total influence    : {total:.6f}")

    print()

    print("Most influential signature")
    print("-" * 60)

    print(influence[0][0])

    print()

    print("=" * 60)
    print("STATUS : GEOMETRIC INFLUENCE NETWORK COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
