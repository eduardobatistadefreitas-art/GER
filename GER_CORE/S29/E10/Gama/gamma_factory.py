"""
=========================================================
GAMMA FACTORY
=========================================================

Factory for Gamma generators.

=========================================================
"""

from __future__ import annotations

from .gamma_generators import (
    ConstantGammaGenerator,
    LinearGammaGenerator,
)
from .gamma_registry import GammaRegistry


_registry = GammaRegistry()

_registry.register(ConstantGammaGenerator())
_registry.register(LinearGammaGenerator())


def build_gamma(
    generator: str = "linear",
    **kwargs,
):
    """
    Build a Gamma object using the selected generator.

    Parameters
    ----------
    generator : str
        Registered Gamma generator.

    **kwargs
        Arguments forwarded to the generator.
    """

    return _registry.get(generator).generate(**kwargs)
