"""
=============================================================
E10 ENGINE
=============================================================

Adapter layer for the E10 experimental series.

This module introduces the Γ and Ω parametrization layers
while delegating all numerical evolution to the validated
GER CORE.
"""

from __future__ import annotations

from GER.CORE.ger_engine import run_engine

from .gamma import build_gamma
from .omega import build_initial_state


def run_e10_engine(
    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    gamma_generator="linear",
    omega_generator="gaussian",
    **kwargs,
):
    """
    Execute the E10 experiment.

    Workflow
    --------
        Γ generator
            ↓
        Ω initial-state generator
            ↓
        GER CORE integrator
    """

    gamma = build_gamma(
        generator=gamma_generator,
        **kwargs,
    )

    def initial_state(**state_kwargs):
        return build_initial_state(
            generator=omega_generator,
            gamma=gamma,
            **state_kwargs,
        )

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
