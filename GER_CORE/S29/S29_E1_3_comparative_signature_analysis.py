"""
=========================================================
GER
S29-E1.3

Comparative Signature Analysis

Compares geometric signatures generated from
multiple external dynamical systems.
=========================================================
"""

from __future__ import annotations

from GER.CORE.default_signature_provider import (
    DefaultSignatureProvider,
)

from GER.CORE.ger_structural_certificate import (
    structural_certificate,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S29.ger_external_modal_embedding import (
    build_external_gamma,
)

from GER_CORE.S29.external_systems import (
    simulate_duffing,
    simulate_harmonic,
    simulate_white_noise,
)


# =========================================================
# Systems
# =========================================================

SYSTEMS = [
    ("Harmonic", simulate_harmonic),
    ("Duffing", simulate_duffing),
    ("White Noise", simulate_white_noise),
]


# =========================================================
# Main
# =========================================================

def main():

    print("=" * 60)
    print("GER S29-E1.3")
    print("Comparative Signature Analysis")
    print("=" * 60)

    provider = DefaultSignatureProvider()

    print()
    print(
        f"{'System':15}"
        f"{'Diameter':>12}"
        f"{'Conv.':>12}"
        f"{'Rec.':>12}"
        f"{'Drift':>12}"
    )

    print("-" * 63)

    for name, simulator in SYSTEMS:

        _, signal = simulator()

        gamma = build_external_gamma(signal)

        snapshot = provider.build_snapshot(gamma)

        signature = run_persistence_observatory(snapshot)

        certificate = structural_certificate(signature)

        print(
            f"{name:15}"
            f"{signature.diameter:12.6f}"
            f"{signature.convergence:12.6f}"
            f"{signature.recurrence:12.6f}"
            f"{signature.drift:12.6e}"
        )

        if not certificate["passed"]:
            print(f"WARNING: Structural certificate failed for {name}")

    print()
    print("STATUS:")
    print("COMPARATIVE SIGNATURE CATALOG GENERATED")


if __name__ == "__main__":
    main()
