"""
============================================================
GER
S29-E6.2.3
CONCENTRATION ANALYSIS OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Characterize the global concentration structure of the
certified Observable Space.

Using the Density Field established in S29-E6.2.2, this
experiment measures how the certified observables are
organized around the geometric center of the space.

The analysis combines radial position and intrinsic local
density in order to quantify the degree of concentration of
each observable without introducing arbitrary parameters.

This experiment establishes the global concentration profile
of the Observable Space and provides the basis for the
subsequent occupancy and structural organization analyses of
the E6.2 series.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_3_concentration_analysis

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

DENSITY_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_2_DensityField"
    / "local_density.csv"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_3_ConcentrationAnalysis"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# GER Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.3")
print("Concentration Analysis of the Observable Space")
print("=" * 70)


# ============================================================
# Load Density Field
# ============================================================

density = pd.read_csv(DENSITY_FILE)

print("[OK] local_density.csv")

print()

print(f"Observables : {len(density)}")

print()

# ============================================================
# Normalized Quantities
# ============================================================

radius = density["RadiusFromCentroid"].to_numpy(dtype=np.float64)
local_density = density["LocalDensity"].to_numpy(dtype=np.float64)

max_radius = radius.max()
max_density = local_density.max()

relative_radius = radius / max_radius

relative_density = local_density / max_density


# ============================================================
# Concentration Index
# ============================================================

concentration_index = (
    relative_density *
    (1.0 - relative_radius)
)


# ============================================================
# Concentration Profile
# ============================================================

profile = density.copy()

profile["RelativeRadius"] = relative_radius
profile["RelativeDensity"] = relative_density
profile["ConcentrationIndex"] = concentration_index

profile = profile.sort_values(
    "ConcentrationIndex",
    ascending=False
)

profile.to_csv(
    OUT / "concentration_profile.csv",
    index=False
)


# ============================================================
# Radial Layers
# ============================================================

n_layers = 5

edges = np.linspace(
    0.0,
    max_radius,
    n_layers + 1
)

layers = []

for i in range(n_layers):

    lower = edges[i]
    upper = edges[i + 1]

    if i == n_layers - 1:

        mask = (
            (radius >= lower) &
            (radius <= upper)
        )

    else:

        mask = (
            (radius >= lower) &
            (radius < upper)
        )

    count = int(mask.sum())

    if count == 0:

        mean_density = np.nan
        mean_concentration = np.nan

    else:

        mean_density = float(
            np.mean(local_density[mask])
        )

        mean_concentration = float(
            np.mean(concentration_index[mask])
        )

    layers.append({

        "Layer": i + 1,
        "RadiusMin": lower,
        "RadiusMax": upper,
        "Observables": count,
        "MeanDensity": mean_density,
        "MeanConcentration": mean_concentration

    })

layers_df = pd.DataFrame(layers)

layers_df.to_csv(
    OUT / "radial_layers.csv",
    index=False
)


# ============================================================
# Global Concentration Statistics
# ============================================================

summary = pd.DataFrame({

    "Metric": [

        "Observables",
        "MeanConcentration",
        "MedianConcentration",
        "StdConcentration",
        "MinimumConcentration",
        "MaximumConcentration",
        "CentralObservable",
        "PeripheralObservable",
        "MostConcentratedObservable"

    ],

    "Value": [

        len(profile),

        np.mean(concentration_index),

        np.median(concentration_index),

        np.std(concentration_index),

        np.min(concentration_index),

        np.max(concentration_index),

        density.loc[
            density["RadiusFromCentroid"].idxmin(),
            "Observable"
        ],

        density.loc[
            density["RadiusFromCentroid"].idxmax(),
            "Observable"
        ],

        profile.iloc[0]["Observable"]

    ]

})

summary.to_csv(
    OUT / "concentration_summary.csv",
    index=False
)


print("=" * 70)
print("Concentration Analysis Summary")
print("=" * 70)

print(f"Observables                : {len(profile)}")
print(f"Mean Concentration         : {np.mean(concentration_index):.6f}")
print(f"Maximum Concentration      : {np.max(concentration_index):.6f}")
print(f"Minimum Concentration      : {np.min(concentration_index):.6f}")
print(f"Central Observable         : {summary.iloc[6]['Value']}")
print(f"Peripheral Observable      : {summary.iloc[7]['Value']}")
print(f"Most Concentrated          : {summary.iloc[8]['Value']}")
print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.3",
    "title": "Concentration Analysis of the Observable Space",

    "observables": int(len(profile)),

    "mean_concentration": float(np.mean(concentration_index)),
    "median_concentration": float(np.median(concentration_index)),
    "std_concentration": float(np.std(concentration_index)),

    "minimum_concentration": float(np.min(concentration_index)),
    "maximum_concentration": float(np.max(concentration_index)),

    "central_observable":
        density.loc[
            density["RadiusFromCentroid"].idxmin(),
            "Observable"
        ],

    "peripheral_observable":
        density.loc[
            density["RadiusFromCentroid"].idxmax(),
            "Observable"
        ],

    "most_concentrated_observable":
        profile.iloc[0]["Observable"],

    "least_concentrated_observable":
        profile.iloc[-1]["Observable"]

}

with open(
    OUT / "concentration_certificate.json",
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
    OUT / "concentration_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("GER\n")
    f.write("S29-E6.2.3\n")
    f.write("Concentration Analysis of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Global Statistics\n")
    f.write("-----------------\n\n")

    f.write(f"Observables                : {len(profile)}\n")
    f.write(f"Mean Concentration         : {np.mean(concentration_index):.6f}\n")
    f.write(f"Median Concentration       : {np.median(concentration_index):.6f}\n")
    f.write(f"Standard Deviation         : {np.std(concentration_index):.6f}\n")
    f.write(f"Minimum Concentration      : {np.min(concentration_index):.6f}\n")
    f.write(f"Maximum Concentration      : {np.max(concentration_index):.6f}\n")

    f.write("\n")

    f.write(
        f"Central Observable         : "
        f"{certificate['central_observable']}\n"
    )

    f.write(
        f"Peripheral Observable      : "
        f"{certificate['peripheral_observable']}\n"
    )

    f.write(
        f"Most Concentrated          : "
        f"{certificate['most_concentrated_observable']}\n"
    )

    f.write(
        f"Least Concentrated         : "
        f"{certificate['least_concentrated_observable']}\n"
    )

    f.write("\n")

    f.write("Ranking\n")
    f.write("-------\n\n")

    for i, row in profile.iterrows():

        f.write(
            f"{row['Observable']:20s}"
            f"  CI={row['ConcentrationIndex']:.6f}"
            f"  Radius={row['RadiusFromCentroid']:.6f}"
            f"  Density={row['LocalDensity']:.6f}\n"
        )

    f.write("\n")

    f.write("Conclusion\n")
    f.write("----------\n")

    f.write(
        "This experiment characterizes the global concentration "
        "structure of the certified Observable Space by combining "
        "intrinsic local density and radial position. The resulting "
        "Concentration Index provides a parameter-free measure of "
        "how strongly each observable participates in the central "
        "organization of the geometric space, establishing the "
        "observational basis for the subsequent occupancy analyses "
        "of the E6.2 series.\n"
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
