from pathlib import Path
import json

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

RESULT_FOLDER = DATA_FOLDER / "L5_IndependenceRanking"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# CORRELATION MATRIX
# ============================================================

corr = df.corr(numeric_only=True).abs()

results = []

print("=" * 70)
print("INDEPENDENCE RANKING")
print("=" * 70)

for column in corr.columns:

    others = [c for c in corr.columns if c != column]

    # --------------------------------------------------------
    # Correlation statistics
    # --------------------------------------------------------

    mean_corr = corr.loc[column, others].mean()
    max_corr = corr.loc[column, others].max()
    min_corr = corr.loc[column, others].min()

    # --------------------------------------------------------
    # Reconstruction using all remaining observables
    # --------------------------------------------------------

    X = df[others]
    y = df[column]

    model = LinearRegression()
    model.fit(X, y)

    r2 = model.score(X, y)

    independence_score = 1.0 - r2

    print(f"{column:20s}  R²={r2:.6f}  Independence={independence_score:.6f}")

    results.append({

        "Observable": column,
        "MeanCorrelation": mean_corr,
        "MaximumCorrelation": max_corr,
        "MinimumCorrelation": min_corr,
        "ReconstructionR2": r2,
        "IndependenceScore": independence_score

    })

# ============================================================
# SORT
# ============================================================

ranking = pd.DataFrame(results)

ranking = ranking.sort_values(
    "IndependenceScore",
    ascending=False
).reset_index(drop=True)

ranking.insert(0, "Rank", np.arange(1, len(ranking) + 1))

# ============================================================
# SAVE CSV
# ============================================================

ranking.to_csv(
    RESULT_FOLDER / "independence_ranking.csv",
    index=False
)

# ============================================================
# SAVE JSON
# ============================================================

with open(
    RESULT_FOLDER / "independence_ranking.json",
    "w"
) as f:

    json.dump(
        ranking.to_dict(orient="records"),
        f,
        indent=4
    )

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "ranking_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L5\n")
    f.write("Independence Ranking\n")
    f.write("=" * 60 + "\n\n")

    for _, row in ranking.iterrows():

        f.write(
            f"{int(row['Rank']):2d}  "
            f"{row['Observable']:20s}  "
            f"Independence={row['IndependenceScore']:.6f}  "
            f"R²={row['ReconstructionR2']:.6f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

most_independent = ranking.iloc[0]
most_redundant = ranking.iloc[-1]

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Observables analyzed : {len(ranking)}\n\n")

    f.write(
        f"Most independent : {most_independent['Observable']} "
        f"(score={most_independent['IndependenceScore']:.6f})\n"
    )

    f.write(
        f"Most redundant   : {most_redundant['Observable']} "
        f"(score={most_redundant['IndependenceScore']:.6f})\n"
    )

    f.write("\n")

    f.write("Ranking generated successfully.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
