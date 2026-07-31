"""
====================================================================
GER
S29 — E10.1.3.E
Response Atlas
====================================================================

Objetivo
--------
Integrar os resultados produzidos pelos módulos anteriores da
E10.1.3 em uma representação unificada da resposta da superfície
relacional.

Enquanto os módulos B, C e D analisam aspectos específicos do
experimento, este módulo consolida essas informações em um atlas
estrutural único, preservando a correspondência entre cada ponto da
malha (γ,ω) e todas as grandezas observadas.

Este módulo não executa novas simulações nem produz novas métricas
primárias.

Sua responsabilidade consiste exclusivamente na integração dos
produtos experimentais já existentes.

--------------------------------------------------------------------
Entrada
--------------------------------------------------------------------

Este módulo utiliza exclusivamente os resultados produzidos por:

E10.1.3.B
    Response Field

E10.1.3.C
    Propagation Analysis

E10.1.3.D
    Stability Map

Arquivos principais:

    response_field.parquet

    propagation_analysis.parquet

    stability_map.parquet

Nenhum processamento do run_e10_engine() é realizado.

--------------------------------------------------------------------
Objetivos Científicos
--------------------------------------------------------------------

Construir um atlas relacional contendo, para cada ponto da malha:

• parâmetros (γ,ω);

• intensidade da resposta;

• resposta relativa;

• gradiente local;

• organização da propagação;

• estabilidade local;

• nível de estabilidade;

• indicadores derivados produzidos pela E10.1.3.

O atlas constitui uma representação integrada do comportamento da
superfície relacional sob perturbações calibradas.

--------------------------------------------------------------------
Estratégia
--------------------------------------------------------------------

Para cada ponto da malha:

1.

Localizar os registros correspondentes nos módulos:

    B

    C

    D

2.

Verificar consistência entre os identificadores da malha.

3.

Integrar todas as observações em um único registro.

4.

Produzir uma tabela consolidada contendo todas as variáveis
experimentais.

Nenhuma interpretação científica é realizada nesta etapa.

--------------------------------------------------------------------
Produtos
--------------------------------------------------------------------

Produz:

response_atlas.parquet

response_atlas.csv

response_atlas_summary.json

response_atlas_summary.txt

FIGURES/

--------------------------------------------------------------------
Saída para E10.1.3.F
--------------------------------------------------------------------

O módulo seguinte utilizará exclusivamente o atlas integrado para
produzir o certificado científico da campanha.

A emissão das conclusões experimentais permanece responsabilidade da
E10.1.3.F.

====================================================================
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

EXPERIMENT_NAME = "S29_E10_1_3_E"

GRID_SIZE = 21


# ============================================================
# DIRETÓRIOS
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

RESPONSE_DIR = (
    ROOT
    / "E10_1_3_B_ResponseField"
)

PROPAGATION_DIR = (
    ROOT
    / "E10_1_3_C_PropagationAnalysis"
)

STABILITY_DIR = (
    ROOT
    / "E10_1_3_D_StabilityMap"
)

OUTPUT_DIR = (
    ROOT
    / "E10_1_3_E_ResponseAtlas"
)

FIGURES_DIR = (
    OUTPUT_DIR
    / "FIGURES"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS
# ============================================================

RESPONSE_FILE = (
    RESPONSE_DIR
    / "response_field.parquet"
)

PROPAGATION_FILE = (
    PROPAGATION_DIR
    / "propagation_analysis.parquet"
)

STABILITY_FILE = (
    STABILITY_DIR
    / "stability_map.parquet"
)

ATLAS_FILE = (
    OUTPUT_DIR
    / "response_atlas.parquet"
)

ATLAS_CSV = (
    OUTPUT_DIR
    / "response_atlas.csv"
)

SUMMARY_JSON = (
    OUTPUT_DIR
    / "response_atlas_summary.json"
)

SUMMARY_TXT = (
    OUTPUT_DIR
    / "response_atlas_summary.txt"
)


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(slots=True)
class AtlasRecord:

    row: int
    col: int

    gamma: float
    omega: float

    response_norm: float
    relative_response: float

    gradient: float
    neighborhood_mean: float
    propagation_index: float

    stability_index: float
    local_variability: float
    neighborhood_stability: float
    stability_level: int

    stable: bool


# ============================================================
# UTILIDADES
# ============================================================

def ensure_output_structure():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def load_response_field():

    return pd.read_parquet(
        RESPONSE_FILE
    )


def load_propagation_analysis():

    return pd.read_parquet(
        PROPAGATION_FILE
    )


def load_stability_map():

    return pd.read_parquet(
        STABILITY_FILE
    )


def save_dataframe(df):

    df.to_parquet(
        ATLAS_FILE,
        index=False,
    )

    df.to_csv(
        ATLAS_CSV,
        index=False,
    )


def save_json(
    data,
    filepath,
):

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            data,
            fp,
            indent=4,
            ensure_ascii=False,
        )


# ============================================================
# VALIDAÇÃO
# ============================================================

def validate_grid_alignment(
    response_df,
    propagation_df,
    stability_df,
):
    """
    Verifica se os três módulos utilizam
    exatamente a mesma malha relacional.
    """

    reference = response_df[
        [
            "row",
            "col",
            "gamma",
            "omega",
        ]
    ]

    propagation = propagation_df[
        [
            "row",
            "col",
            "gamma",
            "omega",
        ]
    ]

    stability = stability_df[
        [
            "row",
            "col",
            "gamma",
            "omega",
        ]
    ]

    if not reference.equals(propagation):

        raise RuntimeError(
            "Response Field e Propagation Analysis utilizam malhas diferentes."
        )

    if not reference.equals(stability):

        raise RuntimeError(
            "Response Field e Stability Map utilizam malhas diferentes."
        )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

print("=" * 72)
print("GER")
print("S29 - E10.1.3.E")
print("Response Atlas")
print("=" * 72)

ensure_output_structure()

print(f"[OK] Response Field : {RESPONSE_DIR}")
print(f"[OK] Propagation    : {PROPAGATION_DIR}")
print(f"[OK] Stability Map  : {STABILITY_DIR}")
print(f"[OK] Output         : {OUTPUT_DIR}")
print(f"[OK] Grid           : {GRID_SIZE} x {GRID_SIZE}")
print(f"[OK] Total Points   : {GRID_SIZE * GRID_SIZE}")

# ============================================================
# CONSTRUÇÃO DO ATLAS
# ============================================================

def build_response_atlas():
    """
    Integra todos os resultados produzidos
    pela campanha E10.1.3.

    Nenhuma nova métrica é criada.

    O atlas é apenas a consolidação dos
    observáveis produzidos anteriormente.
    """

    response_df = load_response_field()

    propagation_df = load_propagation_analysis()

    stability_df = load_stability_map()

    validate_grid_alignment(

        response_df,
        propagation_df,
        stability_df,

    )

    print()
    print("=" * 72)
    print("BUILDING RESPONSE ATLAS")
    print("=" * 72)

    print("[1/4] Merging Response Field...")

    atlas = response_df.copy()

    print("[2/4] Adding Propagation Analysis...")

    propagation_columns = [

        "gradient",

        "neighborhood_mean",

        "propagation_index",

    ]

    atlas = atlas.join(

        propagation_df[
            propagation_columns
        ]

    )

    print("[3/4] Adding Stability Map...")

    stability_columns = [

        "stability_index",

        "local_variability",

        "neighborhood_stability",

        "stability_level",

    ]

    atlas = atlas.join(

        stability_df[
            stability_columns
        ]

    )

    print("[4/4] Ordering columns...")

    atlas = atlas[

        [

            "row",
            "col",

            "gamma",
            "omega",

            "delta",

            "response_norm",
            "relative_response",

            "gradient",
            "neighborhood_mean",
            "propagation_index",

            "stability_index",
            "local_variability",
            "neighborhood_stability",
            "stability_level",

            "stable",

        ]

    ].copy()

    print()

    print(
        f"Integrated records : {len(atlas)}"
    )

    print(
        f"Variables          : {len(atlas.columns)}"
    )

    return atlas


# ============================================================
# CONSISTÊNCIA
# ============================================================

def verify_atlas_integrity(
    atlas,
):
    """
    Executa verificações estruturais do atlas.
    """

    if len(atlas) != GRID_SIZE * GRID_SIZE:

        raise RuntimeError(

            "Unexpected number of atlas records."

        )

    duplicated = atlas.duplicated(

        subset=[

            "row",
            "col",

        ]

    ).sum()

    if duplicated:

        raise RuntimeError(

            "Duplicate grid coordinates detected."

        )

    missing = atlas.isna().sum().sum()

    if missing:

        raise RuntimeError(

            "Missing values detected in atlas."

        )

    print("[OK] Atlas integrity verified.")

# ============================================================
# RESUMO
# ============================================================

def build_summary(
    atlas,
):
    """
    Constrói o resumo estatístico do
    Response Atlas.
    """

    summary = {

        "grid_size":
            GRID_SIZE,

        "number_of_points":
            int(len(atlas)),

        "number_of_variables":
            int(len(atlas.columns)),

        "response_norm_mean":
            float(
                atlas["response_norm"].mean()
            ),

        "relative_response_mean":
            float(
                atlas["relative_response"].mean()
            ),

        "gradient_mean":
            float(
                atlas["gradient"].mean()
            ),

        "propagation_index_mean":
            float(
                atlas["propagation_index"].mean()
            ),

        "stability_index_mean":
            float(
                atlas["stability_index"].mean()
            ),

        "stable_fraction":
            float(
                atlas["stable"].mean()
            ),

        "stability_levels":

            atlas[
                "stability_level"
            ]

            .value_counts()

            .sort_index()

            .astype(int)

            .to_dict(),

    }

    return summary


# ============================================================
# RELATÓRIO
# ============================================================

def write_summary(
    summary,
):

    with open(

        SUMMARY_TXT,

        "w",

        encoding="utf-8",

    ) as fp:

        fp.write(
            "====================================================\n"
        )

        fp.write(
            "GER\n"
        )

        fp.write(
            "S29 - E10.1.3.E\n"
        )

        fp.write(
            "Response Atlas\n"
        )

        fp.write(
            "====================================================\n\n"
        )

        fp.write(
            f"Grid Size            : {summary['grid_size']} x {summary['grid_size']}\n"
        )

        fp.write(
            f"Points               : {summary['number_of_points']}\n"
        )

        fp.write(
            f"Variables            : {summary['number_of_variables']}\n\n"
        )

        fp.write(
            f"Mean Response        : {summary['response_norm_mean']:.6e}\n"
        )

        fp.write(
            f"Mean Relative Resp.  : {summary['relative_response_mean']:.6e}\n"
        )

        fp.write(
            f"Mean Gradient        : {summary['gradient_mean']:.6e}\n"
        )

        fp.write(
            f"Mean Propagation     : {summary['propagation_index_mean']:.6e}\n"
        )

        fp.write(
            f"Mean Stability       : {summary['stability_index_mean']:.6e}\n\n"
        )

        fp.write(
            "Stability Levels\n"
        )

        for level, count in summary[
            "stability_levels"
        ].items():

            fp.write(
                f"  Level {level} : {count}\n"
            )

        fp.write("\n")

        fp.write(
            f"Stable Fraction      : {summary['stable_fraction']:.6f}\n"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    atlas = build_response_atlas()

    verify_atlas_integrity(
        atlas,
    )

    save_dataframe(
        atlas,
    )

    summary = build_summary(
        atlas,
    )

    save_json(
        summary,
        SUMMARY_JSON,
    )

    write_summary(
        summary,
    )

    print()

    print("=" * 72)
    print("RESPONSE ATLAS COMPLETED")
    print("=" * 72)

    print(
        f"Integrated Points : {summary['number_of_points']}"
    )

    print(
        f"Variables         : {summary['number_of_variables']}"
    )

    print(
        f"Stable Fraction   : {summary['stable_fraction']:.6f}"
    )

    print()

    print(
        f"Results saved to:\n{OUTPUT_DIR}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    main()
