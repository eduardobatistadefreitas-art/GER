"""
=========================================================
GER
S29

Duffing Oscillator

Reference external dynamical system.
=========================================================
"""

from __future__ import annotations

import numpy as np

from GER_CORE.S29.external_system import ExternalSystem


class DuffingSystem(ExternalSystem):

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
            - self.beta * self.x ** 3
        )

        self.v += self.dt * a
        self.x += self.dt * self.v
        self.t += self.dt

        self.time.append(self.t)
        self.signal.append(self.x)

        return self.x

    def finished(self):

        return self.t >= self.duration


def simulate_duffing(
    dt=0.01,
    duration=100.0,
    delta=0.2,
    alpha=-1.0,
    beta=1.0,
    gamma=0.3,
    omega=1.2,
):
    """
    Simulate the Duffing oscillator.

    All physical parameters are exposed while preserving the
    original default behaviour used throughout S29.
    """

    system = DuffingSystem(
        dt=dt,
        duration=duration,
        delta=delta,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        omega=omega,
    )

    while not system.finished():
        system.step()

    return (
        np.asarray(system.time),
        np.asarray(system.signal),
    )
