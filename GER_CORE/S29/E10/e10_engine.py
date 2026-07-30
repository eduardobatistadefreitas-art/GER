from __future__ import annotations

from GER.CORE.ger_graph import build_ring_graph


def run_e10_engine(n_vertices: int = 128):

    print("INÍCIO")

    result = build_ring_graph(n_vertices)

    print("RESULT =", type(result), len(result))

    A, L, theta = result

    print("A", A.shape)
    print("L", L.shape)
    print("theta", theta.shape)

    print("FIM")

    return {}
