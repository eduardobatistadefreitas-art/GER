"""
=========================================================
GER CORE
Arquivo : ger_modal.py
=========================================================

Observatório Espectral da Geometria Espectral Relacional.

Este módulo contém todas as ferramentas de análise
modal utilizadas pelas auditorias S26-B.

Responsabilidades:

• Projeção na base espectral
• Distribuição de energia modal
• Entropia espectral
• Centro e largura modal
• Participação modal
• Separação por bandas espectrais
"""

from __future__ import annotations

import numpy as np


EPS = 1e-15


# =========================================================
# Projeção modal
# =========================================================

def modal_projection(
    gamma,
    eigenvectors
):
    """
    Projeta o campo na base espectral.

    gamma_hat = V^T gamma
    """

    gamma = np.asarray(gamma)

    return eigenvectors.T @ gamma


# =========================================================
# Energia modal
# =========================================================

def modal_energy(
    gamma,
    eigenvectors
):
    """
    Energia associada a cada modo espectral.
    """

    coefficients = modal_projection(
        gamma,
        eigenvectors
    )

    energy = np.abs(coefficients)**2

    return energy


# =========================================================
# Probabilidade modal
# =========================================================

def modal_probability(
    gamma,
    eigenvectors
):
    """
    Normalização da energia modal.

    Soma das probabilidades = 1
    """

    energy = modal_energy(
        gamma,
        eigenvectors
    )

    total = np.sum(energy) + EPS

    return energy / total


# =========================================================
# Modo dominante
# =========================================================

def dominant_mode(probability):
    """
    Retorna o modo com maior concentração.
    """

    return int(
        np.argmax(probability)
    )


# =========================================================
# Centro espectral
# =========================================================

def spectral_center(probability):
    """
    Centro médio dos modos.
    """

    modes = np.arange(
        len(probability)
    )

    return np.sum(
        modes * probability
    )


# =========================================================
# Largura espectral
# =========================================================

def spectral_width(probability):
    """
    Desvio modal da distribuição espectral.
    """

    modes = np.arange(
        len(probability)
    )

    center = spectral_center(
        probability
    )

    variance = np.sum(
        probability *
        (modes - center)**2
    )

    return np.sqrt(
        variance
    )


# =========================================================
# Entropia espectral
# =========================================================

def spectral_entropy(probability):
    """
    Entropia de Shannon da distribuição modal.
    """

    p = probability[
        probability > 0
    ]

    return -np.sum(
        p * np.log(p)
    )


# =========================================================
# Participation Ratio
# =========================================================

def participation_ratio(probability):
    """
    Mede quantos modos participam efetivamente.

    PR = 1 / Σp²
    """

    return 1.0 / (
        np.sum(probability**2)
        + EPS
    )


# =========================================================
# Energia por bandas
# =========================================================

def spectral_bands(
    probability
):
    """
    Divide energia espectral em:

    baixa frequência
    média frequência
    alta frequência
    """

    n = len(probability)

    low_end = n // 3
    mid_end = 2 * n // 3

    low = np.sum(
        probability[:low_end]
    )

    medium = np.sum(
        probability[low_end:mid_end]
    )

    high = np.sum(
        probability[mid_end:]
    )

    return {
        "low": low,
        "medium": medium,
        "high": high
    }


# =========================================================
# Auditoria completa
# =========================================================

def analyze_modal_state(
    gamma,
    eigenvectors
):
    """
    Executa todo o observatório espectral.

    Retorna todas as métricas modais.
    """

    probability = modal_probability(
        gamma,
        eigenvectors
    )

    return {

        "modal_energy":
            modal_energy(
                gamma,
                eigenvectors
            ),

        "probability":
            probability,

        "dominant_mode":
            dominant_mode(
                probability
            ),

        "modal_center":
            spectral_center(
                probability
            ),

        "modal_width":
            spectral_width(
                probability
            ),

        "spectral_entropy":
            spectral_entropy(
                probability
            ),

        "participation_ratio":
            participation_ratio(
                probability
            ),

        "spectral_bands":
            spectral_bands(
                probability
            )
    }
# =========================================================
# Snapshot completo da simulação
# =========================================================

from GER.CORE.ger_metrics import (
    compute_hamiltonian,
    compute_l2_norm,
    compute_max_amplitude,
)


def build_snapshot(
    step,
    time,
    gamma,
    velocity,
    laplacian,
    beta,
    potential,
    eigenvectors,
    theta,
):
    """
    Constrói um snapshot completo do estado da simulação.

    Este formato é utilizado pelo GER CORE durante toda
    a evolução temporal.
    """

    modal = analyze_modal_state(
        gamma,
        eigenvectors,
    )

    snapshot = {

        "step": step,

        "time": time,

        "energy": compute_hamiltonian(
            gamma,
            velocity,
            laplacian,
            beta,
            potential,
        ),

        "l2": compute_l2_norm(gamma),

        "amplitude": compute_max_amplitude(gamma),

        "dominant_mode":
            modal["dominant_mode"],

        "modal_center":
            modal["modal_center"],

        "modal_width":
            modal["modal_width"],

        "spectral_entropy":
            modal["spectral_entropy"],

        "participation_ratio":
            modal["participation_ratio"],

        "probability":
            modal["probability"],

        "modal_energy":
            modal["modal_energy"],

        "spectral_bands":
            modal["spectral_bands"],
    }

    return snapshot
