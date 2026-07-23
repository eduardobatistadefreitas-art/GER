# ============================================================
# GER
#
# S27-E4.6
#
# Critical Epsilon
#
# Determina o menor epsilon para o qual
# a recorrência torna-se positiva.
# ============================================================

import numpy as np

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
    build_trajectory,
    compute_recurrence,
)


COARSE = [
    0.050,
    0.060,
    0.070,
    0.080,
    0.090,
    0.100,
]


def find_critical_epsilon(trajectory):

    sigma = np.std(trajectory)

    previous = COARSE[0]

    for factor in COARSE:

        r = compute_recurrence(
            trajectory,
            epsilon=factor * sigma,
        )

        if r > 0:

            start = previous
            stop = factor

            for fine in np.arange(
                start,
                stop + 0.001,
                0.001,
            ):

                rr = compute_recurrence(
                    trajectory,
                    epsilon=fine * sigma,
                )

                if rr > 0:

                    return fine, rr

        previous = factor

    return None, 0.0


def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.6")
    print("Critical Epsilon")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    zeros = [

        row

        for row in results

        if row["signature"].recurrence == 0.0

    ]

    eps_values = []

    print(
        f"{'ID':<4}"
        f"{'eps*':>10}"
        f"{'R':>12}"
    )

    print("-" * 28)

    for row in zeros:

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

        trajectory = build_trajectory(
            observables
        )

        eps, r = find_critical_epsilon(
            trajectory
        )

        if eps is not None:

            eps_values.append(eps)

            print(
                f"{row['simulation_id']:02d}"
                f"{eps:10.3f}"
                f"{r:12.6f}"
            )

    print()

    print("=" * 60)

    if eps_values:

        print(
            f"Mean : {np.mean(eps_values):.4f}"
        )

        print(
            f"Std  : {np.std(eps_values):.4f}"
        )

        print(
            f"Min  : {np.min(eps_values):.4f}"
        )

        print(
            f"Max  : {np.max(eps_values):.4f}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
