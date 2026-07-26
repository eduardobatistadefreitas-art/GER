"""
============================================================
GER
S29-E6.2.2
DENSITY FIELD OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Characterize the occupancy of the certified Observable Space.

Using the geometric representation established by the
Bounding Geometry experiment (S29-E6.2.1), this experiment
measures how observables are distributed inside the
admissible geometric domain.

The analysis is performed exclusively on the certified
geometric features produced by the Feature Audit
(S29-E6.2.1.1), ensuring methodological consistency across
the entire E6.2 series.

This experiment establishes the first intrinsic density map
of the Observable Space and provides the observational basis
for subsequent analyses of concentration, occupancy,
stability and structural organization.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_2_density_field

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

ATLAS_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
    / "L16_StructuralAtlas"
    / "structural_atlas.csv"
)

MASK_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_1_1_FeatureAudit"
    / "geometric_feature_mask.csv"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_2_DensityField"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# GER Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.2")
print("Density Field of the Observable Space")
print("=" * 70)


# ============================================================
# Load data
# ============================================================

atlas = pd.read_csv(ATLAS_FILE)
mask = pd.read_csv(MASK_FILE)

print("[OK] structural_atlas.csv")
print("[OK] geometric_feature_mask.csv")


# ============================================================
# Certified geometric dimensions
# ============================================================

geometry_features = (
    mask.loc[
        mask["RecommendedForGeometry"],
        "Feature"
    ]
    .tolist()
)

space = atlas[geometry_features].copy()

space = space.apply(pd.to_numeric, errors="coerce")
space = space.dropna()

matrix = space.to_numpy(dtype=np.float64)

observables = atlas.iloc[space.index, 0].tolist()

print()
print(f"Observables : {len(observables)}")
print(f"Dimensions  : {matrix.shape[1]}")
print()

# ============================================================
# Distance matrix
# ============================================================

difference = matrix[:, None, :] - matrix[None, :, :]
distance_matrix = np.linalg.norm(difference, axis=2)

distance_df = pd.DataFrame(
    distance_matrix,
    index=observables,
    columns=observables
)

distance_df.to_csv(
    OUT / "neighbor_matrix.csv",
    index=True
)


# ============================================================
# Centroid
# ============================================================

centroid = matrix.mean(axis=0)

radius = np.linalg.norm(
    matrix - centroid,
    axis=1
)


# ============================================================
# Local Density
# ============================================================

mean_neighbor_distance = []
nearest_neighbor = []
nearest_distance = []
local_density = []

for i in range(len(observables)):

    d = distance_matrix[i].copy()

    d[i] = np.nan

    mean_d = np.nanmean(d)

    nearest = np.nanargmin(d)

    nearest_d = np.nanmin(d)

    rho = (
        np.inf
        if mean_d == 0
        else 1.0 / mean_d
    )

    mean_neighbor_distance.append(mean_d)
    nearest_neighbor.append(observables[nearest])
    nearest_distance.append(nearest_d)
    local_density.append(rho)


density_df = pd.DataFrame({

    "Observable": observables,

    "RadiusFromCentroid": radius,

    "MeanNeighborDistance": mean_neighbor_distance,

    "NearestNeighbor": nearest_neighbor,

    "NearestDistance": nearest_distance,

    "LocalDensity": local_density

})

density_df.to_csv(
    OUT / "local_density.csv",
    index=False
)


# ============================================================
# Radial Distribution
# ============================================================

radial_df = pd.DataFrame({

    "Observable": observables,
    "Radius": radius

})

radial_df = radial_df.sort_values(
    "Radius"
)

radial_df.to_csv(
    OUT / "radial_distribution.csv",
    index=False
)


# ============================================================
# Global Density Statistics
# ============================================================

summary = pd.DataFrame({

    "Metric": [

        "Observables",
        "Dimensions",
        "MeanDensity",
        "MedianDensity",
        "DensityStd",
        "MinimumDensity",
        "MaximumDensity",
        "MeanRadius",
        "MaximumRadius",
        "MeanNeighborDistance"

    ],

    "Value": [

        len(observables),
        matrix.shape[1],
        np.mean(local_density),
        np.median(local_density),
        np.std(local_density),
        np.min(local_density),
        np.max(local_density),
        np.mean(radius),
        np.max(radius),
        np.mean(mean_neighbor_distance)

    ]

})

summary.to_csv(
    OUT / "density_summary.csv",
    index=False
)


print("=" * 70)
print("Density Field Summary")
print("=" * 70)

print(f"Observables              : {len(observables)}")
print(f"Dimensions               : {matrix.shape[1]}")
print(f"Mean Density             : {np.mean(local_density):.6f}")
print(f"Maximum Density          : {np.max(local_density):.6f}")
print(f"Minimum Density          : {np.min(local_density):.6f}")
print(f"Mean Radius              : {np.mean(radius):.6f}")
print(f"Maximum Radius           : {np.max(radius):.6f}")
print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.2",
    "title": "Density Field of the Observable Space",

    "feature_mask": str(MASK_FILE),

    "observables": len(observables),
    "dimensions": matrix.shape[1],

    "mean_density": float(np.mean(local_density)),
    "median_density": float(np.median(local_density)),
    "density_std": float(np.std(local_density)),

    "minimum_density": float(np.min(local_density)),
    "maximum_density": float(np.max(local_density)),

    "mean_radius": float(np.mean(radius)),
    "maximum_radius": float(np.max(radius)),

    "mean_neighbor_distance": float(np.mean(mean_neighbor_distance)),

    "densest_observable": density_df.loc[
        density_df["LocalDensity"].idxmax(),
        "Observable"
    ],

    "most_isolated_observable": density_df.loc[
        density_df["LocalDensity"].idxmin(),
        "Observable"
    ]
}

with open(
    OUT / "density_certificate.json",
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
    OUT / "density_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("GER\n")
    f.write("S29-E6.2.2\n")
    f.write("Density Field of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Certified geometric dimensions\n")
    f.write("------------------------------\n")

    for feature in geometry_features:
        f.write(f" - {feature}\n")

    f.write("\n")

    f.write(f"Observables              : {len(observables)}\n")
    f.write(f"Dimensions               : {matrix.shape[1]}\n")
    f.write(f"Mean Density             : {np.mean(local_density):.6f}\n")
    f.write(f"Median Density           : {np.median(local_density):.6f}\n")
    f.write(f"Density Std              : {np.std(local_density):.6f}\n")
    f.write(f"Minimum Density          : {np.min(local_density):.6f}\n")
    f.write(f"Maximum Density          : {np.max(local_density):.6f}\n")
    f.write(f"Mean Radius              : {np.mean(radius):.6f}\n")
    f.write(f"Maximum Radius           : {np.max(radius):.6f}\n")
    f.write(f"Mean Neighbor Distance   : {np.mean(mean_neighbor_distance):.6f}\n")

    f.write("\n")

    f.write(
        f"Densest Observable       : "
        f"{certificate['densest_observable']}\n"
    )

    f.write(
        f"Most Isolated Observable : "
        f"{certificate['most_isolated_observable']}\n"
    )

    f.write("\n")

    f.write(
        "Conclusion\n"
        "----------\n"
    )

    f.write(
        "This experiment characterizes the intrinsic occupancy "
        "of the certified Observable Space using pairwise "
        "Euclidean distances. The resulting density field "
        "provides the observational basis for subsequent "
        "analyses of concentration, occupancy, stability "
        "and structural organization within the E6.2 series.\n"
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
