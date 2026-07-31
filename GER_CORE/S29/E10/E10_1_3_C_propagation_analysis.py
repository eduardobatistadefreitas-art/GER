"""
====================================================================
GER
S29 — E10.1.3.C
Propagation Analysis
====================================================================

Objetivo
--------
Analisar a organização espacial do campo de resposta construído pelo
módulo E10.1.3.B.

Enquanto o módulo anterior produz apenas as respostas locais para
cada ponto da superfície relacional, este módulo investiga se essas
respostas apresentam estrutura coletiva.

O objetivo científico é determinar se pequenas perturbações dos
parâmetros (γ,ω) permanecem estritamente locais ou se existe alguma
forma de propagação organizada sobre a malha relacional.

Este é o primeiro módulo da série E10 dedicado exclusivamente à
análise da dinâmica espacial da resposta.

--------------------------------------------------------------------
Entrada
--------------------------------------------------------------------

Este módulo utiliza exclusivamente os produtos da E10.1.3.B.

Principal arquivo de entrada:

    response_field.parquet

Opcionalmente:

    response_field_summary.json

Nenhuma nova execução do run_e10_engine() é realizada.

Todo o processamento ocorre sobre os resultados já produzidos.

--------------------------------------------------------------------
Objetivos Científicos
--------------------------------------------------------------------

Investigar:

• continuidade espacial;

• regiões de alta resposta;

• regiões de baixa resposta;

• existência de frentes de propagação;

• organização topológica da resposta;

• possíveis direções preferenciais;

• anisotropias;

• conectividade entre regiões responsivas.

Este módulo não produz interpretações físicas.

Seu papel é apenas caracterizar quantitativamente a geometria da
propagação observada.

--------------------------------------------------------------------
Grandezas Investigadas
--------------------------------------------------------------------

Entre as métricas previstas estão:

• mapas de ||ΔS||;

• gradientes locais;

• vizinhança espacial;

• conectividade entre regiões responsivas;

• componentes conexas;

• alcance espacial da resposta;

• raio efetivo;

• comprimento característico;

• distribuição espacial das respostas.

Novas métricas poderão ser incorporadas futuramente sem modificar a
estrutura geral do módulo.

--------------------------------------------------------------------
Produtos
--------------------------------------------------------------------

Produz:

propagation_analysis.parquet

propagation_graph.parquet

propagation_summary.json

propagation_summary.txt

FIGURES/

--------------------------------------------------------------------
Saída para os módulos seguintes
--------------------------------------------------------------------

Os resultados produzidos aqui alimentam diretamente:

E10.1.3.D
    Stability Map

E10.1.3.E
    Response Atlas

E10.1.3.F
    Propagation Certificate

Este módulo não produz mapas finais nem certificados.

Sua responsabilidade termina na caracterização quantitativa da
propagação observada.

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

EXPERIMENT_NAME = "S29_E10_1_3_C"

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
    / "E10_1_3_B_ResponseField"
)

OUTPUT_DIR = (
    ROOT
    / "E10_1_3_C_PropagationAnalysis"
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

RESPONSE_FIELD_FILE = (
    INPUT_DIR
    / "response_field.parquet"
)

SUMMARY_INPUT = (
    INPUT_DIR
    / "response_field_summary.json"
)

PROPAGATION_FILE = (
    OUTPUT_DIR
    / "propagation_analysis.parquet"
)

GRAPH_FILE = (
    OUTPUT_DIR
    / "propagation_graph.parquet"
)

SUMMARY_JSON = (
    OUTPUT_DIR
    / "propagation_summary.json"
)

SUMMARY_TXT = (
    OUTPUT_DIR
    / "propagation_summary.txt"
)


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(slots=True)
class GridNode:

    row: int
    col: int

    gamma: float
    omega: float

    response_norm: float
    relative_response: float

    stable: bool


@dataclass(slots=True)
class PropagationRecord:

    row: int
    col: int

    gamma: float
    omega: float

    response_norm: float
    relative_response: float

    gradient: float

    neighborhood_mean: float

    propagation_index: float

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
        RESPONSE_FIELD_FILE
    )


def load_summary():

    with open(
        SUMMARY_INPUT,
        "r",
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


def save_dataframe(
    df,
    filepath,
):

    df.to_parquet(
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
# MALHA
# ============================================================

def reshape_response_field(df):
    """
    Reconstrói a malha 21×21 do campo de resposta.
    """

    return (
        df
        .pivot(
            index="row",
            columns="col",
            values="response_norm",
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
print("S29 - E10.1.3.C")
print("Propagation Analysis")
print("=" * 72)

ensure_output_structure()

response_summary = load_summary()

print(f"[OK] Input          : {INPUT_DIR}")
print(f"[OK] Output         : {OUTPUT_DIR}")
print(f"[OK] Grid Size      : {GRID_SIZE} x {GRID_SIZE}")
print(f"[OK] Total Points   : {GRID_SIZE * GRID_SIZE}")
print(f"[OK] Mean Response  : {response_summary['response_norm']['mean']:.6e}")
print(f"[OK] Stable Fraction: {response_summary['stable_fraction']:.6f}")

# ============================================================
# VIZINHANÇA
# ============================================================

def get_neighbors(
    row,
    col,
    field,
):
    """
    Retorna os vizinhos de Moore (8-conectividade)
    existentes para um ponto da malha.
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
# GRADIENTE LOCAL
# ============================================================

