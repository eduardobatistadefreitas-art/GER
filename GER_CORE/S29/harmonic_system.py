"""
=========================================================
GER
S29

Harmonic External System

Reference external dynamical system used to validate
the S29 architecture.
=========================================================
"""

from __future__ import annotations

import numpy as np

from GER_CORE.S29.external_systems import (
    ExternalSystem,
)


class HarmonicSystem(ExternalSystem):
    """
    Simple harmonic oscillator.

    The state returned at each step is a 1D vector
    containing the sampled cosine.
    """

    def __init__(
        self,
        omega=1.0,
        amplitude=1.0,
        samples=512,
        dt=1e-2,
    ):

        self.omega = omega
        self.amplitude = amplitude
        self.samples = samples
        self.dt = dt

        self.reset()

    def reset(self):

        self.index = 0

    def step(self):

        t = self.index * self.dt

        value = self.amplitude * np.cos(
            self.omega * t
        )

        self.index += 1

        return np.array([value])

    def finished(self):

        return self.index >= self.samples
