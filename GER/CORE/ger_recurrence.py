"""
=========================================================
GER CORE

ger_recurrence.py

=========================================================

Recurrence Operator

Computes the recurrence of a trajectory.

The recurrence operator measures the fraction of
trajectory point pairs separated by less than a
reference distance.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "compute_recurrence",
]

GER_RECURRENCE_VERSION = "1.0"


def compute_recurrence(
    trajectory,
    epsilon=None,
):
    """
    Computes the trajectory recurrence.

    Parameters
    ----------
    trajectory : numpy.ndarray

    epsilon : float, optional

    Returns
    -------
    float
    """

    n = len(trajectory)

    if n < 2:
        return 0.0

    if epsilon is None:

        epsilon = 0.05 * np.std(
            trajectory
        )

    count = 0
    total = 0

    for i in range(n):

        for j in range(i + 1, n):

            total += 1

            distance = np.linalg.norm(
                trajectory[i] - trajectory[j]
            )

            if distance < epsilon:

                count += 1

    if total == 0:
        return 0.0

    return count / total
