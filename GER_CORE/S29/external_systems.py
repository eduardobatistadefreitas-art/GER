"""
=========================================================
GER
S29

External Dynamical Systems

Reference interface for all external systems used
by the Relational Spectral Geometry framework.
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ExternalSystem(ABC):
    """
    Generic external dynamical system.

    The system is responsible only for evolving its own
    internal state.

    It has absolutely no knowledge of the RSG CORE.
    """

    @abstractmethod
    def reset(self):
        """Reset the system."""
        pass

    @abstractmethod
    def step(self):
        """
        Advance one time step.

        Returns
        -------
        state
            Instantaneous system state.
        """
        pass

    @abstractmethod
    def finished(self):
        """
        True if the simulation is finished.
        """
        pass
