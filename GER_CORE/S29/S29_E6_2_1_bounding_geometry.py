"""
============================================================
GER
S29-E6.2.1
BOUNDING GEOMETRY OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Characterize the global geometric envelope occupied by the
Observable Space produced by the Structural Atlas.

This experiment computes the fundamental geometric limits of
the certified observable representation, including the
bounding box, centroid, geometric radius, compactness and
dimensional extent.

The analysis is performed exclusively on the certified
geometric features produced by the Feature Audit
(S29-E6.2.1.1), ensuring that only geometrically meaningful
attributes participate in the construction of the space.

This experiment establishes the geometric boundary of the
Observable Space and provides the reference structure for all
subsequent occupancy analyses developed in the E6.2 series.

python -m GER_CORE.S29.S29_E6_2_1_bounding_geometry

Author
Eduardo Batista de Freitas 
GER Project
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")

# Alteração 1: Adicionar a leitura da máscara
MASK_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_1_1_FeatureAudit"
    / "geometric_feature_mask.csv"
)

OUT = ROOT / "E6_2_1_BoundingGeometry"
OUT.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GER")
print("S29-E6.2.1")
print("Bounding Geometry of the Observable Space")
print("=" * 70)

# ============================================================
# HELPERS
# ============================================================

def load_csv(path):

    if path.exists():

        print(f"[OK] {path.name}")

        return pd.read_csv(path)

    print(f"[WARNING] Missing: {path.name}")

    return None


# ============================================================
# LOAD DATA
# ============================================================

atlas = load_csv(

    ROOT /
    "L16_StructuralAtlas" /
    "structural_atlas.csv"

)

if atlas is None:

    raise FileNotFoundError(

        "structural_atlas.csv not found."

    )

# Alteração 2: Carregar a máscara
mask = load_csv(MASK_FILE)

if mask is None:

    raise FileNotFoundError(

        f"geometric_feature_mask.csv not found at {MASK_FILE}"

    )

# Alteração 3: Construir a lista oficial de atributos
geometry_features = (
    mask.loc[
        mask["RecommendedForGeometry"],
        "Feature"
    ]
    .tolist()
)

if len(geometry_features) == 0:

    raise RuntimeError(

        "No features recommended for geometry found in mask."

    )

# ============================================================
# NUMERIC SPACE
# ============================================================

# Alteração 4: Filtrar o atlas com a lista oficial de atributos
space = atlas[geometry_features].copy()

space = space.replace(

    [

        np.inf,
        -np.inf

    ],

    np.nan

)

observables = atlas.loc[
    space.index,
    "Observable"
].tolist()

space = space.apply(pd.to_numeric, errors="coerce")

space = space.dropna()

if len(space) == 0:

    raise RuntimeError(

        "Observable space is empty after cleaning."

    )

matrix = space.to_numpy(dtype=np.float64)

dimension = matrix.shape[1]

samples = matrix.shape[0]

print()
print(f"Samples    : {samples}")
print(f"Dimensions : {dimension}")

# ============================================================
# BOUNDING BOX
# ============================================================

minimum = np.min(

    matrix,

    axis=0

)

maximum = np.max(

    matrix,

    axis=0

)

ranges = maximum - minimum

bounding = pd.DataFrame({

    "Dimension": geometry_features,

    "Minimum": minimum,

    "Maximum": maximum,

    "Range": ranges

})

bounding.to_csv(

    OUT /
    "dimension_ranges.csv",

    index=False

)

# ============================================================
# CENTROID
# ============================================================

centroid = np.mean(

    matrix,

    axis=0

)

centroid_df = pd.DataFrame({

    "Dimension": geometry_features,

    "Centroid": centroid

})

centroid_df.to_csv(

    OUT /
    "centroid.csv",

    index=False

)

# ============================================================
# DISTANCE TO CENTROID
# ============================================================

delta = matrix - centroid

distance = np.linalg.norm(

    delta,

    axis=1

)

distance_df = pd.DataFrame({

    "Observable": observables,

    "DistanceToCentroid": distance

})

distance_df = distance_df.sort_values(

    "DistanceToCentroid",

    ascending=False

)

distance_df.to_csv(

    OUT /
    "distance_to_centroid.csv",

    index=False

)

# ============================================================
# BOUNDING RADIUS
# ============================================================

bounding_radius = float(

    np.max(distance)

)

mean_radius = float(

    np.mean(distance)

)

median_radius = float(

    np.median(distance)

)

std_radius = float(

    np.std(distance)

)

# ============================================================
# HYPERBOX VOLUME
# ============================================================

volume = float(

    np.prod(ranges)

)

# ============================================================
# DIMENSION STATISTICS
# ============================================================

statistics = []

for i, column in enumerate(geometry_features):

    values = matrix[:, i]

    statistics.append({

        "Dimension": column,

        "Mean": np.mean(values),

        "Median": np.median(values),

        "Std": np.std(values),

        "Variance": np.var(values),

        "Minimum": np.min(values),

        "Maximum": np.max(values),

        "Range": np.max(values) - np.min(values)

    })

statistics_df = pd.DataFrame(

    statistics

)

statistics_df.to_csv(

    OUT /
    "dimension_statistics.csv",

    index=False

)

# ============================================================
# ANISOTROPY ANALYSIS
# ============================================================

range_mean = float(np.mean(ranges))

range_std = float(np.std(ranges))

range_cv = (

    range_std / range_mean

    if range_mean > 0

    else np.nan

)

anisotropy_df = pd.DataFrame({

    "Dimension": geometry_features,

    "Range": ranges,

    "RelativeRange": (

        ranges / np.max(ranges)

        if np.max(ranges) > 0

        else np.zeros_like(ranges)

    )

})

anisotropy_df.to_csv(

    OUT /
    "anisotropy_analysis.csv",

    index=False

)

# ============================================================
# COLLAPSED DIMENSIONS
# ============================================================

collapsed_threshold = 1e-8

collapsed = ranges <= collapsed_threshold

collapsed_df = pd.DataFrame({

    "Dimension": geometry_features,

    "Collapsed": collapsed,

    "Range": ranges

})

collapsed_df.to_csv(

    OUT /
    "collapsed_dimensions.csv",

    index=False

)

# ============================================================
# BOUNDING BOX
# ============================================================

bounding_box = pd.DataFrame({

    "Dimension": geometry_features,

    "Minimum": minimum,

    "Maximum": maximum

})

bounding_box.to_csv(

    OUT /
    "bounding_box.csv",

    index=False

)

# ============================================================
# GEOMETRIC EXTREMES
# ============================================================

closest_index = int(

    np.argmin(distance)

)

farthest_index = int(

    np.argmax(distance)

)

extremes = pd.DataFrame({

    "Type": [

        "ClosestToCentroid",

        "FarthestFromCentroid"

    ],

    "Observable": [

        observables[closest_index],

        observables[farthest_index]

    ],

    "Distance": [

        distance[closest_index],

        distance[farthest_index]

    ]

})

extremes.to_csv(

    OUT /
    "geometric_extremes.csv",

    index=False

)

# ============================================================
# GEOMETRY SUMMARY
# ============================================================

summary = pd.DataFrame({

    "Metric": [

        "Observables",

        "Dimensions",

        "BoundingRadius",

        "MeanRadius",

        "MedianRadius",

        "RadiusStd",

        "HyperBoxVolume",

        "MeanDimensionRange",

        "RangeStd",

        "RangeCV",

        "CollapsedDimensions"

    ],

    "Value": [

        samples,

        dimension,

        bounding_radius,

        mean_radius,

        median_radius,

        std_radius,

        volume,

        range_mean,

        range_std,

        range_cv,

        int(np.sum(collapsed))

    ]

})

summary.to_csv(

    OUT /
    "geometry_summary.csv",

    index=False

)

# ============================================================
# COMPACTNESS
# ============================================================

compactness = (

    mean_radius /

    bounding_radius

    if bounding_radius > 0

    else np.nan

)

compactness_df = pd.DataFrame({

    "Metric": [

        "BoundingRadius",

        "MeanRadius",

        "CompactnessIndex"

    ],

    "Value": [

        bounding_radius,

        mean_radius,

        compactness

    ]

})

compactness_df.to_csv(

    OUT /
    "compactness.csv",

    index=False

)

# ============================================================
# DIMENSION ORDERING
# ============================================================

ordered_dimensions = bounding.sort_values(

    "Range",

    ascending=False

)

ordered_dimensions.to_csv(

    OUT /
    "dimension_importance.csv",

    index=False

)

# ============================================================
# GEOMETRY REPORT
# ============================================================

# Alteração 6: Atualizar o relatório com as informações da máscara
with open(

    OUT /
    "geometry_report.txt",

    "w"

) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("S29-E6.2.1\n")
    f.write("Bounding Geometry of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Geometry built from certified feature mask.\n")
    f.write(f"Certified dimensions: {len(geometry_features)}\n")
    f.write("Features used:\n")
    for feature in geometry_features:
        f.write(f" - {feature}\n")
    f.write("\n" + "-" * 60 + "\n\n")

    f.write(f"Observables              : {samples}\n")
    f.write(f"Dimensions               : {dimension}\n")
    f.write(f"Bounding Radius          : {bounding_radius:.6f}\n")
    f.write(f"Mean Radius              : {mean_radius:.6f}\n")
    f.write(f"Median Radius            : {median_radius:.6f}\n")
    f.write(f"Radius Std               : {std_radius:.6f}\n")
    f.write(f"HyperBox Volume          : {volume:.6f}\n")
    f.write(f"Mean Dimension Range     : {range_mean:.6f}\n")
    f.write(f"Range Std                : {range_std:.6f}\n")
    f.write(f"Range CV                : {range_cv:.6f}\n")
    f.write(f"Collapsed Dimensions     : {int(np.sum(collapsed))}\n")
    f.write(f"Compactness Index        : {compactness:.6f}\n")

    f.write("\n")
    f.write("Largest Dimensions\n")
    f.write("------------------------------\n")

    for _, row in ordered_dimensions.head(10).iterrows():

        f.write(

            f"{row.Dimension:30s}"

            f"{row.Range:.6f}\n"

        )

    f.write("\n")
    f.write("Geometric Extremes\n")
    f.write("------------------------------\n")

    for _, row in extremes.iterrows():

        f.write(

            f"{row.Type:20s}"

            f"{row.Observable:30s}"

            f"{row.Distance:.6f}\n"

        )

# ============================================================
# SCIENTIFIC CERTIFICATE
# ============================================================

# Alteração 5: Atualizar o certificado científico
certificate = {

    "experiment": "S29-E6.2.1",

    "title": "Bounding Geometry of the Observable Space",

    "feature_mask": str(MASK_FILE),

    "geometry_dimensions": len(geometry_features),

    "observables": int(samples),

    "dimensions": int(dimension),

    "bounding_radius": float(bounding_radius),

    "mean_radius": float(mean_radius),

    "median_radius": float(median_radius),

    "radius_std": float(std_radius),

    "hyperbox_volume": float(volume),

    "mean_dimension_range": float(range_mean),

    "range_std": float(range_std),

    "range_cv": float(range_cv),

    "collapsed_dimensions": int(np.sum(collapsed)),

    "compactness_index": float(compactness),

    "largest_dimension": str(

        ordered_dimensions.iloc[0]["Dimension"]

    ),

    "smallest_dimension": str(

        ordered_dimensions.iloc[-1]["Dimension"]

    ),

    "closest_observable": str(

        extremes.iloc[0]["Observable"]

    ),

    "farthest_observable": str(

        extremes.iloc[1]["Observable"]

    )

}

with open(

    OUT /
    "scientific_certificate.json",

    "w"

) as f:

    json.dump(

        certificate,

        f,

        indent=4

    )

# ============================================================
# FINAL MESSAGE
# ============================================================

print()

print("=" * 70)

print("Experiment completed.")

print("Results saved to:")

print(OUT)

print("=" * 70)

# ============================================================
# MAIN
# ============================================================

def main():

    pass

if __name__ == "__main__":

    main()
    
