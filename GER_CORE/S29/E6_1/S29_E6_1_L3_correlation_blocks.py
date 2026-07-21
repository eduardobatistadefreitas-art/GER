from pathlib import Path
import json

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

RESULT_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1/L3_CorrelationBlocks")
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# CORRELATION MATRIX
# ============================================================

corr = df.corr(numeric_only=True).abs()

print("=" * 70)
print("HIGHLY CORRELATED GROUPS (|r| >= 0.95)")
print("=" * 70)

cols = list(corr.columns)
visited = set()

groups = []

for c in cols:

    if c in visited:
        continue

    group = [c]

    for d in cols:

        if d == c:
            continue

        if corr.loc[c, d] >= 0.95:
            group.append(d)

    if len(group) > 1:

        visited.update(group)

        groups.append(group)

        print(group)

# ============================================================
# SAVE GROUP TABLE
# ============================================================

rows = []

for i, group in enumerate(groups, start=1):

    rows.append({
        "Block": f"Block_{i}",
        "Size": len(group),
        "Variables": ", ".join(group)
    })

blocks_df = pd.DataFrame(rows)

csv_path = RESULT_FOLDER / "correlation_blocks.csv"
blocks_df.to_csv(csv_path, index=False)

# ============================================================
# SAVE JSON
# ============================================================

json_path = RESULT_FOLDER / "correlation_blocks.json"

with open(json_path, "w") as f:

    json.dump(groups, f, indent=4)

# ============================================================
# SAVE REPORT
# ============================================================

report_path = RESULT_FOLDER / "block_summary.txt"

with open(report_path, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L3\n")
    f.write("Correlation Block Analysis\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Correlation threshold : |r| >= 0.95\n")
    f.write(f"Blocks identified     : {len(groups)}\n\n")

    for i, group in enumerate(groups, start=1):

        f.write(f"Block {i}\n")

        for variable in group:
            f.write(f"  - {variable}\n")

        f.write("\n")

# ============================================================
# SCIENTIFIC CERTIFICATE
# ============================================================

certificate_path = RESULT_FOLDER / "scientific_certificate.txt"

largest_block = max(len(g) for g in groups) if groups else 0
covered_variables = sorted({v for g in groups for v in g})

with open(certificate_path, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Correlation threshold      : |r| >= 0.95\n")
    f.write(f"Blocks detected            : {len(groups)}\n")
    f.write(f"Largest block size         : {largest_block}\n")
    f.write(f"Variables inside blocks    : {len(covered_variables)}\n")
    f.write(f"Total observables analyzed : {len(cols)}\n\n")

    f.write("Detected blocks:\n\n")

    for i, group in enumerate(groups, start=1):
        f.write(f"Block {i}: {', '.join(group)}\n")

    f.write("\nConclusion:\n")
    f.write(
        "The correlation analysis identified groups of observables "
        "that exhibit strong internal dependence (|r| >= 0.95), "
        "indicating the presence of structural families within the "
        "relational geometry."
    )

print("\nResults saved to:")
print(RESULT_FOLDER)
