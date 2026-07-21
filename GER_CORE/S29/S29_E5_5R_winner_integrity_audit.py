"""
============================================================
GER S29-E5.5R
Winner Integrity Audit
============================================================

Purpose
-------
Final scientific audit of the scaling laws identified in S29-E5.

This experiment DOES NOT re-fit models and DOES NOT choose
new winners.

The sole objective is to verify whether the OFFICIAL winners
selected in S29-E5.2 remain scientifically valid after:

    • bootstrap validation (E5.3)
    • robustness audit (E5.4)
    • numerical pathology audit (E5.5)

Outputs
-------

winner_integrity.csv

winner_validation_report.txt

scientific_consistency_report.txt

final_scientific_certificate.txt
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# GOOGLE DRIVE
# ============================================================

DRIVE = Path("/content/drive/MyDrive")

if not DRIVE.exists():
    raise RuntimeError("Google Drive not mounted.")

print("[OK] Google Drive detected.")

# ============================================================
# INPUTS
# ============================================================

E52 = (
    DRIVE
    / "GER_RESULTS"
    / "S29_E5.2"
)

E53 = (
    DRIVE
    / "GER_RESULTS"
    / "S29_E5.3"
    / "massive_validation"
)

E54 = (
    DRIVE
    / "GER_RESULTS"
    / "S29_E5.4"
    / "bootstrap_robustness_audit"
)

E55 = (
    DRIVE
    / "GER_RESULTS"
    / "S29_E5.5"
    / "numerical_pathology_audit"
)

OUTPUT = (
    DRIVE
    / "GER_RESULTS"
    / "S29_E5.5R"
    / "winner_integrity_audit"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)

print("[OK] E5.2 :", E52)
print("[OK] E5.3 :", E53)
print("[OK] E5.4 :", E54)
print("[OK] E5.5 :", E55)
print("[OK] Output:", OUTPUT)

# ============================================================
# REQUIRED FILES
# ============================================================

BEST_MODELS = E52 / "best_models.csv"

BOOTSTRAP = E53 / "bootstrap_results.jsonl"

PAIR_QUALITY = E54 / "pair_quality_report.csv"

ROBUST = E54 / "robust_statistics.csv"

MODEL_STABILITY = E55 / "model_stability.csv"

# ============================================================
# OUTPUT FILES
# ============================================================

WINNER_TABLE = OUTPUT / "winner_integrity.csv"

VALIDATION_REPORT = (
    OUTPUT
    / "winner_validation_report.txt"
)

CONSISTENCY_REPORT = (
    OUTPUT
    / "scientific_consistency_report.txt"
)

CERTIFICATE = (
    OUTPUT
    / "final_scientific_certificate.txt"
)

# ============================================================
# LOAD DATA
# ============================================================

best_df = pd.read_csv(BEST_MODELS)

pair_quality_df = pd.read_csv(PAIR_QUALITY)

robust_df = pd.read_csv(ROBUST)

model_stability_df = pd.read_csv(MODEL_STABILITY)

records = []

with open(BOOTSTRAP) as f:

    for line in f:

        line = line.strip()

        if line:

            records.append(json.loads(line))

print()

print("=" * 60)
print("GER")
print("S29-E5.5R")
print("Winner Integrity Audit")
print("=" * 60)

print()

print("Official winners :", len(best_df))
print("Bootstrap pairs  :", len(records))

winner_rows = []

print()
print("Validating official winners...")
print()
# ============================================================
# OFFICIAL WINNER VALIDATION
# ============================================================

for _, winner in best_df.iterrows():

    pair = winner["Pair"]
    official_model = winner["BestModel"]

    print(pair)

    # --------------------------------------------------------
    # Bootstrap record
    # --------------------------------------------------------

    record = None

    for r in records:

        if r["pair"] == pair:

            record = r
            break

    if record is None:

        winner_rows.append(
            {
                "Pair": pair,
                "OfficialModel": official_model,
                "BootstrapFound": False,
                "ValidStatistics": False,
                "ExtremeR2": True,
                "ParameterExplosion": True,
                "BootstrapStable": False,
                "QualityIndex": np.nan,
                "Status": "INVALID",
                "Reason": "Bootstrap record not found",
            }
        )

        continue

    # --------------------------------------------------------
    # Model statistics
    # --------------------------------------------------------

    model_data = record["models"].get(
        official_model
    )

    if model_data is None:

        winner_rows.append(
            {
                "Pair": pair,
                "OfficialModel": official_model,
                "BootstrapFound": True,
                "ValidStatistics": False,
                "ExtremeR2": True,
                "ParameterExplosion": True,
                "BootstrapStable": False,
                "QualityIndex": np.nan,
                "Status": "INVALID",
                "Reason": "Winner model missing",
            }
        )

        continue

    # --------------------------------------------------------
    # Statistics validation
    # --------------------------------------------------------

    valid_statistics = True

    extreme_r2 = False

    parameter_explosion = False

    for parameter, stats in model_data.items():

        values = [
            stats.get("mean"),
            stats.get("median"),
            stats.get("std"),
            stats.get("q025"),
            stats.get("q975"),
        ]

        if any(v is None for v in values):

            valid_statistics = False

        if any(not np.isfinite(v) for v in values):

            valid_statistics = False

        median = stats.get("median", np.nan)

        if np.isfinite(median):

            if median < -100:

                extreme_r2 = True

        if parameter != "R2":

            for value in values:

                if np.isfinite(value):

                    if abs(value) > 1e12:

                        parameter_explosion = True

# --------------------------------------------------------
# Pair quality
# --------------------------------------------------------

q = pair_quality_df.loc[
    (pair_quality_df["X"] == winner["X"])
    &
    (pair_quality_df["Y"] == winner["Y"])
]

if len(q):

    quality = float(
        q.iloc[0]["QualityIndex"]
    )

else:

    quality = np.nan

    bootstrap_stable = (
        np.isfinite(quality)
        and
        quality >= 70
    )

    # --------------------------------------------------------
    # Stability summary
    # --------------------------------------------------------

    if (
        valid_statistics
        and
        not extreme_r2
        and
        not parameter_explosion
        and
        bootstrap_stable
    ):

        status = "VALID"

        reason = "Winner validated"

    elif (
        valid_statistics
        and
        not parameter_explosion
    ):

        status = "VALID WITH WARNING"

        warnings = []

        if extreme_r2:
            warnings.append("Extreme R²")

        if not bootstrap_stable:
            warnings.append("Low bootstrap quality")

        reason = "; ".join(warnings)

    else:

        status = "INVALID"

        problems = []

        if not valid_statistics:
            problems.append("Invalid statistics")

        if parameter_explosion:
            problems.append("Parameter explosion")

        if extreme_r2:
            problems.append("Extreme R²")

        reason = "; ".join(problems)

    winner_rows.append(
        {
            "Pair": pair,
            "OfficialModel": official_model,
            "BootstrapFound": True,
            "ValidStatistics": valid_statistics,
            "ExtremeR2": extreme_r2,
            "ParameterExplosion": parameter_explosion,
            "BootstrapStable": bootstrap_stable,
            "QualityIndex": quality,
            "Status": status,
            "Reason": reason,
        }
    )
  # ============================================================
# RESULTS
# ============================================================

winner_df = pd.DataFrame(winner_rows)

winner_df.to_csv(
    WINNER_TABLE,
    index=False,
)

# ============================================================
# GLOBAL COUNTS
# ============================================================

total = len(winner_df)

valid = int(
    np.sum(
        winner_df["Status"] == "VALID"
    )
)

warning = int(
    np.sum(
        winner_df["Status"] == "VALID WITH WARNING"
    )
)

invalid = int(
    np.sum(
        winner_df["Status"] == "INVALID"
    )
)

stable_bootstrap = int(
    winner_df["BootstrapStable"].sum()
)

invalid_statistics = total - int(
    winner_df["ValidStatistics"].sum()
)

extreme_r2 = int(
    winner_df["ExtremeR2"].sum()
)

parameter_explosions = int(
    winner_df["ParameterExplosion"].sum()
)

# ============================================================
# WINNER VALIDATION REPORT
# ============================================================

with open(
    VALIDATION_REPORT,
    "w",
) as f:

    f.write("GER S29-E5.5R\n")
    f.write("Winner Validation Report\n\n")

    f.write(
        f"Official winners : {total}\n"
    )

    f.write(
        f"Validated        : {valid}\n"
    )

    f.write(
        f"Warnings         : {warning}\n"
    )

    f.write(
        f"Invalid          : {invalid}\n\n"
    )

    f.write(
        f"Bootstrap stable : {stable_bootstrap}\n"
    )

    f.write(
        f"Invalid statistics : {invalid_statistics}\n"
    )

    f.write(
        f"Extreme R²         : {extreme_r2}\n"
    )

    f.write(
        f"Parameter explosions : {parameter_explosions}\n\n"
    )

    f.write("Pair Summary\n")
    f.write("-" * 60 + "\n")

    for _, row in winner_df.iterrows():

        f.write(
            f"{row['Pair']}\n"
        )

        f.write(
            f"Winner : {row['OfficialModel']}\n"
        )

        f.write(
            f"Status : {row['Status']}\n"
        )

        f.write(
            f"Reason : {row['Reason']}\n\n"
        )

# ============================================================
# SCIENTIFIC CONSISTENCY
# ============================================================

with open(
    CONSISTENCY_REPORT,
    "w",
) as f:

    f.write("GER S29-E5.5R\n")
    f.write("Scientific Consistency Report\n\n")

    if invalid == 0:

        f.write(
            "No official scaling law became invalid.\n\n"
        )

    else:

        f.write(
            f"{invalid} official scaling law(s) became invalid.\n\n"
        )

    if warning == 0:

        f.write(
            "No numerical warning detected.\n"
        )

    else:

        f.write(
            f"{warning} scaling law(s) require numerical caution.\n"
        )

    f.write("\n")

    f.write(
        "The audit evaluated only the integrity of "
        "the official winners selected in S29-E5.2.\n"
    )

    f.write(
        "No alternative model selection was performed.\n"
    )
  # ============================================================
# FINAL SCIENTIFIC CERTIFICATE
# ============================================================

with open(
    CERTIFICATE,
    "w",
) as f:

    f.write("GER S29-E5.5R\n")
    f.write("FINAL SCIENTIFIC CERTIFICATE\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        f"Official winners evaluated : {total}\n"
    )

    f.write(
        f"Validated                  : {valid}\n"
    )

    f.write(
        f"Validated with warnings    : {warning}\n"
    )

    f.write(
        f"Invalid                    : {invalid}\n\n"
    )

    if invalid == 0:

        f.write(
            "Scientific Integrity : PASS\n"
        )

    else:

        f.write(
            "Scientific Integrity : FAIL\n"
        )

    if warning == 0:

        f.write(
            "Numerical Robustness : PASS\n"
        )

    else:

        f.write(
            "Numerical Robustness : WARNING\n"
        )

    if stable_bootstrap == total:

        f.write(
            "Bootstrap Stability  : PASS\n"
        )

    else:

        f.write(
            "Bootstrap Stability  : WARNING\n"
        )

    f.write("\n")

    if invalid == 0 and warning == 0:

        verdict = (
            "OFFICIAL SCALING LAWS FULLY VALIDATED"
        )

    elif invalid == 0:

        verdict = (
            "OFFICIAL SCALING LAWS VALIDATED "
            "WITH NUMERICAL WARNINGS"
        )

    else:

        verdict = (
            "SCIENTIFIC REVIEW REQUIRED"
        )

    f.write(
        f"FINAL VERDICT : {verdict}\n"
    )

# ============================================================
# FINAL SCREEN REPORT
# ============================================================

print()

print("=" * 70)
print("Winner integrity audit completed.")
print("=" * 70)

print()

print(f"Official winners : {total}")
print(f"Validated        : {valid}")
print(f"Warnings         : {warning}")
print(f"Invalid          : {invalid}")

print()

print("Generated files")

print(" ", WINNER_TABLE)
print(" ", VALIDATION_REPORT)
print(" ", CONSISTENCY_REPORT)
print(" ", CERTIFICATE)

print()

print("Experiment completed.")

# ============================================================
# END
# ============================================================
