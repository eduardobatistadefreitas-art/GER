"""
============================================================
RSG
S28-E1.3
Minimum Spanning Tree
============================================================

Objective
---------
Construct the Minimum Spanning Tree (MST) of the current
Relational Signature Space.

The MST reveals the minimum set of metric connections
required to keep the Signature Space fully connected.

Computed quantities

    • Minimum Spanning Tree
    • Total Tree Weight
    • Vertex Degrees
    • Maximum Degree Vertices

============================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


# ============================================================
# Reference Signature Space
# ============================================================

SIGNATURES = {
    "Harmonic": (1.992115, 0.083005, 0.022109),
    "Damped": (1.999804, 0.618431, 0.027211),
    "Van der Pol": (1.560891, 0.291408, 0.035714),
    "Logistic": (0.010717, 0.003313, 1.000000),
    "Lorenz": (0.419313, 0.079386, 0.137755),
    "Double Pendulum": (1.301499, 0.388995, 0.069728),
}


# ============================================================
# Utilities
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E1.3")
    print("Minimum Spanning Tree")
    print("=" * 60)
    print()


def build_dataframe():

    return pd.DataFrame(
        list(SIGNATURES.values()),
        index=list(SIGNATURES.keys()),
        columns=[
            "Diameter",
            "Convergence",
            "Recurrence",
        ],
    )


# ============================================================
# Main
# ============================================================

def main():

    print_header()

    df = build_dataframe()

    print("Reference Signature Space")
    print("-" * 60)
    print(df)
    print()

    names = list(df.index)
    X = df.values

    distance_matrix = cdist(X, X)

    graph = nx.Graph()

    graph.add_nodes_from(names)

    for i in range(len(names)):
        for j in range(i + 1, len(names)):

            graph.add_edge(
                names[i],
                names[j],
                weight=float(distance_matrix[i, j]),
            )

    mst = nx.minimum_spanning_tree(
        graph,
        algorithm="kruskal",
        weight="weight",
    )

    edges = []
    total_weight = 0.0

    print("Minimum Spanning Tree")
    print("-" * 60)

    for u, v, data in mst.edges(data=True):

        w = float(data["weight"])

        total_weight += w

        edges.append(
            {
                "From": u,
                "To": v,
                "Distance": w,
            }
        )

        print(f"{u:20s} -- {v:20s} {w:.6f}")

    print()

    mst_df = pd.DataFrame(edges)

    print("Tree Summary")
    print("-" * 60)
    print(f"Vertices              : {mst.number_of_nodes()}")
    print(f"Edges                 : {mst.number_of_edges()}")
    print(f"Total weight          : {total_weight:.6f}")

    degrees = dict(mst.degree())

    print()
    print("Vertex Degrees")
    print("-" * 60)

    for node, degree in degrees.items():
        print(f"{node:20s} {degree}")

    max_degree = max(degrees.values())

    maximum_degree_vertices = [

        node

        for node, degree in degrees.items()

        if degree == max_degree

    ]

    print()
    print("Maximum Degree Vertices")
    print("-" * 60)

    for node in maximum_degree_vertices:
        print(node)

    results_dir = Path("RESULTS")
    results_dir.mkdir(exist_ok=True)

    mst_file = (
        results_dir /
        "S28_E1_3_minimum_spanning_tree.csv"
    )

    figure_file = (
        results_dir /
        "S28_E1_3_minimum_spanning_tree.png"
    )

    mst_df.to_csv(
        mst_file,
        index=False,
    )

    plt.figure(figsize=(8, 6))

    pos = nx.kamada_kawai_layout(
        mst,
        weight="weight",
    )

    nx.draw_networkx_nodes(
        mst,
        pos,
        node_size=900,
    )

    nx.draw_networkx_edges(
        mst,
        pos,
        width=2.5,
    )

    nx.draw_networkx_labels(
        mst,
        pos,
        font_size=9,
    )

    edge_labels = {

        (u, v): f"{d['weight']:.2f}"

        for u, v, d in mst.edges(data=True)

    }

    nx.draw_networkx_edge_labels(
        mst,
        pos,
        edge_labels=edge_labels,
        font_size=8,
    )

    plt.title("Minimum Spanning Tree")
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        figure_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print()
    print("Generated files")
    print("-" * 60)
    print(mst_file)
    print(figure_file)

    print()
    print("=" * 60)
    print("STATUS : MINIMUM SPANNING TREE GENERATED")
    print("=" * 60)


if __name__ == "__main__":
    main()
