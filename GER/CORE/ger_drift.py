"""
=========================================================
GER CORE

ger_drift.py

=========================================================

Drift Operator

Computes the trajectory drift.

The drift operator measures the ratio between the
net displacement and the total trajectory length.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "compute_drift",
]

GER_DRIFT_VERSION = "1.0"


def compute_drift(trajectory):
    """
    Computes the trajectory drift.

    Parameters
    ----------
    trajectory : numpy.ndarray

    Returns
    -------
    tuple
        (drift, trajectory_length)
    """

    if len(trajectory) < 2:
        return 0.0, 0.0

    displacement = np.linalg.norm(
        trajectory[-1] - trajectory[0]
    )

    steps = np.diff(
        trajectory,
        axis=0,
    )

    trajectory_length = np.sum(
        np.linalg.norm(
            steps,
            axis=1,
        )
    )

    if trajectory_length == 0:

        drift = 0.0

    else:

        drift = (
            displacement
            / trajectory_length
        )

    return drift, trajectory_length
