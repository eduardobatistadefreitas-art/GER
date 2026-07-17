import numpy as np

from GER_CORE.S29.S29_E1_2_external_signature_generation import (
    initialize_signature_provider,
    run_external_signature_generation,
)

from GER_CORE.S29.external_systems import (
    simulate_harmonic,
)

# ============================================================
# GER S29-E2.1
# Repeated Signature Stability
# ============================================================

N_RUNS = 20


def coefficient_of_variation(values):

    values = np.asarray(values, dtype=float)

    mean = np.mean(values)
    std = np.std(values)

    if abs(mean) < 1e-15:
        return 0.0

    return std / abs(mean)


def summarize(name, values):

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


def main():

    print("=" * 72)
    print("GER S29-E2.1")
    print("Repeated Signature Stability")
    print("=" * 72)

    provider = initialize_signature_provider()

    diameter = []
    convergence = []
    recurrence = []
    drift = []

    for run in range(N_RUNS):

        result = run_external_signature_generation(
            provider=provider,
            simulator=simulate_harmonic,
            system_name="Harmonic"
        )

        signature = result.signature

        diameter.append(signature.diameter)
        convergence.append(signature.convergence)
        recurrence.append(signature.recurrence)
        drift.append(signature.drift)

        print(
            f"Run {run + 1:02d}/{N_RUNS} completed."
        )

    print()
    print("=" * 72)
    print("SIGNATURE STABILITY REPORT")
    print("=" * 72)
    print()

    summarize("Diameter", diameter)
    summarize("Convergence", convergence)
    summarize("Recurrence", recurrence)
    summarize("Drift", drift)

    print("=" * 72)
    print("STABILITY ANALYSIS COMPLETED")
    print("=" * 72)


if __name__ == "__main__":
    main()
