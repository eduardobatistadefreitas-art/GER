"""
=========================================================
GER
S29

White Noise Generator

Reference external dynamical system.
=========================================================
"""

from __future__ import annotations

import numpy as np


def simulate_white_noise(
    dt=0.01,
    duration=100.0,
    seed=42,
):

    rng = np.random.default_rng(seed)

    n = int(duration / dt)

    time = np.arange(n) * dt

    signal = rng.normal(
        loc=0.0,
        scale=1.0,
        size=n,
    )

    return (
        time,
        signal,
    )
