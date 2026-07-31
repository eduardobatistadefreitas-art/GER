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
    Gamma parametrization.
    """

    name = "gaussian"

    def generate(
        self,
        theta,
        gamma=None,
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
            Currently accepted for interface compatibility.
            It is reserved for future implementations.

        sigma : float
            Gaussian width.

        center : float
            Gaussian center.
        """

        return gaussian_packet(
            theta=theta,
            center=center,
            sigma=sigma,
        )
