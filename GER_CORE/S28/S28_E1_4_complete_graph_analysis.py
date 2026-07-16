"""
============================================================
RSG
S28-E1.4
Complete Graph Analysis
============================================================

Objective
---------
Characterize the global metric structure of the complete
Relational Signature Space graph.

Computed quantities

    • Number of vertices
    • Number of edges
    • Graph density
    • Minimum edge length
    • Maximum edge length
    • Mean edge length
    • Standard deviation
    • Complete ranking of pairwise distances

============================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from GER_CORE.S28.signature_dataset import (
    names,
    distance_matrix,
)


# ============================================================
# Main
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E1.4")
    print("Complete Graph Analysis")
    print("=" * 60)
    print()


def main():

    print_header()

    labels = names()

    D = distance_matrix()

    edges = []

    for i in range(len(labels)):

        for j in range(i + 1, len(labels)):

            edges.append(

                (

                    labels[i],

                    labels[j],

                    float(D[i, j]),

                )

            )

    distances = np.array(

        [d for _, _, d in edges]

    )

    n = len(labels)

    m = len(edges)

    density = (2 * m) / (n * (n - 1))

    print("Complete Graph")
    print("-" * 60)

    print(f"Vertices              : {n}")
    print(f"Edges                 : {m}")
    print(f"Density               : {density:.6f}")

    print()

    print("Edge Statistics")
    print("-" * 60)

    print(f"Minimum distance      : {distances.min():.6f}")
    print(f"Maximum distance      : {distances.max():.6f}")
    print(f"Mean distance         : {distances.mean():.6f}")
    print(f"Std distance          : {distances.std():.6f}")

    print()

    print("Distance Ranking")
    print("-" * 60)

    ranking = sorted(

        edges,

        key=lambda x: x[2]

    )

    for a, b, d in ranking:

        print(

            f"{a:20s}"

            f"{b:20s}"

            f"{d:.6f}"

        )

    results = Path("RESULTS")
    results.mkdir(exist_ok=True)

    plt.figure(figsize=(7,5))

    plt.hist(
        distances,
        bins="auto",
    )

    plt.xlabel("Distance")

    plt.ylabel("Frequency")

    plt.title("Pairwise Distance Distribution")

    plt.tight_layout()

    plt.savefig(

        results /

        "S28_E1_4_distance_histogram.png",

        dpi=300,

        bbox_inches="tight",

    )

    plt.close()

    print()

    print("=" * 60)
    print("STATUS : COMPLETE GRAPH ANALYZED")
    print("=" * 60)


if __name__ == "__main__":

    main()
