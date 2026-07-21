from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from itertools import combinations

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

RESULT_FOLDER = DATA_FOLDER / "L6_PairReconstruction"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

columns = list(df.columns)

results = []

print("=" * 70)
print("PAIR RECONSTRUCTION")
print("=" * 70)

# ============================================================
# SEARCH
# ============================================================

for target in columns:

    predictors = [c for c in columns if c != target]

    best_r2 = -1
    best_pair = None

    for pair in combinations(predictors, 2):

        X = df[list(pair)]
        y = df[target]

        model = LinearRegression()

        model.fit(X, y)

        r2 = model.score(X, y)

        if r2 > best_r2:

            best_r2 = r2
            best_pair = pair

    print(
        f"{target:20s} <- ({best_pair[0]}, {best_pair[1]}) "
        f"R² = {best_r2:.6f}"
    )

    results.append({

        "Target": target,
        "Predictor1": best_pair[0],
        "Predictor2": best_pair[1],
        "BestR2": best_r2

    })

# ============================================================
# SAVE CSV
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    RESULT_FOLDER / "pair_reconstruction.csv",
    index=False
)

# ============================================================
# SAVE JSON
# ============================================================

with open(
    RESULT_FOLDER / "pair_reconstruction.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "pair_reconstruction_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L6\n")
    f.write("Pair Reconstruction\n")
    f.write("=" * 60 + "\n\n")

    for r in results:

        f.write(
            f"{r['Target']:20s} <- "
            f"({r['Predictor1']}, {r['Predictor2']}) "
            f"R²={r['BestR2']:.6f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

perfect = sum(r["BestR2"] >= 0.999999 for r in results)

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Observables analyzed : {len(columns)}\n")
    f.write(f"Perfect reconstructions : {perfect}\n")
    f.write(f"Total targets : {len(columns)}\n\n")

    f.write("Experiment completed successfully.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