def local_gradient(
    row,
    col,
    field,
):
    """
    Calcula o contraste médio entre um ponto
    e sua vizinhança imediata.
    """

    center = field[row, col]

    neighbors = get_neighbors(
        row,
        col,
        field,
    )

    if len(neighbors) == 0:

        return 0.0

    return float(

        np.mean(
            np.abs(
                neighbors
                - center
            )
        )

    )


# ============================================================
# ÍNDICE LOCAL DE PROPAGAÇÃO
# ============================================================

def propagation_index(
    response_norm,
    neighborhood_mean,
):
    """
    Índice adimensional simples utilizado
    para comparar a intensidade local
    com a resposta da vizinhança.
    """

    if neighborhood_mean <= 0.0:

        return 0.0

    return float(
        response_norm
        / neighborhood_mean
    )


# ============================================================
# ANÁLISE DO CAMPO
# ============================================================

def analyze_propagation():

    df = load_response_field()

    field = reshape_response_field(df)

    records = []

    print()
    print("=" * 72)
    print("ANALYZING PROPAGATION")
    print("=" * 72)

    total = len(df)

    for index, row_df in enumerate(

        df.itertuples(index=False),
        start=1,

    ):

        print(

            f"[{index:03d}/{total}] "

            f"γ={row_df.gamma:.6f} "

            f"ω={row_df.omega:.6f}"

        )

        neighbors = get_neighbors(

            row_df.row,
            row_df.col,
            field,

        )

        if len(neighbors):

            neighborhood_mean = float(

                np.mean(neighbors)

            )

        else:

            neighborhood_mean = 0.0

        gradient = local_gradient(

            row_df.row,
            row_df.col,
            field,

        )

        pindex = propagation_index(

            row_df.response_norm,
            neighborhood_mean,

        )

        records.append(

            PropagationRecord(

                row=row_df.row,
                col=row_df.col,

                gamma=row_df.gamma,
                omega=row_df.omega,

                response_norm=row_df.response_norm,

                relative_response=row_df.relative_response,

                gradient=gradient,

                neighborhood_mean=neighborhood_mean,

                propagation_index=pindex,

                stable=row_df.stable,

            )

        )

    propagation_df = pd.DataFrame(records)

    graph_df = propagation_df[
        [
            "row",
            "col",
            "gradient",
            "propagation_index",
        ]
    ].copy()

    return propagation_df, graph_df

# ============================================================
# RESUMO
# ============================================================

def build_summary(df):
    """
    Constrói o resumo estatístico da análise
    de propagação.
    """

    summary = {

        "grid_size": GRID_SIZE,

        "number_of_points":
            int(len(df)),

        "gradient": {

            "mean":
                float(df["gradient"].mean()),

            "std":
                float(df["gradient"].std()),

            "minimum":
                float(df["gradient"].min()),

            "maximum":
                float(df["gradient"].max()),

        },

        "neighborhood_mean": {

            "mean":
                float(df["neighborhood_mean"].mean()),

            "std":
                float(df["neighborhood_mean"].std()),

            "minimum":
                float(df["neighborhood_mean"].min()),

            "maximum":
                float(df["neighborhood_mean"].max()),

        },

        "propagation_index": {

            "mean":
                float(df["propagation_index"].mean()),

            "std":
                float(df["propagation_index"].std()),

            "minimum":
                float(df["propagation_index"].min()),

            "maximum":
                float(df["propagation_index"].max()),

        },

        "stable_fraction":
            float(df["stable"].mean()),

    }

    return summary


# ============================================================
# RELATÓRIO
# ============================================================

def write_summary(summary):

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
            "S29 - E10.1.3.C\n"
        )

        fp.write(
            "Propagation Analysis\n"
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
            "Gradient\n"
        )

        fp.write(
            f"  Mean             : {summary['gradient']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['gradient']['std']:.6e}\n"
        )

        fp.write(
            f"  Min              : {summary['gradient']['minimum']:.6e}\n"
        )

        fp.write(
            f"  Max              : {summary['gradient']['maximum']:.6e}\n\n"
        )

        fp.write(
            "Neighborhood Mean\n"
        )

        fp.write(
            f"  Mean             : {summary['neighborhood_mean']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['neighborhood_mean']['std']:.6e}\n"
        )

        fp.write(
            f"  Min              : {summary['neighborhood_mean']['minimum']:.6e}\n"
        )

        fp.write(
            f"  Max              : {summary['neighborhood_mean']['maximum']:.6e}\n\n"
        )

        fp.write(
            "Propagation Index\n"
        )

        fp.write(
            f"  Mean             : {summary['propagation_index']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['propagation_index']['std']:.6e}\n"
        )

        fp.write(
            f"  Min              : {summary['propagation_index']['minimum']:.6e}\n"
        )

        fp.write(
            f"  Max              : {summary['propagation_index']['maximum']:.6e}\n\n"
        )

        fp.write(
            f"Stable Fraction    : {summary['stable_fraction']:.6f}\n"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    propagation_df, graph_df = analyze_propagation()

    save_dataframe(

        propagation_df,
        PROPAGATION_FILE,

    )

    save_dataframe(

        graph_df,
        GRAPH_FILE,

    )

    summary = build_summary(

        propagation_df,

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
    print("PROPAGATION ANALYSIS COMPLETED")
    print("=" * 72)

    print(
        f"Points Analysed   : {summary['number_of_points']}"
    )

    print(
        f"Gradient Mean     : {summary['gradient']['mean']:.6e}"
    )

    print(
        f"Propagation Mean  : {summary['propagation_index']['mean']:.6e}"
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
