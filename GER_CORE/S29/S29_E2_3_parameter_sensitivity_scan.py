"""
========================================================================
GER S29-E2.3

Parameter Sensitivity Scan

========================================================================

Objective

Map the sensitivity of the Geometric Signature with respect to the
Duffing forcing parameter (gamma).

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

GAMMAS = np.arange(0.30, 0.351, 0.01)

# ============================================================
# Main
# ============================================================

def main():

    print("=" * 72)
    print("GER S29-E2.3")
    print("Parameter Sensitivity Scan")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)

    initialize_signature_provider()

    results = []

    total = len(GAMMAS)

    for index, gamma in enumerate(GAMMAS, start=1):

        print()
        print(f"[{index}/{total}] Running gamma = {gamma:.2f}")

        time, signal = simulate_duffing(
            dt=DT,
            duration=DURATION,
            gamma=float(gamma),
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
                "gamma": float(gamma),
                "diameter": float(s.diameter),
                "convergence": float(s.convergence),
                "recurrence": float(s.recurrence),
                "drift": float(s.drift),
            }
        )

    # ============================================================
    # Signature Table
    # ============================================================

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

    # ============================================================
    # Consecutive Differences
    # ============================================================

    print()
    print("=" * 72)
    print("CONSECUTIVE DIFFERENCES")
    print("=" * 72)

    largest = {
        "diameter": (0.0, ""),
        "convergence": (0.0, ""),
        "recurrence": (0.0, ""),
        "drift": (0.0, ""),
    }

    for i in range(len(results) - 1):

        a = results[i]
        b = results[i + 1]

        dd = b["diameter"] - a["diameter"]
        dc = b["convergence"] - a["convergence"]
        dr = b["recurrence"] - a["recurrence"]
        ddf = b["drift"] - a["drift"]

        interval = f"{a['gamma']:.2f} -> {b['gamma']:.2f}"

        print()
        print(f"Gamma {interval}")
        print(f"  ΔDiameter     : {dd:.6f}")
        print(f"  ΔConvergence  : {dc:.6f}")
        print(f"  ΔRecurrence   : {dr:.6f}")
        print(f"  ΔDrift        : {ddf:.6e}")

        if abs(dd) > largest["diameter"][0]:
            largest["diameter"] = (abs(dd), interval)

        if abs(dc) > largest["convergence"][0]:
            largest["convergence"] = (abs(dc), interval)

        if abs(dr) > largest["recurrence"][0]:
            largest["recurrence"] = (abs(dr), interval)

        if abs(ddf) > largest["drift"][0]:
            largest["drift"] = (abs(ddf), interval)

    # ============================================================
    # Summary
    # ============================================================

    print()
    print("=" * 72)
    print("LARGEST VARIATIONS")
    print("=" * 72)

    print(f"Diameter     : {largest['diameter'][1]}")
    print(f"Convergence  : {largest['convergence'][1]}")
    print(f"Recurrence   : {largest['recurrence'][1]}")
    print(f"Drift        : {largest['drift'][1]}")

    print()
    print("=" * 72)
    print("STATUS : PARAMETER SENSITIVITY SCAN COMPLETED")
    print("=" * 72)


# ============================================================

if __name__ == "__main__":
    main()
