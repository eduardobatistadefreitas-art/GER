from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

warnings.filterwarnings("ignore")

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

RESULT_FOLDER = DATA_FOLDER / "L10_FunctionalFormScan"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# FIT FUNCTIONS
# ============================================================

def fit_linear(x, y):
    c = np.polyfit(x, y, 1)
    yp = np.polyval(c, x)
    return r2_score(y, yp), c

def fit_quadratic(x, y):
    c = np.polyfit(x, y, 2)
    yp = np.polyval(c, x)
    return r2_score(y, yp), c

def fit_logarithmic(x, y):
    mask = x > 0
    xx = np.log(x[mask])
    yy = y[mask]
    c = np.polyfit(xx, yy, 1)
    yp = np.polyval(c, xx)
    return r2_score(yy, yp), c

def fit_power(x, y):
    mask = (x > 0) & (y > 0)
    xx = np.log(x[mask])
    yy = np.log(y[mask])
    c = np.polyfit(xx, yy, 1)
    yp = np.polyval(c, xx)
    return r2_score(yy, yp), c

def fit_exponential(x, y):
    mask = y > 0
    xx = x[mask]
    yy = np.log(y[mask])
    c = np.polyfit(xx, yy, 1)
    yp = np.polyval(c, xx)
    return r2_score(yy, yp), c

models = {
    "Linear": fit_linear,
    "Quadratic": fit_quadratic,
    "Logarithmic": fit_logarithmic,
    "Power": fit_power,
    "Exponential": fit_exponential
}

# ============================================================
# MAIN LOOP
# ============================================================

results = []

cols = list(df.columns)

print("=" * 70)
print("FUNCTIONAL FORM SCAN")
print("=" * 70)

for i in range(len(cols)):
    for j in range(i + 1, len(cols)):

        xname = cols[i]
        yname = cols[j]

        x = df[xname].values.astype(float)
        y = df[yname].values.astype(float)

        best_model = None
        best_r2 = -np.inf

        scores = {}

        for name, func in models.items():

            try:

                r2, coef = func(x, y)

                scores[name] = float(r2)

                if r2 > best_r2:

                    best_r2 = r2
                    best_model = name

            except:

                scores[name] = np.nan

        print(
            f"{xname:20s} -> {yname:20s} "
            f"{best_model:12s} "
            f"R²={best_r2:.6f}"
        )

        results.append({

            "X": xname,
            "Y": yname,
            "BestModel": best_model,
            "BestR2": best_r2,
            **scores

        })

# ============================================================
# SAVE
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    RESULT_FOLDER / "functional_scan.csv",
    index=False
)

with open(
    RESULT_FOLDER / "functional_scan.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

# ============================================================
# MODEL FREQUENCY
# ============================================================

freq = (
    results_df["BestModel"]
    .value_counts()
    .rename_axis("Model")
    .reset_index(name="Count")
)

freq.to_csv(
    RESULT_FOLDER / "model_frequency.csv",
    index=False
)

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "functional_scan_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L10\n")
    f.write("Functional Form Scan\n")
    f.write("=" * 60 + "\n\n")

    for _, row in results_df.iterrows():

        f.write(
            f"{row['X']:20s} -> "
            f"{row['Y']:20s} "
            f"{row['BestModel']:12s} "
            f"R²={row['BestR2']:.6f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        f"Pairs analyzed : {len(results_df)}\n\n"
    )

    f.write("Winning models\n\n")

    for _, row in freq.iterrows():

        f.write(
            f"{row['Model']:15s} "
            f"{int(row['Count'])}\n"
        )

print("\nResults saved to:")
print(RESULT_FOLDER)
