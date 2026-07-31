"""
=========================================================
GAMMA REGISTRY
=========================================================

Registry of Gamma generators.

=========================================================
"""

from __future__ import annotations


class GammaRegistry:
    """
    Registry for Gamma generators.
    """

    def __init__(self):
        self._registry = {}

    def register(self, generator):
        """
        Register a Gamma generator.
        """
        name = generator.name.lower()

        if name in self._registry:
            raise ValueError(
                f"Generator '{name}' already registered."
            )

        self._registry[name] = generator

    def get(self, name):
        """
        Retrieve a registered generator.
        """
        key = name.lower()

        if key not in self._registry:
            raise KeyError(
                f"Unknown Gamma generator '{name}'."
            )

        return self._registry[key]

    def available(self):
        """
        Return available generators.
        """
        return sorted(self._registry.keys())
