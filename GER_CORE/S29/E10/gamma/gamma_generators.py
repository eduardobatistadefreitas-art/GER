"""
=========================================================
GAMMA GENERATORS
=========================================================

Reference Gamma generators.

=========================================================
"""

from __future__ import annotations

import numpy as np

from .gamma_definition import GammaGenerator


class ConstantGammaGenerator(GammaGenerator):
    """
    Constant scalar Gamma generator.
    """

    name = "constant"

    def generate(self, value=1.0, **kwargs):
        return float(value)


class LinearGammaGenerator(GammaGenerator):
    """
    Linear Gamma grid generator.
    """

    name = "linear"

    def generate(
        self,
        gamma_min=0.0,
        gamma_max=1.0,
        num=101,
        **kwargs,
    ):
        return np.linspace(
            gamma_min,
            gamma_max,
            int(num),
        )
