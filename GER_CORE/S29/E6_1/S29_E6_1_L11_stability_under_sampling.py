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

RESULT_FOLDER = DATA_FOLDER / "L11_StabilityUnderSampling"
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

# ============================================================
# PARAMETERS
# ============================================================

SAMPLE_SIZES = [
    100_000,
    250_000,
    500_000,
    1_000_000,
    len(df)
]

SEED = 42

# ============================================================
# REFERENCE
# ============================================================

reference_mean = df.mean(numeric_only=True)
reference_std = df.std(numeric_only=True)
reference_corr = df.corr(numeric_only=True)

summary = []

print("=" * 70)
print("STABILITY UNDER SAMPLING")
print("=" * 70)

# ============================================================
# LOOP
# ============================================================

for n in SAMPLE_SIZES:

    print(f"\nSample: {n:,}")

    if n == len(df):
        sample = df
    else:
        sample = df.sample(
            n=n,
            random_state=SEED
        )

    mean = sample.mean(numeric_only=True)
    std = sample.std(numeric_only=True)
    corr = sample.corr(numeric_only=True)

    mean_error = (mean - reference_mean).abs().mean()

    std_error = (std - reference_std).abs().mean()

    corr_error = (
        corr - reference_corr
    ).abs().values.mean()

    print(f"Mean error : {mean_error:.8f}")
    print(f"Std error  : {std_error:.8f}")
    print(f"Corr error : {corr_error:.8f}")

    summary.append({

        "SampleSize": int(n),
        "MeanError": float(mean_error),
        "StdError": float(std_error),
        "CorrelationError": float(corr_error)

    })

# ============================================================
# SAVE CSV
# ============================================================

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    RESULT_FOLDER / "sampling_stability.csv",
    index=False
)

# ============================================================
# JSON
# ============================================================

with open(
    RESULT_FOLDER / "sampling_stability.json",
    "w"
) as f:

    json.dump(summary, f, indent=4)

# ============================================================
# REPORT
# ============================================================

with open(
    RESULT_FOLDER / "sampling_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.1-L11\n")
    f.write("Stability Under Sampling\n")
    f.write("=" * 60 + "\n\n")

    for s in summary:

        f.write(
            f"{s['SampleSize']:>9,d}   "
            f"{s['MeanError']:.8f}   "
            f"{s['StdError']:.8f}   "
            f"{s['CorrelationError']:.8f}\n"
        )

# ============================================================
# CERTIFICATE
# ============================================================

stable = (
    summary_df["CorrelationError"].max() < 0.01
)

with open(
    RESULT_FOLDER / "scientific_certificate.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Maximum mean error        : {summary_df['MeanError'].max():.8f}\n")
    f.write(f"Maximum std error         : {summary_df['StdError'].max():.8f}\n")
    f.write(f"Maximum correlation error : {summary_df['CorrelationError'].max():.8f}\n\n")

    if stable:
        f.write("Conclusion:\n")
        f.write("Observable statistics are stable under sampling.\n")
    else:
        f.write("Conclusion:\n")
        f.write("Sampling effects were detected.\n")

print("\nResults saved to:")
print(RESULT_FOLDER)
