# ============================================================
# GER
#
# S27-E5.2
#
# Lattice Generating Basis
#
# Determina a menor base capaz de reproduzir
# todas as partições distintas observadas na S27.
# ============================================================

import itertools
import numpy as np

from GER.CORE.partition_builder import build_partition
from GER.CORE.partition_algebra import meet

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
    build_trajectory,
    compute_recurrence,
)


COARSE = np.arange(0.01, 0.201, 0.01)


def find_critical_epsilon(trajectory):

    sigma = np.std(trajectory)

    previous = COARSE[0]

    for factor in COARSE:

        r = compute_recurrence(
            trajectory,
            epsilon=factor * sigma,
        )

        if r > 0:

            for fine in np.arange(
                previous,
                factor + 0.001,
                0.001,
            ):

                rr = compute_recurrence(
                    trajectory,
                    epsilon=fine * sigma,
                )

                if rr > 0:
                    return round(fine, 3)

        previous = factor

    return None


def same_partition(A, B):

    return set(A.blocks) == set(B.blocks)


def main():

    print("=" * 60)
    print("GER")
    print("S27-E5.2")
    print("Lattice Generating Basis")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    signatures = [r["signature"] for r in results]

    eps_map = {}

    for row in results:

        result = run_engine(
            beta=row["beta"],
            sigma=row["sigma"],
            potential=row["potential"],
            timesteps=2000,
            dt=row["dt"],
        )

        observables = run_persistence_observatory(
            result["snapshots"],
            result["configuration"]["dt"],
        )

        trajectory = build_trajectory(observables)

        eps_map[row["simulation_id"]] = find_critical_epsilon(
            trajectory
        )

    signature_to_eps = {
        row["signature"]: eps_map[row["simulation_id"]]
        for row in results
    }

    operators = {

        "D":
            lambda s: s.diameter,

        "C":
            lambda s: s.convergence,

        "R":
            lambda s: s.recurrence,

        "Drift":
            lambda s: s.drift,

        "Eps":
            lambda s: signature_to_eps[s],

    }

    partitions = {}

    for name, op in operators.items():

        partitions[name] = build_partition(
            signatures,
            key=op,
        )

    distinct = []

    distinct_names = []

    for name in partitions:

        already = False

        for P in distinct:

            if same_partition(
                partitions[name],
                P,
            ):
                already = True
                break

        if not already:

            distinct.append(
                partitions[name]
            )

            distinct_names.append(name)

    print(
        "Distinct lattice generators:",
        distinct_names,
    )

    print()

    print(
        "Number of independent partitions:",
        len(distinct),
    )

    print()

    print("Minimal generating bases")
    print("-" * 40)

    names = distinct_names

    for k in range(1, len(names)+1):

        for subset in itertools.combinations(names, k):

            print(subset)

        break

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
