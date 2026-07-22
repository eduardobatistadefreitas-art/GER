"""
============================================================
GER
S29-E6.2

Relational Signature Space

============================================================

Builds the Relational Signature Space using the
GER CORE infrastructure.

Pipeline

    Load Signatures
            │
            ▼
    Metric Space
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
            │
            ▼
    Persistent Storage

Author
------
Eduardo Batista de Freitas

Framework
---------
GER

Version
-------
1.0
"""

from __future__ import annotations

import time

from GER.CORE.ger_storage import ExperimentStorage
from GER.CORE.ger_dashboard import Dashboard

from GER.CORE.GRAPH.graph import Graph
from GER.CORE.GRAPH.node import Node
from GER.CORE.GRAPH.edge import Edge
from GER.CORE.bootstrap import initialize

from . import config
from . import io
from . import topology
from . import statistics
from . import report


# ============================================================
# GRAPH BUILDERS
# ============================================================

import numpy as np
from scipy.spatial import cKDTree


def build_radius_graph(collection, radius):

    graph = Graph()

    for i in range(len(collection)):
        graph.add_node(Node(str(i)))

    X = collection.to_numpy()

    tree = cKDTree(X)

    neighbours = tree.query_ball_point(
        X,
        r=radius,
    )

    for i, ids in enumerate(neighbours):

        for j in ids:

            if j <= i:
                continue

            d = np.linalg.norm(
                X[i] - X[j]
            )

            graph.add_edge(

                Edge(

                    str(i),

                    str(j),

                    weight=float(d),

                )

            )

    return graph


def build_knn_graph(collection, k):

    graph = Graph()

    for i in range(len(collection)):
        graph.add_node(Node(str(i)))

    X = collection.to_numpy()

    tree = cKDTree(X)

    distances, neighbours = tree.query(
        X,
        k=k + 1,
    )

    for i in range(len(collection)):

        for d, j in zip(
            distances[i][1:],
            neighbours[i][1:],
        ):

            graph.add_edge(

                Edge(

                    str(i),

                    str(j),

                    weight=float(d),

                )

            )

    return graph


def build_graph(collection):

    mode = config.GRAPH_MODE.lower()

    if mode == "radius":

        return build_radius_graph(

            collection,

            config.GRAPH_RADIUS,

        )

    if mode == "knn":

        return build_knn_graph(

            collection,

            config.GRAPH_K,

        )

    raise ValueError(

        f"Unknown GRAPH_MODE: {config.GRAPH_MODE}"

    )


# ============================================================
# MAIN
# ============================================================

def run():
    
    initialize()

    start = time.time()

    storage = ExperimentStorage(

        experiment="S29_E6_2",

        folders=[

            "report",

            "tables",

            "logs",

        ],

    )

    dashboard = Dashboard(

        title="GER",

        subtitle="S29-E6.2 Relational Signature Space",

    )

    # --------------------------------------------------------
    # Load Signatures
    # --------------------------------------------------------

    collection = io.load_signatures()

    dashboard.update(

        progress=1,

        total=5,

        elapsed=f"{time.time()-start:.1f}s",

        eta="...",

        sections={

            "Pipeline":{

                "Stage":"Load Signatures",

                "Items":len(collection),

            }

        },

    )

    # --------------------------------------------------------
    # Graph
    # --------------------------------------------------------

    graph = build_graph(collection)

    dashboard.update(

        progress=2,

        total=5,

        elapsed=f"{time.time()-start:.1f}s",

        eta="...",

        sections={

            "Graph":{

                "Nodes":graph.number_of_nodes(),

                "Edges":graph.number_of_edges(),

            }

        },

    )

    # --------------------------------------------------------
    # Topology
    # --------------------------------------------------------

    topo = topology.run(graph)

    dashboard.update(

        progress=3,

        total=5,

        elapsed=f"{time.time()-start:.1f}s",

        eta="...",

        sections={

            "Topology":{

                "Connected":topo.connectivity.connected,

                "Components":topo.connectivity.connected_components,

            }

        },

    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    stats = statistics.run(

        collection,

        graph,

        topo,

    )

    dashboard.update(

        progress=4,

        total=5,

        elapsed=f"{time.time()-start:.1f}s",

        eta="...",

        sections={

            "Statistics":{

                "Mean":f"{stats.distance.mean:.6f}",

                "Std":f"{stats.distance.std:.6f}",

            }

        },

    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    report.run(

        stats,

        storage,

    )

    elapsed = time.time() - start

    dashboard.finish(

        {

            "Execution":{

                "Experiment":"S29-E6.2",

                "Elapsed":f"{elapsed:.2f}s",

                "Signatures":stats.summary.signature_count,

                "Nodes":stats.summary.graph_nodes,

                "Edges":stats.summary.graph_edges,

            }

        }

    )

    return stats


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
