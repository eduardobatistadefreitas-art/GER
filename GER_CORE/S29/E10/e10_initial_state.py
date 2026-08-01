"""
=============================================================
E10 INITIAL STATE
=============================================================

Composition layer for the E10 experimental series.

This module combines the Γ and Ω parametrization layers and
produces the initial state consumed by the GER CORE.

E10-v1
------

The first canonical operator acts as a global scaling of the
historical initial state.

The Γ module provides the parametrization.

The Ω module builds the historical initial state.

compose_initial_state() applies the first admissible operator
defined by the E10 specification.

Ω remains reserved for future operator families.
=============================================================
"""

from __future__ import annotations

from .gamma import build_gamma
from .omega import build_initial_state


def compose_initial_state(
    gamma=0.0,
    omega=0.0,
    **kwargs,
):
    """
    Build the E10 initial-state function.

    Parameters
    ----------
    gamma
        Γ experimental coordinate.

    omega
        Ω experimental coordinate.
        Reserved for future operator families.

    **kwargs
        Additional parameters forwarded to the
        historical initialization.

    Returns
    -------
    callable
        Function compatible with GER CORE:

            initial_state(theta) -> ndarray
    """

    #
    # Gamma parametrization.
    #

    gamma_value = build_gamma(
        generator="constant",
        value=gamma,
    )

    def initial_state(theta):
        """
        Produce the initial state expected by GER CORE.
        """

        #
        # Historical initial state.
        #

        historical_state = build_initial_state(
            theta=theta,
            **kwargs,
        )

        #
        # -----------------------------------------------------
        # Canonical Operator E10-v1
        #
        # Family 1:
        # Global Scale Operator
        #
        # S' = (1 + gamma) S
        #
        # Ω remains reserved for future families.
        # -----------------------------------------------------
        #

        deformed_state = (
            1.0 + gamma_value
        ) * historical_state

        #
        # Ω intentionally inactive in E10-v1.
        #

        _ = omega

        return deformed_state

    return initial_state


__all__ = [
    "compose_initial_state",
]
