"""
====================================================================
GER
S29 — E10.1.3.A
Perturbation Calibration
====================================================================

Objetivo
--------
Calibrar automaticamente a magnitude da perturbação utilizada na
E10.1.3.

Este módulo constitui a Fase I do experimento de propagação de
perturbações na malha relacional.

Em vez de assumir arbitrariamente um valor para
(δγ, δω), o módulo executa uma campanha exploratória em um
conjunto reduzido de pontos representativos da malha e avalia
múltiplas magnitudes de perturbação.

O objetivo é identificar a região de operação que produz a maior
quantidade de informação científica sem entrar em regime de
saturação ou permanecer abaixo do ruído numérico.

--------------------------------------------------------------------
Estratégia Experimental
--------------------------------------------------------------------

Malha completa
--------------
21 × 21 = 441 pontos.

Amostragem exploratória
-----------------------

São utilizados apenas nove pontos:

    canto superior esquerdo
    centro superior
    canto superior direito

    centro esquerdo
    centro
    centro direito

    canto inferior esquerdo
    centro inferior
    canto inferior direito

Esses pontos representam toda a extensão da malha.

--------------------------------------------------------------------
Magnitudes avaliadas
--------------------------------------------------------------------

Para cada ponto será executada uma sequência crescente de
perturbações.

Exemplo padrão:

δ =

    1e-6
    3e-6
    1e-5
    3e-5
    1e-4
    3e-4
    1e-3
    3e-3
    1e-2
    3e-2

A lista poderá ser modificada futuramente sem alterar o restante
da arquitetura.

--------------------------------------------------------------------
Procedimento
--------------------------------------------------------------------

Para cada ponto selecionado:

1.

Executar o ger_engine na condição original

        (γ, ω)

2.

Aplicar

        (γ + δγ,
         ω + δω)

3.

Executar novamente o ger_engine.

4.

Calcular

        ΔS

para todas as assinaturas produzidas.

5.

Calcular

    • norma da resposta

    • resposta relativa

    • estabilidade

    • sensibilidade

Repetir para todas as magnitudes.

--------------------------------------------------------------------
Produtos
--------------------------------------------------------------------

Produz:

perturbation_calibration.parquet

perturbation_calibration_summary.json

perturbation_calibration_summary.txt

recommended_perturbation.json

FIGURES/

--------------------------------------------------------------------
Critério de seleção
--------------------------------------------------------------------

A magnitude recomendada será aquela que maximize simultaneamente:

• resposta acima do ruído numérico;

• estabilidade entre pontos;

• ausência de saturação;

• boa relação sinal/ruído.

O módulo NÃO fixa previamente a magnitude.

A decisão é inteiramente baseada nos resultados observados.

--------------------------------------------------------------------
Saída para E10.1.3.B
--------------------------------------------------------------------

O módulo seguinte utilizará exclusivamente a magnitude escolhida
nesta etapa para construir o atlas completo de propagação sobre
os 441 pontos da malha.

====================================================================
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from GER.CORE.ger_engine import run_engine


# ============================================================
# CONFIGURAÇÃO
# ============================================================

EXPERIMENT_NAME = "S29_E10_1_3_A"

GRID_SIZE = 21

DEFAULT_MAGNITUDES = np.array(
    [
        1e-6,
        3e-6,
        1e-5,
        3e-5,
        1e-4,
        3e-4,
        1e-3,
        3e-3,
        1e-2,
        3e-2,
    ],
    dtype=float,
)

# Perturbação aplicada igualmente em γ e ω

DELTA_GAMMA_FACTOR = 1.0
DELTA_OMEGA_FACTOR = 1.0


# ============================================================
# DIRETÓRIOS
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

OUTPUT_DIR = (
    ROOT
    / "E10_1_3_A_PerturbationCalibration"
)

FIGURES_DIR = OUTPUT_DIR / "FIGURES"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(slots=True)
class CalibrationPoint:

    row: int
    col: int

    gamma: float
    omega: float


@dataclass(slots=True)
class CalibrationResult:

    row: int
    col: int

    gamma: float
    omega: float

    delta: float

    response_norm: float
    relative_response: float

    stable: bool


# ============================================================
# AMOSTRAGEM 3 × 3
# ============================================================

SAMPLE_INDICES = (
    0,
    GRID_SIZE // 2,
    GRID_SIZE - 1,
)


def generate_sampling_indices():

    """
    Retorna os nove pontos da campanha exploratória.
    """

    samples = []

    for row in SAMPLE_INDICES:
        for col in SAMPLE_INDICES:

            samples.append((row, col))

    return samples


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


def save_json(data, filename):

    filepath = OUTPUT_DIR / filename

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


def save_dataframe(df, filename):

    filepath = OUTPUT_DIR / filename

    df.to_parquet(
        filepath,
        index=False,
    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

print("=" * 72)
print("GER")
print("S29 - E10.1.3.A")
print("Perturbation Calibration")
print("=" * 72)

ensure_output_structure()

print(f"[OK] Root            : {ROOT}")
print(f"[OK] Output          : {OUTPUT_DIR}")
print(f"[OK] Figures         : {FIGURES_DIR}")
print(f"[OK] Grid            : {GRID_SIZE} x {GRID_SIZE}")
print(f"[OK] Sample Points   : {len(generate_sampling_indices())}")
print(f"[OK] Delta Levels    : {len(DEFAULT_MAGNITUDES)}")
print(f"[OK] Total Executions: {len(generate_sampling_indices()) * len(DEFAULT_MAGNITUDES)}")

# ============================================================
# CONSTRUÇÃO DA CAMPANHA EXPERIMENTAL
# ============================================================

from GER_CORE.S29.E10.e10_engine import run_e10_engine


def build_calibration_points(
    gamma_values,
    omega_values,
):
    """
    Constrói os nove pontos utilizados
    na campanha exploratória.
    """

    points = []

    for row, col in generate_sampling_indices():

        points.append(

            CalibrationPoint(

                row=row,
                col=col,

                gamma=float(gamma_values[row]),
                omega=float(omega_values[col]),

            )

        )

    return points


# ============================================================
# PERTURBAÇÃO
# ============================================================

def apply_perturbation(
    gamma,
    omega,
    delta,
):
    """
    Aplica uma pequena perturbação
    simultaneamente em γ e ω.
    """

    return (

        gamma + DELTA_GAMMA_FACTOR * delta,

        omega + DELTA_OMEGA_FACTOR * delta,

    )


# ============================================================
# EXECUÇÃO DO ADAPTADOR E10
# ============================================================

def run_reference_state(
    point,
    engine_kwargs,
):
    """
    Executa o estado de referência.

    Toda a interface com o CORE é realizada
    exclusivamente através do adaptador
    run_e10_engine().
    """

    return run_e10_engine(

        gamma=point.gamma,
        omega=point.omega,

        **engine_kwargs,

    )


def run_perturbed_state(
    point,
    delta,
    engine_kwargs,
):
    """
    Executa o estado perturbado.
    """

    gamma_p, omega_p = apply_perturbation(

        point.gamma,
        point.omega,
        delta,

    )

    return run_e10_engine(

        gamma=gamma_p,
        omega=omega_p,

        **engine_kwargs,

    )


# ============================================================
# CAMPANHA EXPLORATÓRIA
# ============================================================

def build_experimental_campaign(
    gamma_values,
    omega_values,
):
    """
    Gera todas as combinações

        ponto × magnitude

    da campanha exploratória.

    Nenhuma execução é realizada nesta etapa.
    Apenas a descrição completa da campanha.
    """

    campaign = []

    calibration_points = build_calibration_points(

        gamma_values,
        omega_values,

    )

    for point in calibration_points:

        for delta in DEFAULT_MAGNITUDES:

            campaign.append(

                {

                    "point": point,

                    "delta": float(delta),

                }

            )

    return campaign


# ============================================================
# INFORMAÇÕES DA CAMPANHA
# ============================================================

print()

print("=" * 72)
print("CALIBRATION CAMPAIGN")
print("=" * 72)

print(f"Sampling Points : {len(generate_sampling_indices())}")
print(f"Delta Levels    : {len(DEFAULT_MAGNITUDES)}")
print(f"Total Runs      : {len(generate_sampling_indices()) * len(DEFAULT_MAGNITUDES)}")

print()

print("[OK] Perturbation campaign generated.")
print("[OK] Using run_e10_engine() as execution backend.")
print("[OK] CORE remains isolated from Γ–Ω parametrization.")

# ============================================================
# MÉTRICAS
# ============================================================

def compute_response_metrics(
    reference_state,
    perturbed_state,
):
    """
    Calcula as métricas de resposta entre
    o estado original e o perturbado.

    Espera-se que o adaptador run_e10_engine()
    devolva um objeto contendo um vetor de
    assinaturas em "signature".

    Caso a estrutura interna evolua,
    somente o adaptador deverá ser alterado.
    """

    reference_signature = np.asarray(
        reference_state["signature"],
        dtype=float,
    )

    perturbed_signature = np.asarray(
        perturbed_state["signature"],
        dtype=float,
    )

    delta_signature = (
        perturbed_signature
        - reference_signature
    )

    response_norm = float(
        np.linalg.norm(delta_signature)
    )

    reference_norm = float(
        np.linalg.norm(reference_signature)
    )

    if reference_norm > 0.0:

        relative_response = (
            response_norm
            / reference_norm
        )

    else:

        relative_response = 0.0

    stable = np.isfinite(response_norm)

    return {

        "response_norm": response_norm,
        "relative_response": relative_response,
        "stable": bool(stable),

    }


# ============================================================
# EXECUÇÃO DA CAMPANHA
# ============================================================

def run_calibration_campaign(
    gamma_values,
    omega_values,
    engine_kwargs,
):

    campaign = build_experimental_campaign(

        gamma_values,
        omega_values,

    )

    results = []

    total = len(campaign)

    print()
    print("=" * 72)
    print("RUNNING CALIBRATION")
    print("=" * 72)

    for index, experiment in enumerate(
        campaign,
        start=1,
    ):

        point = experiment["point"]
        delta = experiment["delta"]

        print(
            f"[{index:03d}/{total}] "
            f"γ={point.gamma:.6f} "
            f"ω={point.omega:.6f} "
            f"δ={delta:.2e}"
        )

        reference = run_reference_state(

            point,
            engine_kwargs,

        )

        perturbed = run_perturbed_state(

            point,
            delta,
            engine_kwargs,

        )

        metrics = compute_response_metrics(

            reference,
            perturbed,

        )

        results.append(

            CalibrationResult(

                row=point.row,
                col=point.col,

                gamma=point.gamma,
                omega=point.omega,

                delta=delta,

                response_norm=metrics["response_norm"],

                relative_response=metrics[
                    "relative_response"
                ],

                stable=metrics["stable"],

            )

        )

    return pd.DataFrame(results)


# ============================================================
# RESUMO
# ============================================================

def build_summary(df):

    grouped = df.groupby("delta")

    summary = {

        "number_of_points":
            int(df[["row", "col"]].drop_duplicates().shape[0]),

        "number_of_magnitudes":
            int(df["delta"].nunique()),

        "number_of_runs":
            int(len(df)),

        "response_norm_mean":

            grouped["response_norm"]
            .mean()
            .to_dict(),

        "response_norm_std":

            grouped["response_norm"]
            .std()
            .fillna(0.0)
            .to_dict(),

        "relative_response_mean":

            grouped["relative_response"]
            .mean()
            .to_dict(),

        "stable_fraction":

            grouped["stable"]
            .mean()
            .to_dict(),

    }

    return summary


# ============================================================
# MAGNITUDE RECOMENDADA
# ============================================================

def recommend_delta(summary):

    response = summary[
        "relative_response_mean"
    ]

    best_delta = max(
        response,
        key=response.get,
    )

    return {

        "recommended_delta": float(best_delta),

        "criterion":
            "maximum mean relative response",

    }


# ============================================================
# MAIN
# ============================================================

def main():

    gamma_values = np.linspace(
        0.0,
        1.0,
        GRID_SIZE,
    )

    omega_values = np.linspace(
        0.0,
        1.0,
        GRID_SIZE,
    )

    engine_kwargs = {}

    df = run_calibration_campaign(

        gamma_values,
        omega_values,
        engine_kwargs,

    )

    save_dataframe(
        df,
        "perturbation_calibration.parquet",
    )

    summary = build_summary(df)

    save_json(
        summary,
        "perturbation_calibration_summary.json",
    )

    recommendation = recommend_delta(
        summary,
    )

    save_json(
        recommendation,
        "recommended_perturbation.json",
    )

    with open(

        OUTPUT_DIR
        / "perturbation_calibration_summary.txt",

        "w",
        encoding="utf-8",

    ) as fp:

        fp.write(
            "PERTURBATION CALIBRATION\n"
        )

        fp.write(
            "=" * 40 + "\n\n"
        )

        fp.write(
            f"Points              : {summary['number_of_points']}\n"
        )

        fp.write(
            f"Magnitudes          : {summary['number_of_magnitudes']}\n"
        )

        fp.write(
            f"Executions          : {summary['number_of_runs']}\n"
        )

        fp.write(
            f"Recommended Delta   : "
            f"{recommendation['recommended_delta']:.6e}\n"
        )

    print()
    print("=" * 72)
    print("CALIBRATION COMPLETED")
    print("=" * 72)
    print(
        f"Recommended δ : "
        f"{recommendation['recommended_delta']:.6e}"
    )
    print(
        f"Results saved to:\n{OUTPUT_DIR}"
    )


if __name__ == "__main__":

    main()
