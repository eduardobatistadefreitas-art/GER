"""
============================================================
GER
S29-E6.2.4
RELATIONAL ORGANIZATION OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Characterize the intrinsic relational organization of the
certified Observable Space.

Using the concentration structure established in
S29-E6.2.3, this experiment investigates how the certified
observables are organized with respect to the geometric
nucleus identified by the previous experiments.

The analysis is entirely observational and does not assume
any predefined hierarchy. Instead, the relational structure
is inferred directly from the geometric organization of the
Observable Space.

This experiment establishes the first relational map of the
Observable Space and provides the structural basis for the
subsequent Occupancy and Stability analyses of the E6.2
series.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_4_relational_organization

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
    / "E6_2_3_ConcentrationAnalysis"
    / "concentration_profile.csv"
)

DISTANCE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_2_DensityField"
    / "neighbor_matrix.csv"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_4_RelationalOrganization"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# GER Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.4")
print("Relational Organization of the Observable Space")
print("=" * 70)


# ============================================================
# Load data
# ============================================================

profile = pd.read_csv(PROFILE_FILE)
distance = pd.read_csv(
    DISTANCE_FILE,
    index_col=0
)

print("[OK] concentration_profile.csv")
print("[OK] neighbor_matrix.csv")

print()

print(f"Observables : {len(profile)}")

print()

# ============================================================
# Geometric Nucleus
# ============================================================

nucleus = profile.iloc[0]["Observable"]

print(f"Geometric Nucleus : {nucleus}")
print()


# ============================================================
# Distance to Nucleus
# ============================================================

distance_to_nucleus = distance.loc[nucleus]

relational = pd.DataFrame({

    "Observable": distance.index,

    "DistanceToNucleus": distance_to_nucleus.values

})

relational = relational.merge(

    profile[[
        "Observable",
        "RadiusFromCentroid",
        "LocalDensity",
        "ConcentrationIndex"
    ]],

    on="Observable",

    how="left"

)


# ============================================================
# Relational Ranking
# ============================================================

relational = relational.sort_values(

    "DistanceToNucleus"

).reset_index(drop=True)

relational["HierarchyRank"] = (

    np.arange(len(relational)) + 1

)


# ============================================================
# Relative Distance
# ============================================================

max_distance = relational["DistanceToNucleus"].max()

if max_distance == 0:

    relational["RelativeDistance"] = 0.0

else:

    relational["RelativeDistance"] = (

        relational["DistanceToNucleus"] /
        max_distance

    )


# ============================================================
# Structural Levels
# ============================================================

n_levels = 5

edges = np.linspace(

    0.0,
    1.0,
    n_levels + 1

)

levels = []

structural_level = []

for value in relational["RelativeDistance"]:

    level = np.searchsorted(

        edges,
        value,
        side="right"

    ) - 1

    level = max(0, min(level, n_levels - 1))

    structural_level.append(level + 1)

relational["StructuralLevel"] = structural_level


# ============================================================
# Relational Profile
# ============================================================

relational.to_csv(

    OUT / "relational_profile.csv",

    index=False

)


# ============================================================
# Structural Levels Summary
# ============================================================

for level in range(1, n_levels + 1):

    subset = relational[
        relational["StructuralLevel"] == level
    ]

    levels.append({

        "Level": level,

        "Observables": len(subset),

        "MeanDistance":

            subset["DistanceToNucleus"].mean(),

        "MeanDensity":

            subset["LocalDensity"].mean(),

        "MeanConcentration":

            subset["ConcentrationIndex"].mean()

    })

levels_df = pd.DataFrame(levels)

levels_df.to_csv(

    OUT / "structural_levels.csv",

    index=False

)


# ============================================================
# Nucleus Hierarchy
# ============================================================

hierarchy = relational[[
    "HierarchyRank",
    "Observable",
    "DistanceToNucleus"
]]

hierarchy.to_csv(

    OUT / "nucleus_hierarchy.csv",

    index=False

)


print("=" * 70)
print("Relational Organization Summary")
print("=" * 70)

print(f"Geometric Nucleus        : {nucleus}")
print(f"Structural Levels        : {n_levels}")
print(f"Most Peripheral Distance : {max_distance:.6f}")
print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.4",

    "title": "Relational Organization of the Observable Space",

    "observables": int(len(relational)),

    "geometric_nucleus": nucleus,

    "structural_levels": int(n_levels),

    "maximum_distance_to_nucleus": float(max_distance),

    "mean_distance_to_nucleus":
        float(relational["DistanceToNucleus"].mean()),

    "mean_density":
        float(relational["LocalDensity"].mean()),

    "mean_concentration":
        float(relational["ConcentrationIndex"].mean()),

    "closest_observable":
        relational.iloc[1]["Observable"],

    "most_peripheral_observable":
        relational.iloc[-1]["Observable"]

}

with open(

    OUT / "relational_certificate.json",

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

    OUT / "relational_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("GER\n")
    f.write("S29-E6.2.4\n")
    f.write("Relational Organization of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Global Statistics\n")
    f.write("-----------------\n\n")

    f.write(f"Observables               : {len(relational)}\n")
    f.write(f"Geometric Nucleus         : {nucleus}\n")
    f.write(f"Structural Levels         : {n_levels}\n")
    f.write(f"Maximum Distance          : {max_distance:.6f}\n")
    f.write(
        f"Mean Distance             : "
        f"{relational['DistanceToNucleus'].mean():.6f}\n"
    )
    f.write(
        f"Mean Density              : "
        f"{relational['LocalDensity'].mean():.6f}\n"
    )
    f.write(
        f"Mean Concentration        : "
        f"{relational['ConcentrationIndex'].mean():.6f}\n"
    )

    f.write("\n")

    f.write("Relational Hierarchy\n")
    f.write("--------------------\n\n")

    for _, row in hierarchy.iterrows():

        f.write(
            f"{int(row['HierarchyRank']):2d}  "
            f"{row['Observable']:20s}"
            f"  Distance={row['DistanceToNucleus']:.6f}\n"
        )

    f.write("\n")

    f.write("Structural Levels\n")
    f.write("-----------------\n\n")

    for _, row in levels_df.iterrows():

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
        "This experiment establishes the first intrinsic "
        "relational organization of the certified Observable "
        "Space. The geometric nucleus is identified directly "
        "from the concentration structure, and every observable "
        "is positioned according to its geometric distance from "
        "this nucleus. The resulting relational hierarchy "
        "provides a parameter-free structural description of the "
        "Observable Space and constitutes the basis for the "
        "subsequent Occupancy and Stability analyses of the "
        "E6.2 series.\n"
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
