"""
E10 diagnostic
"""

from __future__ import annotations

import inspect

from GER.CORE.ger_graph import (
    build_ring_graph,
    spectral_basis,
)


def run_e10_engine(n_vertices: int = 128):

    print("=" * 60)
    print("build_ring_graph :", build_ring_graph)
    print("spectral_basis   :", spectral_basis)
    print("=" * 60)

    print(inspect.getsource(build_ring_graph))
    print(inspect.getsource(spectral_basis))

    print("=" * 60)

    result = build_ring_graph(n_vertices)

    print("type(result) =", type(result))
    print("len(result)  =", len(result))

    A, L, theta = result

    print("A.shape =", A.shape)
    print("L.shape =", L.shape)
    print("theta.shape =", theta.shape)

    print("type(L) =", type(L))
    print("dtype(L) =", L.dtype)

    print("=" * 60)
    print("Chamando spectral_basis...")

    eigvals, eigvecs = spectral_basis(L)

    print("OK")

    return {
        "A": A,
        "L": L,
        "theta": theta,
        "eigenvalues": eigvals,
        "eigenvectors": eigvecs,
    }
