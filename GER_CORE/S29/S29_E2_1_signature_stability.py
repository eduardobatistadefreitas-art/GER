"""
========================================================================
GER S29-E2.1

Repeated Signature Stability
========================================================================

Objetivo

Verificar a reprodutibilidade da Assinatura Geométrica
executando repetidamente o mesmo sistema externo.

========================================================================
"""

import numpy as np

from GER_CORE.S29.S29_E1_2_external_signature_generation import (
    initialize_signature_provider,
    run_external_signature_generation,
)

from GER_CORE.S29.external_systems import (
    simulate_harmonic,
)


# ============================================================
# Configuration
# ============================================================

EXPERIMENT_VERSION = "1.0"

DT = 0.01

N_RUNS = 20


# ============================================================
# Statistics
# ============================================================

def coefficient_of_variation(values):

    values = np.asarray(values, dtype=float)

    mean = np.mean(values)
    std = np.std(values)

    if abs(mean) < 1e-15:
        return 0.0

    return std / abs(mean)


def report(name, values):

    values = np.asarray(values, dtype=float)

    print("-" * 64)
    print(name)
    print("-" * 64)

    print(f"Mean      : {np.mean(values):.12f}")
    print(f"Std       : {np.std(values):.12e}")
    print(f"Minimum   : {np.min(values):.12f}")
    print(f"Maximum   : {np.max(values):.12f}")
    print(f"CV        : {coefficient_of_variation(values):.12e}")
    print()


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 72)
    print("GER S29-E2.1")
    print("Repeated Signature Stability")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)

    initialize_signature_provider()

    diameter = []
    convergence = []
    recurrence = []
    drift = []

    for run in range(N_RUNS):

        time, signal = simulate_harmonic(
            dt=DT,
        )

        result = run_external_signature_generation(

            system_name="Harmonic",

            time=time,

            signal=signal,

            dt=DT,

        )

        signature = result.signature

        diameter.append(signature.diameter)
        convergence.append(signature.convergence)
        recurrence.append(signature.recurrence)
        drift.append(signature.drift)

        print(f"Run {run + 1:02d}/{N_RUNS} completed.")

    print()
    print("=" * 72)
    print("SIGNATURE STABILITY REPORT")
    print("=" * 72)
    print()

    report("Diameter", diameter)
    report("Convergence", convergence)
    report("Recurrence", recurrence)
    report("Drift", drift)

    print("=" * 72)
    print("STATUS : STABILITY ANALYSIS COMPLETED")
    print("=" * 72)


# ============================================================

if __name__ == "__main__":

    main()
