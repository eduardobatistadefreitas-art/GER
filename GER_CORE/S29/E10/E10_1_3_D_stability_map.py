"""
====================================================================
GER
S29 — E10.1.3.D
Stability Map
====================================================================

Objetivo
--------
Construir o mapa global de estabilidade da superfície relacional a
partir da análise de propagação produzida pela E10.1.3.C.

Enquanto o módulo anterior caracteriza quantitativamente como as
respostas se distribuem sobre a malha, este módulo identifica regiões
de comportamento homogêneo e regiões onde pequenas perturbações
produzem maior sensibilidade.

O objetivo é produzir uma representação espacial da estabilidade
local da superfície relacional.

Nenhuma hipótese física é introduzida neste módulo.

Toda a análise permanece estritamente baseada nos observáveis
produzidos pelas etapas anteriores.

--------------------------------------------------------------------
Entrada
--------------------------------------------------------------------

Este módulo utiliza exclusivamente os produtos da E10.1.3.C.

Arquivos principais:

    propagation_analysis.parquet

    propagation_summary.json

Nenhuma nova execução do run_e10_engine() é realizada.

Nenhuma perturbação adicional é aplicada.

--------------------------------------------------------------------
Objetivos Científicos
--------------------------------------------------------------------

Construir uma descrição espacial da estabilidade da superfície
relacional.

Investigar:

• regiões estáveis;

• regiões sensíveis;

• transições entre regimes;

• continuidade espacial da estabilidade;

• distribuição da estabilidade sobre a malha;

• possíveis fronteiras estruturais.

O objetivo não é explicar fisicamente essas regiões, mas apenas
identificá-las de forma quantitativa.

--------------------------------------------------------------------
Grandezas Investigadas
--------------------------------------------------------------------

Entre as métricas previstas encontram-se:

• intensidade média da resposta;

• variabilidade local;

• estabilidade relativa;

• gradiente de estabilidade;

• contraste entre vizinhanças;

• índice local de estabilidade;

• mapa contínuo da estabilidade.

Todas as métricas permanecem estritamente derivadas dos resultados da
E10.1.3.C.

--------------------------------------------------------------------
Produtos
--------------------------------------------------------------------

Produz:

stability_map.parquet

stability_levels.parquet

stability_summary.json

stability_summary.txt

FIGURES/

--------------------------------------------------------------------
Saída para os módulos seguintes
--------------------------------------------------------------------

Os resultados produzidos aqui alimentam diretamente:

E10.1.3.E
    Response Atlas

E10.1.3.F
    Propagation Certificate

Este módulo encerra a etapa de análise espacial.

Os módulos seguintes serão responsáveis apenas pela integração dos
resultados e pela produção do certificado científico.

====================================================================
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

EXPERIMENT_NAME = "S29_E10_1_3_D"

GRID_SIZE = 21


# ============================================================
# DIRETÓRIOS
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

INPUT_DIR = (
    ROOT
    / "E10_1_3_C_PropagationAnalysis"
)

OUTPUT_DIR = (
    ROOT
    / "E10_1_3_D_StabilityMap"
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

PROPAGATION_FILE = (
    INPUT_DIR
    / "propagation_analysis.parquet"
)

SUMMARY_INPUT = (
    INPUT_DIR
    / "propagation_summary.json"
)

STABILITY_MAP_FILE = (
    OUTPUT_DIR
    / "stability_map.parquet"
)

STABILITY_LEVELS_FILE = (
    OUTPUT_DIR
    / "stability_levels.parquet"
)

SUMMARY_JSON = (
    OUTPUT_DIR
    / "stability_summary.json"
)

SUMMARY_TXT = (
    OUTPUT_DIR
    / "stability_summary.txt"
)


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(slots=True)
class StabilityNode:

    row: int
    col: int

    gamma: float
    omega: float

    response_norm: float

    gradient: float

    propagation_index: float

    stable: bool


@dataclass(slots=True)
class StabilityRecord:

    row: int
    col: int

    gamma: float
    omega: float

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


def load_propagation_analysis():

    return pd.read_parquet(
        PROPAGATION_FILE
    )


def load_summary():

    with open(
        SUMMARY_INPUT,
        "r",
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


def save_dataframe(
    dataframe,
    filepath,
):

    dataframe.to_parquet(
        filepath,
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
# RECONSTRUÇÃO DA MALHA
# ============================================================

def reshape_field(
    dataframe,
    column,
):
    """
    Reconstrói uma matriz 21×21 para a
    coluna especificada.
    """

    return (

        dataframe

        .pivot(

            index="row",
            columns="col",
            values=column,

        )

        .sort_index()

        .sort_index(axis=1)

        .to_numpy(dtype=float)

    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

print("=" * 72)
print("GER")
print("S29 - E10.1.3.D")
print("Stability Map")
print("=" * 72)

ensure_output_structure()


print(f"[OK] Input            : {INPUT_DIR}")
print(f"[OK] Output           : {OUTPUT_DIR}")
print(f"[OK] Grid             : {GRID_SIZE} x {GRID_SIZE}")
print(f"[OK] Total Points     : {GRID_SIZE * GRID_SIZE}")
print(
    f"[OK] Mean Gradient    : "
    f"{summary['gradient']['mean']:.6e}"
)
print(
    f"[OK] Mean Propagation : "
    f"{summary['propagation_index']['mean']:.6e}"
)
print(
    f"[OK] Stable Fraction  : "
    f"{summary['stable_fraction']:.6f}"
)

# ============================================================
# VIZINHANÇA
# ============================================================

def get_neighbors(
    row,
    col,
    field,
):
    """
    Retorna os valores da vizinhança de Moore
    (8 conectividade).
    """

    neighbors = []

    rows, cols = field.shape

    for di in (-1, 0, 1):

        for dj in (-1, 0, 1):

            if di == 0 and dj == 0:
                continue

            rr = row + di
            cc = col + dj

            if (
                0 <= rr < rows
                and
                0 <= cc < cols
            ):

                neighbors.append(
                    field[rr, cc]
                )

    return np.asarray(
        neighbors,
        dtype=float,
    )


# ============================================================
# MÉTRICAS LOCAIS
# ============================================================

def local_variability(
    row,
    col,
    field,
):
    """
    Desvio padrão local da vizinhança.
    """

    neighbors = get_neighbors(
        row,
        col,
        field,
    )

    if len(neighbors) == 0:

        return 0.0

    return float(
        np.std(neighbors)
    )


def neighborhood_stability(
    row,
    col,
    field,
):
    """
    Média local da estabilidade.
    """

    neighbors = get_neighbors(
        row,
        col,
        field,
    )

    if len(neighbors) == 0:

        return field[row, col]

    return float(
        np.mean(neighbors)
    )


def stability_index(
    propagation_value,
    variability,
):
    """
    Índice adimensional de estabilidade.

    Valores maiores indicam maior estabilidade
    relativa da resposta.
    """

    return float(

        propagation_value
        /
        (1.0 + variability)

    )


# ============================================================
# CLASSIFICAÇÃO
# ============================================================

def classify_stability(
    stability_value,
):
    """
    Classificação simples em quatro níveis.

    Os limites são derivados da distribuição
    observada no experimento.
    """

    if stability_value >= 1.50:
        return 3

    if stability_value >= 1.00:
        return 2

    if stability_value >= 0.50:
        return 1

    return 0


# ============================================================
# CONSTRUÇÃO DO MAPA
# ============================================================

def build_stability_map():

    dataframe = load_propagation_analysis()

    propagation_field = reshape_field(

        dataframe,
        "propagation_index",

    )

    records = []

    print()
    print("=" * 72)
    print("BUILDING STABILITY MAP")
    print("=" * 72)

    total = len(dataframe)

    for index, record in enumerate(

        dataframe.itertuples(index=False),
        start=1,

    ):

        print(

            f"[{index:03d}/{total}] "

            f"γ={record.gamma:.6f} "

            f"ω={record.omega:.6f}"

        )

        variability = local_variability(

            record.row,
            record.col,
            propagation_field,

        )

        neighborhood = neighborhood_stability(

            record.row,
            record.col,
            propagation_field,

        )

        stability = stability_index(

            record.propagation_index,
            variability,

        )

        level = classify_stability(
            stability
        )

        records.append(

            StabilityRecord(

                row=record.row,
                col=record.col,

                gamma=record.gamma,
                omega=record.omega,

                stability_index=stability,

                local_variability=variability,

                neighborhood_stability=neighborhood,

                stability_level=level,

                stable=record.stable,

            )

        )

    stability_df = pd.DataFrame(records)

    levels_df = stability_df[
        [
            "row",
            "col",
            "stability_level",
        ]
    ].copy()

    return stability_df, levels_df

# ============================================================
# RESUMO
# ============================================================

def build_summary(
    stability_df,
):
    """
    Constrói o resumo estatístico do mapa
    de estabilidade.
    """

    level_counts = (

        stability_df["stability_level"]

        .value_counts()

        .sort_index()

        .to_dict()

    )

    summary = {

        "grid_size":
            GRID_SIZE,

        "number_of_points":
            int(len(stability_df)),

        "stability_index": {

            "mean":
                float(
                    stability_df["stability_index"].mean()
                ),

            "std":
                float(
                    stability_df["stability_index"].std()
                ),

            "minimum":
                float(
                    stability_df["stability_index"].min()
                ),

            "maximum":
                float(
                    stability_df["stability_index"].max()
                ),

        },

        "local_variability": {

            "mean":
                float(
                    stability_df["local_variability"].mean()
                ),

            "std":
                float(
                    stability_df["local_variability"].std()
                ),

            "minimum":
                float(
                    stability_df["local_variability"].min()
                ),

            "maximum":
                float(
                    stability_df["local_variability"].max()
                ),

        },

        "neighborhood_stability": {

            "mean":
                float(
                    stability_df[
                        "neighborhood_stability"
                    ].mean()
                ),

            "std":
                float(
                    stability_df[
                        "neighborhood_stability"
                    ].std()
                ),

            "minimum":
                float(
                    stability_df[
                        "neighborhood_stability"
                    ].min()
                ),

            "maximum":
                float(
                    stability_df[
                        "neighborhood_stability"
                    ].max()
                ),

        },

        "stability_levels": {

            str(level): int(count)

            for level, count in level_counts.items()

        },

        "stable_fraction":
            float(
                stability_df["stable"].mean()
            ),

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
            "S29 - E10.1.3.D\n"
        )

        fp.write(
            "Stability Map\n"
        )

        fp.write(
            "====================================================\n\n"
        )

        fp.write(
            f"Grid Size          : {summary['grid_size']} x {summary['grid_size']}\n"
        )

        fp.write(
            f"Points             : {summary['number_of_points']}\n\n"
        )

        fp.write(
            "Stability Index\n"
        )

        fp.write(
            f"  Mean             : {summary['stability_index']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['stability_index']['std']:.6e}\n"
        )

        fp.write(
            f"  Min              : {summary['stability_index']['minimum']:.6e}\n"
        )

        fp.write(
            f"  Max              : {summary['stability_index']['maximum']:.6e}\n\n"
        )

        fp.write(
            "Local Variability\n"
        )

        fp.write(
            f"  Mean             : {summary['local_variability']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['local_variability']['std']:.6e}\n\n"
        )

        fp.write(
            "Neighborhood Stability\n"
        )

        fp.write(
            f"  Mean             : {summary['neighborhood_stability']['mean']:.6e}\n\n"
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
            f"Stable Fraction    : {summary['stable_fraction']:.6f}\n"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    stability_df, levels_df = build_stability_map()

    save_dataframe(

        stability_df,

        STABILITY_MAP_FILE,

    )

    save_dataframe(

        levels_df,

        STABILITY_LEVELS_FILE,

    )

    summary = build_summary(

        stability_df,

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
    print("STABILITY MAP COMPLETED")
    print("=" * 72)

    print(
        f"Points Analysed  : {summary['number_of_points']}"
    )

    print(
        f"Mean Stability   : "
        f"{summary['stability_index']['mean']:.6e}"
    )

    print(
        f"Stable Fraction  : "
        f"{summary['stable_fraction']:.6f}"
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
