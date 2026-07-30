"""
=============================================================
S29_E10_0_DATA_CONTEXT.py
=============================================================

S29 — E10.0

Camada oficial de acesso aos dados consolidados da Série S29.

Este módulo NÃO executa análises científicas.

Sua única responsabilidade é localizar, validar e carregar
os principais datasets produzidos em S29 para utilização
pelos experimentos E10.

=============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S29")


# ============================================================
# Estrutura de dados
# ============================================================

@dataclass
class S29Context:

    root: Path

    observables: pd.DataFrame
    signatures: pd.DataFrame
    geometries: pd.DataFrame
    density_points: pd.DataFrame

    manifold: pd.DataFrame
    normalized_observables: pd.DataFrame

    atlas_graph: pd.DataFrame

    metric: pd.DataFrame

    curvature: pd.DataFrame

    connection: pd.DataFrame


# ============================================================
# Utilitário
# ============================================================

def _load(path: Path):

    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix == ".parquet":
        return pd.read_parquet(path)

    if path.suffix == ".csv":
        return pd.read_csv(path)

    raise ValueError(f"Formato não suportado: {path}")


# ============================================================
# Interface pública
# ============================================================

def load_s29_context(
    root=ROOT,
    verbose=True,
):

    root = Path(root)

    files = {

        "observables":
            root / "S29_E6.1/observables.parquet",

        "signatures":
            root / "S29_E6.1/signatures.parquet",

        "geometries":
            root / "S29_E6.1/geometries.parquet",

        "density_points":
            root / "S29_E6.1/density_points.parquet",

        "manifold":
            root / "S29_E9_1_MANIFOLD_RECONSTRUCTION/chosen_manifold.parquet",

        "normalized_observables":
            root / "S29_E9_1_MANIFOLD_RECONSTRUCTION/normalized_observables.parquet",

        "atlas_graph":
            root / "S29_E9_2_LOCAL_MANIFOLD_ATLAS/atlas_graph.parquet",

        "metric":
            root / "S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION/metric.csv",

        "curvature":
            root / "S29_E9_4_CURVATURE_FIELD/curvature_field.csv",

        "connection":
            root / "S29_E9_5_DISCRETE_CONNECTION/discrete_connection.csv",

    }

    if verbose:

        print("=" * 70)
        print("S29 DATA CONTEXT")
        print("=" * 70)

    loaded = {}

    for name, path in files.items():

        if verbose:
            print(f"Carregando {name:<25} ... ", end="")

        loaded[name] = _load(path)

        if verbose:
            print("OK")

    if verbose:

        print()
        print("Datasets carregados:", len(loaded))

    return S29Context(

        root=root,

        observables=loaded["observables"],
        signatures=loaded["signatures"],
        geometries=loaded["geometries"],
        density_points=loaded["density_points"],

        manifold=loaded["manifold"],
        normalized_observables=loaded["normalized_observables"],

        atlas_graph=loaded["atlas_graph"],

        metric=loaded["metric"],

        curvature=loaded["curvature"],

        connection=loaded["connection"],
    )


# ============================================================
# Execução direta
# ============================================================

if __name__ == "__main__":

    ctx = load_s29_context()

    print()

    print("Resumo")

    print("------------------------------")

    print("Observables :", len(ctx.observables))
    print("Signatures  :", len(ctx.signatures))
    print("Geometries  :", len(ctx.geometries))
    print("Manifold    :", len(ctx.manifold))
    print("Metric      :", len(ctx.metric))
    print("Curvature   :", len(ctx.curvature))
    print("Connection  :", len(ctx.connection))
