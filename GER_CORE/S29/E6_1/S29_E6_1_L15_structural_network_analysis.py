from pathlib import Path
import json

import networkx as nx
import numpy as np
import pandas as pd

# ============================================================
# GER
# S29-E6.1-L15
# Structural Network Analysis
# ============================================================

DATA_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
INPUT_FOLDER = DATA_FOLDER / "L14_PairStabilityAnalysis"

OUTPUT_FOLDER = DATA_FOLDER / "L15_StructuralNetwork"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GER")
print("S29-E6.1-L15")
print("Structural Network Analysis")
print("=" * 70)

matrix = pd.read_csv(
    INPUT_FOLDER / "pair_stability_matrix.csv",
    index_col=0
)

observables = list(matrix.index)

# ============================================================
# BUILD GRAPH
# ============================================================

G = nx.Graph()

for obs in observables:
    G.add_node(obs)

for i, a in enumerate(observables):

    for j in range(i + 1, len(observables)):

        b = observables[j]

        w = float(matrix.loc[a, b])

        if w > 0:

            G.add_edge(
                a,
                b,
                weight=w
            )

print(f"Nodes : {G.number_of_nodes()}")
print(f"Edges : {G.number_of_edges()}")

# ============================================================
# NETWORK SUMMARY
# ============================================================

weights = [
    d["weight"]
    for _, _, d in G.edges(data=True)
]

summary = pd.DataFrame({

    "Metric": [

        "Nodes",
        "Edges",
        "MeanWeight",
        "MinWeight",
        "MaxWeight",
        "Density"

    ],

    "Value": [

        G.number_of_nodes(),

        G.number_of_edges(),

        np.mean(weights),

        np.min(weights),

        np.max(weights),

        nx.density(G)

    ]

})

summary.to_csv(
    OUTPUT_FOLDER / "network_summary.csv",
    index=False
)

# ============================================================
# NODE METRICS
# ============================================================

degree = dict(nx.degree_centrality(G))

betweenness = nx.betweenness_centrality(
    G,
    weight="weight"
)

closeness = nx.closeness_centrality(G)

pagerank = nx.pagerank(
    G,
    weight="weight"
)

try:

    eigen = nx.eigenvector_centrality(
        G,
        weight="weight",
        max_iter=1000
    )

except Exception:

    eigen = {
        n: np.nan
        for n in G.nodes()
    }

rows = []

for node in G.nodes():

    rows.append({

        "Observable": node,

        "DegreeCentrality": degree[node],

        "Eigenvector": eigen[node],

        "Betweenness": betweenness[node],

        "Closeness": closeness[node],

        "PageRank": pagerank[node]

    })

metrics = pd.DataFrame(rows)

metrics = metrics.sort_values(
    "PageRank",
    ascending=False
)

metrics.to_csv(
    OUTPUT_FOLDER / "centrality_metrics.csv",
    index=False
)

# ============================================================
# EDGE LIST
# ============================================================

edges = []

for u, v, d in G.edges(data=True):

    edges.append({

        "Source": u,

        "Target": v,

        "Weight": d["weight"]

    })

pd.DataFrame(edges).to_csv(
    OUTPUT_FOLDER / "network_edges.csv",
    index=False
)

# ============================================================
# NODES
# ============================================================

pd.DataFrame({

    "Observable": observables

}).to_csv(
    OUTPUT_FOLDER / "network_nodes.csv",
    index=False
)

# ============================================================
# THRESHOLD SCAN
# ============================================================

thresholds = [
    0.20,
    0.40,
    0.60,
    0.80,
    0.90
]

rows = []

for t in thresholds:

    H = nx.Graph()

    H.add_nodes_from(G.nodes())

    for u, v, d in G.edges(data=True):

        if d["weight"] >= t:

            H.add_edge(
                u,
                v,
                weight=d["weight"]
            )

    comps = list(nx.connected_components(H))

    largest = max(
        (len(c) for c in comps),
        default=0
    )

    rows.append({

        "Threshold": t,

        "Edges": H.number_of_edges(),

        "Components": len(comps),

        "LargestComponent": largest,

        "Density": nx.density(H),

        "AverageDegree":

            np.mean([
                d
                for _, d in H.degree()
            ])

    })

threshold_df = pd.DataFrame(rows)

threshold_df.to_csv(
    OUTPUT_FOLDER / "threshold_scan.csv",
    index=False
)

# ============================================================
# MAXIMUM SPANNING TREE
# ============================================================

mst = nx.maximum_spanning_tree(
    G,
    weight="weight"
)

rows = []

for u, v, d in mst.edges(data=True):

    rows.append({

        "Source": u,

        "Target": v,

        "Weight": d["weight"]

    })

pd.DataFrame(rows).to_csv(
    OUTPUT_FOLDER / "maximum_spanning_tree.csv",
    index=False
)

# ============================================================
# COMMUNITIES
# ============================================================

from networkx.algorithms.community import greedy_modularity_communities

communities = list(
    greedy_modularity_communities(
        G,
        weight="weight"
    )
)

rows = []

for idx, c in enumerate(communities):

    for node in sorted(c):

        rows.append({

            "Community": idx,

            "Observable": node

        })

pd.DataFrame(rows).to_csv(
    OUTPUT_FOLDER / "communities.csv",
    index=False
)

# ============================================================
# BACKBONE
# ============================================================

rows = []

for u, v, d in G.edges(data=True):

    if d["weight"] >= 0.75:

        rows.append({

            "Source": u,

            "Target": v,

            "Weight": d["weight"]

        })

pd.DataFrame(rows).to_csv(
    OUTPUT_FOLDER / "backbone_edges.csv",
    index=False
)

# ============================================================
# REPORT
# ============================================================

with open(
    OUTPUT_FOLDER / "network_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L15\n")
    f.write("Structural Network Analysis\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Nodes : {G.number_of_nodes()}\n")
    f.write(f"Edges : {G.number_of_edges()}\n")
    f.write(f"Communities : {len(communities)}\n\n")

    f.write("Communities\n")
    f.write("-----------\n")

    for idx, c in enumerate(communities):

        f.write(
            f"C{idx}: "
            + ", ".join(sorted(c))
            + "\n"
        )

    f.write("\n")

    f.write("Top PageRank\n")
    f.write("------------\n")

    for _, row in metrics.head(10).iterrows():

        f.write(
            f"{row.Observable:20s}"
            f"{row.PageRank:.4f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

certificate = {

    "nodes": G.number_of_nodes(),

    "edges": G.number_of_edges(),

    "communities": len(communities),

    "maximum_spanning_tree_edges":

        mst.number_of_edges(),

    "backbone_edges":

        sum(
            1
            for _, _, d in G.edges(data=True)
            if d["weight"] >= 0.75
        ),

    "graph_connected":

        nx.is_connected(G)

}

with open(
    OUTPUT_FOLDER / "scientific_certificate.json",
    "w"
) as f:

    json.dump(
        certificate,
        f,
        indent=4
    )

print()
print("=" * 70)
print("Experiment completed.")
print("Results saved to:")
print(OUTPUT_FOLDER)
print("=" * 70)
