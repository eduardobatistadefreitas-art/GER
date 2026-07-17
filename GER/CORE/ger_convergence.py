"""
=========================================================
GER CORE
Arquivo : ger_convergence.py
=========================================================

Rotinas de validação de convergência da Geometria
Espectral Relacional.

Este módulo implementa:

• Densidade de energia
• Comparação temporal
• Comparação espacial
• Auditoria de estabilidade

Objetivo:
Garantir que os resultados numéricos sejam robustos
antes das análises espectrais da Série S26-B.

=========================================================
"""

from __future__ import annotations

import numpy as np


# =========================================================
# Densidade de energia
# =========================================================

def energy_density(energy, n):
    """
    Calcula energia por grau de liberdade.

    ε = H / N

    Parâmetros
    ----------
    energy : float
        Energia Hamiltoniana total.

    n : int
        Número de nós da rede.

    Retorno
    -------
    float
    """

    return energy / n



# =========================================================
# Erro relativo entre resoluções
# =========================================================

def relative_difference(a, b):
    """
    Diferença relativa entre dois valores.
    """

    return abs(a - b) / (
        abs(b) + 1e-15
    )



# =========================================================
# Auditoria espacial
# =========================================================

def spatial_convergence_test(results):
    """
    Analisa convergência espacial.

    Espera um dicionário:

    {
        n : resultado_run_engine
    }

    Exemplo:

    {
        192: result192,
        384: result384,
        768: result768
    }

    """

    report = []


    for n, result in sorted(results.items()):

        energy = result["final"]["energy"]

        error = result["final"]["energy_error"]

        density = energy_density(
            energy,
            n
        )

        report.append(
            {
                "n": n,
                "energy": energy,
                "energy_density": density,
                "energy_error": error
            }
        )


    return report



# =========================================================
# Auditoria temporal
# =========================================================

def temporal_convergence_test(results):
    """
    Analisa convergência temporal.

    Espera:

    {
        dt : resultado_run_engine
    }

    """

    report = []


    for dt, result in sorted(
        results.items(),
        reverse=True
    ):

        report.append(
            {
                "dt": dt,
                "energy":
                    result["final"]["energy"],

                "energy_error":
                    result["final"]["energy_error"]
            }
        )


    return report



# =========================================================
# Impressão padronizada
# =========================================================

def print_convergence_report(report):
    """
    Exibe tabela simples de convergência.
    """

    for item in report:

        print(
            item
        )
# =========================================================
# Geometric Convergence Operator
# =========================================================

def compute_convergence(
    trajectory,
    dt,
):
    """
    Computes the geometric convergence operator
    from a trajectory.

    Parameters
    ----------
    trajectory : numpy.ndarray

    dt : float

    Returns
    -------
    float
    """

    if len(trajectory) < 2:
        return 0.0

    steps = np.diff(
        trajectory,
        axis=0,
    )

    speeds = np.linalg.norm(
        steps,
        axis=1,
    )

    return np.mean(
        speeds
    ) / dt
