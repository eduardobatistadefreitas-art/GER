"""
===============================================================================
S29_E9_2_LOCAL_MANIFOLD_ATLAS.py
===============================================================================

GER — Geometria Espectral Relacional

S29.E9.2

LOCAL MANIFOLD ATLAS

Objetivo
--------
Construir o atlas diferencial local do manifold reconstruído no E9.1.

Entrada

chosen_manifold.parquet

Saídas

local_neighbors.parquet
local_density.csv
local_dimension.csv
tangent_basis.parquet
tangent_eigenvalues.csv
tangent_eigenvectors.parquet
local_curvature.csv
anisotropy_profile.csv
stability_profile.csv
atlas_graph.parquet
atlas_statistics.json
atlas_certificate.json
report.txt

===============================================================================
"""

from __future__ import annotations

import json
import warnings

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

warnings.filterwarnings("ignore")

# =============================================================================
# PATHS
# =============================================================================

ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29"
)

INPUT = (
    ROOT
    / "S29_E9_1_MANIFOLD_RECONSTRUCTION"
    / "chosen_manifold.parquet"
)

OUTPUT = (
    ROOT
    / "S29_E9_2_LOCAL_MANIFOLD_ATLAS"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True
)

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

K_NEIGHBORS = 20

RANDOM_STATE = 42

EPS = 1e-12

# =============================================================================
# CARREGAMENTO
# =============================================================================


def load_manifold():

    print()
    print("=" * 80)
    print("LOADING MANIFOLD")
    print("=" * 80)

    manifold = pd.read_parquet(INPUT)

    print(f"Samples    : {len(manifold):,}")
    print(f"Dimensions : {len(manifold.columns)}")

    print()

    for c in manifold.columns:

        print("   ", c)

    return manifold


# =============================================================================
# KNN
# =============================================================================


def build_knn(manifold):

    print()
    print("=" * 80)
    print("BUILDING KNN")
    print("=" * 80)

    nbrs = NearestNeighbors(

        n_neighbors=K_NEIGHBORS,

        algorithm="auto"

    )

    nbrs.fit(manifold.values)

    distances, indices = nbrs.kneighbors(
        manifold.values
    )

    print(
        f"Neighbors : {K_NEIGHBORS}"
    )

    return distances, indices


# =============================================================================
# EXPORTAÇÃO DA REDE LOCAL
# =============================================================================


def export_neighbor_table(indices,
                          distances):

    rows = []

    for point in range(len(indices)):

        for rank in range(K_NEIGHBORS):

            rows.append({

                "point":

                    point,

                "neighbor":

                    int(indices[point, rank]),

                "rank":

                    rank,

                "distance":

                    float(
                        distances[point, rank]
                    )

            })

    neighbors = pd.DataFrame(rows)

    neighbors.to_parquet(

        OUTPUT /
        "local_neighbors.parquet",

        index=False

    )

    print()

    print(
        f"Neighbor relations : {len(neighbors):,}"
    )

    return neighbors


# =============================================================================
# DENSIDADE LOCAL
# =============================================================================


def compute_local_density(distances):

    print()
    print("=" * 80)
    print("LOCAL DENSITY")
    print("=" * 80)

    mean_distance = distances.mean(axis=1)

    density = 1.0 / (

        mean_distance + EPS

    )

    density = pd.DataFrame({

        "point":

            np.arange(len(density)),

        "mean_neighbor_distance":

            mean_distance,

        "local_density":

            density

    })

    density.to_csv(

        OUTPUT /
        "local_density.csv",

        index=False

    )

    print(
        "Density computed."
    )

    return density


# =============================================================================
# PREPARAÇÃO DAS VIZINHANÇAS
# =============================================================================


def build_local_neighborhoods(manifold,
                              indices):

    print()
    print("=" * 80)
    print("PREPARING LOCAL PATCHES")
    print("=" * 80)

    neighborhoods = []

    for idx in indices:

        neighborhoods.append(

            manifold.iloc[idx].values

        )

    print(
        f"Neighborhoods : {len(neighborhoods):,}"
    )

    return neighborhoods

# =============================================================================
# PCA LOCAL
# =============================================================================


