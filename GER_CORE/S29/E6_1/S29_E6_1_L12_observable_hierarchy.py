from pathlib import Path
import json
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd
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
# PARAMETERS
# ============================================================

MAX_PREDICTORS = 2
R2_THRESHOLD = 0.99

print("=" * 70)
print("OBSERVABLE HIERARCHY")
print("=" * 70)

# ============================================================
# BUILD DEPENDENCY GRAPH
# ============================================================

G = nx.DiGraph()

for c in columns:
    G.add_node(c)

hierarchy_rows = []

for target in columns:

    print(f"Processing {target}")

    predictors = [c for c in columns if c != target]

    best_subset = None
    best_r2 = -1

    # procura subconjunto mínimo
    for k in range(1, MAX_PREDICTORS + 1):

        found = False

        for subset in combinations(predictors, k):

            X = df[list(subset)]
            y = df[target]

            model = LinearRegression()
            model.fit(X, y)

            r2 = model.score(X, y)

            if r2 > best_r2:
                best_r2 = r2
                best_subset = subset

            if r2 >= R2_THRESHOLD:

                best_subset = subset
                best_r2 = r2
                found = True
                break

        if found:
            break

    hierarchy_rows.append({

        "Target": target,
        "Predictors": ";".join(best_subset),
        "NumPredictors": len(best_subset),
        "R2": best_r2

    })

    for predictor in best_subset:

        G.add_edge(
            predictor,
            target,
            weight=float(best_r2)
        )

# ============================================================
# REMOVE CYCLES
# ============================================================

while True:

    try:

        cycle = nx.find_cycle(G)

    except nx.NetworkXNoCycle:

        break

    weakest = None
    weakest_weight = np.inf

    for u, v in cycle:

        w = G[u][v]["weight"]

        if w < weakest_weight:

            weakest_weight = w
            weakest = (u, v)

    G.remove_edge(*weakest)

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

metrics = metrics.sort_values(
    "OutStrength",
    ascending=False
)

metrics.to_csv(
    RESULT_FOLDER / "hierarchy_metrics.csv",
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

edges_df = pd.DataFrame(edges)

edges_df.to_csv(
    RESULT_FOLDER / "hierarchy_edges.csv",
    index=False
)

# ============================================================
# TOPOLOGICAL ORDER
# ============================================================

topological = list(nx.topological_sort(G))

pd.DataFrame({

    "Order": range(len(topological)),
    "Observable": topological

}).to_csv(

    RESULT_FOLDER / "topological_order.csv",
    index=False

)

# ============================================================
# ROOTS / LEAVES
# ============================================================

roots = [n for n in G.nodes if G.in_degree(n) == 0]
leaves = [n for n in G.nodes if G.out_degree(n) == 0]

pd.DataFrame({"Root": roots}).to_csv(
    RESULT_FOLDER / "roots.csv",
    index=False
)

pd.DataFrame({"Leaf": leaves}).to_csv(
    RESULT_FOLDER / "leaves.csv",
    index=False
)

# ============================================================
# TARGET SUMMARY
# ============================================================

summary = pd.DataFrame(hierarchy_rows)

summary.to_csv(
    RESULT_FOLDER / "hierarchy_summary.csv",
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

    f.write("Topological Order\n\n")

    for i, node in enumerate(topological):

        f.write(f"{i:2d}  {node}\n")

    f.write("\n\nHierarchy\n\n")

    for _, row in metrics.iterrows():

        f.write(

            f"{row['Observable']:20s}"
            f" Out={row['OutDegree']:2d}"
            f" In={row['InDegree']:2d}"
            f" Strength={row['OutStrength']:.3f}\n"

        )

# ============================================================
# CERTIFICATE
# ============================================================

certificate = {

    "observables": len(columns),

    "edges": G.number_of_edges(),

    "roots": roots,

    "leaves": leaves,

    "acyclic": nx.is_directed_acyclic_graph(G)

}

with open(
    RESULT_FOLDER / "scientific_certificate.json",
    "w"
) as f:

    json.dump(
        certificate,
        f,
        indent=4
    )

print("\nResults saved to:")
print(RESULT_FOLDER)
