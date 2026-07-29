"""
===============================================================================
S29_E9_4_CURVATURE_FIELD.py
===============================================================================

Campo de Curvatura Intrínseca do Manifold Reconstruído

Objetivo
--------
Estimar a curvatura local do manifold reconstruído utilizando apenas
informação geométrica intrínseca.

O experimento utiliza:

    • coordenadas do manifold (PC1, PC2, PC3)
    • direções tangentes estimadas no E9.3

Não utiliza qualquer ordenação temporal dos pontos.

A curvatura é definida a partir da variação angular das direções tangentes
entre vizinhos locais.

Produz:

GER_RESULTS/
    S29_E9_4_CURVATURE_FIELD/

        curvature_field.csv
        curvature_statistics.csv
        curvature_distribution.csv
        curvature_certificate.json
        report.txt

===============================================================================
"""

from __future__ import annotations

import json

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors


# =============================================================================
# CAMINHOS
# =============================================================================

BASE = Path("/content/drive/MyDrive/GER_RESULTS")

INPUT_MANIFOLD = (
    BASE
    / "S29"
    / "S29_E9_1_MANIFOLD_RECONSTRUCTION"
    / "chosen_manifold.parquet"
)

)

INPUT_EIGENVECTORS = (

    BASE
    /"S29"
    /"S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION"
    /"eigenvectors.csv"
)

OUTPUT = (

    BASE
    /
    "S29_E9_4_CURVATURE_FIELD"

)

OUTPUT.mkdir(

    parents=True,
    exist_ok=True

)


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

#
# Escala utilizada para definir o campo tangente.
#
# Deve existir em eigenvectors.csv
#

REFERENCE_SCALE = 100


#
# Número de vizinhos locais utilizados
# para reconstrução da conectividade.
#

K_NEIGHBORS = 20


#
# Pequena constante numérica.
#

EPS = 1e-12


# =============================================================================
# CARREGAMENTO
# =============================================================================

def load_manifold():

    print()
    print("=" * 80)
    print("LOADING MANIFOLD")
    print("=" * 80)

    manifold = pd.read_parquet(
        INPUT_MANIFOLD
    )

    print(f"Samples    : {len(manifold):,}")
    print(f"Dimensions : {manifold.shape[1]}")
    print()

    for c in manifold.columns:
        print(f"    {c}")

    return manifold


def load_tangent_field():

    print()
    print("=" * 80)
    print("LOADING TANGENT FIELD")
    print("=" * 80)

    eigenvectors = pd.read_csv(
        INPUT_EIGENVECTORS
    )

    tangent = eigenvectors[

        (eigenvectors["k"] == REFERENCE_SCALE)

        &

        (eigenvectors["component"] == 1)

    ].copy()

    tangent = tangent.sort_values(
        "point"
    ).reset_index(drop=True)

    vector_columns = [

        c

        for c in tangent.columns

        if c.startswith("v")

    ]

    vectors = tangent[
        vector_columns
    ].to_numpy()

    norms = np.linalg.norm(

        vectors,

        axis=1,

        keepdims=True

    )

    vectors = vectors / (

        norms + EPS

    )

    print(f"Tangent vectors : {len(vectors):,}")
    print(f"Reference scale : {REFERENCE_SCALE}")

    return vectors


# =============================================================================
# CONECTIVIDADE LOCAL
# =============================================================================

def build_local_graph(points):

    print()
    print("=" * 80)
    print("BUILDING LOCAL GRAPH")
    print("=" * 80)

    knn = NearestNeighbors(

        n_neighbors=K_NEIGHBORS + 1

    )

    knn.fit(points)

    distances, indices = knn.kneighbors(points)

    #
    # Remove o próprio ponto
    #

    distances = distances[:, 1:]

    indices = indices[:, 1:]

    print(f"Neighbors : {K_NEIGHBORS}")
    print(f"Edges     : {len(points) * K_NEIGHBORS:,}")

    return distances, indices

# =============================================================================
# CAMPO DE CURVATURA
# =============================================================================

