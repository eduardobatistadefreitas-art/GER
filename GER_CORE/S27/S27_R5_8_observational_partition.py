# ============================================================
# GER
#
# S27-R5.8
#
# Observational Partition
#
# Inserts the external Lorenz signature into
# the observational universe and computes the
# induced partition.
# ============================================================

from copy import deepcopy

from GER.CORE.partition_builder import build_partition

from GER.CORE.signature_api import Signature

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

from GER_CORE.S27_R5_5_geometric_signature import (
    generate_snapshots,
)


# ============================================================
# Signature
# ============================================================

def generate_signature():

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
    print("S27-R5.8")
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
