# ============================================================
# GER CORE
#
# ger_observational_snapshot.py
#
# Snapshot mínimo utilizado pelo Observatório GER.
#
# Não calcula quantidades específicas do motor numérico
# (energia, Hamiltoniano, amplitude, etc.).
#
# ============================================================

from __future__ import annotations

from GER.CORE.ger_modal import (
    analyze_modal_state,
)


def build_observational_snapshot(
    gamma,
    eigenvectors,
    *,
    step=0,
    time=0.0,
):
    """
    Builds the minimal snapshot required by the
    GER observational framework.

    Parameters
    ----------
    gamma :
        State vector.

    eigenvectors :
        Modal basis.

    step :
        Optional simulation step.

    time :
        Optional physical time.
    """

    modal = analyze_modal_state(
        gamma,
        eigenvectors,
    )

    return {

        "step": step,

        "time": time,

        "gamma": gamma.copy(),

        "probability":
            modal["probability"],

        "participation_ratio":
            modal["participation_ratio"],

        "modal_center":
            modal["modal_center"],

        "spectral_entropy":
            modal["spectral_entropy"],

    }