def compute_local_pca(neighborhoods):

    print()
    print("=" * 80)
    print("LOCAL PCA")
    print("=" * 80)

    tangent_rows = []

    eigenvalue_rows = []

    eigenvector_rows = []

    dimension_rows = []

    anisotropy_rows = []

    stability_rows = []

    for point, patch in enumerate(neighborhoods):

        pca = PCA()

        pca.fit(patch)

        eigvals = pca.explained_variance_

        eigvecs = pca.components_

        variance = pca.explained_variance_ratio_

        participation = (

            variance.sum() ** 2

        ) / (

            np.sum(
                variance ** 2
            ) + EPS

        )

        local_dimension = max(
            1,
            int(round(participation))
        )

        tangent = eigvecs[
            :local_dimension
        ]

        # ---------------------------------------------------------
        # Base tangente
        # ---------------------------------------------------------

        for basis_index, vector in enumerate(tangent):

            row = {

                "point": point,

                "basis": basis_index + 1,

                "local_dimension": local_dimension

            }

            for coord_index, value in enumerate(vector):

                row[f"c{coord_index+1}"] = float(value)

            tangent_rows.append(row)

        # ---------------------------------------------------------
        # Dimensão local
        # ---------------------------------------------------------

        dimension_rows.append({

            "point": point,

            "local_dimension": local_dimension

        })

        # ---------------------------------------------------------
        # Autovalores
        # ---------------------------------------------------------

        for i, value in enumerate(eigvals):

            eigenvalue_rows.append({

                "point": point,

                "component": i + 1,

                "eigenvalue": float(value)

            })

        # ---------------------------------------------------------
        # Autovetores
        # ---------------------------------------------------------

        for i, vec in enumerate(eigvecs):

            row = {

                "point": point,

                "component": i + 1

            }

            for j, value in enumerate(vec):

                row[f"v{j+1}"] = float(value)

            eigenvector_rows.append(row)

        # ---------------------------------------------------------
        # Anisotropia
        # ---------------------------------------------------------

        anisotropy = (

            eigvals[0]

            /

            (eigvals.sum() + EPS)

        )

        anisotropy_rows.append({

            "point": point,

            "anisotropy": float(anisotropy),

            "largest_eigenvalue": float(eigvals[0]),

            "smallest_eigenvalue": float(eigvals[-1])

        })

        # ---------------------------------------------------------
        # Estabilidade
        # ---------------------------------------------------------

        stability = 1.0 - np.std(variance)

        stability_rows.append({

            "point": point,

            "stability": float(stability),

            "variance_std": float(

                np.std(variance)

            )

        })

    tangent_basis = pd.DataFrame(
        tangent_rows
    )

    tangent_basis.to_parquet(

        OUTPUT /
        "tangent_basis.parquet",

        index=False

    )

    eigenvalues = pd.DataFrame(
        eigenvalue_rows
    )

    eigenvalues.to_csv(

        OUTPUT /
        "tangent_eigenvalues.csv",

        index=False

    )

    eigenvectors = pd.DataFrame(
        eigenvector_rows
    )

    eigenvectors.to_parquet(

        OUTPUT /
        "tangent_eigenvectors.parquet",

        index=False

    )

    local_dimension = pd.DataFrame(
        dimension_rows
    )

    local_dimension.to_csv(

        OUTPUT /
        "local_dimension.csv",

        index=False

    )

    anisotropy = pd.DataFrame(
        anisotropy_rows
    )

    anisotropy.to_csv(

        OUTPUT /
        "anisotropy_profile.csv",

        index=False

    )

    stability = pd.DataFrame(
        stability_rows
    )

    stability.to_csv(

        OUTPUT /
        "stability_profile.csv",

        index=False

    )

    print()

    print(
        f"Local PCA computed for {len(neighborhoods):,} neighborhoods."
    )

    return (

        tangent_basis,

        eigenvalues,

        eigenvectors,

        local_dimension,

        anisotropy,

        stability

    )

# =============================================================================
# ESTATÍSTICAS DO ATLAS
# =============================================================================


def build_atlas_statistics(local_dimension,
                           anisotropy,
                           density):

    print()
    print("=" * 80)
    print("ATLAS STATISTICS")
    print("=" * 80)

    stats = {

        "points":

            int(len(local_dimension)),

        "mean_local_dimension":

            float(

                local_dimension[
                    "local_dimension"
                ].mean()

            ),

        "minimum_local_dimension":

            int(

                local_dimension[
                    "local_dimension"
                ].min()

            ),

        "maximum_local_dimension":

            int(

                local_dimension[
                    "local_dimension"
                ].max()

            ),

        "mean_anisotropy":

            float(

                anisotropy[
                    "anisotropy"
                ].mean()

            ),

        "maximum_anisotropy":

            float(

                anisotropy[
                    "anisotropy"
                ].max()

            ),

        "minimum_anisotropy":

            float(

                anisotropy[
                    "anisotropy"
                ].min()

            ),

        "mean_density":

            float(

                density[
                    "local_density"
                ].mean()

            )

    }

    with open(

        OUTPUT /
        "atlas_statistics.json",

        "w"

    ) as f:

        json.dump(
            stats,
            f,
            indent=4
        )

    return stats

