"""
============================================================
GER
S29-E6.2.5
OCCUPANCY STRUCTURE OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Characterize the occupancy structure of the certified
Observable Space.

Using the relational organization established in
S29-E6.2.4, this experiment quantifies how the certified
observables occupy the intrinsic geometric space.

The analysis measures occupancy continuity, structural
coverage, radial filling and geometric fragmentation without
introducing arbitrary parameters.

This experiment establishes the first occupancy model of the
Observable Space and provides the structural basis for the
subsequent Stability and Outlier analyses of the E6.2
series.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_5_occupancy_structure

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
    / "E6_2_4_RelationalOrganization"
    / "relational_profile.csv"
)

LEVELS_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_4_RelationalOrganization"
    / "structural_levels.csv"
)

CERTIFICATE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_4_RelationalOrganization"
    / "relational_certificate.json"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_5_OccupancyStructure"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# GER Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.5")
print("Occupancy Structure of the Observable Space")
print("=" * 70)


# ============================================================
# Load data
# ============================================================

profile = pd.read_csv(PROFILE_FILE)

levels = pd.read_csv(LEVELS_FILE)

with open(
    CERTIFICATE_FILE,
    "r",
    encoding="utf-8"
) as f:

    certificate = json.load(f)

nucleus = certificate["geometric_nucleus"]

print("[OK] relational_profile.csv")
print("[OK] structural_levels.csv")
print("[OK] relational_certificate.json")

print()

print(f"Observables : {len(profile)}")
print(f"Geometric Nucleus : {nucleus}")

print()

# ============================================================
# Occupancy Profile
# ============================================================

occupancy = profile.copy()

max_distance = occupancy["DistanceToNucleus"].max()

if max_distance == 0:

    occupancy["NormalizedDistance"] = 0.0

else:

    occupancy["NormalizedDistance"] = (

        occupancy["DistanceToNucleus"] /
        max_distance

    )


# ============================================================
# Structural Coverage
# ============================================================

occupied_levels = int(

    (levels["Observables"] > 0).sum()

)

total_levels = int(len(levels))

coverage = occupied_levels / total_levels


# ============================================================
# Radial Continuity
# ============================================================

radius = occupancy["DistanceToNucleus"].to_numpy()

radius = np.sort(radius)

radial_gap = np.diff(radius)

if len(radial_gap) > 0:

    mean_gap = float(np.mean(radial_gap))
    std_gap = float(np.std(radial_gap))
    max_gap = float(np.max(radial_gap))

else:

    mean_gap = 0.0
    std_gap = 0.0
    max_gap = 0.0


# ============================================================
# Occupancy Index
# ============================================================

occupancy_index = (

    coverage *

    (1.0 / (1.0 + mean_gap))

)

occupancy["OccupancyIndex"] = occupancy_index


# ============================================================
# Occupancy Profile
# ============================================================

occupancy.to_csv(

    OUT / "occupancy_profile.csv",

    index=False

)


# ============================================================
# Occupancy Summary
# ============================================================

summary = pd.DataFrame({

    "Metric":[

        "Observables",
        "OccupiedLevels",
        "TotalLevels",
        "Coverage",
        "MeanRadialGap",
        "StdRadialGap",
        "MaximumRadialGap",
        "OccupancyIndex"

    ],

    "Value":[

        len(occupancy),
        occupied_levels,
        total_levels,
        coverage,
        mean_gap,
        std_gap,
        max_gap,
        occupancy_index

    ]

})

summary.to_csv(

    OUT / "occupancy_summary.csv",

    index=False

)


# ============================================================
# Radial Gaps
# ============================================================

gaps = pd.DataFrame({

    "GapID": np.arange(1, len(radial_gap)+1),

    "Gap": radial_gap

})

gaps.to_csv(

    OUT / "radial_gaps.csv",

    index=False

)


print("=" * 70)
print("Occupancy Structure Summary")
print("=" * 70)

print(f"Geometric Nucleus        : {nucleus}")
print(f"Occupied Levels          : {occupied_levels}")
print(f"Coverage                : {coverage:.6f}")
print(f"Mean Radial Gap         : {mean_gap:.6f}")
print(f"Maximum Radial Gap      : {max_gap:.6f}")
print(f"Occupancy Index         : {occupancy_index:.6f}")
print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.5",

    "title": "Occupancy Structure of the Observable Space",

    "geometric_nucleus": nucleus,

    "observables": int(len(occupancy)),

    "occupied_levels": occupied_levels,

    "total_levels": total_levels,

    "coverage": float(coverage),

    "mean_radial_gap": mean_gap,

    "std_radial_gap": std_gap,

    "maximum_radial_gap": max_gap,

    "occupancy_index": float(occupancy_index)

}

with open(

    OUT / "occupancy_certificate.json",

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

    OUT / "occupancy_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("GER\n")
    f.write("S29-E6.2.5\n")
    f.write("Occupancy Structure of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Global Statistics\n")
    f.write("-----------------\n\n")

    f.write(f"Geometric Nucleus        : {nucleus}\n")
    f.write(f"Observables              : {len(occupancy)}\n")
    f.write(f"Occupied Levels          : {occupied_levels}\n")
    f.write(f"Total Levels             : {total_levels}\n")
    f.write(f"Coverage                 : {coverage:.6f}\n")
    f.write(f"Mean Radial Gap          : {mean_gap:.6f}\n")
    f.write(f"Std Radial Gap           : {std_gap:.6f}\n")
    f.write(f"Maximum Radial Gap       : {max_gap:.6f}\n")
    f.write(f"Occupancy Index          : {occupancy_index:.6f}\n")

    f.write("\n")

    f.write("Occupancy by Structural Level\n")
    f.write("-----------------------------\n\n")

    for _, row in levels.iterrows():

        f.write(
            f"Level {int(row['Level'])}: "
            f"{int(row['Observables'])} observables | "
            f"Mean Distance={row['MeanDistance']:.6f} | "
            f"Mean Density={row['MeanDensity']:.6f} | "
            f"Mean Concentration={row['MeanConcentration']:.6f}\n"
        )

    f.write("\n")

    f.write("Conclusion\n")
    f.write("----------\n")

    f.write(
        "This experiment characterizes the global occupancy "
        "structure of the certified Observable Space. "
        "The resulting occupancy metrics quantify how the "
        "relational hierarchy fills the intrinsic geometric "
        "space, providing a parameter-free description of "
        "coverage, radial continuity and structural "
        "fragmentation. These results establish the "
        "observational basis for the Stability Analysis "
        "developed in the next experiment of the E6.2 series.\n"
    )


# ============================================================
# End
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
    pass


if __name__ == "__main__":
    main()
