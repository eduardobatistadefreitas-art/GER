"""
===============================================================================
GER

DynamicRegime Generator
===============================================================================

Creates a certified DynamicRegime starting from a Configuration.

Unlike DynamicRegimeBuilder, this component generates a new realization
instead of reconstructing an existing one.
===============================================================================
"""

from __future__ import annotations

from .model import (
    Configuration,
    DynamicRegime,
)


class DynamicRegimeGenerator:
    """
    Generates a DynamicRegime from a Configuration.

    Future versions will execute the complete observational pipeline:

        Configuration
            ↓
        Engine
            ↓
        Stationary Scan
            ↓
        Classifier
            ↓
        Classifier Audit
            ↓
        DynamicRegime

    Version 1.0 defines the public API only.
    """

    @staticmethod
    def generate(
        configuration: Configuration,
    ) -> DynamicRegime:
        """
        Generate a DynamicRegime.

        Parameters
        ----------
        configuration
            Configuration describing one realization.

        Returns
        -------
        DynamicRegime

        Raises
        ------
        NotImplementedError
            Until the generation pipeline is connected to
            the GER CORE.
        """

        raise NotImplementedError(
            "DynamicRegime generation pipeline has not been "
            "implemented yet."
        )
