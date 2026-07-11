"""
=========================================================
GER CORE
S26-B.2.1

Transferência Modal

=========================================================

Primeira auditoria espectral da Série B.

Esta rotina utiliza exclusivamente os snapshots produzidos
pelo GER CORE, sem recalcular a base espectral.

Cada snapshot já contém todas as métricas produzidas pelo
Observatório Espectral.

=========================================================
"""

from __future__ import annotations

from GER_CORE.ger_engine import run_engine


# =========================================================
# Auditoria de transferência modal
# =========================================================

def run_modal_transfer(
    n=384,
    beta=1.0,
    sigma=0.10,
    dt=5e-5,
    timesteps=2000,
    snapshot_stride=50,
    potential="A"
):
    """
    Executa uma simulação completa e retorna o histórico
    temporal das métricas espectrais.

    Retorno
    -------

    history : list(dict)

    Cada elemento possui:

        step
        time
        dominant_mode
        entropy
        participation
        modal_center
        modal_width
        modal_energy
        probability
        spectral_bands
    """

    result = run_engine(
        n=n,
        timesteps=timesteps,
        dt=dt,
        beta=beta,
        sigma=sigma,
        potential=potential,
        snapshot_stride=snapshot_stride
    )

    history = []

    for snap in result["snapshots"]:

        history.append({

            "step":
                snap["step"],

            "time":
                snap["time"],

            "dominant_mode":
                snap["dominant_mode"],

            "entropy":
                snap["spectral_entropy"],

            "participation":
                snap["participation_ratio"],

            "modal_center":
                snap["modal_center"],

            "modal_width":
                snap["modal_width"],

            "modal_energy":
                snap["modal_energy"],

            "probability":
                snap["probability"],

            "spectral_bands":
                snap["spectral_bands"]

        })

    return history


# =========================================================
# Impressão resumida
# =========================================================

def print_modal_transfer(history):
    """
    Resumo textual da evolução modal.
    """

    for item in history:

        print(
            f"step: {item['step']:5d} | "
            f"modo: {item['dominant_mode']:3d} | "
            f"entropia: {item['entropy']:.6f} | "
            f"participação: {item['participation']:.6f} | "
            f"largura: {item['modal_width']:.6f}"
        )
