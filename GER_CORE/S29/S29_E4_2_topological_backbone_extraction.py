# =====================================================================
# GER_CORE/S29/S29_E4_2_topological_backbone_extraction.py
# =====================================================================
#
# Project : GER — Geometria Espectral Relacional
#
# Experiment : S29-E4.2
#
# Title
# -----
# Topological Backbone Extraction
#
# Objective
# ---------
# Extract the intrinsic topological backbone of the Region Connectivity
# Graph generated in S29-E4.1.
#
# The original graph is complete (K_n), therefore its topology is
# dominated by geometric completeness rather than structural relevance.
#
# This experiment builds several reduced representations preserving the
# most meaningful geometric relations.
#
# Implemented Backbones
# ---------------------
#
# 1. Minimum Spanning Tree (MST)
#
# 2. k-Nearest Neighbor Graph
#
# 3. Threshold Graph
#
# 4. Consensus Backbone
#
# Input
# -----
#
# /content/drive/MyDrive/GER_RESULTS/S29_E4.1/
#
#     s29_e4_1_connectivity_graph.graphml
#
# Output
# ------
#
# /content/drive/MyDrive/GER_RESULTS/S29_E4.2/
#
#     mst.graphml
#     knn.graphml
#     threshold.graphml
#     consensus.graphml
#
#     mst.png
#     knn.png
#     threshold.png
#     consensus.png
#
#     topology_metrics.json
#     backbone_summary.csv
#
# =====================================================================

import os
import json
import math

import networkx as nx
import pandas as pd

import matplotlib.pyplot as plt


# =====================================================================
# CONFIGURATION
# =====================================================================

INPUT_DIR = "/content/drive/MyDrive/GER_RESULTS/S29_E4.1"

RESULTS_DIR = "/content/drive/MyDrive/GER_RESULTS/S29_E4.2"

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)

GRAPH_FILE = os.path.join(

    INPUT_DIR,

    "s29_e4_1_connectivity_graph.graphml"

)

K_NEIGHBORS = 2

THRESHOLD_PERCENTILE = 25.0


# =====================================================================
# LOAD GRAPH
# =====================================================================

def load_graph():

    graph = nx.read_graphml(GRAPH_FILE)

    for u, v, data in graph.edges(data=True):

        data["weight"] = float(data["weight"])

        data["distance"] = float(data["distance"])

    return graph


# =====================================================================
# GRAPH COPY
# =====================================================================

def clone_graph_structure(graph):

    new_graph = nx.Graph()

    for node, attributes in graph.nodes(data=True):

        new_graph.add_node(

            node,

            **attributes

        )

    return new_graph


# =====================================================================
# SAVE GRAPHML
# =====================================================================

def save_graph(graph, filename):

    nx.write_graphml(

        graph,

        os.path.join(

            RESULTS_DIR,

            filename

        )

    )


# =====================================================================
# SAVE FIGURE
# =====================================================================

def draw_graph(

    graph,

    filename,

    title

):

    plt.figure(figsize=(10,8))

    position = nx.spring_layout(

        graph,

        weight="weight",

        seed=42

    )

    widths = []

    weights = [

        graph[u][v]["weight"]

        for u,v in graph.edges()

    ]

    if len(weights) == 0:

        widths = []

    else:

        minimum = min(weights)

        maximum = max(weights)

        if math.isclose(

            minimum,

            maximum

        ):

            widths = [

                2.0

                for _ in weights

            ]

        else:

            widths = [

                1.0 +

                4.0 *

                (maximum-w)

                /

                (maximum-minimum)

                for w in weights

            ]

    nx.draw_networkx_nodes(

        graph,

        position,

        node_size=900

    )

    nx.draw_networkx_edges(

        graph,

        position,

        width=widths

    )

    nx.draw_networkx_labels(

        graph,

        position,

        font_size=10,

        font_weight="bold"

    )

    plt.title(title)

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            RESULTS_DIR,

            filename

        ),

        dpi=300,

        bbox_inches="tight"

    )

    plt.close()


# =====================================================================
# MINIMUM SPANNING TREE
# =====================================================================

def build_mst(graph):

    mst = nx.minimum_spanning_tree(

        graph,

        weight="weight"

    )

    return mst


# =====================================================================
# K-NEAREST NEIGHBOR GRAPH
# =====================================================================

