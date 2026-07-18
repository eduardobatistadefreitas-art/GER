# ============================================================
# GER
# S29-E3.3
# Intrinsic Geometry of Stability Regions
#
# Computes intrinsic geometric properties of the stability
# regions discovered in S29-E3.2.
#
# Inputs
#   RESULTS/S29/S29_E3_1_signature_map.csv
#   RESULTS/S29/S29_E3_2_stability_regions.csv
#
# Outputs
#   RESULTS/S29/S29_E3_3_region_geometry.csv
#   RESULTS/S29/S29_E3_3_covariances.csv
#   RESULTS/S29/S29_E3_3_region_distance_matrix.csv
#   RESULTS/S29/S29_E3_3_summary.txt
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Directories
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = ROOT / "RESULTS" / "S29"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ------------------------------------------------------------
# Input files
# ------------------------------------------------------------

SIGNATURE_FILE = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E3_1_signature_map.csv"
)

REGIONS_FILE = Path(
    "/content/S29_E3_2_stability_regions.csv"
)

# ------------------------------------------------------------
# Output files
# ------------------------------------------------------------

GEOMETRY_FILE = (
    RESULTS_DIR /
    "S29_E3_3_region_geometry.csv"
)

COVARIANCE_FILE = (
    RESULTS_DIR /
    "S29_E3_3_covariances.csv"
)

DISTANCE_FILE = (
    RESULTS_DIR /
    "S29_E3_3_region_distance_matrix.csv"
)

SUMMARY_FILE = (
    RESULTS_DIR /
    "S29_E3_3_summary.txt"
)
# ============================================================
# BLOCO A
# INTRINSIC METRIC GEOMETRY
# ============================================================

FEATURES = [
    "Diameter",
    "Convergence",
    "Recurrence",
    "Drift"
]


def compute_region_geometry(signature_df, regions_df):
    """
    Computes intrinsic metric properties of each stability region.

    Returns
    -------
    DataFrame
        One row per region.
    """

    results = []

    for _, region in regions_df.iterrows():

        gamma0 = region["gamma_start"]
        gamma1 = region["gamma_end"]
        label = region["classification"]

        subset = signature_df[
            (signature_df["Gamma"] >= gamma0) &
            (signature_df["Gamma"] <= gamma1)
        ].copy()

        n = len(subset)

        if n == 0:
            continue

        X = subset[FEATURES].values

        # ----------------------------------------------------
        # Centroid
        # ----------------------------------------------------

        centroid = np.mean(X, axis=0)

        # ----------------------------------------------------
        # Distance to centroid
        # ----------------------------------------------------

        radius = np.linalg.norm(X - centroid, axis=1)

        mean_radius = float(np.mean(radius))
        std_radius = float(np.std(radius))
        max_radius = float(np.max(radius))

        # ----------------------------------------------------
        # Internal diameter
        # ----------------------------------------------------

        if n > 1:

            diameter = 0.0

            for i in range(n):
                for j in range(i + 1, n):

                    d = np.linalg.norm(X[i] - X[j])

                    if d > diameter:
                        diameter = d

        else:

            diameter = 0.0

                # ----------------------------------------------------
        # Compactness / Packing
        # ----------------------------------------------------

        if diameter > 0:

            compactness = mean_radius / diameter

            packing = n / diameter

        else:

            compactness = 0.0

            packing = 0.0

        # ----------------------------------------------------
        # Gamma interval
        # ----------------------------------------------------

        delta_gamma = gamma1 - gamma0

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        results.append({

            "Region": label,

            "N": n,

            "GammaStart": gamma0,

            "GammaEnd": gamma1,

            "DeltaGamma": delta_gamma,

            "CentroidDiameter": centroid[0],
            "CentroidConvergence": centroid[1],
            "CentroidRecurrence": centroid[2],
            "CentroidDrift": centroid[3],

            "MeanRadius": mean_radius,
            "StdRadius": std_radius,
            "MaxRadius": max_radius,

            "InternalDiameter": diameter,

            "Compactness": compactness,
            "Packing": packing

        })

    return pd.DataFrame(results)
  # ============================================================
# BLOCO B
# INTRINSIC SHAPE ANALYSIS
# ============================================================

