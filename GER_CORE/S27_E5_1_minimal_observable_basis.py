# ============================================================
# GER
#
# S27-E5.1
#
# Minimal Observable Basis
#
# Determina quais observáveis são realmente
# independentes na estrutura de partições.
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


def same_partition(P, Q):

    return set(P.blocks) == set(Q.blocks)


def combined_partition(signatures, observables):

    P = None

    for obs in observables:

        Pi = build_partition(
            signatures,
            key=obs,
        )

        if P is None:
            P = Pi
        else:
            P = meet(P, Pi)

    return P


def main():

    print("=" * 60)
    print("GER")
    print("S27-E5.1")
    print("Minimal Observable Basis")
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

    full = combined_partition(
        signatures,
        operators.values(),
    )

    print(
        "Full partition blocks:",
        len(full.blocks),
    )

    print()

    print("Candidate bases")
    print("-" * 40)

    found = False

    names = list(operators.keys())

    for k in range(1, len(names) + 1):

        for subset in itertools.combinations(names, k):

            P = combined_partition(

                signatures,

                [
                    operators[name]
                    for name in subset
                ],

            )

            if same_partition(P, full):

                print(
                    subset,
                    "->",
                    len(P.blocks),
                    "blocks",
                )

                found = True

        if found:
            break

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
