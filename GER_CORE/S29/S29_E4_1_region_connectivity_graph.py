# =====================================================================
# GER_CORE/S29/S29_E4_1_region_connectivity_graph.py
# =====================================================================
#
# Project : GER — Geometria Espectral Relacional
# Experiment : S29-E4.1
#
# Title:
# Region Connectivity Graph
#
# Objective
# ---------
# Build the weighted connectivity graph between Stability Regions using
# the geometric database produced by S29-E3.
#
# Input
# -----
# GER_CORE/S29/geometric_database/
#
#     s29_e3_2_stability_regions.json
#     s29_e3_3_region_geometry.json
#     s29_e3_3_region_distance_matrix.json
#
# Output
# ------
# /content/drive/MyDrive/GER_RESULTS/S29_E4.1/
#
#     s29_e4_1_connectivity_graph.graphml
#     s29_e4_1_edge_list.csv
#     s29_e4_1_node_table.csv
#     s29_e4_1_adjacency_matrix.csv
#     s29_e4_1_metrics_summary.json
#     s29_e4_1_network.png
#
# =====================================================================

import os
import json
import math

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# =====================================================================
# CONFIGURATION
# =====================================================================

DATABASE_DIR = "GER_CORE/S29/geometric_database"

REGIONS_FILE = os.path.join(
    DATABASE_DIR,
    "s29_e3_2_stability_regions.json"
)

GEOMETRY_FILE = os.path.join(
    DATABASE_DIR,
    "s29_e3_3_region_geometry.json"
)

DISTANCE_FILE = os.path.join(
    DATABASE_DIR,
    "s29_e3_3_region_distance_matrix.json"
)

RESULTS_DIR = "/content/drive/MyDrive/GER_RESULTS/S29_E4.1"

os.makedirs(RESULTS_DIR, exist_ok=True)


# =====================================================================
# LOAD JSON
# =====================================================================

def load_json(filename):

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================================
# LOAD DATABASE
# =====================================================================

def load_database():

    regions = load_json(REGIONS_FILE)

    geometry = load_json(GEOMETRY_FILE)

    distance_matrix = load_json(DISTANCE_FILE)

    return regions, geometry, distance_matrix


# =====================================================================
# BUILD GRAPH
# =====================================================================

def build_graph(regions, geometry, distance_matrix):

    graph = nx.Graph()

    geometry_lookup = {
        g["Region"]: g
        for g in geometry
    }

    region_lookup = {}

    for region in regions:

        region_name = region["classification"]

        region_lookup[region_name] = region

    # --------------------------------------------------------------
    # Nodes
    # --------------------------------------------------------------

    for region_name in geometry_lookup:

        g = geometry_lookup[region_name]
        r = region_lookup[region_name]

        graph.add_node(

            region_name,

            region_id=r["region_id"],

            gamma_start=r["gamma_start"],
            gamma_end=r["gamma_end"],
            delta_gamma=r["length"],

            centroid_diameter=g["CentroidDiameter"],
            centroid_convergence=g["CentroidConvergence"],
            centroid_recurrence=g["CentroidRecurrence"],
            centroid_drift=g["CentroidDrift"],

            mean_radius=g["MeanRadius"],
            internal_diameter=g["InternalDiameter"],

            compactness=g["Compactness"],
            packing=g["Packing"],

            anisotropy=g["Anisotropy"],
            uniformity=g["Uniformity"],

            nearest_region_distance=g["NearestRegionDistance"],
            farthest_region_distance=g["FarthestRegionDistance"],
            separation_ratio=g["SeparationRatio"]

        )

    # --------------------------------------------------------------
    # Edges
    # --------------------------------------------------------------

    for row in distance_matrix:

        source = row["Region"]

        for target, distance in row.items():

            if target == "Region":
                continue

            if source == target:
                continue

            if graph.has_edge(source, target):
                continue

            graph.add_edge(

                source,

                target,

                distance=float(distance),

                weight=float(distance)

            )

    return graph


# =====================================================================
# NODE TABLE
# =====================================================================

def save_node_table(graph):

    rows = []

    for node, attributes in graph.nodes(data=True):

        row = {"Region": node}

        row.update(attributes)

        rows.append(row)

    dataframe = pd.DataFrame(rows)

    filename = os.path.join(
        RESULTS_DIR,
        "s29_e4_1_node_table.csv"
    )

    dataframe.to_csv(filename, index=False)

    return dataframe


# =====================================================================
# EDGE TABLE
# =====================================================================

