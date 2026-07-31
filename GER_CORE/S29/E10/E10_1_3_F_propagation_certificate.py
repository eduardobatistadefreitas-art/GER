"""
====================================================================
GER
S29 — E10.1.3.B
Response Field
====================================================================

Objetivo
--------
Construir o campo global de resposta da superfície relacional a uma
perturbação calibrada.

Este módulo constitui a Fase II da E10.1.3.

A magnitude da perturbação é obtida automaticamente pela
E10.1.3.A através do arquivo

    recommended_perturbation.json

Para cada ponto da malha oficial Γ–Ω, o módulo executa o estado
de referência e o estado perturbado, reconstrói a assinatura pelo
pipeline oficial da E10.1.1 e calcula a resposta local.

Não realiza qualquer interpretação espacial; produz apenas o
campo completo de resposta utilizado pelos módulos seguintes.

====================================================================
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# GER CORE
# ============================================================

from GER.CORE.bootstrap import initialize

from GER.CORE.experiment_pipeline import (
    run_signature_pipeline,
)

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S29.E10.e10_engine import (
    run_e10_engine,
)

# ============================================================
# CONFIGURAÇÃO
# ============================================================

EXPERIMENT_NAME = "S29_E10_1_3_B"

GRID_SIZE = 21
DEFAULT_DT = 2.5e-4

# ============================================================
# DIRETÓRIOS
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

CALIBRATION_DIR = (
    ROOT
    / "E10_1_3_A_PerturbationCalibration"
)

OUTPUT_DIR = (
    ROOT
    / "E10_1_3_B_ResponseField"
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

RECOMMENDED_DELTA_FILE = (
    CALIBRATION_DIR
    / "recommended_perturbation.json"
)

RESPONSE_FIELD_FILE = (
    OUTPUT_DIR
    / "response_field.parquet"
)

SUMMARY_JSON = (
    OUTPUT_DIR
    / "response_field_summary.json"
)

SUMMARY_TXT = (
    OUTPUT_DIR
    / "response_field_summary.txt"
)


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(slots=True)
class ResponsePoint:

    row: int
    col: int

    gamma: float
    omega: float


@dataclass(slots=True)
class ResponseRecord:

    row: int
    col: int

    gamma: float
    omega: float

    delta: float

    response_norm: float
    relative_response: float

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


def load_recommended_delta():

    with open(
        RECOMMENDED_DELTA_FILE,
        "r",
        encoding="utf-8",
    ) as fp:

        data = json.load(fp)

    return float(
        data["recommended_delta"]
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


def save_dataframe(df):

    df.to_parquet(
        RESPONSE_FIELD_FILE,
        index=False,
    )


# ============================================================
# MALHA
# ============================================================

def build_full_grid():

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

    grid = []

    for row, gamma in enumerate(gamma_values):

        for col, omega in enumerate(omega_values):

            grid.append(

                ResponsePoint(

                    row=row,
                    col=col,

                    gamma=float(gamma),
                    omega=float(omega),

                )

            )

    return grid


# ============================================================
# INICIALIZAÇÃO
# ============================================================

print("=" * 72)
print("GER")
print("S29 - E10.1.3.B")
print("Response Field")
print("=" * 72)

ensure_output_structure()

print(f"[OK] Root            : {ROOT}")
print(f"[OK] Calibration     : {CALIBRATION_DIR}")
print(f"[OK] Output          : {OUTPUT_DIR}")
print(f"[OK] Grid            : {GRID_SIZE} x {GRID_SIZE}")
print(f"[OK] Total Points    : {GRID_SIZE * GRID_SIZE}")
print("[OK] Delta           : carregado durante a execução")

# ============================================================
# PERTURBAÇÃO
# ============================================================

DELTA_GAMMA_FACTOR = 1.0
DELTA_OMEGA_FACTOR = 1.0


def apply_perturbation(
    gamma,
    omega,
    delta,
):
    """
    Aplica a perturbação calibrada aos
    parâmetros Γ–Ω.
    """

    gamma_p = (
        gamma
        + DELTA_GAMMA_FACTOR * delta
    )

    omega_p = (
        omega
        + DELTA_OMEGA_FACTOR * delta
    )

    return gamma_p, omega_p


# ============================================================
# EXECUÇÃO
# ============================================================

def run_reference_state(
    point,
    engine_kwargs,
):
    """
    Executa o estado de referência.
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
# MÉTRICAS
# ============================================================

