# ============================================================
# GER
#
# S27-R2.8
#
# Observational Partition
#
# Inserts the external Damped Oscillator into the
# observational universe and computes the induced
# partition using the recurrence observable.
# ============================================================

from copy import deepcopy

import numpy as np

from GER.CORE.signature_api import Signature

from GER.CORE.partition_builder import build_partition

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


OMEGA = 1.0
GAMMA = 0.15

DIMENSION = 2048
N_SNAPSHOTS = 50
DT = 1.0


def generate_signature():

    eigenvectors = (
        np.fft.fft(
            np.eye(DIMENSION)
        ) / np.sqrt(DIMENSION)
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

    return Signature(

        diameter=compute_confinement(
            trajectory
        ),

        convergence=compute_convergence(
            trajectory,
            DT,
        ),

        recurrence=compute_recurrence(
            trajectory
        ),

        drift=compute_drift(
            trajectory
        )[0],

    )


def main():

    print("=" * 60)
    print("GER")
    print("S27-R2.8")
    print("Observational Partition")
    print("=" * 60)
    print()

    universe = deepcopy(
        run_geometry_scan()
    )

    signature = generate_signature()

    universe.append({

        "simulation_id": "EXTERNAL",

        "signature": signature,

    })

    signatures = [

        row["signature"]

        for row in universe

    ]

    partition = build_partition(

        universe=signatures,

        key=lambda s: s.recurrence,

    )

    print(
        f"Universe size : {len(signatures)}"
    )

    print()

    print(
        f"Number of blocks : {len(partition.blocks)}"
    )

    print()

    external = signature

    block = partition.block_of(
        external
    )

    print("External block")
    print("-" * 60)

    print(
        f"Block size : {len(block)}"
    )

    print()

    for s in block:

        print(s)

    print()

    print("=" * 60)
    print("STATUS : PARTITION GENERATED")
    print("=" * 60)


if __name__ == "__main__":

    main()
