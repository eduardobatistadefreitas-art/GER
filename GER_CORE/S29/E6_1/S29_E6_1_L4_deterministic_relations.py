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

RESULT_FOLDER = DATA_FOLDER / "L4_DeterministicRelations"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# PARAMETERS
# ============================================================

TOL = 1e-12

# ============================================================
# SEARCH
# ============================================================

relations = []

columns = list(df.columns)

print("=" * 70)
print("DETERMINISTIC RELATION SEARCH")
print("=" * 70)

for i in range(len(columns)):
    for j in range(i + 1, len(columns)):

        x = columns[i]
        y = columns[j]

        X = df[x].values
        Y = df[y].values

        # ----------------------------------------------------
        # Equality
        # ----------------------------------------------------

        if np.allclose(X, Y, atol=TOL, rtol=TOL):

            print(f"{x} == {y}")

            relations.append({
                "X": x,
                "Y": y,
                "Relation": "Equality",
                "a": 1.0,
                "b": 0.0
            })

            continue

        # ----------------------------------------------------
        # Proportionality
        # ----------------------------------------------------

        mask = np.abs(Y) > TOL

        if mask.sum() > 0:

            ratio = X[mask] / Y[mask]

            if np.allclose(ratio, ratio[0], atol=TOL, rtol=TOL):

                print(f"{x} = {ratio[0]:.12f} * {y}")

                relations.append({
                    "X": x,
                    "Y": y,
                    "Relation": "Proportional",
                    "a": float(ratio[0]),
                    "b": 0.0
                })

                continue

        # ----------------------------------------------------
        # Affine
        # ----------------------------------------------------

        coef = np.polyfit(Y, X, 1)

        pred = coef[0] * Y + coef[1]

        if np.allclose(pred, X, atol=TOL, rtol=TOL):

            print(f"{x} = {coef[0]:.12f} * {y} + {coef[1]:.12f}")

            relations.append({
                "X": x,
                "Y": y,
                "Relation": "Affine",
                "a": float(coef[0]),
                "b": float(coef[1])
            })

# ============================================================
# SAVE CSV
# ============================================================

relations_df = pd.DataFrame(relations)

csv_path = RESULT_FOLDER / "deterministic_relations.csv"
relations_df.to_csv(csv_path, index=False)

# ============================================================
# SAVE JSON
# ============================================================

json_path = RESULT_FOLDER / "deterministic_relations.json"

with open(json_path, "w") as f:
    json.dump(relations, f, indent=4)

# ============================================================
# REPORT
# ============================================================

report_path = RESULT_FOLDER / "deterministic_relations_report.txt"

with open(report_path, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L4\n")
    f.write("Deterministic Relations\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Relations found : {len(relations)}\n\n")

    for r in relations:

        f.write(f"{r['X']}  <->  {r['Y']}\n")
        f.write(f"Type : {r['Relation']}\n")
        f.write(f"a    : {r['a']:.12f}\n")
        f.write(f"b    : {r['b']:.12f}\n")
        f.write("\n")

# ============================================================
# CERTIFICATE
# ============================================================

certificate_path = RESULT_FOLDER / "scientific_certificate.txt"

equalities = sum(r["Relation"] == "Equality" for r in relations)
proportional = sum(r["Relation"] == "Proportional" for r in relations)
affine = sum(r["Relation"] == "Affine" for r in relations)

with open(certificate_path, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Observables analyzed : {len(columns)}\n")
    f.write(f"Pairs analyzed       : {len(columns)*(len(columns)-1)//2}\n\n")

    f.write(f"Equalities found     : {equalities}\n")
    f.write(f"Proportional found   : {proportional}\n")
    f.write(f"Affine found         : {affine}\n")
    f.write(f"Total relations      : {len(relations)}\n\n")

    if len(relations) == 0:
        f.write("Conclusion:\n")
        f.write("No deterministic relations were detected.\n")
    else:
        f.write("Conclusion:\n")
        f.write("Deterministic structural relations were detected among the observables.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
