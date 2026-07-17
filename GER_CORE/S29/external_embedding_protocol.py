"""
=========================================================
GER
S29

External Embedding Protocol

Official interface between external dynamical systems
and the Relational Spectral Geometry CORE.
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ExternalEmbedding(ABC):
    """
    Abstract embedding protocol.

    Any external system compatible with the RSG CORE
    must provide a temporal sequence of relational
    states gamma(t).
    """

    @abstractmethod
    def reset(self):
        """
        Reset the embedding state.
        """
        pass

    @abstractmethod
    def step(self):
        """
        Advance one temporal step.

        Returns
        -------
        gamma : ndarray
            Relational state at current time.
        """
        pass

    @abstractmethod
    def finished(self):
        """
        True when the temporal sequence ends.
        """
        pass
