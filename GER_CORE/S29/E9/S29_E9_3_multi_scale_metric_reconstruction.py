"""
===============================================================================
S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION.py
===============================================================================

GER — Geometria Espectral Relacional

S29.E9.3

MULTI-SCALE METRIC RECONSTRUCTION

Hipótese
---------
A métrica local reconstruída converge quando a escala observacional aumenta.

Entrada
-------
chosen_manifold.parquet

Saídas
------
metric_scan.parquet
metric_summary.csv
covariance_tensors.parquet
dimension_profile.csv
anisotropy_profile.csv
stability_profile.csv
scale_statistics.json
metric_certificate.json
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
    / "S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True
)

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

NEIGHBOR_SCALES = [

    10,
    20,
    30,
    40,
    50,
    75,
    100,
    150,
    200,
    300

]

EPS = 1e-12

RANDOM_STATE = 42

# =============================================================================
# LEITURA
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
# KNN POR ESCALA
# =============================================================================


def build_knn(manifold, k):

    nbrs = NearestNeighbors(

        n_neighbors=k,

        algorithm="auto"

    )

    nbrs.fit(

        manifold.values

    )

    distances, indices = nbrs.kneighbors(

        manifold.values

    )

    return distances, indices


# =============================================================================
# PREPARAÇÃO DAS VIZINHANÇAS
# =============================================================================


def build_neighborhoods(manifold,
                        indices):

    neighborhoods = []

    for idx in indices:

        neighborhoods.append(

            manifold.iloc[idx].values

        )

    return neighborhoods


# =============================================================================
# PARTICIPATION RATIO
# =============================================================================


def participation_dimension(variance):

    participation = (

        variance.sum() ** 2

    ) / (

        np.sum(

            variance ** 2

        ) + EPS

    )

    return max(

        1,

        int(

            round(participation)

        )

    )

# =============================================================================
# ANÁLISE DE UMA ESCALA
# =============================================================================


def analyze_scale(manifold,
                  k):

    print()
    print("=" * 80)
    print(f"SCALE k = {k}")
    print("=" * 80)

    distances, indices = build_knn(
        manifold,
        k
    )

    neighborhoods = build_neighborhoods(
        manifold,
        indices
    )

    metric_rows = []

    covariance_rows = []

    eigenvalue_rows = []

    eigenvector_rows = []

    dimension_rows = []

    anisotropy_rows = []

    stability_rows = []

    for point, patch in enumerate(neighborhoods):

        # ---------------------------------------------------------
        # Covariância
        # ---------------------------------------------------------

        covariance = np.cov(
            patch,
            rowvar=False
        )

        row = {

            "k": k,

            "point": point

        }

        for i in range(covariance.shape[0]):

            for j in range(covariance.shape[1]):

                row[f"c{i+1}_{j+1}"] = float(

                    covariance[i, j]

                )

        covariance_rows.append(row)

        # ---------------------------------------------------------
        # PCA
        # ---------------------------------------------------------

        pca = PCA()

        pca.fit(patch)

        eigvals = pca.explained_variance_

        eigvecs = pca.components_

        variance = pca.explained_variance_ratio_

        # ---------------------------------------------------------
        # Dimensão Local
        # ---------------------------------------------------------

        local_dimension = participation_dimension(
            variance
        )

        dimension_rows.append({

            "k": k,

            "point": point,

            "dimension": local_dimension

        })

        # ---------------------------------------------------------
        # Autovalores
        # ---------------------------------------------------------

        for component, value in enumerate(eigvals):

            eigenvalue_rows.append({

                "k": k,

                "point": point,

                "component": component + 1,

                "eigenvalue": float(value)

            })

        # ---------------------------------------------------------
        # Autovetores
        # ---------------------------------------------------------

        for component, vector in enumerate(eigvecs):

            row = {

                "k": k,

                "point": point,

                "component": component + 1

            }

            for coordinate, value in enumerate(vector):

                row[f"v{coordinate+1}"] = float(value)

            eigenvector_rows.append(row)

        # ---------------------------------------------------------
        # Anisotropia
        # ---------------------------------------------------------

        anisotropy = (

            eigvals[0]

            /

            (

                eigvals.sum()

                + EPS

            )

        )

        anisotropy_rows.append({

            "k": k,

            "point": point,

            "anisotropy": float(
                anisotropy
            )

        })

        # ---------------------------------------------------------
        # Estabilidade
        # ---------------------------------------------------------

        stability = 1.0 - np.std(
            variance
        )

        stability_rows.append({

            "k": k,

            "point": point,

            "stability": float(
                stability
            )

        })

        # ---------------------------------------------------------
        # Resumo
        # ---------------------------------------------------------

        metric_rows.append({

            "k": k,

            "point": point,

            "dimension": local_dimension,

            "anisotropy": float(
                anisotropy
            ),

            "stability": float(
                stability
            ),

            "largest_eigenvalue": float(
                eigvals[0]
            ),

            "smallest_eigenvalue": float(
                eigvals[-1]
            )

        })

    metric = pd.DataFrame(
        metric_rows
    )

    covariance = pd.DataFrame(
        covariance_rows
    )

    eigenvalues = pd.DataFrame(
        eigenvalue_rows
    )

    eigenvectors = pd.DataFrame(
        eigenvector_rows
    )

    dimension = pd.DataFrame(
        dimension_rows
    )

    anisotropy = pd.DataFrame(
        anisotropy_rows
    )

    stability = pd.DataFrame(
        stability_rows
    )

    print()

    print(
        f"Processed {len(metric):,} local metrics."
    )

    return (

        metric,

        covariance,

        eigenvalues,

        eigenvectors,

        dimension,

        anisotropy,

        stability

    )

# =============================================================================
# EXECUÇÃO MULTI-ESCALA
# =============================================================================


def run_multiscale(manifold):

    metric_all = []

    covariance_all = []

    eigenvalues_all = []

    eigenvectors_all = []

    dimension_all = []

    anisotropy_all = []

    stability_all = []

    for k in NEIGHBOR_SCALES:

        (

            metric,

            covariance,

            eigenvalues,

            eigenvectors,

            dimension,

            anisotropy,

            stability

        ) = analyze_scale(

            manifold,

            k

        )

        metric_all.append(
            metric
        )

        covariance_all.append(
            covariance
        )

        eigenvalues_all.append(
            eigenvalues
        )

        eigenvectors_all.append(
            eigenvectors
        )

        dimension_all.append(
            dimension
        )

        anisotropy_all.append(
            anisotropy
        )

        stability_all.append(
            stability
        )

    metric_all = pd.concat(

        metric_all,

        ignore_index=True

    )

    covariance_all = pd.concat(

        covariance_all,

        ignore_index=True

    )

    eigenvalues_all = pd.concat(

        eigenvalues_all,

        ignore_index=True

    )

    eigenvectors_all = pd.concat(

        eigenvectors_all,

        ignore_index=True

    )

    dimension_all = pd.concat(

        dimension_all,

        ignore_index=True

    )

    anisotropy_all = pd.concat(

        anisotropy_all,

        ignore_index=True

    )

    stability_all = pd.concat(

        stability_all,

        ignore_index=True

    )

    print()

    print("=" * 80)

    print("MULTI-SCALE SUMMARY")

    print("=" * 80)

    print(f"Scales processed : {len(NEIGHBOR_SCALES)}")

    print(f"Total analyses   : {len(metric_all):,}")

    print()

    return (

        metric_all,

        covariance_all,

        eigenvalues_all,

        eigenvectors_all,

        dimension_all,

        anisotropy_all,

        stability_all

    )

# =============================================================================
# EXECUÇÃO MULTI-ESCALA
# =============================================================================


def run_multiscale(manifold):

    metric_all = []

    covariance_all = []

    eigenvalues_all = []

    eigenvectors_all = []

    dimension_all = []

    anisotropy_all = []

    stability_all = []

    for k in NEIGHBOR_SCALES:

        (

            metric,

            covariance,

            eigenvalues,

            eigenvectors,

            dimension,

            anisotropy,

            stability

        ) = analyze_scale(

            manifold,

            k

        )

        metric_all.append(
            metric
        )

        covariance_all.append(
            covariance
        )

        eigenvalues_all.append(
            eigenvalues
        )

        eigenvectors_all.append(
            eigenvectors
        )

        dimension_all.append(
            dimension
        )

        anisotropy_all.append(
            anisotropy
        )

        stability_all.append(
            stability
        )

    metric_all = pd.concat(

        metric_all,

        ignore_index=True

    )

    covariance_all = pd.concat(

        covariance_all,

        ignore_index=True

    )

    eigenvalues_all = pd.concat(

        eigenvalues_all,

        ignore_index=True

    )

    eigenvectors_all = pd.concat(

        eigenvectors_all,

        ignore_index=True

    )

    dimension_all = pd.concat(

        dimension_all,

        ignore_index=True

    )

    anisotropy_all = pd.concat(

        anisotropy_all,

        ignore_index=True

    )

    stability_all = pd.concat(

        stability_all,

        ignore_index=True

    )

    print()

    print("=" * 80)

    print("MULTI-SCALE SUMMARY")

    print("=" * 80)

    print(f"Scales processed : {len(NEIGHBOR_SCALES)}")

    print(f"Total analyses   : {len(metric_all):,}")

    print()

    return (

        metric_all,

        covariance_all,

        eigenvalues_all,

        eigenvectors_all,

        dimension_all,

        anisotropy_all,

        stability_all

    )

# =============================================================================
# CONVERGÊNCIA ENTRE ESCALAS
# =============================================================================


def analyze_convergence(metric,
                        eigenvectors):

    print()
    print("=" * 80)
    print("MULTI-SCALE CONVERGENCE")
    print("=" * 80)

    convergence_rows = []

    scales = sorted(

        metric["k"].unique()

    )

    for i in range(

        len(scales) - 1

    ):

        k1 = scales[i]

        k2 = scales[i + 1]

        m1 = (

            metric[
                metric["k"] == k1
            ]

            .sort_values("point")

            .reset_index(drop=True)

        )

        m2 = (

            metric[
                metric["k"] == k2
            ]

            .sort_values("point")

            .reset_index(drop=True)

        )

        dim_delta = np.abs(

            m2["dimension"]

            -

            m1["dimension"]

        )

        aniso_delta = np.abs(

            m2["anisotropy"]

            -

            m1["anisotropy"]

        )

        stab_delta = np.abs(

            m2["stability"]

            -

            m1["stability"]

        )

        # -------------------------------------------------------------
        # Orientação do autovetor principal
        # -------------------------------------------------------------

        e1 = (

            eigenvectors[
                (eigenvectors["k"] == k1)

                &

                (eigenvectors["component"] == 1)

            ]

            .sort_values("point")

            .reset_index(drop=True)

        )

        e2 = (

            eigenvectors[
                (eigenvectors["k"] == k2)

                &

                (eigenvectors["component"] == 1)

            ]

            .sort_values("point")

            .reset_index(drop=True)

        )

        vector_columns = [

            c

            for c in e1.columns

            if c.startswith("v")

        ]

        angles = []

        for row in range(len(e1)):

            v1 = e1.loc[

                row,

                vector_columns

            ].values.astype(float)

            v2 = e2.loc[

                row,

                vector_columns

            ].values.astype(float)

            cos_theta = np.dot(

                v1,

                v2

            )

            cos_theta = np.clip(

                cos_theta,

                -1.0,

                1.0

            )

            theta = np.degrees(

                np.arccos(

                    np.abs(cos_theta)

                )

            )

            angles.append(theta)

        convergence_rows.append({

            "k_from":

                k1,

            "k_to":

                k2,

            "mean_dimension_change":

                float(

                    dim_delta.mean()

                ),

            "max_dimension_change":

                float(

                    dim_delta.max()

                ),

            "mean_anisotropy_change":

                float(

                    aniso_delta.mean()

                ),

            "max_anisotropy_change":

                float(

                    aniso_delta.max()

                ),

            "mean_stability_change":

                float(

                    stab_delta.mean()

                ),

            "max_stability_change":

                float(

                    stab_delta.max()

                ),

            "mean_orientation_change_deg":

                float(

                    np.mean(

                        angles

                    )

                ),

            "max_orientation_change_deg":

                float(

                    np.max(

                        angles

                    )

                )

        })

    convergence = pd.DataFrame(

        convergence_rows

    )

    convergence.to_csv(

        OUTPUT /

        "metric_convergence.csv",

        index=False

    )

    print()

    print(

        convergence

    )

    return convergence


# =============================================================================
# ESTATÍSTICAS GLOBAIS
# =============================================================================


def build_scale_statistics(metric,
                           convergence):

    print()
    print("=" * 80)
    print("GLOBAL STATISTICS")
    print("=" * 80)

    summary = []

    for k in sorted(

        metric["k"].unique()

    ):

        subset = metric[

            metric["k"] == k

        ]

        summary.append({

            "k":

                k,

            "mean_dimension":

                float(

                    subset["dimension"].mean()

                ),

            "mean_anisotropy":

                float(

                    subset["anisotropy"].mean()

                ),

            "mean_stability":

                float(

                    subset["stability"].mean()

                )

        })

    summary = pd.DataFrame(

        summary

    )

    summary.to_csv(

        OUTPUT /

        "metric_summary.csv",

        index=False

    )

    statistics = {

        "number_of_scales":

            int(

                len(summary)

            ),

        "total_local_reconstructions":

            int(

                len(metric)

            ),

        "mean_dimension":

            float(

                metric["dimension"].mean()

            ),

        "mean_anisotropy":

            float(

                metric["anisotropy"].mean()

            ),

        "mean_stability":

            float(

                metric["stability"].mean()

            ),

        "mean_dimension_change":

            float(

                convergence[
                    "mean_dimension_change"
                ].mean()

            ),

        "mean_orientation_change_deg":

            float(

                convergence[
                    "mean_orientation_change_deg"
                ].mean()

            )

    }

    with open(

        OUTPUT /

        "scale_statistics.json",

        "w"

    ) as f:

        json.dump(

            statistics,

            f,

            indent=4

        )

    return (

        summary,

        statistics

    )

# =============================================================================
# EXPORTAÇÃO DOS RESULTADOS
# =============================================================================

def export_results(metric,
                   covariance,
                   eigenvalues,
                   eigenvectors,
                   dimension,
                   anisotropy,
                   stability,
                   convergence,
                   summary):

    print()
    print("=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)

    metric.to_csv(
        OUTPUT / "metric.csv",
        index=False
    )

    covariance.to_csv(
        OUTPUT / "covariance.csv",
        index=False
    )

    eigenvalues.to_csv(
        OUTPUT / "eigenvalues.csv",
        index=False
    )

    eigenvectors.to_csv(
        OUTPUT / "eigenvectors.csv",
        index=False
    )

    dimension.to_csv(
        OUTPUT / "dimension.csv",
        index=False
    )

    anisotropy.to_csv(
        OUTPUT / "anisotropy.csv",
        index=False
    )

    stability.to_csv(
        OUTPUT / "stability.csv",
        index=False
    )

    convergence.to_csv(
        OUTPUT / "metric_convergence.csv",
        index=False
    )

    summary.to_csv(
        OUTPUT / "metric_summary.csv",
        index=False
    )

    print("Export complete.")


# =============================================================================
# CERTIFICADO
# =============================================================================

def build_certificate(statistics):

    certificate = {

        "experiment":
            "S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION",

        "samples":
            int(statistics["total_local_reconstructions"]),

        "scales":
            int(statistics["number_of_scales"]),

        "mean_dimension":
            statistics["mean_dimension"],

        "mean_anisotropy":
            statistics["mean_anisotropy"],

        "mean_stability":
            statistics["mean_stability"],

        "mean_dimension_change":
            statistics["mean_dimension_change"],

        "mean_orientation_change_deg":
            statistics["mean_orientation_change_deg"]

    }

    with open(

        OUTPUT / "certificate.json",

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

def build_report(statistics):

    report = []

    report.append("=" * 80)
    report.append("S29 E9.3")
    report.append("MULTI-SCALE METRIC RECONSTRUCTION")
    report.append("=" * 80)
    report.append("")

    report.append(f"Scales: {statistics['number_of_scales']}")
    report.append(f"Reconstructions: {statistics['total_local_reconstructions']:,}")
    report.append("")

    report.append(f"Mean local dimension       : {statistics['mean_dimension']:.6f}")
    report.append(f"Mean anisotropy           : {statistics['mean_anisotropy']:.6f}")
    report.append(f"Mean stability            : {statistics['mean_stability']:.6f}")
    report.append(f"Mean dimension change     : {statistics['mean_dimension_change']:.6f}")
    report.append(f"Mean orientation change   : {statistics['mean_orientation_change_deg']:.6f} deg")

    report.append("")
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    with open(

        OUTPUT / "report.txt",

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
    print("S29 E9.3")
    print("MULTI-SCALE METRIC RECONSTRUCTION")
    print("=" * 80)

    OUTPUT.mkdir(

        parents=True,

        exist_ok=True

    )

    manifold = load_manifold()

    (

        metric,
        covariance,
        eigenvalues,
        eigenvectors,
        dimension,
        anisotropy,
        stability

    ) = run_multiscale(

        manifold

    )

    convergence = analyze_convergence(

        metric,

        eigenvectors

    )

    (

        summary,

        statistics

    ) = build_scale_statistics(

        metric,

        convergence

    )

    export_results(

        metric,
        covariance,
        eigenvalues,
        eigenvectors,
        dimension,
        anisotropy,
        stability,
        convergence,
        summary

    )

    build_certificate(

        statistics

    )

    build_report(

        statistics

    )

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()
