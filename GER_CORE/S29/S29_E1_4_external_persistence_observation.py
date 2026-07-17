"""
=========================================================
GER
S29-E1.5

External Signature Generation

Validates that an external system can generate an
official GER Geometric Signature.
=========================================================
"""

from __future__ import annotations

import numpy as np

from GER_CORE.S29.harmonic_system import HarmonicSystem
from GER_CORE.S29.identity_embedding import IdentityEmbedding
from GER_CORE.S29.external_pipeline import ExternalPipeline

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER.CORE.signature_api import (
    generate_signature,
)


# =========================================================
# Configuration
# =========================================================

DT = 0.1


# =========================================================
# Main
# =========================================================

def main():

    print("=" * 56)
    print("GER")
    print("S29-E1.5")
    print("External Signature Generation")
    print("=" * 56)

    # -----------------------------------------------------
    # External system
    # -----------------------------------------------------

    system = HarmonicSystem()

    embedding = IdentityEmbedding()

    pipeline = ExternalPipeline(
        system,
        embedding,
    )

    gamma_sequence = pipeline.run()

    print()
    print("Gamma sequence:", len(gamma_sequence))

    # -----------------------------------------------------
    # Modal basis
    # -----------------------------------------------------

    dimension = len(gamma_sequence[0])

    eigenvectors = np.eye(dimension)

    # -----------------------------------------------------
    # Snapshot sequence
    # -----------------------------------------------------

    snapshots = []

    for step, gamma in enumerate(gamma_sequence):

        snapshot = build_observational_snapshot(

            gamma=gamma,
            eigenvectors=eigenvectors,
            step=step,
            time=step * DT,

        )

        snapshots.append(snapshot)

    print("Snapshots:", len(snapshots))

    # -----------------------------------------------------
    # Persistence Observatory
    # -----------------------------------------------------

    observables = run_persistence_observatory(
        snapshots,
        DT,
    )

    print("Observables: OK")

    # -----------------------------------------------------
    # Signature generation
    # -----------------------------------------------------

    signature = generate_signature(
        observables,
        DT,
    )

    print()
    print("=" * 56)
    print("Geometric Signature")
    print("=" * 56)

    print(f"Diameter     : {signature.diameter:.12f}")
    print(f"Convergence  : {signature.convergence:.12f}")
    print(f"Recurrence   : {signature.recurrence:.12f}")
    print(f"Drift        : {signature.drift:.12f}")

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    assert np.isfinite(signature.diameter)
    assert np.isfinite(signature.convergence)
    assert np.isfinite(signature.recurrence)
    assert np.isfinite(signature.drift)

    print()
    print("=" * 56)
    print("STATUS : PASS")
    print("=" * 56)


# =========================================================

if __name__ == "__main__":
    main()
