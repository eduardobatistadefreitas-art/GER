from pathlib import Path
from itertools import combinations
import json

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ============================================================
# GER
# S29-E6.1-L13
# Condensation Robustness
# ============================================================

DATA_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
DATA_FILE = DATA_FOLDER / "observables.parquet"

OUTPUT_FOLDER = DATA_FOLDER / "L13_CondensationRobustness"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GER")
print("S29-E6.1-L13")
print("Condensation Robustness")
print("=" * 70)

df = pd.read_parquet(DATA_FILE)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")
print()

columns = list(df.columns)

# ============================================================
# PARAMETERS
# ============================================================

R2_VALUES = [
    0.950,
    0.970,
    0.980,
    0.990,
    0.995,
    0.999,
]

MAX_PREDICTORS_LIST = [
    1,
    2,
    3,
]

# ============================================================
# STORAGE
# ============================================================

metrics = []
memberships = []
depth_rows = []

membership_counter = {}

run_id = 0

# ============================================================
# MAIN LOOP
# ============================================================

for max_predictors in MAX_PREDICTORS_LIST:

    for threshold in R2_VALUES:

        run_id += 1

        print("=" * 60)
        print(
            f"Run {run_id:02d}/18"
            f" | Predictors={max_predictors}"
            f" | R²={threshold:.3f}"
        )

        G = nx.DiGraph()

        for c in columns:
            G.add_node(c)

        # -----------------------------------------------------

        for target in columns:

            predictors = [c for c in columns if c != target]

            best_subset = None
            best_r2 = -1

            found = False

            for k in range(1, max_predictors + 1):

                for subset in combinations(predictors, k):

                    X = df[list(subset)]
                    y = df[target]

                    model = LinearRegression()

                    model.fit(X, y)

                    r2 = model.score(X, y)

                    if r2 > best_r2:
                        best_r2 = r2
                        best_subset = subset

                    if r2 >= threshold:

                        best_subset = subset
                        best_r2 = r2
                        found = True
                        break

                if found:
                    break

            if best_subset is None:
                continue

            for predictor in best_subset:
                G.add_edge(
                    predictor,
                    target,
                    weight=float(best_r2)
                )

        # -----------------------------------------------------

        sccs = list(nx.strongly_connected_components(G))

        CG = nx.condensation(G)

        try:
            depth = len(nx.dag_longest_path(CG))
        except Exception:
            depth = 0

        component_sizes = [len(c) for c in sccs]

        roots = sum(
            1
            for n in CG.nodes()
            if CG.in_degree(n) == 0
        )

        leaves = sum(
            1
            for n in CG.nodes()
            if CG.out_degree(n) == 0
        )

        metrics.append({

            "Run": run_id,

            "R2Threshold": threshold,

            "MaxPredictors": max_predictors,

            "DependencyEdges": G.number_of_edges(),

            "NumSCC": len(sccs),

            "LargestSCC": max(component_sizes),

            "SingletonSCC": sum(
                1
                for s in component_sizes
                if s == 1
            ),

            "MeanSCCSize": np.mean(component_sizes),

            "HierarchyDepth": depth,

            "Roots": roots,

            "Leaves": leaves,

            "Acyclic": nx.is_directed_acyclic_graph(CG)

        })

        depth_rows.append({

            "Run": run_id,
            "HierarchyDepth": depth

        })

        for idx, comp in enumerate(sccs):

            ordered = tuple(sorted(comp))

            membership_counter.setdefault(
                ordered,
                0
            )

            membership_counter[ordered] += 1

            memberships.append({

                "Run": run_id,

                "R2Threshold": threshold,

                "MaxPredictors": max_predictors,

                "Component": idx,

                "Size": len(comp),

                "Members": ";".join(ordered)

            })

# ============================================================
# STABILITY INDEX
# ============================================================

stable_nodes = set()

for observable in columns:

    groups = []

    for row in memberships:

        members = row["Members"].split(";")

        if observable in members:

            groups.append(tuple(sorted(members)))

    if len(set(groups)) == 1:
        stable_nodes.add(observable)

SSI = len(stable_nodes) / len(columns)

# ============================================================
# SAVE
# ============================================================

metrics_df = pd.DataFrame(metrics)

memberships_df = pd.DataFrame(memberships)

depth_df = pd.DataFrame(depth_rows)

summary = pd.DataFrame({

    "Metric": [

        "Executions",
        "SSI",
        "MinSCC",
        "MaxSCC",
        "MeanHierarchyDepth",
        "StableObservables"

    ],

    "Value": [

        run_id,

        SSI,

        metrics_df["NumSCC"].min(),

        metrics_df["NumSCC"].max(),

        metrics_df["HierarchyDepth"].mean(),

        ";".join(sorted(stable_nodes))

    ]

})

metrics_df.to_csv(
    OUTPUT_FOLDER / "robustness_metrics.csv",
    index=False
)

memberships_df.to_csv(
    OUTPUT_FOLDER / "scc_memberships.csv",
    index=False
)

depth_df.to_csv(
    OUTPUT_FOLDER / "hierarchy_depth.csv",
    index=False
)

summary.to_csv(
    OUTPUT_FOLDER / "robustness_summary.csv",
    index=False
)

# ============================================================
# REPORT
# ============================================================

with open(
    OUTPUT_FOLDER / "robustness_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L13\n")
    f.write("Condensation Robustness\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Executions          : {run_id}\n")
    f.write(f"Structural SSI      : {SSI:.3f}\n")
    f.write(f"Minimum SCCs        : {metrics_df['NumSCC'].min()}\n")
    f.write(f"Maximum SCCs        : {metrics_df['NumSCC'].max()}\n")
    f.write(f"Average Depth       : {metrics_df['HierarchyDepth'].mean():.3f}\n")
    f.write("\n")

    f.write("Stable observables\n")
    f.write("------------------\n")

    if stable_nodes:
        for obs in sorted(stable_nodes):
            f.write(obs + "\n")
    else:
        f.write("None\n")

    f.write("\n")

    f.write("Most frequent SCCs\n")
    f.write("------------------\n")

    for comp, count in sorted(
        membership_counter.items(),
        key=lambda x: (-x[1], -len(x[0]))
    ):

        f.write(
            f"{count:2d}x : "
            + ", ".join(comp)
            + "\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

certificate = {

    "executions": run_id,

    "r2_thresholds": R2_VALUES,

    "max_predictors": MAX_PREDICTORS_LIST,

    "ssi": float(SSI),

    "min_scc": int(metrics_df["NumSCC"].min()),

    "max_scc": int(metrics_df["NumSCC"].max()),

    "largest_component":

        int(metrics_df["LargestSCC"].max()),

    "smallest_component":

        int(metrics_df["LargestSCC"].min()),

    "mean_depth":

        float(metrics_df["HierarchyDepth"].mean()),

    "stable_observables":

        sorted(stable_nodes)

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
print()
print("Results saved to:")
print(OUTPUT_FOLDER)
print("=" * 70)
