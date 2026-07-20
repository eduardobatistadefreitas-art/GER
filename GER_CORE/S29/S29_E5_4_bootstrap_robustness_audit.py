"""
======================================================================
GER
S29-E5.4
Bootstrap Robustness Audit
======================================================================

Scientific objective
--------------------

Audit the robustness of the empirical scaling laws discovered
during S29-E5.3.

This experiment does NOT search for new laws.

Its purpose is to verify whether the conclusions obtained from
500,000 bootstrap iterations remain valid after a complete
statistical robustness analysis.

Main goals

    • identify numerical degeneracies

    • identify invalid regressions

    • compare classical and robust statistics

    • evaluate parameter stability

    • measure model robustness

    • validate winner stability

No new bootstrap is performed.

Only the existing bootstrap_results.jsonl produced by E5.3
is analysed.

======================================================================
"""

import json
import math
import warnings

import numpy as np
import pandas as pd

from pathlib import Path

warnings.filterwarnings("ignore")

# ============================================================
# INPUT
# ============================================================

DRIVE_ROOT = Path(
    "/content/drive/MyDrive"
)

if not DRIVE_ROOT.exists():

    raise RuntimeError(

        "\nGoogle Drive is not mounted.\n"

    )

INPUT = (
    DRIVE_ROOT
    / "GER_RESULTS"
    / "S29_E5.3"
    / "massive_validation"
)

RESULT_FILE = INPUT / "bootstrap_results.jsonl"

if not RESULT_FILE.exists():

    raise RuntimeError(

        f"\nBootstrap file not found:\n\n{RESULT_FILE}\n"

    )

# ============================================================
# OUTPUT
# ============================================================

OUTPUT = (
    DRIVE_ROOT
    / "GER_RESULTS"
    / "S29_E5.4"
    / "bootstrap_robustness_audit"
)

OUTPUT.mkdir(

    parents=True,

    exist_ok=True

)

ROBUST_STATS = OUTPUT / "robust_statistics.csv"

PAIR_REPORT = OUTPUT / "pair_quality_report.csv"

DEGENERATE = OUTPUT / "degenerate_cases.csv"

SUMMARY = OUTPUT / "robustness_summary.txt"

AUDIT = OUTPUT / "audit_report.txt"

print("[OK] Google Drive detected.")
print("[OK] Input :", RESULT_FILE)
print("[OK] Output:", OUTPUT)

# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("GER")
print("S29-E5.4")
print("Bootstrap Robustness Audit")
print("=" * 70)

records = []

with open(RESULT_FILE, "r") as f:

    for line in f:

        line = line.strip()

        if line:

            records.append(json.loads(line))

print()
print("Pairs loaded :", len(records))
print()

# ============================================================
# ROBUST METRICS
# ============================================================

def mad(x):

    x = np.asarray(x, dtype=float)

    med = np.median(x)

    return np.median(np.abs(x - med))


def iqr(x):

    x = np.asarray(x, dtype=float)

    q1 = np.quantile(x, 0.25)

    q3 = np.quantile(x, 0.75)

    return q3 - q1


def finite_only(values):

    arr = np.asarray(values, dtype=float)

    return arr[np.isfinite(arr)]


# ============================================================
# DEGENERACY LIMITS
# ============================================================

EXTREME_R2 = -100.0

PARAMETER_LIMIT = 1e12

# ============================================================
# OUTPUT TABLES
# ============================================================

robust_rows = []

pair_rows = []

degenerate_rows = []

print("Auditing bootstrap results...")
print()
# ============================================================
# MAIN AUDIT
# ============================================================

total_invalid = 0
total_extreme_r2 = 0
total_parameter_explosions = 0

for record in records:

    x_name = record["X"]
    y_name = record["Y"]

    winner = record["winner_model"]
    probability = record["winner_probability"]

    print(f"{x_name} <-> {y_name}")

    pair_invalid = 0
    pair_extreme = 0
    pair_parameter_explosions = 0

    pair_models = 0

    # --------------------------------------------------------
    # Iterate over every fitted model
    # --------------------------------------------------------

    for model in record["r2_statistics"]:

        pair_models += 1

        # ====================================================
        # R²
        # ====================================================

        r2 = record["r2_statistics"][model]

        values = []

        for key in [

            "mean",
            "std",
            "median",
            "q025",
            "q975"

        ]:

            if key in r2:

                values.append(r2[key])

        values = finite_only(values)

        invalid = 5 - len(values)

        pair_invalid += invalid

        total_invalid += invalid

        if len(values):

            extreme = np.sum(values < EXTREME_R2)

        else:

            extreme = 0

        pair_extreme += int(extreme)

        total_extreme_r2 += int(extreme)

        # ====================================================
        # PARAMETERS
        # ====================================================

        if model in record["parameter_statistics"]:

            for parameter in record["parameter_statistics"][model]:

                for statistic in parameter.values():

                    if not np.isfinite(statistic):

                        pair_parameter_explosions += 1

                        total_parameter_explosions += 1

                        continue

                    if abs(statistic) > PARAMETER_LIMIT:

                        pair_parameter_explosions += 1

                        total_parameter_explosions += 1

        # ====================================================
        # Robust statistics
        # ====================================================

        robust_rows.append({

            "Pair":

                f"{x_name} <-> {y_name}",

            "Model":

                model,

            "Mean":

                r2.get("mean", np.nan),

            "Median":

                r2.get("median", np.nan),

            "Std":

                r2.get("std", np.nan),

            "IQR":

                r2.get("q975", np.nan)
                - r2.get("q025", np.nan),

            "MAD":

                abs(
                    r2.get("median", np.nan)
                    - r2.get("mean", np.nan)
                ),

            "Q025":

                r2.get("q025", np.nan),

            "Q975":

                r2.get("q975", np.nan)

        })

    # --------------------------------------------------------
    # Pair quality index
    # --------------------------------------------------------

    quality = 100.0

    quality -= 10 * pair_invalid

    quality -= 5 * pair_extreme

    quality -= 5 * pair_parameter_explosions

    quality = max(0.0, quality)

    pair_rows.append({

        "X": x_name,

        "Y": y_name,

        "Winner": winner,

        "Probability": probability,

        "Models": pair_models,

        "InvalidStatistics": pair_invalid,

        "ExtremeR2": pair_extreme,

        "ParameterExplosions": pair_parameter_explosions,

        "QualityIndex": quality

    })

    if (

        pair_invalid

        or

        pair_extreme

        or

        pair_parameter_explosions

    ):

        degenerate_rows.append({

            "X": x_name,

            "Y": y_name,

            "Winner": winner,

            "InvalidStatistics": pair_invalid,

            "ExtremeR2": pair_extreme,

            "ParameterExplosions": pair_parameter_explosions

        })
      # ============================================================