def compute_curvature_field(manifold,
                            tangent_vectors,
                            distances,
                            indices):

    print()
    print("=" * 80)
    print("COMPUTING CURVATURE FIELD")
    print("=" * 80)

    points = manifold.to_numpy()

    curvature_rows = []

    tangent_change_rows = []

    for i in range(len(points)):

        p = points[i]

        t = tangent_vectors[i]

        local_curvatures = []

        local_angles = []

        local_distances = []

        for d, j in zip(distances[i], indices[i]):

            q = points[j]

            tj = tangent_vectors[j]

            cos_theta = np.dot(t, tj)

            cos_theta = np.clip(

                np.abs(cos_theta),

                -1.0,

                1.0

            )

            theta = np.arccos(cos_theta)

            curvature = theta / (d + EPS)

            local_curvatures.append(curvature)

            local_angles.append(

                np.degrees(theta)

            )

            local_distances.append(d)

            tangent_change_rows.append({

                "point": i,

                "neighbor": int(j),

                "distance": float(d),

                "angle_deg": float(

                    np.degrees(theta)

                ),

                "curvature": float(curvature)

            })

        local_curvatures = np.asarray(local_curvatures)

        local_angles = np.asarray(local_angles)

        local_distances = np.asarray(local_distances)

        curvature_rows.append({

            "point": i,

            "curvature_mean":
                float(local_curvatures.mean()),

            "curvature_median":
                float(np.median(local_curvatures)),

            "curvature_std":
                float(local_curvatures.std()),

            "curvature_max":
                float(local_curvatures.max()),

            "angle_mean_deg":
                float(local_angles.mean()),

            "angle_max_deg":
                float(local_angles.max()),

            "neighbor_distance_mean":
                float(local_distances.mean()),

            "neighbor_distance_max":
                float(local_distances.max())

        })

        if (i + 1) % 100 == 0:

            print(

                f"{i+1:5d} / {len(points)}"

            )

    curvature = pd.DataFrame(

        curvature_rows

    )

    tangent_changes = pd.DataFrame(

        tangent_change_rows

    )

    print()

    print(

        f"Computed curvature for {len(curvature):,} points."

    )

    return (

        curvature,

        tangent_changes

    )


# =============================================================================
# RESUMO LOCAL
# =============================================================================

def summarize_curvature(curvature):

    print()
    print("=" * 80)
    print("LOCAL CURVATURE SUMMARY")
    print("=" * 80)

    summary = {

        "points":
            int(len(curvature)),

        "mean_curvature":
            float(

                curvature["curvature_mean"].mean()

            ),

        "median_curvature":
            float(

                curvature["curvature_median"].median()

            ),

        "max_curvature":
            float(

                curvature["curvature_max"].max()

            ),

        "mean_angle":
            float(

                curvature["angle_mean_deg"].mean()

            ),

        "max_angle":
            float(

                curvature["angle_max_deg"].max()

            )

    }

    for key, value in summary.items():

        print(

            f"{key:25s}: {value}"

        )

    return summary

# =============================================================================
# ESTATÍSTICAS DA CURVATURA
# =============================================================================

def build_curvature_statistics(curvature,
                               tangent_changes):

    print()
    print("=" * 80)
    print("CURVATURE STATISTICS")
    print("=" * 80)

    statistics = {

        "points":
            int(len(curvature)),

        "mean_curvature":
            float(
                curvature["curvature_mean"].mean()
            ),

        "median_curvature":
            float(
                curvature["curvature_mean"].median()
            ),

        "std_curvature":
            float(
                curvature["curvature_mean"].std()
            ),

        "min_curvature":
            float(
                curvature["curvature_mean"].min()
            ),

        "max_curvature":
            float(
                curvature["curvature_mean"].max()
            ),

        "p90_curvature":
            float(
                np.percentile(
                    curvature["curvature_mean"],
                    90
                )
            ),

        "p95_curvature":
            float(
                np.percentile(
                    curvature["curvature_mean"],
                    95
                )
            ),

        "p99_curvature":
            float(
                np.percentile(
                    curvature["curvature_mean"],
                    99
                )
            ),

        "mean_angle_deg":
            float(
                tangent_changes["angle_deg"].mean()
            ),

        "median_angle_deg":
            float(
                tangent_changes["angle_deg"].median()
            ),

        "max_angle_deg":
            float(
                tangent_changes["angle_deg"].max()
            )

    }

    print()

    for key, value in statistics.items():

        print(

            f"{key:25s}: {value}"

        )

    return statistics


# =============================================================================
# DISTRIBUIÇÃO DA CURVATURA
# =============================================================================

