"""
=============================================================
OMEGA DEFINITION
=============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class OmegaGenerator(ABC):
    """
    Base class for every Ω generator.
    """

    name = "undefined"

    @abstractmethod
    def generate(self, **kwargs):
        """
        Must return the initial state required by the CORE.
        """
        raise NotImplementedError
