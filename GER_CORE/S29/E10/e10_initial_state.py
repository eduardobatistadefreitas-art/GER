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
=============================================================
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
        Reserved for future E10 implementations.

    **kwargs
        Additional parameters forwarded to the
        initialization routine.

    Returns
    -------
    callable
        Function compatible with GER CORE:

            initial_state(theta) -> ndarray
    """

    #
    # Build Gamma parametrization.
    #
    # It is intentionally kept available for
    # future Γ–Ω coupling.
    #

    gamma_object = build_gamma(
        value=gamma,
        **kwargs,
    )

    def initial_state(theta):
        """
        Produce the initial state expected by GER CORE.

        The current implementation intentionally preserves
        the historical initialization while keeping the
        Gamma parametrization available for future
        developments.
        """

        #
        # Prevent unused-variable warnings.
        # Gamma will be used once the Γ–Ω coupling
        # is formally introduced.
        #

        _ = gamma_object
        _ = omega

        return build_initial_state(
            theta=theta,
            **kwargs,
        )

    return initial_state


__all__ = [
    "compose_initial_state",
]
