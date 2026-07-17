"""
=========================================================
GER CORE

ger_confinement.py

=========================================================

Confinement Operator

Computes the metric diameter of a trajectory.

The confinement operator measures the maximum pairwise
distance between all trajectory points.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "compute_confinement",
]

GER_CONFINEMENT_VERSION = "1.0"


def compute_confinement(trajectory):
    """
    Computes the confinement (trajectory diameter).

    Parameters
    ----------
    trajectory : numpy.ndarray

    Returns
    -------
    float
    """

    n = len(trajectory)

    if n < 2:
        return 0.0

    diameter = 0.0

    for i in range(n):

        for j in range(i + 1, n):

            distance = np.linalg.norm(
                trajectory[i] - trajectory[j]
            )

            if distance > diameter:

                diameter = distance

    return diameter
```