# =============================================================================
# CURVATURA LOCAL
# =============================================================================


def compute_local_curvature(neighborhoods):

    print()
    print("=" * 80)
    print("LOCAL CURVATURE")
    print("=" * 80)

    rows = []

    for point, patch in enumerate(neighborhoods):

        center = patch[0]

        centered = patch - center

        radius = np.linalg.norm(
            centered,
            axis=1
        )

        curvature = np.mean(radius)

        maximum = np.max(radius)

        minimum = np.min(radius)

        rows.append({

            "point": point,

            "mean_radius": float(curvature),

            "minimum_radius": float(minimum),

            "maximum_radius": float(maximum),

            "local_curvature": float(
                1.0 / (curvature + EPS)
            )

        })

    curvature = pd.DataFrame(rows)

    curvature.to_csv(

        OUTPUT /
        "local_curvature.csv",

        index=False

    )

    return curvature


# =============================================================================
# GRAFO DO ATLAS
# =============================================================================


def export_atlas_graph(indices,
                       distances):

    edges = []

    for i in range(len(indices)):

        for j in range(1, K_NEIGHBORS):

            edges.append({

                "source": i,

                "target": int(indices[i, j]),

                "distance": float(
                    distances[i, j]
                )

            })

    graph = pd.DataFrame(edges)

    graph.to_parquet(

        OUTPUT /
        "atlas_graph.parquet",

        index=False

    )

    return graph


# =============================================================================
# CERTIFICADO
# =============================================================================


def export_certificate(stats):

    certificate = {

        "experiment":

            "S29_E9_2_LOCAL_MANIFOLD_ATLAS",

        "points":

            stats["points"],

        "neighbors":

            K_NEIGHBORS,

        "mean_local_dimension":

            stats["mean_local_dimension"],

        "minimum_local_dimension":

            stats["minimum_local_dimension"],

        "maximum_local_dimension":

            stats["maximum_local_dimension"],

        "mean_anisotropy":

            stats["mean_anisotropy"],

        "mean_density":

            stats["mean_density"]

    }

    with open(

        OUTPUT /
        "atlas_certificate.json",

        "w"

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4

        )

    return certificate


# =============================================================================
# RELATÓRIO
# =============================================================================


def export_report(certificate,
                  stats):

    lines = []

    lines.append("=" * 80)
    lines.append("S29 E9.2")
    lines.append("LOCAL MANIFOLD ATLAS")
    lines.append("=" * 80)
    lines.append("")

    for key, value in certificate.items():

        lines.append(
            f"{key:30s}: {value}"
        )

    lines.append("")
    lines.append("STATISTICS")
    lines.append("-" * 80)

    for key, value in stats.items():

        lines.append(
            f"{key:30s}: {value}"
        )

    with open(

        OUTPUT /
        "report.txt",

        "w"

    ) as f:

        f.write("\n".join(lines))


# =============================================================================
# MAIN
# =============================================================================


def main():

    print()
    print("=" * 80)
    print("S29 E9.2")
    print("LOCAL MANIFOLD ATLAS")
    print("=" * 80)

    manifold = load_manifold()

    distances, indices = build_knn(
        manifold
    )

    export_neighbor_table(
        indices,
        distances
    )

    density = compute_local_density(
        distances
    )

    neighborhoods = build_local_neighborhoods(
        manifold,
        indices
    )

    (
        tangent_basis,
        eigenvalues,
        eigenvectors,
        local_dimension,
        anisotropy,
        stability

    ) = compute_local_pca(
        neighborhoods
    )

    curvature = compute_local_curvature(
        neighborhoods
    )

    graph = export_atlas_graph(
        indices,
        distances
    )

    stats = build_atlas_statistics(

        local_dimension,

        anisotropy,

        density

    )

    certificate = export_certificate(
        stats
    )

    export_report(
        certificate,
        stats
    )

    print()
    print("=" * 80)
    print("LOCAL MANIFOLD ATLAS FINISHED")
    print("=" * 80)
    print()

    print("Points            :", len(manifold))
    print("Neighbors         :", K_NEIGHBORS)
    print(
        "Mean dimension    :",
        round(
            stats["mean_local_dimension"],
            3
        )
    )
    print(
        "Mean anisotropy   :",
        round(
            stats["mean_anisotropy"],
            6
        )
    )
    print()

    print("Results saved to:")
    print(OUTPUT)
    print()


if __name__ == "__main__":
    main()                             
