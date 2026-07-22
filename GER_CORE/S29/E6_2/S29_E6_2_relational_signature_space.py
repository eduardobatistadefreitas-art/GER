"""
============================================================
GER
S29-E6.2

Intrinsic Geometry of the Relational Signature Space

Main Experiment
============================================================

Pipeline

Load Signatures
        │
        ▼
SignatureCollection
        │
        ▼
Distance Matrix
        │
        ▼
Graph Construction
        │
        ▼
Topology Analysis
        │
        ▼
Statistical Analysis
        │
        ▼
Report Generation

Author : GER Project
"""

from __future__ import annotations

import numpy as np

from .config import Config
from . import io
from . import topology
from . import statistics
from . import report

from GER.CORE.GRAPH.graph import Graph
from GER.CORE.GRAPH.node import Node
from GER.CORE.GRAPH.edge import Edge


# ============================================================
# GRAPH CONSTRUCTION
# ============================================================

def build_graph(collection, threshold):
    """
    Build an undirected similarity graph from the
    SignatureCollection distance matrix.
    """

    distance = collection.distance_matrix()

    graph = Graph()

    graph_nodes = []

    for i, signature in enumerate(collection):

        node = Node(identifier=i)

        node.signature = signature

        graph.add_node(node)

        graph_nodes.append(node)

    n = len(graph_nodes)

    for i in range(n):

        for j in range(i + 1, n):

            if distance[i, j] <= threshold:

                graph.add_edge(
                    Edge(
                        graph_nodes[i],
                        graph_nodes[j],
                        weight=float(distance[i, j]),
                    )
                )

    return graph


# ============================================================
# MAIN PIPELINE
# ============================================================

def run(config: Config | None = None):

    if config is None:
        config = Config()

    print("=" * 60)
    print("GER")
    print("S29-E6.2")
    print("Intrinsic Geometry of the Relational Signature Space")
    print("=" * 60)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print("\nLoading signatures...")

    collection = io.load_signatures(config)

    print(f"Loaded signatures : {len(collection)}")

    # --------------------------------------------------------
    # Distance Matrix
    # --------------------------------------------------------

    print("Computing distance matrix...")

    distance_matrix = collection.distance_matrix()

    print(distance_matrix.shape)

    # --------------------------------------------------------
    # Graph
    # --------------------------------------------------------

    print("Building graph...")

    graph = build_graph(
        collection,
        config.graph_threshold,
    )

    print(f"Nodes : {graph.number_of_nodes()}")
    print(f"Edges : {graph.number_of_edges()}")

    # --------------------------------------------------------
    # Topology
    # --------------------------------------------------------

    print("Computing topology...")

    topology_results = topology.run(graph)

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print("Computing statistics...")

    statistics_results = statistics.run(
        collection,
        graph,
        topology_results,
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print("Generating report...")

    report.run(
        collection=collection,
        graph=graph,
        topology=topology_results,
        statistics=statistics_results,
        config=config,
    )

    print("\nExperiment completed.")

    return statistics_results


# ============================================================
# SCRIPT
# ============================================================

if __name__ == "__main__":

    run()
