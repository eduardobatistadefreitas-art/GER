%%writefile GER_CORE/ger_metrics.py

"""
=========================================================
GER CORE
Arquivo : ger_metrics.py
=========================================================

Métricas globais da Geometria Espectral Relacional.

Este módulo implementa:

• Energia Hamiltoniana
• Norma L²
• Amplitude máxima
• Erro relativo de energia
• Critério automático de divergência

Todas as auditorias utilizam estas rotinas.
"""

from __future__ import annotations

import numpy as np

from ger_potential import Potential


# =========================================================
# Configurações globais
# =========================================================

ENERGY_TOL = 1e-4

DIVERGENCE_AMPLITUDE = 1e6

EPS = 1e-15


# =========================================================
# Norma L²
# =========================================================

def compute_l2_norm(gamma):
    """
    Norma L² do campo.
    """

    gamma = np.asarray(gamma)

    return np.sqrt(np.sum(gamma**2))


# =========================================================
# Amplitude máxima
# =========================================================

def compute_max_amplitude(gamma):
    """
    Valor absoluto máximo do campo.
    """

    gamma = np.asarray(gamma)

    return np.max(np.abs(gamma))


# =========================================================
# Energia Hamiltoniana
# =========================================================

def compute_hamiltonian(
    gamma,
    velocity,
    laplacian,
    beta,
    potential="A"
):
    """
    Energia Hamiltoniana completa.

    H =
        Energia cinética
      + Energia elástica
      + Energia potencial não linear
    """

    gamma = np.asarray(gamma)

    velocity = np.asarray(velocity)

    kinetic = 0.5 * np.sum(velocity**2)

    elastic = 0.5 * gamma @ (laplacian @ gamma)

    _, potential_energy = Potential.evaluate(
        gamma,
        potential
    )

    nonlinear = beta * np.sum(potential_energy)

    return kinetic + elastic + nonlinear


# =========================================================
# Erro relativo de energia
# =========================================================

def relative_energy_error(
    reference_energy,
    current_energy
):
    """
    Erro relativo da energia Hamiltoniana.
    """

    return abs(
        current_energy - reference_energy
    ) / (
        abs(reference_energy) + EPS
    )


# =========================================================
# Critério automático de divergência
# =========================================================

def check_divergence(
    gamma,
    energy_error
):
    """
    Detecta automaticamente explosões numéricas.
    """

    amplitude = compute_max_amplitude(gamma)

    if amplitude > DIVERGENCE_AMPLITUDE:

        return True

    if np.isnan(amplitude):

        return True

    if np.isinf(amplitude):

        return True

    if np.isnan(energy_error):

        return True

    if np.isinf(energy_error):

        return True

    return False
