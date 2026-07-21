from pathlib import Path
import json
from itertools import combinations

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

RESULT_FOLDER = DATA_FOLDER / "L9_MinimalObservableSet"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

columns = list(df.columns)

TARGET_R2 = 0.999

results = []

print("=" * 70)
print("MINIMAL OBSERVABLE SET")
print("=" * 70)

# ============================================================
# SEARCH
# ============================================================

for target in columns:

    predictors = [c for c in columns if c != target]

    found = False

    for size in range(1, len(predictors) + 1):

        best_r2 = -1
        best_subset = None

        for subset in combinations(predictors, size):

            X = df[list(subset)]
            y = df[target]

            model = LinearRegression()

            model.fit(X, y)

            r2 = model.score(X, y)

            if r2 > best_r2:

                best_r2 = r2
                best_subset = subset

            if r2 >= TARGET_R2:

                results.append({

                    "Target": target,
                    "SubsetSize": size,
                    "Subset": ", ".join(subset),
                    "BestR2": r2

                })

                print(
                    f"{target:20s} <- {subset} "
                    f"(k={size}) "
                    f"R²={r2:.6f}"
                )

                found = True
                break

        if found:
            break

    if not found:

        results.append({

            "Target": target,
            "SubsetSize": len(predictors),
            "Subset": ", ".join(best_subset),
            "BestR2": best_r2

        })

# ============================================================
# SAVE CSV
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    RESULT_FOLDER / "minimal_observable_set.csv",
    index=False
)

# ============================================================
# JSON
# ============================================================

with open(
    RESULT_FOLDER / "minimal_observable_set.json",
    "w"
) as f:

    json.dump(results, f, indent=4)

# ============================================================
# GLOBAL ANALYSIS
# ============================================================

usage = {}

for r in results:

    subset = r["Subset"].split(", ")

    for obs in subset:

        usage[obs] = usage.get(obs, 0) + 1

usage_df = pd.DataFrame({

    "Observable": list(usage.keys()),
    "UsageCount": list(usage.values())

})

usage_df = usage_df.sort_values(
    "UsageCount",
    ascending=False
)

usage_df.to_csv(
    RESULT_FOLDER / "observable_usage.csv",
    index=False
)

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "minimal_set_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L9\n")
    f.write("Minimal Observable Set\n")
    f.write("=" * 60 + "\n\n")

    for r in results:

        f.write(
            f"{r['Target']:20s} "
            f"k={r['SubsetSize']} "
            f"R²={r['BestR2']:.6f}\n"
        )

        f.write(f"Subset : {r['Subset']}\n\n")

# ============================================================
# CERTIFICATE
# ============================================================

avg_size = results_df["SubsetSize"].mean()

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Targets analyzed      : {len(columns)}\n")
    f.write(f"Target R²             : {TARGET_R2}\n")
    f.write(f"Average subset size   : {avg_size:.2f}\n\n")

    f.write("Most frequently used observables:\n\n")

    for _, row in usage_df.iterrows():

        f.write(
            f"{row['Observable']:20s} "
            f"{int(row['UsageCount'])}\n"
        )

print("\nResults saved to:")
print(RESULT_FOLDER)
