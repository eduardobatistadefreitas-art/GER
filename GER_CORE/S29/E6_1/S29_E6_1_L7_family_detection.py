from pathlib import Path
import json

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

RESULT_FOLDER = DATA_FOLDER / "L7_FamilyDetection"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

corr = df.corr(numeric_only=True).abs()

thresholds = [0.80, 0.85, 0.90, 0.95, 0.99]

summary = []

report_lines = []

print("=" * 70)
print("FAMILY DETECTION")
print("=" * 70)

# ============================================================
# CONNECTED COMPONENTS
# ============================================================

def connected_groups(matrix, threshold):

    cols = list(matrix.columns)

    visited = set()

    groups = []

    for node in cols:

        if node in visited:
            continue

        stack = [node]

        component = []

        while stack:

            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            component.append(current)

            neighbors = []

            for other in cols:

                if other == current:
                    continue

                if matrix.loc[current, other] >= threshold:
                    neighbors.append(other)

            stack.extend(neighbors)

        groups.append(sorted(component))

    return groups

# ============================================================
# MAIN LOOP
# ============================================================

for threshold in thresholds:

    groups = connected_groups(corr, threshold)

    print("\n" + "=" * 60)
    print(f"Threshold = {threshold:.2f}")

    report_lines.append("=" * 60)
    report_lines.append(f"Threshold = {threshold:.2f}")

    for g in groups:

        print(g)

        report_lines.append(str(g))

    summary.append({

        "Threshold": threshold,
        "Groups": len(groups),
        "LargestGroup": max(len(g) for g in groups),
        "Families": groups

    })

# ============================================================
# SUMMARY CSV
# ============================================================

summary_df = pd.DataFrame([
    {
        "Threshold": s["Threshold"],
        "Groups": s["Groups"],
        "LargestGroup": s["LargestGroup"]
    }
    for s in summary
])

summary_df.to_csv(
    RESULT_FOLDER / "family_summary.csv",
    index=False
)

# ============================================================
# JSON
# ============================================================

with open(
    RESULT_FOLDER / "family_detection.json",
    "w"
) as f:

    json.dump(summary, f, indent=4)

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "family_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L7\n")
    f.write("Family Detection\n")
    f.write("=" * 60 + "\n\n")

    for line in report_lines:

        f.write(line + "\n")

# ============================================================
# CERTIFICATE
# ============================================================

stable = True

reference = summary[0]["Families"]

for s in summary[1:]:

    if s["Families"] != reference:

        stable = False

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Thresholds analyzed : {len(thresholds)}\n\n")

    if stable:

        f.write("Family structure remained invariant.\n")

    else:

        f.write("Family structure changes with threshold.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
