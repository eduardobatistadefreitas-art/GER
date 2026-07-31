"""
=============================================================
E10 ENGINE
=============================================================

Adapter layer for the E10 experimental series.

This module connects the E10 parametrization layers to the
validated GER CORE without introducing new numerical logic.

Responsibilities
----------------

- Build the E10 initial state.
- Delegate numerical evolution to the GER CORE.
- Return the standard engine output.
"""

from __future__ import annotations

from GER.CORE.ger_engine import run_engine

from .e10_initial_state import compose_initial_state


def run_e10_engine(
    *,
    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    gamma=1.0,
    omega=1.0,
    **kwargs,
):
    """
    Execute an E10 simulation.

    Parameters
    ----------
    gamma
        Γ parametrization.

    omega
        Ω parametrization.

    Remaining parameters are forwarded directly to the
    validated GER CORE.
    """

    # ---------------------------------------------------------
    # Build initial state
    # ---------------------------------------------------------

    initial_state = compose_initial_state(
        gamma=gamma,
        omega=omega,
        **kwargs,
    )

    # ---------------------------------------------------------
    # GER CORE
    # ---------------------------------------------------------

    return run_engine(
        n=n,
        timesteps=timesteps,
        dt=dt,
        beta=beta,
        potential=potential,
        snapshot_stride=snapshot_stride,
        initial_state=initial_state,
    )


__all__ = [
    "run_e10_engine",
]
