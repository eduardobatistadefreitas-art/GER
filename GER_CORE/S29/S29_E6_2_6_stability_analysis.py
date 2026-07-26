"""
============================================================
GER
S29-E6.2.6
STABILITY ANALYSIS OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Evaluate the intrinsic structural stability of the certified
Observable Space.

This experiment measures the robustness of the relational
organization obtained in previous experiments by analysing
distance distributions, occupancy regularity and structural
balance.

No perturbations, simulations or arbitrary parameters are
introduced. Stability is inferred exclusively from the
geometry certified by the E6.2 pipeline.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_6_stability_analysis

Author
------
Eduardo Batista de Freitas
GER Project
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd


# ============================================================
# INPUT
# ============================================================

PROFILE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_5_OccupancyStructure"
    / "occupancy_profile.csv"
)

SUMMARY_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_5_OccupancyStructure"
    / "occupancy_summary.csv"
)

CERTIFICATE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_5_OccupancyStructure"
    / "occupancy_certificate.json"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_6_StabilityAnalysis"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.6")
print("Stability Analysis of the Observable Space")
print("=" * 70)


# ============================================================
# Load
# ============================================================

profile = pd.read_csv(PROFILE_FILE)

summary = pd.read_csv(SUMMARY_FILE)

with open(
    CERTIFICATE_FILE,
    "r",
    encoding="utf-8"
) as f:

    certificate = json.load(f)

nucleus = certificate["geometric_nucleus"]

print("[OK] occupancy_profile.csv")
print("[OK] occupancy_summary.csv")
print("[OK] occupancy_certificate.json")

print()

print(f"Observables : {len(profile)}")
print(f"Geometric Nucleus : {nucleus}")

print()

# ============================================================
# Distance Statistics
# ============================================================

distance = profile["DistanceToNucleus"].to_numpy()

mean_distance = float(np.mean(distance))
std_distance = float(np.std(distance))

if mean_distance > 0:

    distance_cv = std_distance / mean_distance

else:

    distance_cv = 0.0


# ============================================================
# Radial Regularity
# ============================================================

radius = np.sort(distance)

gaps = np.diff(radius)

if len(gaps) > 0:

    gap_mean = float(np.mean(gaps))
    gap_std = float(np.std(gaps))

    radial_regularity = 1.0 / (1.0 + gap_std)

else:

    gap_mean = 0.0
    gap_std = 0.0
    radial_regularity = 1.0


# ============================================================
# Structural Balance
# ============================================================

level_counts = (
    profile
    .groupby("StructuralLevel")
    .size()
    .sort_index()
)

balance_mean = float(level_counts.mean())
balance_std = float(level_counts.std(ddof=0))

if balance_mean > 0:

    balance_cv = balance_std / balance_mean

else:

    balance_cv = 0.0

structural_balance = 1.0 / (1.0 + balance_cv)


# ============================================================
# Coverage
# ============================================================

coverage = float(
    certificate["coverage"]
)


# ============================================================
# Stability Index
# ============================================================

stability_index = float(

    np.mean(

        [

            radial_regularity,
            structural_balance,
            coverage

        ]

    )

)


# ============================================================
# Stability Summary
# ============================================================

summary = pd.DataFrame({

    "Metric":[

        "Coverage",
        "MeanDistance",
        "StdDistance",
        "DistanceCV",
        "GapMean",
        "GapStd",
        "RadialRegularity",
        "StructuralBalance",
        "StabilityIndex"

    ],

    "Value":[

        coverage,
        mean_distance,
        std_distance,
        distance_cv,
        gap_mean,
        gap_std,
        radial_regularity,
        structural_balance,
        stability_index

    ]

})

summary.to_csv(

    OUT / "stability_summary.csv",

    index=False

)


# ============================================================
# Stability Profile
# ============================================================

stability = profile.copy()

stability["DistanceDeviation"] = (

    stability["DistanceToNucleus"] -
    mean_distance

)

stability["RelativeDeviation"] = (

    stability["DistanceDeviation"] /
    mean_distance

    if mean_distance > 0 else 0.0

)

stability.to_csv(

    OUT / "stability_profile.csv",

    index=False

)


print("=" * 70)
print("Stability Analysis Summary")
print("=" * 70)

print(f"Geometric Nucleus      : {nucleus}")
print(f"Coverage              : {coverage:.6f}")
print(f"Distance CV           : {distance_cv:.6f}")
print(f"Radial Regularity     : {radial_regularity:.6f}")
print(f"Structural Balance    : {structural_balance:.6f}")
print(f"Stability Index       : {stability_index:.6f}")
print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.6",

    "title": "Stability Analysis of the Observable Space",

    "geometric_nucleus": nucleus,

    "observables": int(len(profile)),

    "coverage": float(coverage),

    "mean_distance": mean_distance,

    "std_distance": std_distance,

    "distance_cv": distance_cv,

    "gap_mean": gap_mean,

    "gap_std": gap_std,

    "radial_regularity": radial_regularity,

    "structural_balance": structural_balance,

    "stability_index": stability_index

}

with open(

    OUT / "stability_certificate.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        certificate,

        f,

        indent=4

    )


# ============================================================
# Scientific Report
# ============================================================

with open(

    OUT / "stability_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("GER\n")
    f.write("S29-E6.2.6\n")
    f.write("Stability Analysis of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Global Stability Statistics\n")
    f.write("---------------------------\n\n")

    f.write(f"Geometric Nucleus      : {nucleus}\n")
    f.write(f"Observables            : {len(profile)}\n")
    f.write(f"Coverage               : {coverage:.6f}\n")
    f.write(f"Mean Distance          : {mean_distance:.6f}\n")
    f.write(f"Std Distance           : {std_distance:.6f}\n")
    f.write(f"Distance CV            : {distance_cv:.6f}\n")
    f.write(f"Mean Radial Gap        : {gap_mean:.6f}\n")
    f.write(f"Std Radial Gap         : {gap_std:.6f}\n")
    f.write(f"Radial Regularity      : {radial_regularity:.6f}\n")
    f.write(f"Structural Balance     : {structural_balance:.6f}\n")
    f.write(f"Stability Index        : {stability_index:.6f}\n")

    f.write("\n")

    f.write("Observable Deviations\n")
    f.write("---------------------\n\n")

    for _, row in stability.iterrows():

        f.write(
            f"{row['Observable']:<20}"
            f"Distance={row['DistanceToNucleus']:.6f}   "
            f"Deviation={row['DistanceDeviation']:.6f}   "
            f"Relative={row['RelativeDeviation']:.6f}\n"
        )

    f.write("\n")

    f.write("Conclusion\n")
    f.write("----------\n")

    f.write(
        "The Stability Analysis quantifies the intrinsic "
        "structural robustness of the certified Observable "
        "Space using only geometric properties derived from "
        "the E6.2 pipeline. The resulting Stability Index "
        "summarizes radial regularity, structural balance "
        "and occupancy coverage, providing a global "
        "description of the internal consistency of the "
        "observable organization without relying on external "
        "perturbations or arbitrary thresholds.\n"
    )


# ============================================================
# Final Console Summary
# ============================================================

print("=" * 70)
print("Experiment completed.")
print()
print("Results saved to:")
print(OUT)
print("=" * 70)


# ============================================================
# Main
# ============================================================

def main():
    """Main entry point."""
    pass


if __name__ == "__main__":
    main()
