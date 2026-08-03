"""
=============================================================
OMEGA GENERATORS
=============================================================
"""

from __future__ import annotations

import numpy as np

from GER.CORE.ger_graph import gaussian_packet

from .omega_definition import OmegaGenerator


class GaussianPacketGenerator(OmegaGenerator):
    """
    Reference Gaussian packet generator.

    This generator reproduces the current initial condition
    implemented by the GER CORE while accepting the E10
    Gamma and Omega parametrizations.
    """

    name = "gaussian"

    def generate(
        self,
        theta,
        gamma=None,
        omega=0.0,
        sigma=0.1,
        center=np.pi,
    ):
        """
        Generate an initial state.

        Parameters
        ----------
        theta : ndarray
            Angular coordinates.

        gamma : optional
            E10 Gamma parametrization.

        omega : float
            E10 Omega parametrization.

        sigma : float
            Gaussian width.

        center : float
            Gaussian center.
        """

        #
        # Gamma remains handled by compose_initial_state().
        #

        _ = gamma

        return gaussian_packet(
            theta=theta,
            center=center,
            sigma=sigma,
            omega=omega,
        )