def build_curvature_distribution(curvature):

    print()
    print("=" * 80)
    print("CURVATURE DISTRIBUTION")
    print("=" * 80)

    values = curvature["curvature_mean"].to_numpy()

    histogram, edges = np.histogram(

        values,

        bins=30

    )

    distribution = pd.DataFrame({

        "bin_left": edges[:-1],

        "bin_right": edges[1:],

        "count": histogram

    })

    print(

        f"Histogram bins : {len(distribution)}"

    )

    return distribution


# =============================================================================
# REGIÕES DE CURVATURA
# =============================================================================

def classify_curvature_regions(curvature):

    print()
    print("=" * 80)
    print("CURVATURE REGIONS")
    print("=" * 80)

    p25 = np.percentile(

        curvature["curvature_mean"],

        25

    )

    p75 = np.percentile(

        curvature["curvature_mean"],

        75

    )

    labels = []

    for value in curvature["curvature_mean"]:

        if value <= p25:

            labels.append(

                "LOW"

            )

        elif value >= p75:

            labels.append(

                "HIGH"

            )

        else:

            labels.append(

                "MEDIUM"

            )

    regions = curvature.copy()

    regions["region"] = labels

    counts = (

        regions["region"]

        .value_counts()

        .sort_index()

    )

    print()

    print(counts)

    return regions


# =============================================================================
# IDENTIFICAÇÃO DE SINGULARIDADES
# =============================================================================

def detect_curvature_singularities(curvature):

    print()
    print("=" * 80)
    print("CURVATURE SINGULARITIES")
    print("=" * 80)

    threshold = np.percentile(

        curvature["curvature_mean"],

        99

    )

    singularities = curvature[

        curvature["curvature_mean"]

        >=

        threshold

    ].copy()

    singularities = singularities.sort_values(

        "curvature_mean",

        ascending=False

    )

    print(

        f"Threshold : {threshold:.6f}"

    )

    print(

        f"Points    : {len(singularities)}"

    )

    return singularities

# =============================================================================
# ANÁLISE ESTRUTURAL DA CURVATURA
# =============================================================================

def analyze_curvature_structure(curvature,
                                regions,
                                singularities):

    print()
    print("=" * 80)
    print("STRUCTURAL CURVATURE ANALYSIS")
    print("=" * 80)

    analysis = {}

    values = curvature["curvature_mean"].to_numpy()

    analysis["points"] = int(len(values))

    analysis["mean"] = float(np.mean(values))
    analysis["median"] = float(np.median(values))
    analysis["std"] = float(np.std(values))

    analysis["cv"] = float(

        np.std(values)

        /

        (

            np.mean(values)

            + EPS

        )

    )

    analysis["low_regions"] = int(

        (regions["region"] == "LOW").sum()

    )

    analysis["medium_regions"] = int(

        (regions["region"] == "MEDIUM").sum()

    )

    analysis["high_regions"] = int(

        (regions["region"] == "HIGH").sum()

    )

    analysis["singularities"] = int(

        len(singularities)

    )

    analysis["singularity_fraction"] = float(

        len(singularities)

        /

        len(curvature)

    )

    print()

    for key, value in analysis.items():

        print(

            f"{key:25s}: {value}"

        )

    return analysis


# =============================================================================
# PERFIL GEOMÉTRICO
# =============================================================================

def classify_geometry(analysis):

    print()
    print("=" * 80)
    print("GEOMETRIC PROFILE")
    print("=" * 80)

    cv = analysis["cv"]

    singular_fraction = analysis["singularity_fraction"]

    if cv < 0.10:

        profile = "UNIFORM"

    elif cv < 0.30:

        profile = "SMOOTH"

    elif cv < 0.60:

        profile = "MODERATELY_STRUCTURED"

    else:

        profile = "HIGHLY_STRUCTURED"

    if singular_fraction > 0.05:

        singular_profile = "DISTRIBUTED"

    else:

        singular_profile = "LOCALIZED"

    result = {

        "geometric_profile": profile,

        "singularity_profile": singular_profile

    }

    print()

    print(f"Geometry      : {profile}")
    print(f"Singularities : {singular_profile}")

    return result


# =============================================================================
# CONSISTÊNCIA DO CAMPO
# =============================================================================

def evaluate_field_consistency(curvature):

    print()
    print("=" * 80)
    print("FIELD CONSISTENCY")
    print("=" * 80)

    values = curvature["curvature_mean"].to_numpy()

    gradient = np.abs(

        np.diff(

            np.sort(values)

        )

    )

    consistency = {

        "mean_gradient":

            float(

                gradient.mean()

            ),

        "max_gradient":

            float(

                gradient.max()

            ),

        "median_gradient":

            float(

                np.median(

                    gradient

                )

            )

    }

    print()

    for key, value in consistency.items():

        print(

            f"{key:25s}: {value}"

        )

    return consistency

