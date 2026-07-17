"""
=========================================================
GER
S29

Harmonic Oscillator

Reference external dynamical system.
=========================================================
"""

from __future__ import annotations

import numpy as np

from GER_CORE.S29.external_system import ExternalSystem


class HarmonicSystem(ExternalSystem):

    def __init__(
        self,
        dt=0.01,
        duration=100.0,
        omega=1.0,
    ):

        self.dt = dt
        self.duration = duration
        self.omega = omega

        self.reset()

    def reset(self):

        self.t = 0.0

        self.x = 1.0
        self.v = 0.0

        self.time = []
        self.signal = []

    def step(self):

        a = -(self.omega ** 2) * self.x

        self.v += self.dt * a
        self.x += self.dt * self.v
        self.t += self.dt

        self.time.append(self.t)
        self.signal.append(self.x)

        return self.x

    def finished(self):

        return self.t >= self.duration


def simulate_harmonic(
    dt=0.01,
    duration=100.0,
):

    system = HarmonicSystem(
        dt=dt,
        duration=duration,
    )

    while not system.finished():
        system.step()

    return (
        np.asarray(system.time),
        np.asarray(system.signal),
    )
