# ============================================================
# GER
#
# S27-R3.8
#
# Observational Partition
#
# Inserts the external Van der Pol Oscillator into
# the observational universe and computes the
# induced partition using the recurrence operator.
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

# ============================================================
# Parameters
# ============================================================

MU = 1.0

DT = 0.01

NSTEPS = 5000

N_SNAPSHOTS = 50


# ============================================================
# External Signature
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

    return Signature(

        diameter=compute_confinement(
            trajectory
        ),

        convergence=compute_convergence(
            trajectory,
            1.0,
        ),

        recurrence=compute_recurrence(
            trajectory
        ),

        drift=compute_drift(
            trajectory
        )[0],

    )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R3.8")
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

    block = partition.block_of(
        signature
    )

    print("External block")
    print("-" * 60)

    print(
        f"Block size : {len(block)}"
    )

    print()

    for element in block:

        print(element)

    print()

    print("=" * 60)
    print("STATUS : PARTITION GENERATED")
    print("=" * 60)


if __name__ == "__main__":

    main()