def compute_region_shape(signature_df, regions_df):
    """
    Computes intrinsic shape descriptors of each stability region.

    Returns
    -------
    geometry_df
        Shape metrics.

    covariance_dict
        Covariance matrix for each region.
    """

    results = []

    covariance_dict = {}

    for _, region in regions_df.iterrows():

        gamma0 = region["gamma_start"]
        gamma1 = region["gamma_end"]
        label = region["classification"]

        subset = signature_df[
            (signature_df["Gamma"] >= gamma0) &
            (signature_df["Gamma"] <= gamma1)
        ].copy()

        n = len(subset)

        if n < 2:

            results.append({

                "Region": label,

                "VarDiameter": 0.0,
                "VarConvergence": 0.0,
                "VarRecurrence": 0.0,
                "VarDrift": 0.0,

                "Eigenvalue1": 0.0,
                "Eigenvalue2": 0.0,
                "Eigenvalue3": 0.0,
                "Eigenvalue4": 0.0,

                "Anisotropy": 0.0,

                "Uniformity": 0.0

            })

            covariance_dict[label] = np.zeros((4, 4))

            continue

        X = subset[FEATURES].values

        # ----------------------------------------------------
        # Covariance
        # ----------------------------------------------------

        cov = np.cov(X.T)

        covariance_dict[label] = cov

        # ----------------------------------------------------
        # Eigenvalues
        # ----------------------------------------------------

        eigvals = np.linalg.eigvalsh(cov)

        eigvals = np.sort(eigvals)[::-1]

        total = np.sum(eigvals)

        if total > 0:

            anisotropy = eigvals[0] / total

        else:

            anisotropy = 0.0

        # ----------------------------------------------------
        # Variances
        # ----------------------------------------------------

        variances = np.var(X, axis=0)

        # ----------------------------------------------------
        # Uniformity
        # ----------------------------------------------------

        centroid = np.mean(X, axis=0)

        radius = np.linalg.norm(X - centroid, axis=1)

        mean_radius = np.mean(radius)

        std_radius = np.std(radius)

        if mean_radius > 0:

            uniformity = std_radius / mean_radius

        else:

            uniformity = 0.0

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        results.append({

            "Region": label,

            "VarDiameter": variances[0],
            "VarConvergence": variances[1],
            "VarRecurrence": variances[2],
            "VarDrift": variances[3],

            "Eigenvalue1": eigvals[0],
            "Eigenvalue2": eigvals[1],
            "Eigenvalue3": eigvals[2],
            "Eigenvalue4": eigvals[3],

            "Anisotropy": anisotropy,

            "Uniformity": uniformity

        })

    geometry_df = pd.DataFrame(results)

    return geometry_df, covariance_dict
  # ============================================================
# BLOCO C
# INTER-REGION GEOMETRY
# ============================================================

def compute_region_separation(geometry_df):
    """
    Computes geometric relationships between region centroids.

    Returns
    -------
    distance_matrix : DataFrame
        Pairwise centroid distances.

    summary_df : DataFrame
        Separation metrics.
    """

    centroid_cols = [
        "CentroidDiameter",
        "CentroidConvergence",
        "CentroidRecurrence",
        "CentroidDrift"
    ]

    regions = geometry_df["Region"].tolist()

    centroids = geometry_df[centroid_cols].values

    n = len(regions)

    D = np.zeros((n, n))

    # --------------------------------------------------------
    # Pairwise centroid distances
    # --------------------------------------------------------

    for i in range(n):
        for j in range(i + 1, n):

            d = np.linalg.norm(
                centroids[i] - centroids[j]
            )

            D[i, j] = d
            D[j, i] = d

    distance_matrix = pd.DataFrame(
        D,
        index=regions,
        columns=regions
    )

    # --------------------------------------------------------
    # Separation metrics
    # --------------------------------------------------------

    summary = []

    for i in range(n):

        distances = D[i].copy()

        distances[i] = np.inf

        nearest = np.min(distances)

        farthest = np.max(
            distances[np.isfinite(distances)]
        )

        radius = max(
            geometry_df.iloc[i]["MeanRadius"],
            1e-12
        )

        separation_ratio = nearest / radius

        summary.append({

            "Region": regions[i],

            "NearestRegionDistance": nearest,

            "FarthestRegionDistance": farthest,

            "SeparationRatio": separation_ratio

        })

    summary_df = pd.DataFrame(summary)

    return distance_matrix, summary_df
  # ============================================================
# BLOCO D
# REPORTS AND VISUALIZATION
# ============================================================

