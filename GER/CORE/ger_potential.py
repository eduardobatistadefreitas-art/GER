"""
=========================================================
GER CORE
Arquivo : ger_potential.py
=========================================================

Potenciais não lineares utilizados pela Geometria
Espectral Relacional.

Este módulo concentra toda a física não linear do
projeto.

Cada potencial retorna:

    força
    energia potencial

A interface pública é a classe:

    Potential.evaluate(...)
"""

from __future__ import annotations

import numpy as np


# =========================================================
# Potencial A
# =========================================================

def potential_A(gamma):
    """
    Potencial cúbico (φ⁴).

    V = γ⁴ / 4
    """

    force = gamma**3

    energy = -0.25 * gamma**4

    return force, energy


# =========================================================
# Potencial C
# =========================================================

def potential_C(gamma):
    """
    Potencial saturante.

    V = log(cosh(γ))
    """

    force = np.tanh(gamma)

    energy = np.log(np.cosh(gamma))

    return force, energy


# =========================================================
# Interface pública
# =========================================================

class Potential:
    """
    Interface única para todos os potenciais.

    Exemplo
    -------

    force, energy = Potential.evaluate(
        gamma,
        "A"
    )
    """

    @staticmethod
    def evaluate(gamma, potential="A"):

        potential = potential.upper()

        if potential == "A":

            return potential_A(gamma)

        elif potential == "C":

            return potential_C(gamma)

        raise ValueError(
            f"Potencial '{potential}' não reconhecido."
        )