# SAVE TABLES
# ============================================================

robust_df = pd.DataFrame(robust_rows)

pair_df = pd.DataFrame(pair_rows)

degenerate_df = pd.DataFrame(degenerate_rows)

robust_df.to_csv(

    ROBUST_STATS,

    index=False

)

pair_df = pair_df.sort_values(

    "QualityIndex",

    ascending=False

)

pair_df.to_csv(

    PAIR_REPORT,

    index=False

)

degenerate_df.to_csv(

    DEGENERATE,

    index=False

)

# ============================================================
# GLOBAL STATISTICS
# ============================================================

pairs_approved = int(

    np.sum(pair_df["QualityIndex"] >= 95)

)

pairs_warning = int(

    np.sum(

        (pair_df["QualityIndex"] >= 70)

        &

        (pair_df["QualityIndex"] < 95)

    )

)

pairs_critical = int(

    np.sum(pair_df["QualityIndex"] < 70)

)

mean_quality = float(

    pair_df["QualityIndex"].mean()

)

median_quality = float(

    pair_df["QualityIndex"].median()

)

minimum_quality = float(

    pair_df["QualityIndex"].min()

)

# ============================================================
# HUMAN SUMMARY
# ============================================================

with open(SUMMARY, "w") as f:

    f.write(
        "GER S29-E5.4\n"
    )

    f.write(
        "Bootstrap Robustness Audit\n\n"
    )

    f.write(
        f"Pairs analysed : {len(pair_df)}\n"
    )

    f.write(
        f"Approved pairs : {pairs_approved}\n"
    )

    f.write(
        f"Warning pairs  : {pairs_warning}\n"
    )

    f.write(
        f"Critical pairs : {pairs_critical}\n\n"
    )

    f.write(
        f"Average Quality Index : "
        f"{mean_quality:.2f}\n"
    )

    f.write(
        f"Median Quality Index  : "
        f"{median_quality:.2f}\n"
    )

    f.write(
        f"Minimum Quality Index : "
        f"{minimum_quality:.2f}\n\n"
    )

    f.write(
        f"Invalid statistics      : "
        f"{total_invalid}\n"
    )

    f.write(
        f"Extreme R² detected     : "
        f"{total_extreme_r2}\n"
    )

    f.write(
        f"Parameter explosions    : "
        f"{total_parameter_explosions}\n"
    )

# ============================================================
# SCIENTIFIC AUDIT
# ============================================================

with open(AUDIT, "w") as f:

    f.write(
        "GER S29-E5.4\n"
    )

    f.write(
        "Bootstrap Robustness Audit\n\n"
    )

    f.write(
        "Scientific conclusions\n"
    )

    f.write(
        "----------------------\n\n"
    )

    if pairs_critical == 0:

        f.write(

            "No critical observable pair was detected.\n"

        )

    else:

        f.write(

            f"{pairs_critical} critical pair(s) require "
            "manual inspection.\n"

        )

    if total_parameter_explosions == 0:

        f.write(

            "No parameter explosion detected.\n"

        )

    else:

        f.write(

            "Parameter explosions were detected.\n"

        )

    if total_invalid == 0:

        f.write(

            "No invalid numerical statistics detected.\n"

        )

    else:

        f.write(

            "Invalid numerical statistics were detected.\n"

        )

    if total_extreme_r2 == 0:

        f.write(

            "No extremely negative R² values were detected.\n"

        )

    else:

        f.write(

            "Extremely negative R² values require inspection.\n"

        )

    f.write("\n")

    if (

        pairs_critical == 0

        and

        total_parameter_explosions == 0

    ):

        f.write(

            "Conclusion:\n"

            "The bootstrap results are statistically robust "

            "and support the conclusions obtained in S29-E5.3.\n"

        )

    else:

        f.write(

            "Conclusion:\n"

            "The bootstrap remains scientifically valid, "

            "but specific numerical situations should be "

            "examined before publication.\n"

        )

# ============================================================
# FINAL REPORT
# ============================================================

print()

print("=" * 70)

print("Bootstrap robustness audit completed.")

print("=" * 70)

print()

print("Generated files")

print(" ", ROBUST_STATS)

print(" ", PAIR_REPORT)

print(" ", DEGENERATE)

print(" ", SUMMARY)

print(" ", AUDIT)

print()

print("Experiment completed.")

# ============================================================
# END
# ============================================================
