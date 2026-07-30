from __future__ import annotations

import numpy as np

from GER.CORE.ger_engine import run_engine
from .e10_engine import run_e10_engine


def run_e10_audit():

    print("=" * 70)
    print("E10 STRUCTURAL AUDIT")
    print("=" * 70)

    core = run_engine(timesteps=0)
    e10 = run_e10_engine(timesteps=0)

    checks = {

        "Adjacency": np.array_equal(core["adjacency"], e10["adjacency"]),
        "Laplacian": np.array_equal(core["laplacian"], e10["laplacian"]),
        "Theta": np.array_equal(core["theta"], e10["theta"]),
        "Eigenvalues": np.allclose(
            core["eigenvalues"],
            e10["eigenvalues"],
        ),
        "Eigenvectors": np.allclose(
            core["eigenvectors"],
            e10["eigenvectors"],
        ),

        "Initial gamma identical":
            np.allclose(core["gamma"], e10["gamma"]),

    }

    print()

    for name, value in checks.items():

        print(f"{name:25s}: {value}")

    print()

    diff = np.linalg.norm(
        core["gamma"] - e10["gamma"]
    )

    print(f"||γCORE − γE10|| = {diff:.8e}")

    print()

    if (
        checks["Adjacency"]
        and checks["Laplacian"]
        and checks["Theta"]
        and checks["Eigenvalues"]
        and checks["Eigenvectors"]
        and not checks["Initial gamma identical"]
    ):

        print("AUDIT PASSED")

    else:

        print("AUDIT FAILED")

    return checks
