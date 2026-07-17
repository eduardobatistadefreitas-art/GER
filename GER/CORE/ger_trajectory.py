"""
=========================================================
GER CORE

ger_trajectory.py

=========================================================

Trajectory construction for Geometric Signatures.

This module converts observational time series into the
trajectory representation used by the Geometric Signature
operators.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "build_trajectory",
]

GER_TRAJECTORY_VERSION = "1.0"


def build_trajectory(observables):
    """
    Builds the trajectory used by the Geometric
    Signature operators.

    Parameters
    ----------
    observables : dict

    Returns
    -------
    numpy.ndarray
    """

    return np.column_stack([

        np.asarray(
            observables["Rloc"],
            dtype=float,
        ),

        np.asarray(
            observables["Dspec"],
            dtype=float,
        ),

        np.asarray(
            observables["Hshape"],
            dtype=float,
        ),

        np.asarray(
            observables["Cauto"],
            dtype=float,
        ),

        np.asarray(
            observables["Rmacro"],
            dtype=float,
        ),

        np.asarray(
            observables["entropy"],
            dtype=float,
        ),

    ])