def compute_response_metrics(
    reference_state,
    perturbed_state,
    dt,
):
    """
    Calcula as métricas locais de resposta.

    A assinatura é reconstruída pelo
    pipeline oficial da E10.1.1.
    """

    # ---------------------------------------------------------
    # Estado de referência
    # ---------------------------------------------------------

    reference_observables = run_persistence_observatory(

        snapshots=reference_state["snapshots"],
        dt=dt,

    )

    reference_pipeline = run_signature_pipeline(

        reference_observables,
        dt,

    )

    reference = reference_pipeline["signature"]

    reference_signature = np.array(

        [
            reference.diameter,
            reference.convergence,
            reference.recurrence,
            reference.drift,
        ],

        dtype=float,

    )

    # ---------------------------------------------------------
    # Estado perturbado
    # ---------------------------------------------------------

    perturbed_observables = run_persistence_observatory(

        snapshots=perturbed_state["snapshots"],
        dt=dt,

    )

    perturbed_pipeline = run_signature_pipeline(

        perturbed_observables,
        dt,

    )

    perturbed = perturbed_pipeline["signature"]

    perturbed_signature = np.array(

        [
            perturbed.diameter,
            perturbed.convergence,
            perturbed.recurrence,
            perturbed.drift,
        ],

        dtype=float,

    )

    # ---------------------------------------------------------
    # Métricas
    # ---------------------------------------------------------

    delta_signature = (

        perturbed_signature
        - reference_signature

    )

    response_norm = float(

        np.linalg.norm(
            delta_signature
        )

    )

    reference_norm = float(

        np.linalg.norm(
            reference_signature
        )

    )

    if reference_norm > 0.0:

        relative_response = (

            response_norm
            / reference_norm

        )

    else:

        relative_response = 0.0

    stable = bool(
        np.isfinite(response_norm)
    )

    return {

        "response_norm": response_norm,

        "relative_response": relative_response,

        "stable": stable,

    }


# ============================================================
# CAMPO DE RESPOSTA
# ============================================================

def build_response_field(
    engine_kwargs,
):
    """
    Executa os 441 pontos da malha
    e constrói o campo de resposta.
    """

    grid = build_full_grid()

    records = []

    total = len(grid)

    print()
    print("=" * 72)
    print("BUILDING RESPONSE FIELD")
    print("=" * 72)

    for index, point in enumerate(
        grid,
        start=1,
    ):

        print(

            f"[{index:03d}/{total}] "
            f"γ={point.gamma:.6f} "
            f"ω={point.omega:.6f}"

        )

        reference_state = run_reference_state(

            point,
            engine_kwargs,

        )

        perturbed_state = run_perturbed_state(

            point,
            DELTA,
            engine_kwargs,

        )

        metrics = compute_response_metrics(

            reference_state,
            perturbed_state,
            engine_kwargs["dt"],

        )

        records.append(

            ResponseRecord(

                row=point.row,
                col=point.col,

                gamma=point.gamma,
                omega=point.omega,

                delta=DELTA,

                response_norm=metrics[
                    "response_norm"
                ],

                relative_response=metrics[
                    "relative_response"
                ],

                stable=metrics[
                    "stable"
                ],

            )

        )

    return pd.DataFrame(records)

# ============================================================
# RESUMO
# ============================================================

def build_summary(df):
    """
    Constrói o resumo estatístico do
    campo de resposta.
    """

    summary = {

        "grid_size": GRID_SIZE,

        "number_of_points":

            int(len(df)),

        "delta":

            float(DELTA),

        "response_norm": {

            "minimum":

                float(df["response_norm"].min()),

            "maximum":

                float(df["response_norm"].max()),

            "mean":

                float(df["response_norm"].mean()),

            "std":

                float(df["response_norm"].std()),

        },

        "relative_response": {

            "minimum":

                float(df["relative_response"].min()),

            "maximum":

                float(df["relative_response"].max()),

            "mean":

                float(df["relative_response"].mean()),

            "std":

                float(df["relative_response"].std()),

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
            "S29 - E10.1.3.B\n"
        )

        fp.write(
            "Response Field\n"
        )

        fp.write(
            "====================================================\n\n"
        )

        fp.write(
            f"Grid Size          : {summary['grid_size']} x {summary['grid_size']}\n"
        )

        fp.write(
            f"Points             : {summary['number_of_points']}\n"
        )

        fp.write(
            f"Delta              : {summary['delta']:.6e}\n\n"
        )

        fp.write(
            "Response Norm\n"
        )

        fp.write(
            f"  Mean             : {summary['response_norm']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['response_norm']['std']:.6e}\n"
        )

        fp.write(
            f"  Min              : {summary['response_norm']['minimum']:.6e}\n"
        )

        fp.write(
            f"  Max              : {summary['response_norm']['maximum']:.6e}\n\n"
        )

        fp.write(
            "Relative Response\n"
        )

        fp.write(
            f"  Mean             : {summary['relative_response']['mean']:.6e}\n"
        )

        fp.write(
            f"  Std              : {summary['relative_response']['std']:.6e}\n"
        )

        fp.write(
            f"  Min              : {summary['relative_response']['minimum']:.6e}\n"
        )

        fp.write(
            f"  Max              : {summary['relative_response']['maximum']:.6e}\n\n"
        )

        fp.write(
            f"Stable Fraction    : {summary['stable_fraction']:.6f}\n"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    initialize()

    global DELTA

    DELTA = load_recommended_delta()

    print(
        f"[OK] Delta           : {DELTA:.6e}"
    )

    engine_kwargs = {

        "dt": DEFAULT_DT,

    }

    response_field = build_response_field(

        engine_kwargs,

    )

    save_dataframe(

        response_field,

    )

    summary = build_summary(

        response_field,

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
    print("RESPONSE FIELD COMPLETED")
    print("=" * 72)

    print(
        f"Points Processed : {summary['number_of_points']}"
    )

    print(
        f"Delta Used       : {summary['delta']:.6e}"
    )

    print(
        f"Stable Fraction  : {summary['stable_fraction']:.6f}"
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
