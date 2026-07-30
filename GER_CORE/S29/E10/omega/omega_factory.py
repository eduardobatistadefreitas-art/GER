"""
=============================================================
OMEGA FACTORY
=============================================================

High-level interface for building initial conditions.

This module hides the registry implementation from the
rest of the project.

=============================================================
"""

from __future__ import annotations

from .omega_registry import OmegaRegistry
from .omega_generators import GaussianPacketGenerator


_registry = OmegaRegistry()
_registry.register(GaussianPacketGenerator())


def build_initial_state(
    generator: str = "gaussian",
    **kwargs,
):
    """
    Build an initial state using the selected generator.

    Parameters
    ----------
    generator : str
        Registered generator name.

    **kwargs
        Arguments forwarded to the generator.

    Returns
    -------
    numpy.ndarray
        Initial state.
    """

    return _registry.get(generator).generate(**kwargs)
