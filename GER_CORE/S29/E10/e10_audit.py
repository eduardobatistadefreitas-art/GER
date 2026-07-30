"""
=============================================================
E10 STRUCTURAL AUDIT
=============================================================

Structural audit for the E10 infrastructure.

Objective
---------
Verify that the E10 experiment reuses the GER CORE numerical
engine without modifying its geometry or integrator.

This audit validates the architecture, not the physics.

The current reference Ω generator intentionally reproduces
the original Gaussian packet implemented by the GER CORE.

=============================================================
"""

from __future__ import annotations

import numpy as np

from GER.CORE.ger_engine import run_engine
from .e10_engine import run_e10_engine


# ============================================================
# MAIN AUDIT
# ============================================================

def run_e10_audit():

    print("=" * 70)
    print("E10 STRUCTURAL AUDIT")
    print("=" * 70)

    # --------------------------------------------------------
    # Execute both engines
    # --------------------------------------------------------

    core = run_engine(
        timesteps=0,
    )

    e10 = run_e10_engine(
        timesteps=0,
    )

    # --------------------------------------------------------
    # Structural checks
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print()

    for name, value in checks.items():

        print(f"{name:30s}: {value}")

    print()

    gamma_difference = np.linalg.norm(
        core["gamma"] - e10["gamma"]
    )

    print(f"||γCORE − γE10|| = {gamma_difference:.8e}")

    print()

    if checks["Initial gamma identical"]:

        print(
            "INFO   : Ω reference generator reproduces "
            "the GER CORE Gaussian packet."
        )

    else:

        print(
            "INFO   : Ω generator defines a distinct "
            "initial state."
        )

    print()

    # --------------------------------------------------------
    # Architecture certificate
    # --------------------------------------------------------

    passed = (

        checks["Configuration"]
        and checks["Laplacian"]
        and checks["Eigenvalues"]
        and checks["Eigenvectors"]

    )

    if passed:

        print("STATUS : AUDIT PASSED")
        print("RESULT : E10 correctly reuses the GER CORE engine.")

    else:

        print("STATUS : AUDIT FAILED")
        print("RESULT : Structural inconsistency detected.")

    print("=" * 70)

    return {

        "checks": checks,

        "gamma_difference": gamma_difference,

        "passed": passed,

    }


__all__ = [
    "run_e10_audit",
]
