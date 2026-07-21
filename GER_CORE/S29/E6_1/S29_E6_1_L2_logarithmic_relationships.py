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

RESULT_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1/L2_LogarithmicRelationships")
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# ANALYSIS
# ============================================================

tests = [
    ("Vertices", "AverageDistance"),
    ("Vertices", "Density"),
    ("Edges", "Degree"),
]

results = []

print("=" * 70)
print("LOGARITHMIC RELATIONSHIP ANALYSIS")
print("=" * 70)

for x, y in tests:

    print("=" * 70)
    print(f"{x} -> {y}")

    coef = np.polyfit(np.log(df[x]), df[y], 1)

    pred = coef[0] * np.log(df[x]) + coef[1]

    ss_res = ((df[y] - pred) ** 2).sum()
    ss_tot = ((df[y] - df[y].mean()) ** 2).sum()

    r2 = 1 - ss_res / ss_tot

    print("Linear fit on log(X)")
    print("slope     =", coef[0])
    print("intercept =", coef[1])
    print("R²        =", r2)

    results.append({
        "X": x,
        "Y": y,
        "Slope": float(coef[0]),
        "Intercept": float(coef[1]),
        "R2": float(r2),
    })

# ============================================================
# SAVE CSV
# ============================================================

results_df = pd.DataFrame(results)

csv_path = RESULT_FOLDER / "logarithmic_relationships.csv"
results_df.to_csv(csv_path, index=False)

# ============================================================
# SAVE JSON
# ============================================================

json_path = RESULT_FOLDER / "logarithmic_relationships.json"

with open(json_path, "w") as f:
    json.dump(results, f, indent=4)

# ============================================================
# SAVE REPORT
# ============================================================

report_path = RESULT_FOLDER / "regression_summary.txt"

with open(report_path, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L2\n")
    f.write("Logarithmic Relationship Analysis\n")
    f.write("=" * 60 + "\n\n")

    for row in results:

        f.write(f"{row['X']} -> {row['Y']}\n")
        f.write(f"Slope      : {row['Slope']:.12f}\n")
        f.write(f"Intercept  : {row['Intercept']:.12f}\n")
        f.write(f"R²         : {row['R2']:.12f}\n")
        f.write("\n")

# ============================================================
# CERTIFICATE
# ============================================================

certificate_path = RESULT_FOLDER / "scientific_certificate.txt"

very_strong = sum(r["R2"] >= 0.95 for r in results)
strong = sum(0.90 <= r["R2"] < 0.95 for r in results)
moderate = sum(0.70 <= r["R2"] < 0.90 for r in results)
weak = sum(r["R2"] < 0.70 for r in results)

with open(certificate_path, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Relationships analyzed      : {len(results)}\n")
    f.write(f"Very strong (R² ≥ 0.95)     : {very_strong}\n")
    f.write(f"Strong (0.90 ≤ R² < 0.95)   : {strong}\n")
    f.write(f"Moderate (0.70 ≤ R² < 0.90) : {moderate}\n")
    f.write(f"Weak (R² < 0.70)            : {weak}\n\n")

    f.write("Conclusion:\n")

    if very_strong > 0:
        f.write("At least one logarithmic relationship exhibits excellent explanatory power.\n")
    elif strong > 0:
        f.write("The analyzed logarithmic relationships are strong but not dominant.\n")
    else:
        f.write("The analyzed logarithmic relationships do not provide a dominant description.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