def save_summary(geometry_df, output_dir):
    """
    Generates a textual summary of the intrinsic geometry.
    """

    lines = []

    lines.append("=" * 60)
    lines.append("S29-E3.3")
    lines.append("INTRINSIC GEOMETRY OF STABILITY REGIONS")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Regions analysed : {len(geometry_df)}")
    lines.append("")

    # --------------------------------------------------------
    # Rankings
    # --------------------------------------------------------

    compact = geometry_df.sort_values("Compactness")

    lines.append(
        f"Most compact region : {compact.iloc[0]['Region']}"
    )

    lines.append(
        f"Least compact region : {compact.iloc[-1]['Region']}"
    )

    anis = geometry_df.sort_values("Anisotropy")

    lines.append(
        f"Most isotropic region : {anis.iloc[0]['Region']}"
    )

    lines.append(
        f"Most anisotropic region : {anis.iloc[-1]['Region']}"
    )

    dens = geometry_df.sort_values("Packing")

    lines.append(
        f"Highest packing : {dens.iloc[-1]['Region']}"
    )

    lines.append(
        f"Lowest packing : {dens.iloc[0]['Region']}"
    )

    diam = geometry_df.sort_values("InternalDiameter")

    lines.append(
        f"Largest diameter : {diam.iloc[-1]['Region']}"
    )

    lines.append(
        f"Smallest diameter : {diam.iloc[0]['Region']}"
    )

    sep = geometry_df.sort_values("SeparationRatio")

    lines.append(
        f"Best separated : {sep.iloc[-1]['Region']}"
    )

    lines.append(
        f"Worst separated : {sep.iloc[0]['Region']}"
    )

    with open(
        output_dir / "S29_E3_3_summary.txt",
        "w"
    ) as f:

        for line in lines:
            f.write(line + "\n")
# ============================================================
# BLOCO E
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("GER S29-E3.3")
    print("Intrinsic Geometry of Stability Regions")
    print("=" * 60)

    # --------------------------------------------------------
    # Read input files
    # --------------------------------------------------------

    print("\nReading input files...")

    signature_df = pd.read_csv(SIGNATURE_FILE)
    regions_df = pd.read_csv(REGIONS_FILE)

    print(f"Signatures : {len(signature_df)}")
    print(f"Regions    : {len(regions_df)}")

    # --------------------------------------------------------
    # Metric geometry
    # --------------------------------------------------------

    print("\nComputing intrinsic metric geometry...")

    geometry_df = compute_region_geometry(
        signature_df,
        regions_df
    )

    # --------------------------------------------------------
    # Shape analysis
    # --------------------------------------------------------

    print("Computing intrinsic shape...")

    shape_df, covariance_dict = compute_region_shape(
        signature_df,
        regions_df
    )

    geometry_df = geometry_df.merge(
        shape_df,
        on="Region",
        how="left"
    )

    # --------------------------------------------------------
    # Region separation
    # --------------------------------------------------------

    print("Computing region separation...")

    distance_df, separation_df = compute_region_separation(
        geometry_df
    )

    geometry_df = geometry_df.merge(
        separation_df,
        on="Region",
        how="left"
    )

    # --------------------------------------------------------
    # Save CSV files
    # --------------------------------------------------------

    print("Saving outputs...")

    geometry_df.to_csv(
        GEOMETRY_FILE,
        index=False
    )

    distance_df.to_csv(
        DISTANCE_FILE
    )

    cov_rows = []

    for region, cov in covariance_dict.items():

        row = {"Region": region}

        for i in range(4):
            for j in range(4):
                row[f"C{i+1}{j+1}"] = cov[i, j]

        cov_rows.append(row)

    pd.DataFrame(cov_rows).to_csv(
        COVARIANCE_FILE,
        index=False
    )

    save_summary(
        geometry_df,
        RESULTS_DIR
    )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print("\nDone.")
    print("-" * 60)
    print(f"Regions analysed : {len(geometry_df)}")
    print()

    print("Files generated:")

    print(f"  ✓ {GEOMETRY_FILE.name}")
    print(f"  ✓ {COVARIANCE_FILE.name}")
    print(f"  ✓ {DISTANCE_FILE.name}")
    print(f"  ✓ {SUMMARY_FILE.name}")

    print("=" * 60)


if __name__ == "__main__":
    main()
