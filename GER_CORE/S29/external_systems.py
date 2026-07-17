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

import numpy as np


# =========================================================
# Base Interface
# =========================================================

class ExternalSystem(ABC):
    """
    Generic external dynamical system.
    """

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def finished(self):
        pass


# =========================================================
# Duffing Oscillator
# =========================================================

class DuffingSystem(ExternalSystem):
    """
    Forced Duffing oscillator.

        x'' + δx' + αx + βx³ = γ cos(ωt)

    Only the displacement x(t) is exported.
    """

    def __init__(
        self,
        dt=0.01,
        duration=100.0,
        delta=0.2,
        alpha=-1.0,
        beta=1.0,
        gamma=0.3,
        omega=1.2,
    ):

        self.dt = dt
        self.duration = duration

        self.delta = delta
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.omega = omega

        self.reset()

    def reset(self):

        self.t = 0.0

        self.x = 0.1
        self.v = 0.0

        self.time = []
        self.signal = []

    def step(self):

        a = (
            self.gamma * np.cos(self.omega * self.t)
            - self.delta * self.v
            - self.alpha * self.x
            - self.beta * self.x**3
        )

        self.v += self.dt * a
        self.x += self.dt * self.v
        self.t += self.dt

        self.time.append(self.t)
        self.signal.append(self.x)

        return self.x

    def finished(self):

        return self.t >= self.duration


# =========================================================
# Public API
# =========================================================

def simulate_duffing(
    dt=0.01,
    duration=100.0,
):
    """
    Simulate the Duffing oscillator.

    Returns
    -------
    time : ndarray

    signal : ndarray
    """

    system = DuffingSystem(
        dt=dt,
        duration=duration,
    )

    while not system.finished():
        system.step()

    return (
        np.asarray(system.time),
        np.asarray(system.signal),
    )
