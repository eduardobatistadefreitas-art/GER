"""
============================================================
RSG
S28-E1.2
Neighborhood Graph of the Relational Signature Space
============================================================

Objective
---------
Construct the nearest-neighbour graph induced by the metric
of the Relational Signature Space.

For each Geometric Signature, connect it to its nearest
neighbour according to the Euclidean metric.

This experiment investigates the local organization of the
Signature Space without introducing any machine learning or
graph optimization.

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
# Header
# ============================================================

def print_header():

    print("=" * 60)
    print("RSG")
    print("S28-E1.2")
    print("Neighborhood Graph")
    print("=" * 60)
    print()


# ============================================================
# Dataset
# ============================================================

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

    X = df.values

    D = cdist(X, X)

    names = list(df.index)

    graph = nx.DiGraph()

    graph.add_nodes_from(names)

    nearest = []

    for i, name in enumerate(names):

        row = D[i].copy()
        row[i] = np.inf

        j = np.argmin(row)

        neighbour = names[j]
        distance = D[i, j]

        graph.add_edge(name, neighbour, weight=distance)

        nearest.append(
            {
                "Signature": name,
                "Nearest": neighbour,
                "Distance": distance,
            }
        )

    nearest_df = pd.DataFrame(nearest)

    print("Nearest Neighbours")
    print("-" * 60)

    for row in nearest:

        print(
            f"{row['Signature']:20s} -> "
            f"{row['Nearest']:20s} "
            f"{row['Distance']:.6f}"
        )

    print()

    reciprocal = []

    for u, v in graph.edges():

        if graph.has_edge(v, u):

            pair = tuple(sorted((u, v)))

            if pair not in reciprocal:
                reciprocal.append(pair)

    undirected = graph.to_undirected()

    connected = nx.is_connected(undirected)

    isolated = [
        node
        for node in graph.nodes()
        if graph.in_degree(node) == 0
    ]

    print("Graph Summary")
    print("-" * 60)

    print(f"Vertices              : {graph.number_of_nodes()}")
    print(f"Edges                 : {graph.number_of_edges()}")
    print(f"Reciprocal pairs      : {len(reciprocal)}")
    print(f"Connected             : {connected}")

    if isolated:
        print("Isolated vertices     :")
        for node in isolated:
            print(f"  {node}")
    else:
        print("Isolated vertices     : None")

    results = Path("RESULTS")
    results.mkdir(exist_ok=True)

    nearest_df.to_csv(
        results / "S28_E1_2_nearest_neighbors.csv",
        index=False,
    )

    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(
        graph,
        seed=42,
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=900,
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        font_size=9,
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        width=1.8,
    )

    plt.title("Nearest-Neighbour Graph")
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        results / "S28_E1_2_neighborhood_graph.png",
        dpi=300,
    )

    plt.close()

    print()
    print("Generated files")
    print("-" * 60)
    print("RESULTS/S28_E1_2_nearest_neighbors.csv")
    print("RESULTS/S28_E1_2_neighborhood_graph.png")

    print()
    print("=" * 60)
    print("STATUS : NEIGHBORHOOD GRAPH GENERATED")
    print("=" * 60)


if __name__ == "__main__":
    main()
