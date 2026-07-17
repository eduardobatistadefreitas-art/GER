"""
========================================================================
GER S29-E2.2

Parameter Sensitivity Pilot

========================================================================

Objective

Evaluate whether a small variation of the Duffing forcing parameter
(gamma) produces measurable changes in the resulting Geometric Signature.

This is a pilot experiment using only two parameter values.

========================================================================
"""

import numpy as np

from GER_CORE.S29.S29_E1_2_external_signature_generation import (
    initialize_signature_provider,
    run_external_signature_generation,
)

from GER_CORE.S29.external_systems.duffing import (
    simulate_duffing,
)

# ============================================================
# Configuration
# ============================================================

EXPERIMENT_VERSION = "1.0"

DT = 0.01
DURATION = 100.0

GAMMAS = [
    0.30,
    0.35,
]


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 72)
    print("GER S29-E2.2")
    print("Parameter Sensitivity Pilot")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)

    initialize_signature_provider()

    results = []

    for gamma in GAMMAS:

        print()
        print(f"Running gamma = {gamma:.2f}")

        time, signal = simulate_duffing(
            dt=DT,
            duration=DURATION,
            gamma=gamma,
        )

        result = run_external_signature_generation(

            system_name=f"Duffing (gamma={gamma:.2f})",

            time=time,

            signal=signal,

            dt=DT,

        )

        s = result.signature

        results.append(

            {
                "gamma": gamma,
                "diameter": s.diameter,
                "convergence": s.convergence,
                "recurrence": s.recurrence,
                "drift": s.drift,
            }

        )

    print()
    print("=" * 72)
    print("GEOMETRIC SIGNATURES")
    print("=" * 72)
    print()

    print(
        f"{'Gamma':>8}"
        f"{'Diameter':>16}"
        f"{'Conv.':>16}"
        f"{'Rec.':>12}"
        f"{'Drift':>16}"
    )

    print("-" * 72)

    for r in results:

        print(
            f"{r['gamma']:8.2f}"
            f"{r['diameter']:16.6f}"
            f"{r['convergence']:16.6f}"
            f"{r['recurrence']:12.6f}"
            f"{r['drift']:16.6e}"
        )

    print()
    print("=" * 72)
    print("SIGNATURE DIFFERENCE")
    print("=" * 72)

    r0 = results[0]
    r1 = results[1]

    print(f"ΔDiameter     : {r1['diameter'] - r0['diameter']:.6f}")
    print(f"ΔConvergence  : {r1['convergence'] - r0['convergence']:.6f}")
    print(f"ΔRecurrence   : {r1['recurrence'] - r0['recurrence']:.6f}")
    print(f"ΔDrift        : {r1['drift'] - r0['drift']:.6e}")

    print()
    print("=" * 72)
    print("STATUS : PARAMETER SENSITIVITY PILOT COMPLETED")
    print("=" * 72)


# ============================================================

if __name__ == "__main__":

    main()
