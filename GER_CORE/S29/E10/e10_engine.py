"""
=============================================================
E10 ENGINE
=============================================================

Adapter layer for the E10 experimental series.

This module reuses the GER CORE infrastructure while
delegating the construction of the initial condition to
the Omega module.

No scientific logic is implemented here.

=============================================================
"""

from __future__ import annotations

from GER.CORE.ger_engine import (
    build_ring_graph,
    spectral_basis,
    initialize_verlet,
    central_velocity,
)

from .omega import build_initial_state


def run_e10_engine(n_vertices: int = 128):

    A, L, theta = build_ring_graph(n_vertices)

    print("A:", type(A), getattr(A, "shape", None))
    print("L:", type(L), getattr(L, "shape", None))
    print("theta:", type(theta), getattr(theta, "shape", None))

    return {}
