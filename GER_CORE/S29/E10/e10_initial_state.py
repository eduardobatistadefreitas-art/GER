"""
=============================================================
E10 INITIAL STATE
=============================================================

Composition layer for the E10 experimental series.

This module combines the Γ and Ω parametrization layers and
produces the initial state consumed by the GER CORE.

At the current stage, the historical initialization is
preserved. The Γ–Ω coupling will be introduced in future
E10 revisions.
"""

from __future__ import annotations

from .gamma import build_gamma
from .omega import build_initial_state


def compose_initial_state(
    gamma=1.0,
    omega=1.0,
    **kwargs,
):
    """
    Build the E10 initial-state function.

    Parameters
    ----------
    gamma
        Γ parameter.

    omega
        Ω parameter.

    **kwargs
        Additional parameters forwarded to the
        parametrization layers.

    Returns
    -------
    callable
        Function compatible with GER CORE:

            initial_state(theta) -> ndarray
    """

    gamma_object = build_gamma(
        value=gamma,
        **kwargs,
    )

    omega_generator = build_initial_state(
        omega=omega,
        **kwargs,
    )

    def initial_state(theta):
        """
        Compose the initial state.

        The Γ object is intentionally kept available
        but does not yet modify the historical Ω
        initialization.
        """

        _ = gamma_object

        return omega_generator(
            theta=theta,
        )

    return initial_state


__all__ = [
    "compose_initial_state",
]
