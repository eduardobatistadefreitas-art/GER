"""
=========================================================
GER
S29-E1.4

External Persistence Observation

Compara os observáveis produzidos pelo
Observatório de Persistência para diferentes
sistemas externos.

=========================================================
"""

from __future__ import annotations

from GER_CORE.S29.S29_E1_2_external_signature_generation import (
    initialize_signature_provider,
    run_external_signature_generation,
)

from GER_CORE.S29.external_systems import (
    simulate_duffing,
    simulate_harmonic,
    simulate_white_noise,
)

# =========================================================
# Version
# =========================================================

EXPERIMENT_VERSION = "1.0"

DT = 0.01


# =========================================================
# Systems
# =========================================================

SYSTEMS = [

    (
        "Duffing",
        simulate_duffing,
    ),

    (
        "Harmonic",
        simulate_harmonic,
    ),

    (
        "White Noise",
        simulate_white_noise,
    ),

]


# =========================================================
# Helpers
# =========================================================

def format_value(value):

    try:
        return f"{float(value):.6f}"
    except Exception:
        return str(value)


# =========================================================
# Main
# =========================================================

def main():

    initialize_signature_provider()

    print("=" * 72)
    print("GER S29-E1.4")
    print("External Persistence Observation")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)

    for system_name, simulator in SYSTEMS:

        time, signal = simulator(
            dt=DT,
        )

        result = run_external_signature_generation(

            system_name=system_name,

            time=time,

            signal=signal,

            dt=DT,

        )

        print()
        print("=" * 72)
        print(system_name)
        print("=" * 72)

        print()
        print("Persistence Observatory")
        print("-----------------------")

        observables = result.observables

        for key in sorted(observables.keys()):

            print(
                f"{key:<25}"
                f"{format_value(observables[key])}"
            )

        print()
        print("Geometric Signature")
        print("-------------------")

        print(
            f"Diameter     : {result.signature.diameter:.6f}"
        )

        print(
            f"Convergence : {result.signature.convergence:.6f}"
        )

        print(
            f"Recurrence  : {result.signature.recurrence:.6f}"
        )

        print(
            f"Drift       : {result.signature.drift:.6e}"
        )

    print()
    print("=" * 72)
    print("STATUS : PERSISTENCE OBSERVATION COMPLETED")
    print("=" * 72)


# =========================================================

if __name__ == "__main__":

    main()