def save_edge_table(graph):

    rows = []

    for source, target, attributes in graph.edges(data=True):

        rows.append(

            {

                "Source": source,

                "Target": target,

                "Distance": attributes["distance"],

                "Weight": attributes["weight"]

            }

        )

    dataframe = pd.DataFrame(rows)

    filename = os.path.join(
        RESULTS_DIR,
        "s29_e4_1_edge_list.csv"
    )

    dataframe.to_csv(filename, index=False)

    return dataframe


# =====================================================================
# ADJACENCY MATRIX
# =====================================================================

def save_adjacency_matrix(graph):

    matrix = nx.to_pandas_adjacency(

        graph,

        weight="weight"

    )

    filename = os.path.join(

        RESULTS_DIR,

        "s29_e4_1_adjacency_matrix.csv"

    )

    matrix.to_csv(filename)

    return matrix


# =====================================================================
# GRAPHML
# =====================================================================

def save_graphml(graph):

    filename = os.path.join(

        RESULTS_DIR,

        "s29_e4_1_connectivity_graph.graphml"

    )

    nx.write_graphml(

        graph,

        filename

    )


# =====================================================================
# GRAPH STATISTICS
# =====================================================================

def compute_statistics(graph):

    weights = [

        edge["weight"]

        for _, _, edge

        in graph.edges(data=True)

    ]

    statistics = {

        "project": "GER",

        "experiment": "S29-E4.1",

        "title": "REGION CONNECTIVITY GRAPH",

        "regions": graph.number_of_nodes(),

        "edges": graph.number_of_edges(),

        "graph_type": "weighted_complete_graph",

        "connected": nx.is_connected(graph),

        "weighted": True,

        "undirected": True,

        "density": nx.density(graph),

        "average_edge_weight": sum(weights) / len(weights),

        "minimum_edge_weight": min(weights),

        "maximum_edge_weight": max(weights)

    }

    filename = os.path.join(

        RESULTS_DIR,

        "s29_e4_1_metrics_summary.json"

    )

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            statistics,

            f,

            indent=4

        )

    return statistics
  # =====================================================================
# NETWORK VISUALIZATION
# =====================================================================

def save_network_plot(graph):

    plt.figure(figsize=(10, 8))

    position = nx.spring_layout(
        graph,
        weight="weight",
        seed=42
    )

    weights = [
        graph[u][v]["weight"]
        for u, v in graph.edges()
    ]

    min_weight = min(weights)
    max_weight = max(weights)

    if math.isclose(max_weight, min_weight):

        edge_widths = [2.0 for _ in weights]

    else:

        edge_widths = [

            1.0
            + 4.0
            * (max_weight - w)
            / (max_weight - min_weight)

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
        width=edge_widths
    )

    nx.draw_networkx_labels(
        graph,
        position,
        font_size=10,
        font_weight="bold"
    )

    plt.title(
        "S29-E4.1\nRegion Connectivity Graph",
        fontsize=14
    )

    plt.axis("off")

    plt.tight_layout()

    filename = os.path.join(
        RESULTS_DIR,
        "s29_e4_1_network.png"
    )

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# =====================================================================
# REPORT
# =====================================================================

def print_report(statistics):

    print()
    print("=" * 68)
    print("GER")
    print("S29-E4.1")
    print("REGION CONNECTIVITY GRAPH")
    print("=" * 68)
    print()

    print(f"Regions              : {statistics['regions']}")
    print(f"Edges                : {statistics['edges']}")
    print(f"Connected            : {statistics['connected']}")
    print(f"Weighted             : {statistics['weighted']}")
    print(f"Undirected           : {statistics['undirected']}")
    print()

    print(f"Density              : {statistics['density']:.6f}")
    print(f"Average Weight       : {statistics['average_edge_weight']:.6f}")
    print(f"Minimum Weight       : {statistics['minimum_edge_weight']:.6f}")
    print(f"Maximum Weight       : {statistics['maximum_edge_weight']:.6f}")

    print()
    print("Results saved to:")
    print(RESULTS_DIR)
    print()
    print("=" * 68)


# =====================================================================
# MAIN
# =====================================================================

def main():

    print("=" * 68)
    print("GER")
    print("S29-E4.1")
    print("Loading geometric database...")
    print("=" * 68)
    print()

    regions, geometry, distance_matrix = load_database()

    graph = build_graph(
        regions,
        geometry,
        distance_matrix
    )

    print(
        f"Regions loaded : {graph.number_of_nodes()}"
    )

    print(
        f"Edges created  : {graph.number_of_edges()}"
    )

    print()

    save_node_table(graph)

    save_edge_table(graph)

    save_adjacency_matrix(graph)

    save_graphml(graph)

    save_network_plot(graph)

    statistics = compute_statistics(graph)

    print_report(statistics)


# =====================================================================
# ENTRY POINT
# =====================================================================

if __name__ == "__main__":

    main()
