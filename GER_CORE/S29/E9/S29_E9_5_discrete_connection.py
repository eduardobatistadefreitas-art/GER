"""
===============================================================================
S29_E9_5_DISCRETE_CONNECTION.py
===============================================================================

Conexão Discreta e Transporte Paralelo

Objetivo
--------
Construir uma conexão discreta sobre o manifold reconstruído utilizando
o campo tangente obtido no E9.3.

A conexão é definida exclusivamente pela geometria local do manifold.

Cada aresta do grafo local possui uma transformação que relaciona os
espaços tangentes de dois pontos vizinhos.

Produtos:

GER_RESULTS/

    S29/

        S29_E9_5_DISCRETE_CONNECTION/

            discrete_connection.csv

            transport_field.csv

            connection_statistics.csv

            connection_certificate.json

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
    /
    "S29"
    /
    "S29_E9_1_MANIFOLD_RECONSTRUCTION"
    /
    "chosen_manifold.parquet"

)

INPUT_EIGENVECTORS = (

    BASE
    /
    "S29"
    /
    "S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION"
    /
    "eigenvectors.csv"

)

INPUT_CURVATURE = (

    BASE
    /
    "S29"
    /
    "S29_E9_4_CURVATURE_FIELD"
    /
    "curvature_field.csv"

)

OUTPUT = (

    BASE
    /
    "S29"
    /
    "S29_E9_5_DISCRETE_CONNECTION"

)

OUTPUT.mkdir(

    parents=True,
    exist_ok=True

)


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

REFERENCE_SCALE = 100

K_NEIGHBORS = 20

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

    for column in manifold.columns:

        print(f"    {column}")

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

    tangent = (

        tangent

        .sort_values("point")

        .reset_index(drop=True)

    )

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


def load_curvature():

    print()
    print("=" * 80)
    print("LOADING CURVATURE FIELD")
    print("=" * 80)

    curvature = pd.read_csv(

        INPUT_CURVATURE

    )

    print(

        f"Curvature samples : {len(curvature):,}"

    )

    return curvature


# =============================================================================
# GRAFO LOCAL
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

    distances = distances[:, 1:]

    indices = indices[:, 1:]

    print(f"Neighbors : {K_NEIGHBORS}")
    print(f"Edges     : {len(points) * K_NEIGHBORS:,}")

    return (

        distances,

        indices

    )

# =============================================================================
# CONEXÃO DISCRETA
# =============================================================================

def compute_discrete_connection(manifold,
                                tangent_vectors,
                                curvature,
                                distances,
                                indices):

    print()
    print("=" * 80)
    print("COMPUTING DISCRETE CONNECTION")
    print("=" * 80)

    points = manifold.to_numpy()

    curvature_values = curvature[
        "curvature_mean"
    ].to_numpy()

    connection_rows = []

    transport_rows = []

    for i in range(len(points)):

        pi = points[i]

        ti = tangent_vectors[i]

        ki = curvature_values[i]

        for d, j in zip(

            distances[i],

            indices[i]

        ):

            pj = points[j]

            tj = tangent_vectors[j]

            kj = curvature_values[j]

            # ---------------------------------------------------------
            # Ângulo entre espaços tangentes
            # ---------------------------------------------------------

            cosine = np.dot(

                ti,

                tj

            )

            cosine = np.clip(

                np.abs(cosine),

                -1.0,

                1.0

            )

            angle = np.degrees(

                np.arccos(cosine)

            )

            # ---------------------------------------------------------
            # Vetor de transporte
            # ---------------------------------------------------------

            delta = tj - ti

            transport_norm = np.linalg.norm(

                delta

            )

            # ---------------------------------------------------------
            # Diferença de curvatura
            # ---------------------------------------------------------

            curvature_difference = np.abs(

                kj - ki

            )

            # ---------------------------------------------------------
            # Intensidade da conexão
            # ---------------------------------------------------------

            connection_strength = (

                transport_norm

                /

                (

                    d + EPS

                )

            )

            connection_rows.append({

                "source":
                    i,

                "target":
                    int(j),

                "distance":
                    float(d),

                "angle_deg":
                    float(angle),

                "connection_strength":
                    float(connection_strength),

                "curvature_difference":
                    float(curvature_difference)

            })

            transport_rows.append({

                "source":
                    i,

                "target":
                    int(j),

                "dx":
                    float(delta[0]),

                "dy":
                    float(delta[1]),

                "dz":
                    float(delta[2]),

                "transport_norm":
                    float(transport_norm)

            })

        if (i + 1) % 100 == 0:

            print(

                f"{i+1:5d} / {len(points)}"

            )

    connection = pd.DataFrame(

        connection_rows

    )

    transport = pd.DataFrame(

        transport_rows

    )

    print()

    print(

        f"Connections : {len(connection):,}"

    )

    print(

        f"Transport vectors : {len(transport):,}"

    )

    return (

        connection,

        transport

    )


# =============================================================================
# RESUMO DA CONEXÃO
# =============================================================================

def summarize_connection(connection):

    print()
    print("=" * 80)
    print("LOCAL CONNECTION SUMMARY")
    print("=" * 80)

    summary = {

        "connections":

            int(

                len(connection)

            ),

        "mean_strength":

            float(

                connection[
                    "connection_strength"
                ].mean()

            ),

        "median_strength":

            float(

                connection[
                    "connection_strength"
                ].median()

            ),

        "max_strength":

            float(

                connection[
                    "connection_strength"
                ].max()

            ),

        "mean_angle":

            float(

                connection[
                    "angle_deg"
                ].mean()

            ),

        "max_angle":

            float(

                connection[
                    "angle_deg"
                ].max()

            )

    }

    print()

    for key, value in summary.items():

        print(

            f"{key:25s}: {value}"

        )

    return summary

# =============================================================================
# CONNECTION STATISTICS
# =============================================================================

def build_connection_statistics(connection):

    print()
    print("=" * 80)
    print("CONNECTION STATISTICS")
    print("=" * 80)

    stats = {

        "connections":

            int(len(connection)),

        "mean_strength":

            float(
                connection["connection_strength"].mean()
            ),

        "median_strength":

            float(
                connection["connection_strength"].median()
            ),

        "std_strength":

            float(
                connection["connection_strength"].std()
            ),

        "min_strength":

            float(
                connection["connection_strength"].min()
            ),

        "max_strength":

            float(
                connection["connection_strength"].max()
            ),

        "p90_strength":

            float(
                connection["connection_strength"].quantile(0.90)
            ),

        "p95_strength":

            float(
                connection["connection_strength"].quantile(0.95)
            ),

        "p99_strength":

            float(
                connection["connection_strength"].quantile(0.99)
            ),

        "mean_angle_deg":

            float(
                connection["angle_deg"].mean()
            ),

        "median_angle_deg":

            float(
                connection["angle_deg"].median()
            ),

        "max_angle_deg":

            float(
                connection["angle_deg"].max()
            ),

        "mean_curvature_difference":

            float(
                connection[
                    "curvature_difference"
                ].mean()
            )

    }

    print()

    for key, value in stats.items():

        print(f"{key:30s}: {value}")

    return stats


# =============================================================================
# CONNECTION DISTRIBUTION
# =============================================================================

def build_connection_distribution(connection):

    print()
    print("=" * 80)
    print("CONNECTION DISTRIBUTION")
    print("=" * 80)

    hist, edges = np.histogram(

        connection["connection_strength"],

        bins=30

    )

    distribution = pd.DataFrame({

        "bin_left": edges[:-1],

        "bin_right": edges[1:],

        "count": hist

    })

    print("Histogram bins : 30")

    return distribution


# =============================================================================
# CONNECTION REGIONS
# =============================================================================

def classify_connection_regions(connection):

    print()
    print("=" * 80)
    print("CONNECTION REGIONS")
    print("=" * 80)

    q25 = connection[
        "connection_strength"
    ].quantile(0.25)

    q75 = connection[
        "connection_strength"
    ].quantile(0.75)

    connection = connection.copy()

    connection["region"] = np.where(

        connection["connection_strength"] <= q25,

        "LOW",

        np.where(

            connection["connection_strength"] >= q75,

            "HIGH",

            "MEDIUM"

        )

    )

    print()

    print(

        connection["region"].value_counts()

    )

    return connection


# =============================================================================
# CONNECTION SINGULARITIES
# =============================================================================

def detect_connection_singularities(connection):

    print()
    print("=" * 80)
    print("CONNECTION SINGULARITIES")
    print("=" * 80)

    threshold = connection[
        "connection_strength"
    ].quantile(0.99)

    singularities = connection[

        connection["connection_strength"]

        >=

        threshold

    ].copy()

    print(

        f"Threshold : {threshold:.6f}"

    )

    print(

        f"Connections : {len(singularities):,}"

    )

    return singularities

# =============================================================================
# STRUCTURAL CONNECTION ANALYSIS
# =============================================================================

def analyze_connection_structure(connection_regions,
                                 singularities):

    print()
    print("=" * 80)
    print("STRUCTURAL CONNECTION ANALYSIS")
    print("=" * 80)

    strength = connection_regions[
        "connection_strength"
    ]

    summary = {

        "connections":

            int(len(connection_regions)),

        "mean":

            float(strength.mean()),

        "median":

            float(strength.median()),

        "std":

            float(strength.std()),

        "cv":

            float(

                strength.std()

                /

                (

                    strength.mean()

                    + EPS

                )

            ),

        "low_regions":

            int(

                (connection_regions["region"] == "LOW").sum()

            ),

        "medium_regions":

            int(

                (connection_regions["region"] == "MEDIUM").sum()

            ),

        "high_regions":

            int(

                (connection_regions["region"] == "HIGH").sum()

            ),

        "singular_connections":

            int(

                len(singularities)

            ),

        "singularity_fraction":

            float(

                len(singularities)

                /

                len(connection_regions)

            )

    }

    print()

    for key, value in summary.items():

        print(f"{key:25s}: {value}")

    return summary


# =============================================================================
# CONNECTION PROFILE
# =============================================================================

def classify_connection_profile(summary):

    print()
    print("=" * 80)
    print("CONNECTION PROFILE")
    print("=" * 80)

    cv = summary["cv"]

    fraction = summary["singularity_fraction"]

    if cv < 0.50:

        profile = "UNIFORM"

    elif cv < 1.00:

        profile = "SMOOTH"

    elif cv < 2.00:

        profile = "STRUCTURED"

    else:

        profile = "HIGHLY_STRUCTURED"

    if fraction < 0.01:

        singularity = "RARE"

    elif fraction < 0.05:

        singularity = "LOCALIZED"

    else:

        singularity = "WIDESPREAD"

    result = {

        "connection_profile":

            profile,

        "singularity_profile":

            singularity

    }

    print()

    print(

        f"Connection   : {profile}"

    )

    print(

        f"Singularity  : {singularity}"

    )

    return result


# =============================================================================
# CONNECTION CONSISTENCY
# =============================================================================

def evaluate_connection_consistency(connection):

    print()
    print("=" * 80)
    print("CONNECTION CONSISTENCY")
    print("=" * 80)

    gradients = np.abs(

        np.diff(

            np.sort(

                connection[
                    "connection_strength"
                ].to_numpy()

            )

        )

    )

    consistency = {

        "mean_gradient":

            float(

                gradients.mean()

            ),

        "median_gradient":

            float(

                np.median(

                    gradients

                )

            ),

        "max_gradient":

            float(

                gradients.max()

            )

    }

    print()

    for key, value in consistency.items():

        print(f"{key:25s}: {value}")

    return consistency

# =============================================================================
# EXPORT
# =============================================================================

def export_results(connection,
                   transport,
                   distribution,
                   connection_regions,
                   singularities,
                   statistics,
                   structure,
                   profile,
                   consistency):

    print()
    print("=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)

    connection.to_csv(
        OUTPUT / "discrete_connection.csv",
        index=False
    )

    transport.to_csv(
        OUTPUT / "transport_field.csv",
        index=False
    )

    distribution.to_csv(
        OUTPUT / "connection_distribution.csv",
        index=False
    )

    connection_regions.to_csv(
        OUTPUT / "connection_regions.csv",
        index=False
    )

    singularities.to_csv(
        OUTPUT / "connection_singularities.csv",
        index=False
    )

    pd.DataFrame(
        [statistics]
    ).to_csv(
        OUTPUT / "connection_statistics.csv",
        index=False
    )

    certificate = {

        "statistics": statistics,

        "structure": structure,

        "profile": profile,

        "consistency": consistency

    }

    with open(

        OUTPUT / "connection_certificate.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("Export complete.")


# =============================================================================
# REPORT
# =============================================================================

def build_report(statistics,
                 profile,
                 structure,
                 consistency):

    lines = [

        "=" * 80,
        "S29 E9.5",
        "DISCRETE CONNECTION",
        "=" * 80,
        "",

        f"Connections            : {statistics['connections']:,}",
        f"Mean Strength          : {statistics['mean_strength']:.6f}",
        f"Median Strength        : {statistics['median_strength']:.6f}",
        f"Std Strength           : {statistics['std_strength']:.6f}",
        f"P95 Strength           : {statistics['p95_strength']:.6f}",
        "",

        f"Connection Profile     : {profile['connection_profile']}",
        f"Singularity Profile    : {profile['singularity_profile']}",
        f"Singularity Fraction   : {structure['singularity_fraction']:.6f}",
        "",

        f"Mean Gradient          : {consistency['mean_gradient']:.6f}",
        f"Median Gradient        : {consistency['median_gradient']:.6f}",
        f"Max Gradient           : {consistency['max_gradient']:.6f}",
        "",

        "=" * 80,
        "END OF REPORT",
        "=" * 80

    ]

    report = "\n".join(lines)

    print()
    print(report)

    with open(

        OUTPUT / "report.txt",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(report)


# =============================================================================
# MAIN
# =============================================================================

def main():

    print()
    print("=" * 80)
    print("S29 E9.5")
    print("DISCRETE CONNECTION")
    print("=" * 80)

    manifold = load_manifold()

    tangent = load_tangent_field()

    curvature = load_curvature()

    distances, indices = build_local_graph(

        manifold.to_numpy()

    )

    connection, transport = compute_discrete_connection(

        manifold,

        tangent,

        curvature,

        distances,

        indices

    )

    summarize_connection(

        connection

    )

    statistics = build_connection_statistics(

        connection

    )

    distribution = build_connection_distribution(

        connection

    )

    connection_regions = classify_connection_regions(

        connection

    )

    singularities = detect_connection_singularities(

        connection

    )

    structure = analyze_connection_structure(

        connection_regions,

        singularities

    )

    profile = classify_connection_profile(

        structure

    )

    consistency = evaluate_connection_consistency(

        connection

    )

    export_results(

        connection,

        transport,

        distribution,

        connection_regions,

        singularities,

        statistics,

        structure,

        profile,

        consistency

    )

    build_report(

        statistics,

        profile,

        structure,

        consistency

    )

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()
