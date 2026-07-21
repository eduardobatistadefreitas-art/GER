from pathlib import Path
import json

import networkx as nx
import numpy as np
import pandas as pd

# ============================================================
# INPUT DATA
# ============================================================

DATA_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
DATA_FILE = DATA_FOLDER / "observables.parquet"

print("=" * 60)
print("Loading dataset...")
print(DATA_FILE)

df = pd.read_parquet(DATA_FILE)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")
print("=" * 60)

# ============================================================
# RESULT FOLDER
# ============================================================

RESULT_FOLDER = DATA_FOLDER / "L8_CorrelationNetwork"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# PARAMETERS
# ============================================================

THRESHOLD = 0.80

# ============================================================
# CORRELATION MATRIX
# ============================================================

corr = df.corr(numeric_only=True).abs()

# ============================================================
# BUILD GRAPH
# ============================================================

G = nx.Graph()

for col in corr.columns:
    G.add_node(col)

cols = list(corr.columns)

for i in range(len(cols)):
    for j in range(i + 1, len(cols)):

        weight = corr.iloc[i, j]

        if weight >= THRESHOLD:

            G.add_edge(
                cols[i],
                cols[j],
                weight=float(weight)
            )

# ============================================================
# METRICS
# ============================================================

degree = dict(G.degree())

weighted_degree = dict(G.degree(weight="weight"))

betweenness = nx.betweenness_centrality(
    G,
    weight="weight"
)

closeness = nx.closeness_centrality(G)

eigenvector = nx.eigenvector_centrality(
    G,
    max_iter=500,
    weight="weight"
)

components = list(nx.connected_components(G))

# ============================================================
# NODE TABLE
# ============================================================

rows = []

for node in G.nodes():

    rows.append({

        "Observable": node,
        "Degree": degree[node],
        "WeightedDegree": weighted_degree[node],
        "Betweenness": betweenness[node],
        "Closeness": closeness[node],
        "Eigenvector": eigenvector[node]

    })

metrics = pd.DataFrame(rows)

metrics = metrics.sort_values(
    "Eigenvector",
    ascending=False
)

metrics.to_csv(
    RESULT_FOLDER / "network_metrics.csv",
    index=False
)

# ============================================================
# COMPONENTS
# ============================================================

component_rows = []

for i, comp in enumerate(components):

    component_rows.append({

        "Component": i + 1,
        "Size": len(comp),
        "Members": ", ".join(sorted(comp))

    })

component_df = pd.DataFrame(component_rows)

component_df.to_csv(
    RESULT_FOLDER / "components.csv",
    index=False
)

# ============================================================
# GRAPH EDGES
# ============================================================

edges = []

for u, v, d in G.edges(data=True):

    edges.append({

        "Node1": u,
        "Node2": v,
        "Weight": d["weight"]

    })

edges_df = pd.DataFrame(edges)

edges_df.to_csv(
    RESULT_FOLDER / "edges.csv",
    index=False
)

# ============================================================
# HUBS / PERIPHERAL
# ============================================================

hub = metrics.iloc[0]

peripheral = metrics.iloc[-1]

# ============================================================
# JSON
# ============================================================

with open(
    RESULT_FOLDER / "network_summary.json",
    "w"
) as f:

    json.dump({

        "Nodes": G.number_of_nodes(),
        "Edges": G.number_of_edges(),
        "Components": len(components),
        "Hub": hub["Observable"],
        "Peripheral": peripheral["Observable"]

    }, f, indent=4)

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "network_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L8\n")
    f.write("Correlation Network\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Threshold : {THRESHOLD}\n")
    f.write(f"Nodes     : {G.number_of_nodes()}\n")
    f.write(f"Edges     : {G.number_of_edges()}\n")
    f.write(f"Components: {len(components)}\n\n")

    f.write("Hub\n")
    f.write(f"{hub['Observable']}\n\n")

    f.write("Peripheral\n")
    f.write(f"{peripheral['Observable']}\n\n")

    f.write("Connected Components\n")

    for i, comp in enumerate(components):

        f.write(f"\nComponent {i+1}\n")

        for node in sorted(comp):

            f.write(f"   {node}\n")

# ============================================================
# CERTIFICATE
# ============================================================

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Observables : {G.number_of_nodes()}\n")
    f.write(f"Edges       : {G.number_of_edges()}\n")
    f.write(f"Components  : {len(components)}\n\n")

    f.write(f"Hub         : {hub['Observable']}\n")
    f.write(f"Peripheral  : {peripheral['Observable']}\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
