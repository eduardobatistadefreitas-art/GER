"""
===============================================================================
S29_E9_1_MANIFOLD_RECONSTRUCTION.py
===============================================================================

GER — Geometria Espectral Relacional

S29.E9.1
MANIFOLD RECONSTRUCTION

Objetivo
--------
Reconstruir automaticamente um manifold contínuo a partir da trajetória
produzida na série E8.

Fluxo

trajectory.csv
        │
        ▼
seleção das observáveis
        │
        ▼
normalização
        │
        ▼
estimativa da dimensão intrínseca
        │
        ▼
reconstruções independentes

    PCA
    Isomap
    Spectral Embedding
    UMAP (opcional)

        │
        ▼
comparação objetiva

        │
        ▼
chosen_manifold.parquet

===============================================================================
"""

from __future__ import annotations

import json
import warnings

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA

from sklearn.manifold import (
    Isomap,
    SpectralEmbedding
)

from sklearn.metrics import pairwise_distances

from sklearn.neighbors import NearestNeighbors

warnings.filterwarnings("ignore")

# =============================================================================
# UMAP (opcional)
# =============================================================================

HAS_UMAP = False

try:

    import umap

    HAS_UMAP = True

except Exception:

    HAS_UMAP = False


# =============================================================================
# PATHS
# =============================================================================

ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29"
)

TRAJECTORY = (
    ROOT /
    "S29_E8" /
    "20260728_170754" /
    "trajectory.csv"
)

OUTPUT = (
    ROOT /
    "S29_E9_1_MANIFOLD_RECONSTRUCTION"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True
)

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

RANDOM_STATE = 42

N_NEIGHBORS = 15

MAX_INTRINSIC_DIM = 10

EMBEDDING_DIM = 3

# =============================================================================
# CARREGAMENTO
# =============================================================================


