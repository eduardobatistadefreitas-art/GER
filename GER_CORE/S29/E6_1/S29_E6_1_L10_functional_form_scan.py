from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

warnings.filterwarnings("ignore")

# ============================================================
# INPUT
# ============================================================

DATA_FOLDER = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
DATA_FILE = DATA_FOLDER / "observables.parquet"

print("=" * 60)
print("Loading dataset...")
print(DATA_FILE)

df = pd.read_parquet(DATA_FILE)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# ============================================================
# PARAMETERS
# ============================================================

SAMPLE_SIZE = 250_000
CORR_THRESHOLD = 0.80
SEED = 42

print(f"Sample   : {SAMPLE_SIZE:,}")
print(f"Threshold: {CORR_THRESHOLD}")

# ============================================================

if len(df) > SAMPLE_SIZE:
    df = df.sample(SAMPLE_SIZE, random_state=SEED)

# ============================================================

RESULT_FOLDER = DATA_FOLDER / "L10_FunctionalFormScan"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

corr = df.corr(numeric_only=True)

# ============================================================

pairs = []

cols = list(corr.columns)

for i in range(len(cols)):
    for j in range(i + 1, len(cols)):

        if abs(corr.iloc[i, j]) >= CORR_THRESHOLD:

            pairs.append((cols[i], cols[j]))

print(f"Relevant pairs : {len(pairs)}")

# ============================================================

def evaluate_linear(x, y):

    c = np.polyfit(x, y, 1)

    pred = np.polyval(c, x)

    return r2_score(y, pred), c

# ------------------------------------------------------------

def evaluate_quadratic(x, y):

    c = np.polyfit(x, y, 2)

    pred = np.polyval(c, x)

    return r2_score(y, pred), c

# ------------------------------------------------------------

def evaluate_log(x, y):

    mask = x > 0

    if mask.sum() < 100:
        raise Exception()

    xx = np.log(x[mask])

    yy = y[mask]

    c = np.polyfit(xx, yy, 1)

    pred = np.polyval(c, xx)

    pred_full = np.full(len(y), np.nan)

    pred_full[mask] = pred

    return r2_score(yy, pred), c

# ------------------------------------------------------------

def evaluate_power(x, y):

    mask = (x > 0) & (y > 0)

    if mask.sum() < 100:
        raise Exception()

    xx = np.log(x[mask])

    yy = np.log(y[mask])

    c = np.polyfit(xx, yy, 1)

    a = np.exp(c[1])

    b = c[0]

    pred = a * x[mask] ** b

    return r2_score(y[mask], pred), [a, b]

# ------------------------------------------------------------

def evaluate_exp(x, y):

    mask = y > 0

    if mask.sum() < 100:
        raise Exception()

    xx = x[mask]

    yy = np.log(y[mask])

    c = np.polyfit(xx, yy, 1)

    a = np.exp(c[1])

    b = c[0]

    pred = a * np.exp(b * x[mask])

    return r2_score(y[mask], pred), [a, b]

# ============================================================

models = {

    "Linear": evaluate_linear,
    "Quadratic": evaluate_quadratic,
    "Power": evaluate_power,
    "Exponential": evaluate_exp,
    "Logarithmic": evaluate_log

}

results = []

print("=" * 60)
print("FUNCTIONAL FORM SCAN")
print("=" * 60)

for xname, yname in pairs:

    x = df[xname].values.astype(float)

    y = df[yname].values.astype(float)

    winner = None

    winner_r2 = -np.inf

    winner_coef = None

    scores = {}

    for name, func in models.items():

        try:

            r2, coef = func(x, y)

            scores[name] = float(r2)

            if r2 > winner_r2:

                winner = name

                winner_r2 = r2

                winner_coef = coef

        except:

            scores[name] = np.nan

    print(f"{xname:20s} -> {yname:20s} {winner:12s} R²={winner_r2:.6f}")

    results.append({

        "X": xname,

        "Y": yname,

        "Winner": winner,

        "BestR2": winner_r2,

        "Coefficients": str(winner_coef),

        **scores

    })

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

    json.dump(results, f, indent=4)

# ============================================================

freq = (

    results_df["Winner"]

    .value_counts()

    .rename_axis("Model")

    .reset_index(name="Count")

)

freq.to_csv(

    RESULT_FOLDER / "model_frequency.csv",

    index=False

)

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

    f.write(f"Relevant pairs : {len(results_df)}\n\n")

    for _, row in results_df.iterrows():

        f.write(

            f"{row['X']:20s} -> "

            f"{row['Y']:20s} "

            f"{row['Winner']:12s} "

            f"R²={row['BestR2']:.6f}\n"

        )

# ============================================================

with open(

    RESULT_FOLDER / "scientific_certificate.txt",

    "w"

) as f:

    f.write("=" * 60 + "\n")

    f.write("SCIENTIFIC CERTIFICATE\n")

    f.write("=" * 60 + "\n\n")

    f.write(f"Relevant pairs : {len(results_df)}\n\n")

    f.write("Winning models\n\n")

    for _, row in freq.iterrows():

        f.write(

            f"{row['Model']:15s} "

            f"{int(row['Count'])}\n"

        )

print()

print("Results saved to:")

print(RESULT_FOLDER)
