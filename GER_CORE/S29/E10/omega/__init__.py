"""
=============================================================
GER :: OMEGA MODULE
=============================================================

Initial-condition generator subsystem for E10.

This package defines the Ω interface used by E10 to construct
initial conditions before the CORE engine is executed.
"""

from .omega_definition import OmegaGenerator
from .omega_registry import OmegaRegistry

__all__ = [
    "OmegaGenerator",
    "OmegaRegistry",
]
