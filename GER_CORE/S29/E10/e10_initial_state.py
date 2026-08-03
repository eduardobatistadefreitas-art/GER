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

compose_initial_state() applies the canonical E10 operators
defined by the E10 specification.
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
        # Historical state.
        #
        # The historical generator is now selected through the
        # Omega infrastructure. The active generator receives
        # omega and may decide how to use it.
        #

        historical_state = build_initial_state(

            theta=theta,

            gamma=gamma,

            omega=omega,

            **kwargs,

        )

        #
        # -----------------------------------------------------
        # Canonical Operator
        #
        # Family 1:
        #
        #     S' = (1 + gamma) S
        #
        # Family 2:
        #
        #     Implemented inside the selected Omega generator.
        #
        # The two operator families therefore compose naturally:
        #
        #     Generator(Ω)
        #          ↓
        #     Global Scale(Γ)
        # -----------------------------------------------------
        #

        deformed_state = (

            1.0 + gamma_value

        ) * historical_state

        return deformed_state

    return initial_state


__all__ = [
    "compose_initial_state",
]
