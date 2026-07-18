"""
========================================================================
GER S29-E2.4

High Sensitivity Scan

========================================================================

Objective

Refine the parameter sensitivity analysis around the region where
S29-E2.3 detected the strongest variation of the Geometric Signature.

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
    0.340,
    0.342,
    0.344,
    0.346,
    0.348,
    0.350,
]

# ============================================================
# Main
# ============================================================

def main():

    print("=" * 72)
    print("GER S29-E2.4")
    print("High Sensitivity Scan")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)

    initialize_signature_provider()

    results = []

    total = len(GAMMAS)

    for index, gamma in enumerate(GAMMAS, start=1):

        print()
        print(f"[{index}/{total}] Running gamma = {gamma:.3f}")

        time, signal = simulate_duffing(
            dt=DT,
            duration=DURATION,
            gamma=gamma,
        )

        result = run_external_signature_generation(
            system_name=f"Duffing (gamma={gamma:.3f})",
            time=time,
            signal=signal,
            dt=DT,
        )

        signature = result.signature

        results.append(
            {
                "gamma": gamma,
                "diameter": float(signature.diameter),
                "convergence": float(signature.convergence),
                "recurrence": float(signature.recurrence),
                "drift": float(signature.drift),
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
            f"{r['gamma']:8.3f}"
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

        interval = f"{a['gamma']:.3f} -> {b['gamma']:.3f}"

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

    print(
        f"Diameter     : {largest['diameter'][1]} "
        f"(Δ={largest['diameter'][0]:.6f})"
    )

    print(
        f"Convergence  : {largest['convergence'][1]} "
        f"(Δ={largest['convergence'][0]:.6f})"
    )

    print(
        f"Recurrence   : {largest['recurrence'][1]} "
        f"(Δ={largest['recurrence'][0]:.6f})"
    )

    print(
        f"Drift        : {largest['drift'][1]} "
        f"(Δ={largest['drift'][0]:.6e})"
    )

    print()
    print("=" * 72)
    print("INTERPRETATION")
    print("=" * 72)

    print("Region scanned : gamma = 0.340 -> 0.350")
    print("Objective      : refine the strongest sensitivity interval")
    print("Output         : compact geometric report only")

    print()
    print("=" * 72)
    print("STATUS : HIGH SENSITIVITY SCAN COMPLETED")
    print("=" * 72)


# ============================================================

if __name__ == "__main__":
    main()