def load_trajectory():

    print()
    print("=" * 80)
    print("LOADING TRAJECTORY")
    print("=" * 80)

    df = pd.read_csv(TRAJECTORY)

    print(f"Samples : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    return df


# =============================================================================
# OBSERVÁVEIS
# =============================================================================


IGNORE_COLUMNS = {

    "index",
    "sigma"

}


def build_observable_matrix(df):

    columns = [

        c

        for c in df.columns

        if c not in IGNORE_COLUMNS

    ]

    X = df[columns].copy()

    numeric = X.select_dtypes(include="number")

    print()
    print("=" * 80)
    print("OBSERVABLE SPACE")
    print("=" * 80)

    print(f"Variables : {len(numeric.columns)}")

    for c in numeric.columns:

        print("   ", c)

    numeric.to_parquet(

        OUTPUT /
        "manifold_input.parquet",

        index=False

    )

    return numeric


# =============================================================================
# NORMALIZAÇÃO
# =============================================================================


def normalize_observables(X):

    print()
    print("=" * 80)
    print("NORMALIZATION")
    print("=" * 80)

    scaler = StandardScaler()

    Xn = scaler.fit_transform(X)

    Xn = pd.DataFrame(

        Xn,

        columns=X.columns

    )

    Xn.to_parquet(

        OUTPUT /
        "normalized_observables.parquet",

        index=False

    )

    return Xn, scaler


# =============================================================================
# DIMENSÃO INTRÍNSECA
# =============================================================================


def estimate_intrinsic_dimension(X):

    """
    Participation Ratio

    d = (Σλ)^2 / Σλ²

    """

    print()
    print("=" * 80)
    print("INTRINSIC DIMENSION")
    print("=" * 80)

    cov = np.cov(

        X.values.T

    )

    eig = np.linalg.eigvalsh(cov)

    eig = eig[eig > 1e-12]

    participation = (

        eig.sum() ** 2

    ) / (

        np.sum(eig ** 2)

    )

    estimated = int(

        np.clip(

            round(participation),

            2,

            MAX_INTRINSIC_DIM

        )

    )

    explained = (

        PCA()

        .fit(X)

        .explained_variance_ratio_

    )

    intrinsic = pd.DataFrame({

        "component":

            np.arange(

                1,

                len(explained) + 1

            ),

        "variance":

            explained,

        "cumulative":

            np.cumsum(explained)

    })

    intrinsic.to_csv(

        OUTPUT /
        "intrinsic_dimension.csv",

        index=False

    )

    print(f"Participation Ratio : {participation:.3f}")
    print(f"Estimated Dimension : {estimated}")

    return estimated

# =============================================================================
# EMBEDDINGS
# =============================================================================


def build_pca_embedding(X, dimension):

    print()
    print("=" * 80)
    print("PCA")
    print("=" * 80)

    model = PCA(
        n_components=dimension,
        random_state=RANDOM_STATE
    )

    embedding = model.fit_transform(X)

    columns = [

        f"PC{i+1}"

        for i in range(dimension)

    ]

    embedding = pd.DataFrame(
        embedding,
        columns=columns
    )

    embedding.to_parquet(
        OUTPUT /
        "embedding_pca.parquet",
        index=False
    )

    return embedding


# =============================================================================


def build_isomap_embedding(X, dimension):

    print()
    print("=" * 80)
    print("ISOMAP")
    print("=" * 80)

    model = Isomap(
        n_neighbors=N_NEIGHBORS,
        n_components=dimension
    )

    embedding = model.fit_transform(X)

    columns = [

        f"ISO{i+1}"

        for i in range(dimension)

    ]

    embedding = pd.DataFrame(
        embedding,
        columns=columns
    )

    embedding.to_parquet(
        OUTPUT /
        "embedding_isomap.parquet",
        index=False
    )

    return embedding


# =============================================================================


def build_spectral_embedding(X, dimension):

    print()
    print("=" * 80)
    print("SPECTRAL EMBEDDING")
    print("=" * 80)

    model = SpectralEmbedding(

        n_components=dimension,

        n_neighbors=N_NEIGHBORS,

        random_state=RANDOM_STATE

    )

    embedding = model.fit_transform(X)

    columns = [

        f"SPEC{i+1}"

        for i in range(dimension)

    ]

    embedding = pd.DataFrame(
        embedding,
        columns=columns
    )

    embedding.to_parquet(

        OUTPUT /
        "embedding_spectral.parquet",

        index=False

    )

    return embedding


# =============================================================================


def build_umap_embedding(X, dimension):

    print()
    print("=" * 80)
    print("UMAP")
    print("=" * 80)

    if not HAS_UMAP:

        print("UMAP not installed.")

        return None

    reducer = umap.UMAP(

        n_neighbors=N_NEIGHBORS,

        n_components=dimension,

        random_state=RANDOM_STATE

    )

    embedding = reducer.fit_transform(X)

    columns = [

        f"UMAP{i+1}"

        for i in range(dimension)

    ]

    embedding = pd.DataFrame(
        embedding,
        columns=columns
    )

    embedding.to_parquet(

        OUTPUT /
        "embedding_umap.parquet",

        index=False

    )

    return embedding


# =============================================================================
# DISTÂNCIAS
# =============================================================================


def distance_preservation(reference, embedding):

    d0 = pairwise_distances(reference)

    d1 = pairwise_distances(embedding)

    correlation = np.corrcoef(

        d0.ravel(),

        d1.ravel()

    )[0, 1]

    rmse = np.sqrt(

        np.mean(

            (d0 - d1) ** 2

        )

    )

    return {

        "distance_correlation": float(correlation),

        "distance_rmse": float(rmse)

    }


# =============================================================================
# VIZINHANÇA
# =============================================================================


def neighborhood_preservation(reference,
                              embedding,
                              k=N_NEIGHBORS):

    nn0 = NearestNeighbors(

        n_neighbors=k

    ).fit(reference)

    nn1 = NearestNeighbors(

        n_neighbors=k

    ).fit(embedding)

    idx0 = nn0.kneighbors(

        return_distance=False

    )

    idx1 = nn1.kneighbors(

        return_distance=False

    )

    scores = []

    for a, b in zip(idx0, idx1):

        scores.append(

            len(set(a).intersection(set(b))) / k

        )

    return float(np.mean(scores))


# =============================================================================
# AVALIAÇÃO DOS EMBEDDINGS
# =============================================================================


def evaluate_embedding(name,
                       reference,
                       embedding):

    dist = distance_preservation(

        reference,

        embedding

    )

    neigh = neighborhood_preservation(

        reference,

        embedding

    )

    return {

        "embedding": name,

        "distance_correlation":
            dist["distance_correlation"],

        "distance_rmse":
            dist["distance_rmse"],

        "neighbor_preservation":
            neigh

    }


# =============================================================================


def evaluate_all_embeddings(X,
                            embeddings):

    print()
    print("=" * 80)
    print("EMBEDDING EVALUATION")
    print("=" * 80)

    rows = []

    for name, emb in embeddings.items():

        if emb is None:

            continue

        result = evaluate_embedding(

            name,

            X,

            emb

        )

        rows.append(result)

        print(
            f"{name:12s}"
            f" Corr={result['distance_correlation']:.5f}"
            f"  RMSE={result['distance_rmse']:.5f}"
            f"  Neighbor={result['neighbor_preservation']:.5f}"
        )

    quality = pd.DataFrame(rows)

    quality.to_csv(

        OUTPUT /
        "embedding_quality.csv",

        index=False

    )

    return quality

# =============================================================================
# ESCOLHA DO MELHOR EMBEDDING
# =============================================================================


def choose_best_embedding(quality):

    print()
    print("=" * 80)
    print("SELECTING BEST EMBEDDING")
    print("=" * 80)

    quality = quality.copy()

    quality["score"] = (

        quality["distance_correlation"]

        +

        quality["neighbor_preservation"]

        -

        quality["distance_rmse"]

    )

    quality = quality.sort_values(

        "score",

        ascending=False

    ).reset_index(drop=True)

    best = quality.iloc[0]

    print()
    print("Best embedding :", best.embedding)
    print("Score          :", round(best.score, 6))

    return best, quality


# =============================================================================
# EXPORTAÇÃO
# =============================================================================


def export_best_embedding(best_name,
                          embeddings):

    embedding = embeddings[best_name].copy()

    embedding.to_parquet(

        OUTPUT /
        "chosen_manifold.parquet",

        index=False

    )

    return embedding


# =============================================================================


def export_certificate(best,
                       quality,
                       intrinsic_dimension):

    certificate = {

        "experiment":
            "S29_E9_1_MANIFOLD_RECONSTRUCTION",

        "trajectory_samples":
            int(len(pd.read_csv(TRAJECTORY))),

        "intrinsic_dimension":
            int(intrinsic_dimension),

        "embedding_dimension":
            EMBEDDING_DIM,

        "candidate_embeddings":
            quality.embedding.tolist(),

        "selected_embedding":
            best.embedding,

        "distance_correlation":
            float(best.distance_correlation),

        "neighbor_preservation":
            float(best.neighbor_preservation),

        "distance_rmse":
            float(best.distance_rmse),

        "score":
            float(best.score)

    }

    with open(

        OUTPUT /
        "manifold_certificate.json",

        "w"

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4

        )

    return certificate


# =============================================================================


def export_report(certificate,
                  quality):

    lines = []

    lines.append("=" * 80)
    lines.append("S29 E9.1")
    lines.append("MANIFOLD RECONSTRUCTION")
    lines.append("=" * 80)
    lines.append("")

    lines.append(
        f"Trajectory samples : {certificate['trajectory_samples']}"
    )

    lines.append(
        f"Intrinsic dimension : {certificate['intrinsic_dimension']}"
    )

    lines.append(
        f"Embedding dimension : {certificate['embedding_dimension']}"
    )

    lines.append("")

    lines.append("Candidate embeddings")
    lines.append("--------------------")

    for _, row in quality.iterrows():

        lines.append(

            f"{row.embedding:12s} "

            f"Corr={row.distance_correlation:.5f} "

            f"Neighbor={row.neighbor_preservation:.5f} "

            f"RMSE={row.distance_rmse:.5f} "

            f"Score={row.score:.5f}"

        )

    lines.append("")
    lines.append("Selected embedding")
    lines.append("------------------")
    lines.append(certificate["selected_embedding"])

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
    print("S29 E9.1")
    print("MANIFOLD RECONSTRUCTION")
    print("=" * 80)

    df = load_trajectory()

    X = build_observable_matrix(df)

    Xn, scaler = normalize_observables(X)

    intrinsic_dimension = estimate_intrinsic_dimension(Xn)

    dimension = min(

        intrinsic_dimension,

        EMBEDDING_DIM

    )

    embeddings = {}

    embeddings["PCA"] = build_pca_embedding(

        Xn,

        dimension

    )

    embeddings["ISOMAP"] = build_isomap_embedding(

        Xn,

        dimension

    )

    embeddings["SPECTRAL"] = build_spectral_embedding(

        Xn,

        dimension

    )

    umap_embedding = build_umap_embedding(

        Xn,

        dimension

    )

    if umap_embedding is not None:

        embeddings["UMAP"] = umap_embedding

    quality = evaluate_all_embeddings(

        Xn,

        embeddings

    )

    best, quality = choose_best_embedding(

        quality

    )

    export_best_embedding(

        best.embedding,

        embeddings

    )

    certificate = export_certificate(

        best,

        quality,

        intrinsic_dimension

    )

    export_report(

        certificate,

        quality

    )

    print()
    print("=" * 80)
    print("RECONSTRUCTION FINISHED")
    print("=" * 80)
    print()

    print("Selected embedding :", certificate["selected_embedding"])
    print("Intrinsic dimension:", certificate["intrinsic_dimension"])
    print()

    print("Results saved to:")
    print(OUTPUT)
    print()


if __name__ == "__main__":
    main()