def build_knn(graph):

    knn = clone_graph_structure(graph)

    for node in graph.nodes():

        edges = []

        for neighbor in graph.neighbors(node):

            distance = graph[node][neighbor]["weight"]

            edges.append(

                (

                    distance,

                    node,

                    neighbor

                )

            )

        edges.sort()

        for edge in edges[:K_NEIGHBORS]:

            _, u, v = edge

            if not knn.has_edge(u, v):

                knn.add_edge(

                    u,

                    v,

                    **graph[u][v]

                )

    return knn
  # =====================================================================
# THRESHOLD GRAPH
# =====================================================================

def build_threshold_graph(graph):

    threshold = clone_graph_structure(graph)

    distances = [

        graph[u][v]["weight"]

        for u, v in graph.edges()

    ]

    dataframe = pd.Series(distances)

    cutoff = dataframe.quantile(

        THRESHOLD_PERCENTILE / 100.0

    )

    for u, v, data in graph.edges(data=True):

        if data["weight"] <= cutoff:

            threshold.add_edge(

                u,

                v,

                **data

            )

    return threshold


# =====================================================================
# CONSENSUS BACKBONE
# =====================================================================

def build_consensus_backbone(

    mst,

    knn,

    threshold,

    reference_graph

):

    consensus = clone_graph_structure(

        reference_graph

    )

    for source, target in reference_graph.edges():

        present = 0

        if mst.has_edge(source, target):

            present += 1

        if knn.has_edge(source, target):

            present += 1

        if threshold.has_edge(source, target):

            present += 1

        if present >= 2:

            consensus.add_edge(

                source,

                target,

                **reference_graph[source][target]

            )

    return consensus


# =====================================================================
# BASIC METRICS
# =====================================================================

def graph_metrics(

    graph,

    name

):

    metrics = {}

    metrics["graph"] = name

    metrics["nodes"] = graph.number_of_nodes()

    metrics["edges"] = graph.number_of_edges()

    metrics["density"] = nx.density(graph)

    metrics["connected"] = nx.is_connected(graph)

    metrics["components"] = nx.number_connected_components(graph)

    metrics["average_degree"] = (

        sum(

            dict(

                graph.degree()

            ).values()

        )

        /

        graph.number_of_nodes()

    )

    return metrics


# =====================================================================
# DEGREE TABLE
# =====================================================================

def node_degree_table(graph):

    rows = []

    weighted_degree = dict(

        graph.degree(

            weight="weight"

        )

    )

    degree = dict(

        graph.degree()

    )

    for node in graph.nodes():

        rows.append(

            {

                "Region": node,

                "Degree": degree[node],

                "WeightedDegree":

                    weighted_degree[node]

            }

        )

    return pd.DataFrame(rows)


# =====================================================================
# CENTRALITIES
# =====================================================================

def compute_centralities(graph):

    results = {}

    results["degree"] = nx.degree_centrality(

        graph

    )

    results["betweenness"] = nx.betweenness_centrality(

        graph,

        weight="weight"

    )

    results["closeness"] = nx.closeness_centrality(

        graph,

        distance="weight"

    )

    try:

        results["eigenvector"] = nx.eigenvector_centrality(

            graph,

            weight="weight",

            max_iter=1000

        )

    except Exception:

        results["eigenvector"] = {

            node: 0.0

            for node in graph.nodes()

        }

    try:

        results["pagerank"] = nx.pagerank(

            graph,

            weight="weight"

        )

    except Exception:

        results["pagerank"] = {

            node: 0.0

            for node in graph.nodes()

        }

    return results


# =====================================================================
# CENTRALITY TABLE
# =====================================================================

def centrality_dataframe(

    graph,

    centralities

):

    rows = []

    for node in graph.nodes():

        rows.append(

            {

                "Region": node,

                "Degree":

                    centralities["degree"][node],

                "Betweenness":

                    centralities["betweenness"][node],

                "Closeness":

                    centralities["closeness"][node],

                "Eigenvector":

                    centralities["eigenvector"][node],

                "PageRank":

                    centralities["pagerank"][node]

            }

        )

    return pd.DataFrame(rows)


# =====================================================================
# TOPOLOGICAL FEATURES
# =====================================================================

