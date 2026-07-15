# ============================================================
# GER
#
# S27-R2.7
#
# Reference Universe Augmentation
#
# Inserts the external Damped Oscillator
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

OMEGA = 1.0

GAMMA = 0.15

DIMENSION = 2048

N_SNAPSHOTS = 50

DT = 1.0


# ============================================================
# External Signature
# ============================================================

def generate_signature():

    eigenvectors = (

        np.fft.fft(

            np.eye(DIMENSION)

        )

        / np.sqrt(DIMENSION)

    )

    snapshots = []

    for step in range(N_SNAPSHOTS):

        t = step * DT

        theta = np.linspace(
            0.0,
            2.0*np.pi,
            DIMENSION,
            endpoint=False,
        )

        amplitude = np.exp(-GAMMA*t)

        gamma = amplitude*np.cos(
            theta + OMEGA*t
        )

        snapshots.append(

            build_observational_snapshot(

                gamma=gamma,

                eigenvectors=eigenvectors,

                step=step,

                time=t,

            )

        )

    observables = run_persistence_observatory(
        snapshots,
        DT,
    )

    trajectory = build_trajectory(
        observables
    )

    diameter = compute_confinement(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        DT,
    )

    recurrence = compute_recurrence(
        trajectory
    )

    drift, trajectory_length = compute_drift(
        trajectory
    )

    return Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    ), trajectory_length


# ============================================================
# Main
# ============================================================

def main():

    print("="*60)
    print("GER")
    print("S27-R2.7")
    print("Reference Universe Augmentation")
    print("="*60)
    print()

    universe = deepcopy(
        run_geometry_scan()
    )

    print("Reference Universe")
    print("-"*60)

    print(
        f"Internal signatures : {len(universe)}"
    )

    signature, length = generate_signature()

    universe.append({

        "simulation_id": "EXTERNAL",

        "system": "Damped Oscillator",

        "beta": None,

        "sigma": None,

        "potential": None,

        "dt": DT,

        "window_size": N_SNAPSHOTS-1,

        "diameter": signature.diameter,

        "convergence": signature.convergence,

        "recurrence": signature.recurrence,

        "drift": signature.drift,

        "trajectory_length": length,

        "signature": signature,

    })

    print()
    print("Augmented Universe")
    print("-"*60)

    print(
        f"Total signatures : {len(universe)}"
    )

    print()
    print("Last entry")
    print("-"*60)

    for key, value in universe[-1].items():

        print(f"{key:<20}{value}")

    print()
    print("="*60)
    print("STATUS : EXTERNAL SIGNATURE INSERTED")
    print("="*60)


if __name__ == "__main__":

    main()
