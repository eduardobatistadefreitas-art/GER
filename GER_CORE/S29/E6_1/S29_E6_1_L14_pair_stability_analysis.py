from pathlib import Path
from itertools import combinations
import json

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ============================================================
# GER
# S29-E6.1-L14
# Pair Stability Analysis
# ============================================================

DATA_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
DATA_FILE = DATA_FOLDER / "observables.parquet"

OUTPUT_FOLDER = DATA_FOLDER / "L14_PairStabilityAnalysis"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GER")
print("S29-E6.1-L14")
print("Pair Stability Analysis")
print("=" * 70)

df = pd.read_parquet(DATA_FILE)

columns = list(df.columns)
N = len(columns)

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

pair_counts = {
    (a, b): 0
    for a, b in combinations(columns, 2)
}

runs = 0

# ============================================================
# MAIN LOOP
# ============================================================

for max_predictors in MAX_PREDICTORS_LIST:

    for threshold in R2_VALUES:

        runs += 1

        print(
            f"Run {runs:02d}/18"
            f" | Predictors={max_predictors}"
            f" | R²={threshold:.3f}"
        )

        G = nx.DiGraph()

        G.add_nodes_from(columns)

        # ----------------------------------------------------

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
                        found = True
                        best_subset = subset
                        break

                if found:
                    break

            if best_subset is None:
                continue

            for p in best_subset:
                G.add_edge(p, target)

        # ----------------------------------------------------

        sccs = list(nx.strongly_connected_components(G))

        for comp in sccs:

            comp = sorted(comp)

            if len(comp) < 2:
                continue

            for a, b in combinations(comp, 2):

                pair_counts[(a, b)] += 1

# ============================================================
# MATRIX
# ============================================================

matrix = pd.DataFrame(
    np.eye(N),
    index=columns,
    columns=columns
)

rows = []

for (a, b), count in sorted(pair_counts.items()):

    frac = count / runs

    matrix.loc[a, b] = frac
    matrix.loc[b, a] = frac

    rows.append({

        "ObservableA": a,
        "ObservableB": b,
        "TimesTogether": count,
        "FractionTogether": frac

    })

matrix.to_csv(
    OUTPUT_FOLDER / "pair_stability_matrix.csv"
)

pairs = pd.DataFrame(rows)

pairs = pairs.sort_values(
    "FractionTogether",
    ascending=False
)

pairs.to_csv(
    OUTPUT_FOLDER / "pair_stability_long.csv",
    index=False
)

# ============================================================
# SBS
# ============================================================

sbs = []

for obs in columns:

    vals = []

    for other in columns:

        if obs == other:
            continue

        vals.append(matrix.loc[obs, other])

    sbs.append({

        "Observable": obs,

        "StructuralBondStrength": np.mean(vals)

    })

sbs_df = pd.DataFrame(sbs)

sbs_df = sbs_df.sort_values(
    "StructuralBondStrength",
    ascending=False
)

sbs_df.to_csv(
    OUTPUT_FOLDER / "structural_bond_strength.csv",
    index=False
)

# ============================================================
# TOP/BOTTOM PAIRS
# ============================================================

pairs.head(20).to_csv(
    OUTPUT_FOLDER / "most_stable_pairs.csv",
    index=False
)

pairs.sort_values(
    "FractionTogether"
).head(20).to_csv(
    OUTPUT_FOLDER / "least_stable_pairs.csv",
    index=False
)

# ============================================================
# REPORT
# ============================================================

with open(
    OUTPUT_FOLDER / "pair_stability_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L14\n")
    f.write("Pair Stability Analysis\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Executions : {runs}\n")
    f.write(f"Observables: {N}\n")
    f.write(f"Pairs      : {len(pair_counts)}\n\n")

    f.write("Most stable pairs\n")
    f.write("-----------------\n")

    for _, row in pairs.head(15).iterrows():

        f.write(
            f"{row.ObservableA:18s}"
            f"{row.ObservableB:18s}"
            f"{row.FractionTogether:.3f}\n"
        )

    f.write("\n")

    f.write("Highest SBS\n")
    f.write("-----------\n")

    for _, row in sbs_df.head(10).iterrows():

        f.write(
            f"{row.Observable:20s}"
            f"{row.StructuralBondStrength:.3f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

certificate = {

    "executions": runs,

    "observables": N,

    "pairs": len(pair_counts),

    "highest_pair_stability":

        float(pairs.iloc[0]["FractionTogether"]),

    "lowest_pair_stability":

        float(pairs.iloc[-1]["FractionTogether"]),

    "mean_pair_stability":

        float(pairs["FractionTogether"].mean())

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
