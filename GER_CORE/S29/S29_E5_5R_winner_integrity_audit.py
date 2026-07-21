"""
============================================================
GER S29-E5.5R
Winner Integrity Audit
============================================================

Final audit of the OFFICIAL scaling laws selected in S29-E5.2.

This experiment NEVER searches for a new winner.
It only validates the official winner of each observable pair
using the bootstrap statistics generated in S29-E5.3 and the
robustness audit produced in S29-E5.4.
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
# INPUT FOLDERS
# ============================================================

E52 = DRIVE / "GER_RESULTS" / "S29_E5.2"

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

# ============================================================
# INPUT FILES
# ============================================================

BEST_MODELS = E52 / "best_models.csv"

BOOTSTRAP = E53 / "bootstrap_results.jsonl"

PAIR_QUALITY = E54 / "pair_quality_report.csv"

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

bootstrap_records = []

with open(BOOTSTRAP) as f:

    for line in f:

        line = line.strip()

        if line:

            bootstrap_records.append(
                json.loads(line)
            )

print()

print("=" * 60)
print("GER")
print("S29-E5.5R")
print("Winner Integrity Audit")
print("=" * 60)

print()

print("Official winners :", len(best_df))
print("Bootstrap records:", len(bootstrap_records))

# ============================================================
# INDEX BOOTSTRAP RECORDS
# ============================================================

bootstrap_index = {}

for record in bootstrap_records:

    key = (
        record["X"],
        record["Y"],
    )

    bootstrap_index[key] = record

winner_rows = []

print()
print("Validating official winners...")
print()
# ============================================================
# OFFICIAL WINNER VALIDATION
# ============================================================

for _, winner in best_df.iterrows():

    x = winner["X"]
    y = winner["Y"]

    pair = f"{x} ↔ {y}"

    official_model = winner["BestModel"]

    print(pair)

    record = bootstrap_index.get((x, y))

    if record is None:

        winner_rows.append(
            {
                "X": x,
                "Y": y,
                "OfficialModel": official_model,
                "BootstrapFound": False,
                "ValidStatistics": False,
                "ParameterExplosion": False,
                "BootstrapStable": False,
                "QualityIndex": np.nan,
                "Status": "INVALID",
                "Reason": "Bootstrap record not found",
            }
        )

        continue

    # --------------------------------------------------------
    # Winner consistency
    # --------------------------------------------------------

    bootstrap_winner = record["winner_model"]

    same_winner = (
        bootstrap_winner == official_model
    )

    # --------------------------------------------------------
    # R² statistics
    # --------------------------------------------------------

    r2_stats = record["r2_statistics"].get(
        official_model
    )

    if r2_stats is None:

        winner_rows.append(
            {
                "X": x,
                "Y": y,
                "OfficialModel": official_model,
                "BootstrapFound": True,
                "ValidStatistics": False,
                "ParameterExplosion": False,
                "BootstrapStable": False,
                "QualityIndex": np.nan,
                "Status": "INVALID",
                "Reason": "Missing R² statistics",
            }
        )

        continue

    valid_statistics = True

    for key in (
        "mean",
        "median",
        "std",
        "q025",
        "q975",
    ):

        value = r2_stats.get(key)

        if value is None:

            valid_statistics = False

        elif not np.isfinite(value):

            valid_statistics = False

    # --------------------------------------------------------
    # Parameter statistics
    # --------------------------------------------------------

    parameter_explosion = False

    parameters = record["parameter_statistics"].get(
        official_model,
        [],
    )

    for parameter in parameters:

        for key in (
            "mean",
            "median",
            "std",
            "q025",
            "q975",
        ):

            value = parameter.get(key)

            if value is None:

                continue

            if np.isfinite(value):

                if abs(value) > 1e12:

                    parameter_explosion = True

    # --------------------------------------------------------
    # Pair quality
    # --------------------------------------------------------

    q = pair_quality_df.loc[
        (pair_quality_df["X"] == x)
        &
        (pair_quality_df["Y"] == y)
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
    # Final classification
    # --------------------------------------------------------

    if (
        same_winner
        and
        valid_statistics
        and
        not parameter_explosion
        and
        bootstrap_stable
    ):

        status = "VALID"

        reason = "Official winner confirmed"

    elif (
        valid_statistics
        and
        not parameter_explosion
    ):

        status = "VALID WITH WARNING"

        warnings = []

        if not same_winner:
            warnings.append(
                "Bootstrap selected another winner"
            )

        if not bootstrap_stable:
            warnings.append(
                "Low bootstrap quality"
            )

        reason = "; ".join(warnings)

    else:

        status = "INVALID"

        problems = []

        if not valid_statistics:
            problems.append(
                "Invalid statistics"
            )

        if parameter_explosion:
            problems.append(
                "Parameter explosion"
            )

        if not same_winner:
            problems.append(
                "Winner mismatch"
            )

        reason = "; ".join(problems)

    winner_rows.append(
        {
            "X": x,
            "Y": y,
            "OfficialModel": official_model,
            "BootstrapWinner": bootstrap_winner,
            "WinnerConfirmed": same_winner,
            "BootstrapFound": True,
            "ValidStatistics": valid_statistics,
            "ParameterExplosion": parameter_explosion,
            "BootstrapStable": bootstrap_stable,
            "QualityIndex": quality,
            "Status": status,
            "Reason": reason,
        }
    )

# ============================================================
# RESULTS TABLE
# ============================================================

winner_df = pd.DataFrame(winner_rows)

winner_df.to_csv(
    WINNER_TABLE,
    index=False,
)

total = len(winner_df)

valid = int(
    (winner_df["Status"] == "VALID").sum()
)

warning = int(
    (winner_df["Status"] == "VALID WITH WARNING").sum()
)

invalid = int(
    (winner_df["Status"] == "INVALID").sum()
)

print()
print("Validation finished.")
print()
# ============================================================
# WINNER VALIDATION REPORT
# ============================================================

with open(
    VALIDATION_REPORT,
    "w",
) as f:

    f.write("GER S29-E5.5R\n")
    f.write("Winner Validation Report\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Official winners : {total}\n")
    f.write(f"Validated        : {valid}\n")
    f.write(f"Warnings         : {warning}\n")
    f.write(f"Invalid          : {invalid}\n\n")

    for _, row in winner_df.iterrows():

        f.write(
            f"{row['X']} ↔ {row['Y']}\n"
        )

        f.write(
            f"Official Winner : {row['OfficialModel']}\n"
        )

        f.write(
            f"Bootstrap Winner: {row['BootstrapWinner']}\n"
        )

        f.write(
            f"Status          : {row['Status']}\n"
        )

        f.write(
            f"Reason          : {row['Reason']}\n"
        )

        f.write(
            f"Quality Index   : {row['QualityIndex']:.2f}\n"
        )

        f.write("\n")

# ============================================================
# SCIENTIFIC CONSISTENCY REPORT
# ============================================================

with open(
    CONSISTENCY_REPORT,
    "w",
) as f:

    f.write("GER S29-E5.5R\n")
    f.write("Scientific Consistency Report\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        "Objective\n"
    )

    f.write(
        "---------\n"
    )

    f.write(
        "Evaluate whether the official scaling laws "
        "selected in S29-E5.2 remain scientifically "
        "valid after bootstrap validation.\n\n"
    )

    f.write(
        f"Validated laws : {valid}/{total}\n"
    )

    f.write(
        f"Laws with warnings : {warning}\n"
    )

    f.write(
        f"Invalid laws : {invalid}\n\n"
    )

    if invalid == 0:

        f.write(
            "No official scaling law became invalid.\n"
        )

    else:

        f.write(
            "One or more official scaling laws "
            "failed the integrity audit.\n"
        )

    f.write(
        "\nNo alternative winner was selected.\n"
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

    if invalid == 0 and warning == 0:

        verdict = (
            "PASS"
        )

        conclusion = (
            "All official scaling laws remain "
            "scientifically valid."
        )

    elif invalid == 0:

        verdict = (
            "PASS WITH WARNINGS"
        )

        conclusion = (
            "Official scaling laws remain valid, "
            "but numerical cautions are recommended."
        )

    else:

        verdict = (
            "FAIL"
        )

        conclusion = (
            "One or more official scaling laws "
            "lost scientific validity."
        )

    f.write(
        f"Scientific Integrity : {verdict}\n\n"
    )

    f.write(
        conclusion + "\n"
    )

# ============================================================
# FINAL SUMMARY
# ============================================================

print("=" * 60)
print("Winner Integrity Audit completed.")
print("=" * 60)

print()

print("Validated :", valid)
print("Warnings  :", warning)
print("Invalid   :", invalid)

print()

print("Results saved to:")

print(WINNER_TABLE)
print(VALIDATION_REPORT)
print(CONSISTENCY_REPORT)
print(CERTIFICATE)

print()

print("Experiment completed.")

# ============================================================
# END
# ============================================================