# =============================================================================
# EXPORTAÇÃO
# =============================================================================

def export_results(curvature,
                   tangent_changes,
                   distribution,
                   regions,
                   singularities):

    print()
    print("=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)

    curvature.to_csv(
        OUTPUT / "curvature_field.csv",
        index=False
    )

    tangent_changes.to_csv(
        OUTPUT / "tangent_changes.csv",
        index=False
    )

    distribution.to_csv(
        OUTPUT / "curvature_distribution.csv",
        index=False
    )

    regions.to_csv(
        OUTPUT / "curvature_regions.csv",
        index=False
    )

    singularities.to_csv(
        OUTPUT / "curvature_singularities.csv",
        index=False
    )

    print("Export complete.")


# =============================================================================
# CERTIFICADO
# =============================================================================

def build_certificate(statistics,
                      analysis,
                      profile,
                      consistency):

    certificate = {

        "experiment":
            "S29_E9_4_CURVATURE_FIELD",

        "points":
            statistics["points"],

        "mean_curvature":
            statistics["mean_curvature"],

        "median_curvature":
            statistics["median_curvature"],

        "std_curvature":
            statistics["std_curvature"],

        "p95_curvature":
            statistics["p95_curvature"],

        "geometric_profile":
            profile["geometric_profile"],

        "singularity_profile":
            profile["singularity_profile"],

        "singularity_fraction":
            analysis["singularity_fraction"],

        "mean_gradient":
            consistency["mean_gradient"],

        "max_gradient":
            consistency["max_gradient"]

    }

    with open(

        OUTPUT /
        "curvature_certificate.json",

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

def build_report(statistics,
                 analysis,
                 profile,
                 consistency):

    report = []

    report.append("=" * 80)
    report.append("S29 E9.4")
    report.append("CURVATURE FIELD")
    report.append("=" * 80)
    report.append("")

    report.append(f"Points                 : {statistics['points']:,}")
    report.append(f"Mean Curvature         : {statistics['mean_curvature']:.6f}")
    report.append(f"Median Curvature       : {statistics['median_curvature']:.6f}")
    report.append(f"Std Curvature          : {statistics['std_curvature']:.6f}")
    report.append(f"P95 Curvature          : {statistics['p95_curvature']:.6f}")
    report.append("")

    report.append(f"Geometry Profile       : {profile['geometric_profile']}")
    report.append(f"Singularity Profile    : {profile['singularity_profile']}")
    report.append(f"Singularity Fraction   : {analysis['singularity_fraction']:.6f}")
    report.append("")

    report.append(f"Mean Gradient          : {consistency['mean_gradient']:.6f}")
    report.append(f"Median Gradient        : {consistency['median_gradient']:.6f}")
    report.append(f"Max Gradient           : {consistency['max_gradient']:.6f}")

    report.append("")
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    with open(

        OUTPUT /
        "report.txt",

        "w",

        encoding="utf-8"

    ) as f:

        f.write("\n".join(report))

    print()
    print("\n".join(report))


# =============================================================================
# MAIN
# =============================================================================

def main():

    print()
    print("=" * 80)
    print("S29 E9.4")
    print("CURVATURE FIELD")
    print("=" * 80)

    manifold = load_manifold()

    tangent_vectors = load_tangent_field()

    distances, indices = build_local_graph(

        manifold.to_numpy()

    )

    curvature, tangent_changes = compute_curvature_field(

        manifold,
        tangent_vectors,
        distances,
        indices

    )

    summarize_curvature(

        curvature

    )

    statistics = build_curvature_statistics(

        curvature,
        tangent_changes

    )

    distribution = build_curvature_distribution(

        curvature

    )

    regions = classify_curvature_regions(

        curvature

    )

    singularities = detect_curvature_singularities(

        curvature

    )

    analysis = analyze_curvature_structure(

        curvature,
        regions,
        singularities

    )

    profile = classify_geometry(

        analysis

    )

    consistency = evaluate_field_consistency(

        curvature

    )

    export_results(

        curvature,
        tangent_changes,
        distribution,
        regions,
        singularities

    )

    build_certificate(

        statistics,
        analysis,
        profile,
        consistency

    )

    build_report(

        statistics,
        analysis,
        profile,
        consistency

    )

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()
