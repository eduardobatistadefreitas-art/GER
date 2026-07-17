"""
============================================================
RSG

S29-E1.1

Duffing Oscillator

============================================================

First external validation of the Relational Signature
Space using the classical Duffing Oscillator.
"""

from GER_CORE.S29.duffing_solver import (
    solve_duffing,
)

from GER_CORE.S29.snapshot_generator import (
    generate_snapshots,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER.CORE.signature_api import (
    generate_signature,
)

from GER.CORE.ger_structural_certificate import (
    structural_certificate,
)

from GER.CORE.reference import (
    load_reference,
)

from GER.CORE.builder import (
    extend_reference_universe,
)

from GER.CORE.audit import (
    ReferenceUniverseAudit,
)

import numpy as np

from GER.CORE.bootstrap import initialize

# ==========================================================
# Temporary Modal Basis
# ==========================================================

def build_modal_basis(dimension):

    return np.eye(dimension)


# ==========================================================
# Experiment
# ==========================================================

def run_experiment():

    print()

    print("Step 1")
    print("Generating Duffing trajectory...")

    result = solve_duffing(
        t_max=20.0,
        dt=0.01,
    )

    trajectory = result["trajectory"]

    print("Trajectory generated.")
    print("Samples :", len(trajectory))

    print()

    print("Step 2")
    print("Generating snapshots...")

    eigenvectors = build_modal_basis(
        trajectory.shape[1]
    )

    snapshots = generate_snapshots(
        trajectory,
        eigenvectors,
        dt=0.01,
    )

    print("Snapshots :", len(snapshots))

    print()

    print("Step 3")
    print("Running Persistence Observatory...")

    observables = run_persistence_observatory(
        snapshots,
        dt=0.01,
    )

    print("Observatory completed.")

    print()

    print("Step 4")
    print("Generating Geometric Signature...")

    signature = generate_signature(
        observables,
        dt=0.01,
    )

    print(signature)

    print()

    print("Step 5")
    print("Running Structural Certificate...")

    certificate = structural_certificate(
        signature
    )

    print(certificate)

    print()

    print("Step 6")
    print("Loading S28 Reference Universe...")

    reference = load_reference(
        "S28_REFERENCE"
    )

    print("Reference loaded.")

    print()

    print("Step 7")
    print("Extending Reference Universe...")

    temporary_reference = extend_reference_universe(
        reference,
        signature,
    )

    print("Temporary universe created.")

    print()

    print("Step 8")
    print("Running Reference Universe Audit...")

    audit = ReferenceUniverseAudit()

    report = audit.compare(
        baseline=reference,
        candidate=temporary_reference,
    )

    print(report)

    print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print("Trajectory Samples :", len(trajectory))
    print("Snapshots          :", len(snapshots))

    print()

    print("Signature")

    print(signature)

    print()

    print("Certificate")

    print(certificate)

    print()

    print("Audit")

    print(report)

    print()

    print("=" * 60)
    print("STATUS : FIRST DUFFING SIGNATURE GENERATED")
    print("=" * 60)

    return {

        "trajectory": trajectory,

        "snapshots": snapshots,

        "observables": observables,

        "signature": signature,

        "certificate": certificate,

        "audit": report,

    }


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("RSG")
    print("S29-E1.1")
    print("Duffing Oscillator")
    print("=" * 60)

    print()
    print("Initializing RSG CORE...")
    initialize()
    print()

    run_experiment()


if __name__ == "__main__":

    main()
