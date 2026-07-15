"""
=========================================================
GER CORE

ger_geometric_signature.py

=========================================================

Computação da Assinatura Geométrica.

Esta rotina transforma uma trajetória observacional
produzida pelo Observatório de Persistência (B35)
em uma Assinatura Geométrica composta pelos quatro
Operadores Geométricos Fundamentais (OGFs).

Ela constitui a interface oficial entre:

    Observables
            ↓
    Geometric Signature
            ↓
    Structural Certificate
"""

from GER.CORE.signature_api import Signature

from GER.CORE.ger_confinement import (
    compute_confinement,
)

from GER.CORE.ger_convergence import (
    compute_convergence,
)

from GER.CORE.ger_recurrence import (
    compute_recurrence,
)

from GER.CORE.ger_drift import (
    compute_drift,
)

from GER.CORE.ger_trajectory import (
    build_trajectory,
)


# =========================================================
# Public API
# =========================================================

def compute_geometric_signature(
    observables,
    dt,
):
    """
    Computes the GER Geometric Signature from a
    sequence of observables.

    Parameters
    ----------
    observables : dict
        Output of run_persistence_observatory()

    dt : float
        Time step.

    Returns
    -------
    Signature
    """

    trajectory = build_trajectory(
        observables
    )

    diameter = compute_confinement(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        dt,
    )

    recurrence = compute_recurrence(
        trajectory
    )

    drift, _ = compute_drift(
        trajectory
    )

    return Signature(
        diameter=diameter,
        convergence=convergence,
        recurrence=recurrence,
        drift=drift,
    )
