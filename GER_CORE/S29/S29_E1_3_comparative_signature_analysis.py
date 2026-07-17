"""
=========================================================
GER
S29-E1.3

Comparative Signature Analysis

Compara Assinaturas Geométricas produzidas
por diferentes sistemas externos utilizando
o pipeline oficial do experimento S29-E1.2.

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
# Main
# =========================================================

def main():

    initialize_signature_provider()

    print("=" * 72)
    print("GER S29-E1.3")
    print("Comparative Signature Analysis")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)
    print()

    print(
        f"{'System':15}"
        f"{'Diameter':>14}"
        f"{'Conv.':>14}"
        f"{'Rec.':>14}"
        f"{'Drift':>16}"
        f"{'Status':>12}"
    )

    print("-" * 85)

    results = []

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

        results.append(result)

        summary = result.certificate["summary"]

        status = (
            "PASS"
            if summary["failed"] == 0
            else "FAIL"
        )

        print(

            f"{system_name:15}"

            f"{result.signature.diameter:14.6f}"

            f"{result.signature.convergence:14.6f}"

            f"{result.signature.recurrence:14.6f}"

            f"{result.signature.drift:16.6e}"

            f"{status:>12}"

        )

    print()
    print("=" * 72)
    print("Structural Certificate Summary")
    print("=" * 72)

    for result in results:

        summary = result.certificate["summary"]

        print()

        print(result.system)

        print(
            f"Passed : {summary['passed']}"
        )

        print(
            f"Failed : {summary['failed']}"
        )

    print()
    print("=" * 72)
    print("STATUS : COMPARATIVE SIGNATURE ANALYSIS COMPLETED")
    print("=" * 72)


# =========================================================

if __name__ == "__main__":

    main()
