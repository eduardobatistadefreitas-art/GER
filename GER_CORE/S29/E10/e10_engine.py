"""
=============================================================
E10 ENGINE
=============================================================

Adapter layer for the E10 experimental series.

This module delegates all numerical evolution to the GER CORE,
changing only the construction of the initial state.
"""

from __future__ import annotations

from GER.CORE.ger_engine import run_engine

from .omega import build_initial_state


def run_e10_engine(
    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    sigma=0.10,
):
    """
    Execute the E10 experiment using the standard GER CORE
    integrator and the Omega initial-state generator.
    """

    return run_engine(
        n=n,
        timesteps=timesteps,
        dt=dt,
        beta=beta,
        potential=potential,
        snapshot_stride=snapshot_stride,
        sigma=sigma,
        initial_state=build_initial_state,
    )


__all__ = [
    "run_e10_engine",
]
