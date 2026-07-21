from pathlib import Path
import json

import numpy as np
import pandas as pd
import networkx as nx
from sklearn.linear_model import LinearRegression

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

RESULT_FOLDER = DATA_FOLDER / "L12_ObservableHierarchy"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

columns = list(df.columns)

# ============================================================
# INFLUENCE MATRIX
# ============================================================

print("=" * 70)
print("OBSERVABLE HIERARCHY")
print("=" * 70)

influence = pd.DataFrame(
    np.zeros((len(columns), len(columns))),
    index=columns,
    columns=columns
)

for source in columns:

    X = df[[source]]

    for target in columns:

        if source == target:
            continue

        y = df[target]

        model = LinearRegression()

        model.fit(X, y)

        influence.loc[source, target] = model.score(X, y)

# ============================================================
# BUILD DIRECTED GRAPH
# ============================================================

G = nx.DiGraph()

for c in columns:
    G.add_node(c)

EDGE_THRESHOLD = 0.80
DELTA = 0.05

for i in columns:

    for j in columns:

        if i == j:
            continue

        rij = influence.loc[i, j]
        rji = influence.loc[j, i]

        if rij >= EDGE_THRESHOLD and rij > rji + DELTA:

            G.add_edge(
                i,
                j,
                weight=float(rij)
            )

# ============================================================
# METRICS
# ============================================================

rows = []

for node in G.nodes():

    rows.append({

        "Observable": node,
        "OutDegree": G.out_degree(node),
        "InDegree": G.in_degree(node),
        "OutStrength": sum(
            d["weight"]
            for _, _, d in G.out_edges(node, data=True)
        ),
        "InStrength": sum(
            d["weight"]
            for _, _, d in G.in_edges(node, data=True)
        )

    })

metrics = pd.DataFrame(rows)

metrics.to_csv(
    RESULT_FOLDER / "hierarchy_metrics.csv",
    index=False
)

# ============================================================
# INFLUENCE MATRIX
# ============================================================

influence.to_csv(
    RESULT_FOLDER / "influence_matrix.csv"
)

# ============================================================
# EDGE LIST
# ============================================================

edges = []

for u, v, d in G.edges(data=True):

    edges.append({

        "Source": u,
        "Target": v,
        "Influence": d["weight"]

    })

edges_df = pd.DataFrame(edges)

edges_df.to_csv(
    RESULT_FOLDER / "hierarchy_edges.csv",
    index=False
)

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "hierarchy_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L12\n")
    f.write("Observable Hierarchy\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Nodes : {G.number_of_nodes()}\n")
    f.write(f"Edges : {G.number_of_edges()}\n\n")

    f.write("Hierarchy\n\n")

    metrics = metrics.sort_values(
        "OutStrength",
        ascending=False
    )

    for _, row in metrics.iterrows():

        f.write(
            f"{row['Observable']:20s} "
            f"Out={row['OutDegree']:2d} "
            f"In={row['InDegree']:2d} "
            f"Strength={row['OutStrength']:.3f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

root = metrics.iloc[0]["Observable"]

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Observables : {len(columns)}\n")
    f.write(f"Hierarchy edges : {G.number_of_edges()}\n")
    f.write(f"Candidate root : {root}\n\n")

    if nx.is_directed_acyclic_graph(G):
        f.write("The inferred dependency graph is acyclic.\n")
    else:
        f.write("Cycles were detected in the inferred dependency graph.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