def compute_topological_features(

    graph

):

    report = {}

    report["bridges"] = list(

        nx.bridges(graph)

    )

    report["articulation_points"] = list(

        nx.articulation_points(graph)

    )

    report["connected_components"] = [

        sorted(list(component))

        for component

        in nx.connected_components(

            graph

        )

    ]

    try:

        report["eccentricity"] = nx.eccentricity(

            graph

        )

    except Exception:

        report["eccentricity"] = {}

    try:

        report["clustering"] = nx.clustering(

            graph,

            weight="weight"

        )

    except Exception:

        report["clustering"] = {}

    return report
  # =====================================================================
# SAVE TABLES
# =====================================================================

def export_results(
    name,
    graph
):

    metrics = graph_metrics(
        graph,
        name
    )

    degree_table = node_degree_table(
        graph
    )

    centralities = compute_centralities(
        graph
    )

    centrality_table = centrality_dataframe(
        graph,
        centralities
    )

    topology = compute_topological_features(
        graph
    )

    degree_table.to_csv(

        os.path.join(
            RESULTS_DIR,
            f"{name}_degrees.csv"
        ),

        index=False

    )

    centrality_table.to_csv(

        os.path.join(
            RESULTS_DIR,
            f"{name}_centralities.csv"
        ),

        index=False

    )

    with open(

        os.path.join(
            RESULTS_DIR,
            f"{name}_topology.json"
        ),

        "w",
        encoding="utf-8"

    ) as f:

        json.dump(

            topology,

            f,

            indent=4

        )

    return metrics


# =====================================================================
# GLOBAL SUMMARY
# =====================================================================

def build_summary(metrics):

    dataframe = pd.DataFrame(metrics)

    dataframe.to_csv(

        os.path.join(

            RESULTS_DIR,

            "backbone_summary.csv"

        ),

        index=False

    )

    with open(

        os.path.join(

            RESULTS_DIR,

            "topology_metrics.json"

        ),

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            metrics,

            f,

            indent=4

        )


# =====================================================================
# REPORT
# =====================================================================

def print_report(metrics):

    print()
    print("=" * 70)
    print("GER")
    print("S29-E4.2")
    print("TOPOLOGICAL BACKBONE EXTRACTION")
    print("=" * 70)
    print()

    for item in metrics:

        print(
            f"{item['graph']:12s}"
            f" Nodes={item['nodes']:2d}"
            f" Edges={item['edges']:2d}"
            f" Density={item['density']:.4f}"
            f" Connected={item['connected']}"
        )

    print()
    print("Results saved to:")
    print(RESULTS_DIR)
    print()
    print("=" * 70)


# =====================================================================
# MAIN
# =====================================================================

def main():

    print("=" * 70)
    print("GER")
    print("S29-E4.2")
    print("Topological Backbone Extraction")
    print("=" * 70)
    print()

    graph = load_graph()

    print(
        f"Reference graph : {graph.number_of_nodes()} regions"
    )

    print(
        f"Edges           : {graph.number_of_edges()}"
    )

    print()

    mst = build_mst(graph)

    knn = build_knn(graph)

    threshold = build_threshold_graph(graph)

    consensus = build_consensus_backbone(

        mst,

        knn,

        threshold,

        graph

    )

    save_graph(
        mst,
        "mst.graphml"
    )

    save_graph(
        knn,
        "knn.graphml"
    )

    save_graph(
        threshold,
        "threshold.graphml"
    )

    save_graph(
        consensus,
        "consensus.graphml"
    )

    draw_graph(
        mst,
        "mst.png",
        "Minimum Spanning Tree"
    )

    draw_graph(
        knn,
        "knn.png",
        "k-Nearest Neighbor Graph"
    )

    draw_graph(
        threshold,
        "threshold.png",
        "Threshold Graph"
    )

    draw_graph(
        consensus,
        "consensus.png",
        "Consensus Backbone"
    )

    metrics = []

    metrics.append(

        export_results(
            "mst",
            mst
        )

    )

    metrics.append(

        export_results(
            "knn",
            knn
        )

    )

    metrics.append(

        export_results(
            "threshold",
            threshold
        )

    )

    metrics.append(

        export_results(
            "consensus",
            consensus
        )

    )

    build_summary(metrics)

    print_report(metrics)


# =====================================================================
# ENTRY POINT
# =====================================================================

if __name__ == "__main__":

    main()
