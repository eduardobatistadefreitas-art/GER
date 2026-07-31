"""
=========================================================
GAMMA DEFINITION
=========================================================

Base interface for Gamma generators.

=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class GammaGenerator(ABC):
    """
    Base class for every Γ generator.
    """

    name: str = "base"

    @abstractmethod
    def generate(self, **kwargs):
        """
        Generate a Gamma object.

        Returns
        -------
        Any
            Gamma representation defined by the generator.
        """
        raise NotImplementedError
