"""
=========================================================
GER CORE
Arquivo : ger_validation.py
=========================================================

Validação automática do núcleo computacional GER.

Executa testes mínimos para garantir que:

• módulos carregam corretamente
• geometria funciona
• motor executa
• snapshots são produzidos
• observatório espectral está ativo
"""

from __future__ import annotations


import numpy as np


from GER.CORE.ger_graph import (
    build_ring_graph,
    spectral_basis,
    gaussian_packet
)


from GER.CORE.ger_engine import (
    run_engine
)



# =========================================================
# Validação da geometria
# =========================================================

def validate_graph():

    A, L, theta = build_ring_graph(
        64
    )

    assert A.shape == (
        64,
        64
    )

    assert L.shape == (
        64,
        64
    )

    assert len(theta) == 64


    return True



# =========================================================
# Validação espectral
# =========================================================

def validate_spectrum():

    _, L, _ = build_ring_graph(
        64
    )


    eigenvalues, eigenvectors = (
        spectral_basis(L)
    )


    assert len(eigenvalues) == 64

    assert eigenvectors.shape == (
        64,
        64
    )


    return True



# =========================================================
# Validação do motor
# =========================================================

def validate_engine():

    result = run_engine(
        n=128,
        timesteps=100,
        dt=2.5e-4,
        beta=1.0,
        potential="A",
        snapshot_stride=20
    )


    assert "snapshots" in result

    assert len(
        result["snapshots"]
    ) > 0


    assert (
        result["diverged"]
        is False
    )


    snapshot = (
        result["snapshots"][0]
    )


    required = [

        "energy",

        "dominant_mode",

        "modal_width",

        "spectral_entropy"

    ]


    for key in required:

        assert key in snapshot


    return True



# =========================================================
# Validação completa
# =========================================================

def validate_GER_CORE():

    print(
        "================================"
    )

    print(
        " GER CORE VALIDATION"
    )

    print(
        "================================"
    )


    tests = [

        (
            "Geometria",
            validate_graph
        ),

        (
            "Espectro",
            validate_spectrum
        ),

        (
            "Motor",
            validate_engine
        )

    ]


    for name, test in tests:

        test()

        print(
            f"[OK] {name}"
        )


    print(
        "================================"
    )

    print(
        " GER CORE VALIDADO "
    )

    print(
        "================================"
    )


    return True
