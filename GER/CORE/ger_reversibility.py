%%writefile GER_CORE/ger_reversibility.py

"""
=========================================================
GER CORE
Arquivo : ger_reversibility.py
=========================================================

Auditoria de reversibilidade temporal.

Esta primeira versão prepara a infraestrutura para os
testes de reversibilidade do integrador Verlet.

=========================================================
"""

from __future__ import annotations

import numpy as np


# =========================================================
# Norma relativa
# =========================================================

def relative_norm(a, b):
    """
    Erro relativo entre dois vetores.
    """

    a = np.asarray(a)
    b = np.asarray(b)

    den = np.linalg.norm(a)

    if den < 1e-15:
        den = 1.0

    return np.linalg.norm(a - b) / den


# =========================================================
# Comparação de estados
# =========================================================

def compare_states(reference, recovered):
    """
    Compara dois estados do sistema.
    """

    return {

        "gamma_error":
            relative_norm(
                reference["gamma"],
                recovered["gamma"]
            ),

        "energy_error":
            abs(
                reference["final"]["energy"]
                -
                recovered["final"]["energy"]
            ),

        "l2_error":
            abs(
                reference["snapshots"][-1]["l2"]
                -
                recovered["snapshots"][-1]["l2"]
            ),

        "amplitude_error":
            abs(
                reference["snapshots"][-1]["amplitude"]
                -
                recovered["snapshots"][-1]["amplitude"]
            )
    }


# =========================================================
# Relatório
# =========================================================

def print_reversibility_report(report):

    print("=" * 60)
    print("AUDITORIA DE REVERSIBILIDADE")
    print("=" * 60)

    for key, value in report.items():

        print(f"{key}: {value}")
