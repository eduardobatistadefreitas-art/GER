"""
=========================================================
GER CORE
S26-B.2.3

Dependência com β

=========================================================

Varredura automática do parâmetro β.

Executa diversas simulações utilizando o GER CORE e
registra as métricas finais produzidas pelo
Observatório Espectral.

=========================================================
"""

from __future__ import annotations

from GER.CORE.ger_engine import run_engine


# =========================================================
# Auditoria principal
# =========================================================

def run_beta_dependence(

    betas=(
        0.0,
        0.1,
        1.0,
        5.0,
        10.0,
        20.0,
        50.0,
        100.0
    ),

    n=384,
    sigma=0.10,
    dt=2.5e-5,
    timesteps=2000,
    snapshot_stride=200,
    potential="A"

):
    """
    Executa uma varredura completa em β.
    """

    results = []

    for beta in betas:

        simulation = run_engine(

            n=n,
            beta=beta,
            sigma=sigma,
            dt=dt,
            timesteps=timesteps,
            snapshot_stride=snapshot_stride,
            potential=potential

        )

        final = simulation["snapshots"][-1]

        results.append({

            "beta": beta,

            "energy":
                simulation["final"]["energy"],

            "energy_error":
                simulation["final"]["energy_error"],

            "amplitude":
                simulation["final"]["amplitude"],

            "dominant_mode":
                final["dominant_mode"],

            "entropy":
                final["spectral_entropy"],

            "participation":
                final["participation_ratio"],

            "modal_width":
                final["modal_width"],

            "modal_center":
                final["modal_center"],

            "diverged":
                simulation["diverged"]

        })

    return results


# =========================================================
# Impressão
# =========================================================

def print_beta_dependence(results):

    for r in results:

        print()

        print("========================")

        print(f"β = {r['beta']}")

        print("========================")

        print("Energia:", r["energy"])

        print("Erro:", r["energy_error"])

        print("Amplitude:", r["amplitude"])

        print("Modo dominante:", r["dominant_mode"])

        print("Entropia:", r["entropy"])

        print("Participação:", r["participation"])

        print("Largura modal:", r["modal_width"])

        print("Centro modal:", r["modal_center"])

        print("Divergiu:", r["diverged"])
