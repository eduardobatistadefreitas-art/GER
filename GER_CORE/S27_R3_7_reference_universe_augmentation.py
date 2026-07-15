# ============================================================
# GER
#
# S27-R3.7
#
# Reference Universe Augmentation
#
# Inserts the external Van der Pol Oscillator
# into the official GER observational universe.
# ============================================================

from copy import deepcopy

import numpy as np

from GER.CORE.signature_api import Signature

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
    build_trajectory,
    compute_confinement,
    compute_convergence,
    compute_recurrence,
    compute_drift,
)

# ============================================================
# Parameters
# ============================================================

MU = 1.0

DT = 0.01

NSTEPS = 5000

N_SNAPSHOTS = 50


# ============================================================
# Van der Pol
# ============================================================

def generate_signature():

    x = 1.0
    y = 0.0

    trajectory = []

    for _ in range(NSTEPS):

        trajectory.append(x)

        dx = y

        dy = MU * (1.0 - x**2) * y - x

        x += DT * dx
        y += DT * dy

    trajectory = np.asarray(trajectory)

    dimension = len(trajectory)

    stride = max(
        1,
        dimension // N_SNAPSHOTS,
    )

    eigenvectors = (

        np.fft.fft(
            np.eye(dimension)

        )

        / np.sqrt(dimension)

    )

    snapshots = []

    for step in range(N_SNAPSHOTS):

        gamma = np.roll(
            trajectory,
            step * stride,
        )

        snapshots.append(

            build_observational_snapshot(

                gamma=gamma,

                eigenvectors=eigenvectors,

                step=step,

                time=float(step),

            )

        )

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

    return signature, trajectory_length


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R3.7")
    print("Reference Universe Augmentation")
    print("=" * 60)
    print()

    universe = deepcopy(
        run_geometry_scan()
    )

    print("Reference Universe")
    print("-" * 60)

    print(
        f"Internal signatures : {len(universe)}"
    )

    signature, length = generate_signature()

    universe.append({

        "simulation_id": "EXTERNAL",

        "system": "Van der Pol Oscillator",

        "beta": None,

        "sigma": None,

        "potential": None,

        "dt": 1.0,

        "window_size": N_SNAPSHOTS - 1,

        "diameter": signature.diameter,

        "convergence": signature.convergence,

        "recurrence": signature.recurrence,

        "drift": signature.drift,

        "trajectory_length": length,

        "signature": signature,

    })

    print()

    print("Augmented Universe")
    print("-" * 60)

    print(
        f"Total signatures : {len(universe)}"
    )

    print()

    print("Last entry")
    print("-" * 60)

    for key, value in universe[-1].items():

        print(f"{key:<20}{value}")

    print()

    print("=" * 60)
    print("STATUS : EXTERNAL SIGNATURE INSERTED")
    print("=" * 60)


if __name__ == "__main__":

    main()
