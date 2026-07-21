from pathlib import Path
from itertools import combinations
import json

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ============================================================
# INPUT
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

columns = list(df.columns)

# ============================================================
# OUTPUT
# ============================================================

RESULT_FOLDER = DATA_FOLDER / "L12_CondensationHierarchy"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# PARAMETERS
# ============================================================

MAX_PREDICTORS = 2
R2_THRESHOLD = 0.99

# ============================================================
# BUILD FULL DEPENDENCY GRAPH
# ============================================================

print("=" * 70)
print("CONDENSATION HIERARCHY")
print("=" * 70)

G = nx.DiGraph()

for c in columns:
    G.add_node(c)

summary_rows = []

for target in columns:

    print(f"Processing {target}")

    predictors = [c for c in columns if c != target]

    best_subset = None
    best_r2 = -1

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

    summary_rows.append({
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
# SAVE ORIGINAL EDGES
# ============================================================

edges = []

for u, v, d in G.edges(data=True):

    edges.append({
        "Source": u,
        "Target": v,
        "Weight": d["weight"]
    })

pd.DataFrame(edges).to_csv(
    RESULT_FOLDER / "dependency_edges.csv",
    index=False
)

pd.DataFrame(summary_rows).to_csv(
    RESULT_FOLDER / "hierarchy_summary.csv",
    index=False
)

# ============================================================
# STRONGLY CONNECTED COMPONENTS
# ============================================================

sccs = list(nx.strongly_connected_components(G))

component_map = {}

component_rows = []

for idx, comp in enumerate(sccs):

    ordered = sorted(comp)

    component_rows.append({
        "Component": idx,
        "Size": len(comp),
        "Observables": ";".join(ordered)
    })

    for node in comp:
        component_map[node] = idx

components_df = pd.DataFrame(component_rows)

components_df.to_csv(
    RESULT_FOLDER / "strongly_connected_components.csv",
    index=False
)

# ============================================================
# CONDENSATION GRAPH
# ============================================================

CG = nx.condensation(G)

# ============================================================
# NODE METRICS
# ============================================================

rows = []

for node in CG.nodes():

    members = sorted(sccs[node])

    rows.append({

        "Component": node,
        "Members": ";".join(members),
        "Size": len(members),
        "OutDegree": CG.out_degree(node),
        "InDegree": CG.in_degree(node)

    })

metrics = pd.DataFrame(rows)

metrics.to_csv(
    RESULT_FOLDER / "condensation_nodes.csv",
    index=False
)

# ============================================================
# EDGES
# ============================================================

rows = []

for u, v in CG.edges():

    rows.append({

        "SourceComponent": u,
        "TargetComponent": v,
        "SourceMembers": ";".join(sorted(sccs[u])),
        "TargetMembers": ";".join(sorted(sccs[v]))

    })

pd.DataFrame(rows).to_csv(
    RESULT_FOLDER / "condensation_edges.csv",
    index=False
)

# ============================================================
# ROOTS / LEAVES
# ============================================================

roots = []

leaves = []

for node in CG.nodes():

    if CG.in_degree(node) == 0:
        roots.append(node)

    if CG.out_degree(node) == 0:
        leaves.append(node)

pd.DataFrame({

    "Component": roots,
    "Members": [
        ";".join(sorted(sccs[i]))
        for i in roots
    ]

}).to_csv(
    RESULT_FOLDER / "roots.csv",
    index=False
)

pd.DataFrame({

    "Component": leaves,
    "Members": [
        ";".join(sorted(sccs[i]))
        for i in leaves
    ]

}).to_csv(
    RESULT_FOLDER / "leaves.csv",
    index=False
)

# ============================================================
# TOPOLOGICAL ORDER
# ============================================================

order = list(nx.topological_sort(CG))

pd.DataFrame({

    "Order": range(len(order)),
    "Component": order,
    "Members": [
        ";".join(sorted(sccs[i]))
        for i in order
    ]

}).to_csv(
    RESULT_FOLDER / "topological_order.csv",
    index=False
)

# ============================================================
# HIERARCHY DEPTH
# ============================================================

depth = 0

if len(CG):

    longest = nx.dag_longest_path(CG)

    depth = len(longest)

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
    f.write("Condensation Hierarchy\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Original observables : {len(columns)}\n")
    f.write(f"Original edges       : {G.number_of_edges()}\n\n")

    f.write(f"SCCs                 : {len(sccs)}\n")
    f.write(f"Condensation nodes   : {CG.number_of_nodes()}\n")
    f.write(f"Condensation edges   : {CG.number_of_edges()}\n")
    f.write(f"Hierarchy depth      : {depth}\n\n")

    f.write("Strongly Connected Components\n\n")

    for idx, comp in enumerate(sccs):

        f.write(
            f"SCC {idx:02d} "
            f"({len(comp)}): "
            f"{', '.join(sorted(comp))}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

certificate = {

    "observables": len(columns),

    "dependency_edges": G.number_of_edges(),

    "strongly_connected_components": len(sccs),

    "largest_component": max(len(c) for c in sccs),

    "condensation_nodes": CG.number_of_nodes(),

    "condensation_edges": CG.number_of_edges(),

    "hierarchy_depth": depth,

    "roots": len(roots),

    "leaves": len(leaves),

    "acyclic": nx.is_directed_acyclic_graph(CG)

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
