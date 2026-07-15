# ============================================================
# GER
#
# S27-R1.8
#
# Observational Partition
#
# First observational partition containing
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
# Harmonic snapshots
# ============================================================

def generate_harmonic_signature():

    basis = (

        np.fft.fft(
            np.eye(2048)
        )

        / np.sqrt(2048)

    )

    theta = np.linspace(

        0,

        2 * np.pi,

        2048,

        endpoint=False,

    )

    snapshots = []

    for step in range(50):

        phase = (

            2 * np.pi * step

            / 50

        )

        gamma = np.cos(

            theta + phase

        )

        snapshots.append(

            build_observational_snapshot(

                gamma=gamma,

                eigenvectors=basis,

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

    drift, _ = compute_drift(

        trajectory

    )

    return Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )


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

    results = run_geometry_scan()

    signatures = [

        row["signature"]

        for row in results

    ]

    external = generate_harmonic_signature()

    signatures.append(

        external

    )

    print(f"Universe size : {len(signatures)}")
    print()

    partition = build_partition(

        universe=signatures,

        key=lambda s: round(

            s.recurrence,

            6,

        ),

    )

    print(f"Number of blocks : {len(partition)}")
    print()

    block = partition.block_of(

        external

    )

    print("External block")
    print("-" * 60)

    print(f"Block size : {len(block)}")
    print()

    for signature in block:

        print(signature)

    print()
    print("=" * 60)
    print("STATUS : PARTITION GENERATED")
    print("=" * 60)


if __name__ == "__main__":

    main()
