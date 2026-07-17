"""
=========================================================
GER
S29

External System Interface

Abstract interface implemented by all external
dynamical systems used by the GER framework.
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ExternalSystem(ABC):
    """
    Base interface for external dynamical systems.
    """

    @abstractmethod
    def reset(self):
        """
        Reset the system to its initial state.
        """
        pass

    @abstractmethod
    def step(self):
        """
        Advance the system by one integration step.
        """
        pass

    @abstractmethod
    def finished(self):
        """
        Return True when the simulation has finished.
        """
        pass
