# ============================================================
# GER
#
# S27-R1.7
#
# Reference Universe Augmentation
#
# Inserts the first external Geometric Signature
# into the GER reference universe.
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

    run_geometry_scan,

    build_trajectory,

    compute_confinement,

    compute_convergence,

    compute_recurrence,

    compute_drift,

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
# External signature
# ============================================================

def generate_external_signature():

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

    return {

        "simulation_id": "EXTERNAL",

        "system": "Harmonic Oscillator",

        "beta": None,

        "sigma": None,

        "potential": None,

        "dt": 1.0,

        "window_size": len(trajectory),

        "diameter": diameter,

        "convergence": convergence,

        "recurrence": recurrence,

        "drift": drift,

        "trajectory_length": trajectory_length,

        "signature": signature,

    }


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1.7")
    print("Reference Universe Augmentation")
    print("=" * 60)
    print()

    universe = run_geometry_scan()

    print("Reference Universe")
    print("-" * 60)

    print(f"Internal signatures : {len(universe)}")

    external = generate_external_signature()

    universe.append(

        external

    )

    print()

    print("Augmented Universe")
    print("-" * 60)

    print(f"Total signatures : {len(universe)}")

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
