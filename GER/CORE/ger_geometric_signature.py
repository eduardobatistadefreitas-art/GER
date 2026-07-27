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


# =========================================================
# Compatibility API
# =========================================================

def is_signature(obj):
    """
    Returns True if the object is a GER Signature.
    """

    return isinstance(obj, Signature)


def extract_signature(obj):
    """
    Extracts a GER Signature from supported objects.

    Accepted inputs
    ---------------
    - Signature
    - dict containing a "signature" field

    Returns
    -------
    Signature

    Raises
    ------
    TypeError
        If the object cannot be interpreted as a
        GER Signature.
    """

    if isinstance(obj, Signature):
        return obj

    if isinstance(obj, dict):

        signature = obj.get("signature")

        if isinstance(signature, Signature):
            return signature

    raise TypeError(
        f"Cannot extract GER Signature from object "
        f"of type '{type(obj).__name__}'."
    )


def extract_signature_metadata(obj):
    """
    Returns metadata associated with a Signature.

    If the object is a Geometry Scan record,
    returns all fields except 'signature'.

    If the object is already a Signature,
    returns an empty dictionary.
    """

    if isinstance(obj, dict):

        return {
            key: value
            for key, value in obj.items()
            if key != "signature"
        }

    if isinstance(obj, Signature):
        return {}

    raise TypeError(
        f"Cannot extract metadata from object "
        f"of type '{type(obj).__name__}'."
    )
