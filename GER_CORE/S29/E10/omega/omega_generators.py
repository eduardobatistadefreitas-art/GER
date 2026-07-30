"""
=============================================================
OMEGA GENERATORS
=============================================================
"""

from __future__ import annotations

from .omega_definition import OmegaGenerator


class NullGenerator(OmegaGenerator):
    """
    Minimal generator used to validate the Ω infrastructure.
    """

    name = "null"

    def generate(self, **kwargs):

        return {
            "q0": None,
            "p0": None,
        }
