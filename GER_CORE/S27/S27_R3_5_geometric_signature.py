# ============================================================
# GER
#
# S27-R3.5
#
# Geometric Signature
#
# Generates the first external Geometric Signature
# for the Van der Pol oscillator.
# ============================================================

import numpy as np

from GER_CORE.S27_R3_1_vanderpol_state import (
    generate_vanderpol_state,
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

from GER.CORE.signature_api import (
    Signature,
)


# ============================================================
# Parameters
# ============================================================

N_SNAPSHOTS = 50


# ============================================================
# Snapshot generation
# ============================================================

def generate_snapshots():

    trajectory = generate_vanderpol_state()

    dimension = len(trajectory)

    step_size = max(
        1,
        dimension // N_SNAPSHOTS,
    )

    eigenvectors = (

        np.fft.fft(
            np.eye(dimension)

        ) / np.sqrt(dimension)

    )

    snapshots = []

    for step in range(N_SNAPSHOTS):

        gamma = np.roll(
            trajectory,
            step * step_size,
        )

        snapshot = build_observational_snapshot(

            gamma=gamma,

            eigenvectors=eigenvectors,

            step=step,

            time=float(step),

        )

        snapshots.append(snapshot)

    return snapshots


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R3.5")
    print("Geometric Signature")
    print("=" * 60)
    print()

    snapshots = generate_snapshots()

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
    print("STATUS : FIRST VAN DER POL SIGNATURE GENERATED")
    print("=" * 60)


if __name__ == "__main__":

    main()
