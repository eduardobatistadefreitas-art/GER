# ============================================================
# GER
#
# S27-R1.6
#
# Structural Certificate
#
# First Structural Certificate generated from
# an external Geometric Signature.
# ============================================================

import numpy as np

from GER.CORE.signature_api import (
    Signature,
)

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (

    build_trajectory,

    compute_confinement,

    compute_convergence,

    compute_recurrence,

    compute_drift,

)

from GER_CORE.S26_B36_stationary_scan import (

    stationary_scan,

)
# ============================================================
# Harmonic trajectory
# ============================================================

def generate_harmonic_snapshots(

    samples=50,

    dimension=2048,

):

    snapshots = []

    basis = (

        np.fft.fft(
            np.eye(dimension)
        )

        / np.sqrt(dimension)

    )

    theta = np.linspace(

        0,

        2 * np.pi,

        dimension,

        endpoint=False,

    )

    for step in range(samples):

        phase = (

            2 * np.pi * step

            / samples

        )

        gamma = np.cos(

            theta + phase

        )

        snapshot = build_observational_snapshot(

            gamma=gamma,

            eigenvectors=basis,

            step=step,

            time=float(step),

        )

        snapshots.append(
            snapshot
        )

    return snapshots
  # ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1.6")
    print("Structural Certificate")
    print("=" * 60)
    print()

    snapshots = generate_harmonic_snapshots()

    observables = run_persistence_observatory(

        snapshots,

        dt=1.0,

    )

    trajectory = build_trajectory(

        observables

    )

    diameter = compute_confinement(

        trajectory

    )

    convergence = compute_convergence(

        trajectory,

        1.0,

    )

    recurrence = compute_recurrence(

        trajectory

    )

    drift, _ = compute_drift(

        trajectory

    )

    signature = Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )

    certificate = stationary_scan(
        signature
    )

    print("Signature")
    print("-" * 60)

    print(signature)

    print()
    print("Certificate summary")
    print("-" * 60)

    print(certificate["summary"])

    print()

    print("Deductions")
    print("-" * 60)

    for deduction in certificate["deductions"]:

        print(deduction)

    print()
    print("=" * 60)
    print("STATUS : FIRST EXTERNAL STRUCTURAL CERTIFICATE")
    print("=" * 60)


if __name__ == "__main__":
    main()
