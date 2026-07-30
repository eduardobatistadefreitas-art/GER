"""
=============================================================
E10 ENGINE
=============================================================

Adapter layer for the E10 experimental series.

This module contains no scientific logic.
It only orchestrates calls to the GER CORE.
"""

from __future__ import annotations

from GER.CORE.ger_graph import (
    build_ring_graph,
    spectral_basis,
)

from .omega import build_initial_state


def run_e10_engine(
    n_vertices: int = 128,
):
    """
    Build the geometric objects required by E10.

    Returns
    -------
    dict
        Dictionary containing the graph geometry,
        spectral basis and initial state.
    """

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    A, L, theta = build_ring_graph(n_vertices)

    # ---------------------------------------------------------
    # Spectral basis
    # ---------------------------------------------------------

    eigenvalues, eigenvectors = spectral_basis(L)

    # ---------------------------------------------------------
    # Initial state
    # ---------------------------------------------------------

    gamma = build_initial_state(theta=theta)

    # ---------------------------------------------------------
    # Return
    # ---------------------------------------------------------

    return {
        "A": A,
        "L": L,
        "theta": theta,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "gamma": gamma,
    }


__all__ = [
    "run_e10_engine",
]
