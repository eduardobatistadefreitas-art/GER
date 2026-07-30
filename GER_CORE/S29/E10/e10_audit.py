"""
=============================================================
E10 STRUCTURAL AUDIT
=============================================================

Auditoria estrutural da E10.

Objetivo
--------
Verificar que a E10 reutiliza integralmente o GER CORE,
alterando exclusivamente a condição inicial Ω.

A auditoria compara:

- configuração numérica
- operador laplaciano
- espectro
- base espectral
- condição inicial

=============================================================
"""

from __future__ import annotations

import numpy as np

from GER.CORE.ger_engine import run_engine
from .e10_engine import run_e10_engine


def run_e10_audit():

    print("=" * 70)
    print("E10 STRUCTURAL AUDIT")
    print("=" * 70)

    # ---------------------------------------------------------
    # Executa ambos os motores sem evolução temporal
    # ---------------------------------------------------------

    core = run_engine(
        timesteps=0,
    )

    e10 = run_e10_engine(
        timesteps=0,
    )

    # ---------------------------------------------------------
    # Comparações estruturais
    # ---------------------------------------------------------

    checks = {

        "Configuration":
            core["configuration"] == e10["configuration"],

        "Laplacian":
            np.array_equal(
                core["laplacian"],
                e10["laplacian"],
            ),

        "Eigenvalues":
            np.allclose(
                core["eigenvalues"],
                e10["eigenvalues"],
            ),

        "Eigenvectors":
            np.allclose(
                core["eigenvectors"],
                e10["eigenvectors"],
            ),

        "Initial gamma identical":
            np.allclose(
                core["gamma"],
                e10["gamma"],
            ),

    }

    # ---------------------------------------------------------
    # Relatório
    # ---------------------------------------------------------

    print()

    for name, value in checks.items():

        print(f"{name:30s}: {value}")

    print()

    gamma_difference = np.linalg.norm(
        core["gamma"] - e10["gamma"]
    )

    print(f"||γCORE − γE10|| = {gamma_difference:.8e}")

    print()

    # ---------------------------------------------------------
    # Certificado
    # ---------------------------------------------------------

    passed = (
        checks["Configuration"]
        and checks["Laplacian"]
        and checks["Eigenvalues"]
        and checks["Eigenvectors"]
        and not checks["Initial gamma identical"]
    )

    if passed:

        print("STATUS : AUDIT PASSED")
        print("RESULT : E10 modifies only the initial state.")

    else:

        print("STATUS : AUDIT FAILED")
        print("RESULT : Structural differences detected.")

    print("=" * 70)

    return {
        "checks": checks,
        "gamma_difference": gamma_difference,
        "passed": passed,
    }


__all__ = [
    "run_e10_audit",
]
