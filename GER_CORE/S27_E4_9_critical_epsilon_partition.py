# ============================================================
# GER
#
# S27-E4.9
#
# Critical Epsilon Partition
#
# Constrói a partição induzida pelo epsilon crítico
# e compara sua posição no reticulado com os demais
# observáveis.
# ============================================================

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


def same_partition(P, Q):

    return set(P.blocks) == set(Q.blocks)


def relation(PA, PB):

    M = meet(PA, PB)

    if same_partition(M, PA) and same_partition(M, PB):
        return "="

    if same_partition(M, PA):
        return "<="

    if same_partition(M, PB):
        return ">="

    return "?"


def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.9")
    print("Critical Epsilon Partition")
    print("=" * 60)
    print()

    results = run_geometry_scan()

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

    signatures = [r["signature"] for r in results]

    P_D = build_partition(
        signatures,
        key=lambda s: s.diameter,
    )

    P_C = build_partition(
        signatures,
        key=lambda s: s.convergence,
    )

    P_R = build_partition(
        signatures,
        key=lambda s: s.recurrence,
    )

    P_Drift = build_partition(
        signatures,
        key=lambda s: s.drift,
    )

    P_Eps = build_partition(
        results,
        key=lambda row: eps_map[row["simulation_id"]],
    )

    partitions = {
        "D": P_D,
        "C": P_C,
        "R": P_R,
        "Drift": P_Drift,
        "Eps*": P_Eps,
    }

    print(f"{'Partition':<10}{'Blocks':>8}")
    print("-" * 20)

    for name, part in partitions.items():

        print(
            f"{name:<10}"
            f"{len(part.blocks):>8}"
        )

    print()
    print("=" * 60)
    print("Relations")
    print("=" * 60)

    names = list(partitions.keys())

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            A = names[i]
            B = names[j]

            print(
                f"{A:<10}"
                f"{relation(partitions[A], partitions[B]):^6}"
                f"{B}"
            )


if __name__ == "__main__":
    main()
