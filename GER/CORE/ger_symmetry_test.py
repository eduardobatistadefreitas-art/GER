"""
=========================================================
GER CORE
Arquivo : ger_symmetry_test.py
=========================================================

Auditoria de simetria translacional no anel.

Testa se deslocamentos da condição inicial
preservam observáveis globais.

=========================================================
"""

from __future__ import annotations

import numpy as np


from GER.CORE.ger_graph import (
    build_ring_graph,
    gaussian_packet
)


from GER.CORE.ger_engine import run_engine



def compare_states(
    a,
    b
):

    return (
        np.linalg.norm(a-b)
        /
        (np.linalg.norm(a)+1e-15)
    )



def test_ring_symmetry(
    n=384,
    shift=50,
    dt=5e-5
):

    # geometria

    _, L, theta = build_ring_graph(n)


    # condição inicial original

    gamma_1 = gaussian_packet(
        theta,
        sigma=0.10
    )


    # condição deslocada

    gamma_2 = np.roll(
        gamma_1,
        shift
    )


    # observáveis iniciais

    initial_difference = compare_states(
        gamma_1,
        np.roll(gamma_2, -shift)
    )


    return {
        "initial_difference":
            initial_difference,

        "gamma_original":
            gamma_1,

        "gamma_shifted":
            gamma_2
    }
