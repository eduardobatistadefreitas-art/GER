"""
=============================================================
OMEGA REGISTRY
=============================================================
"""

from __future__ import annotations


class OmegaRegistry:

    def __init__(self):
        self._registry = {}

    def register(self, generator):

        name = generator.name.lower()

        if name in self._registry:
            raise ValueError(
                f"Generator '{name}' already registered."
            )

        self._registry[name] = generator

    def get(self, name):

        return self._registry[name.lower()]

    def names(self):

        return sorted(self._registry.keys())
