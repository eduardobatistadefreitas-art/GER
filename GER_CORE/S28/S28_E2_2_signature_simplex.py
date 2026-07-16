"""
============================================================
RSG
S28-E2.2
Signature Simplex
============================================================

Objective
---------
Investigate the geometric occupancy of the current
Relational Signature Space by constructing its Convex Hull.

Computed quantities

    • Convex Hull vertices
    • Hull volume
    • Hull surface area
    • Interior signatures

============================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.spatial import ConvexHull

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
    print("S28-E2.2")
    print("Signature Simplex")
    print("=" * 60)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    labels = names()
    X = vectors()

    hull = ConvexHull(X)

    hull_vertices = sorted(hull.vertices.tolist())

    hull_names = [labels[i] for i in hull_vertices]

    interior = [
        labels[i]
        for i in range(len(labels))
        if i not in hull_vertices
    ]

    print("Convex Hull")
    print("-" * 60)
    print(f"Dimension             : {X.shape[1]}")
    print(f"Hull vertices         : {len(hull_vertices)}")
    print(f"Interior signatures   : {len(interior)}")
    print()

    print("Hull Vertices")
    print("-" * 60)

    for name in hull_names:
        print(name)

    print()

    print("Interior Signatures")
    print("-" * 60)

    if interior:
        for name in interior:
            print(name)
    else:
        print("None")

    print()

    print("Geometric Properties")
    print("-" * 60)
    print(f"Hull volume           : {hull.volume:.6f}")
    print(f"Hull surface area     : {hull.area:.6f}")

    results = Path("RESULTS")
    results.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(
        X[:, 0],
        X[:, 1],
        X[:, 2],
        s=70,
    )

    for i, label in enumerate(labels):
        ax.text(
            X[i, 0],
            X[i, 1],
            X[i, 2],
            label,
            fontsize=8,
        )

    for simplex in hull.simplices:

        simplex = np.append(simplex, simplex[0])

        ax.plot(
            X[simplex, 0],
            X[simplex, 1],
            X[simplex, 2],
            linewidth=1.2,
        )

    ax.set_xlabel("Diameter")
    ax.set_ylabel("Convergence")
    ax.set_zlabel("Recurrence")

    plt.tight_layout()

    plt.savefig(
        results / "S28_E2_2_signature_simplex.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print()
    print("=" * 60)
    print("STATUS : SIGNATURE SIMPLEX COMPUTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
