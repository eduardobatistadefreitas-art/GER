# ============================================================
# GER
#
# S27-R1.8
#
# Observational Partition
#
# Builds the first observational partition of the
# augmented universe and locates the external system.
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

from GER_CORE.S27_E2_1_partition_lattice import (
    build_partition,
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

        snapshots.append(snapshot)

    return snapshots


# ============================================================
# External Signature
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
    print("S27-R1.8")
    print("Observational Partition")
    print("=" * 60)
    print()

    universe = run_geometry_scan()

    universe.append(

        generate_external_signature()

    )

    print("Augmented universe")
    print("-" * 60)

    print(f"Total signatures : {len(universe)}")

    print()

    # --------------------------------------------------------
    # First observational partition
    #
    # Current observable:
    # recurrence
    # --------------------------------------------------------

    partition = build_partition(

        universe,

        key=lambda row: round(
            row["signature"].recurrence,
            6,
        ),

    )

    print("Partition")
    print("-" * 60)

    print(f"Number of blocks : {len(partition.blocks)}")

    print()

    external_block = None

    for block in partition.blocks:

        for row in block:

            if row["simulation_id"] == "EXTERNAL":

                external_block = block

                break

        if external_block is not None:
            break

    print("External block")
    print("-" * 60)

    print(f"Block size : {len(external_block)}")

    print()

    for row in external_block:

        print(

            row["simulation_id"],

            row["signature"],

        )

    print()
    print("=" * 60)
    print("STATUS : EXTERNAL PARTITION LOCATED")
    print("=" * 60)


if __name__ == "__main__":

    main()
