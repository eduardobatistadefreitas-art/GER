# ============================================================
# GER
#
# S27-R1.5
#
# Geometric Signature
#
# First Geometric Signature generated from
# an external dynamical system.
# ============================================================

import numpy as np

from GER.CORE.signature_api import (
    Signature,
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
# ============================================================
# Harmonic trajectory
# ============================================================

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)


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
    print("S27-R1.5")
    print("Geometric Signature")
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

    drift, trajectory_length = compute_drift(

        trajectory

    )

    signature = Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )

    print("Signature")
    print("-" * 60)

    print(f"Diameter     : {signature.diameter}")
    print(f"Convergence  : {signature.convergence}")
    print(f"Recurrence   : {signature.recurrence}")
    print(f"Drift        : {signature.drift}")

    print()
    print(f"Trajectory length : {trajectory_length}")

    print()
    print("=" * 60)
    print("STATUS : FIRST EXTERNAL SIGNATURE GENERATED")
    print("=" * 60)


if __name__ == "__main__":
    main()
