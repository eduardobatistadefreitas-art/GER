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
    implemented by the GER CORE.
    """

    name = "gaussian"

    def generate(
        self,
        theta,
        sigma=0.1,
        center=np.pi,
    ):

        return gaussian_packet(
            theta=theta,
            center=center,
            sigma=sigma,
        )
