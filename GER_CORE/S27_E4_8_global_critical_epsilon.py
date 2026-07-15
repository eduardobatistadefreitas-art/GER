# ============================================================
# GER
#
# S27-E4.8
#
# Global Critical Epsilon
#
# Calcula o epsilon crítico para todas as assinaturas
# produzidas pelo Geometry Scan.
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

                    return fine

        previous = factor

    return None


def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.8")
    print("Global Critical Epsilon")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    eps_values = []

    print(
        f"{'ID':<4}"
        f"{'eps*':>8}"
        f"{'R0':>10}"
        f"{'Beta':>8}"
        f"{'Sigma':>8}"
        f"{'Pot':>6}"
    )

    print("-" * 48)

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

        trajectory = build_trajectory(
            observables
        )

        eps = find_critical_epsilon(
            trajectory
        )

        if eps is None:
            continue

        eps_values.append(eps)

        print(
            f"{row['simulation_id']:02d}"
            f"{eps:8.3f}"
            f"{row['signature'].recurrence:10.6f}"
            f"{row['beta']:8.2f}"
            f"{row['sigma']:8.2f}"
            f"{str(row['potential']):>6}"
        )

    print()

    print("=" * 60)
    print("Statistics")
    print("=" * 60)

    print(f"Count : {len(eps_values)}")
    print(f"Mean  : {np.mean(eps_values):.4f}")
    print(f"Std   : {np.std(eps_values):.4f}")
    print(f"Min   : {np.min(eps_values):.4f}")
    print(f"Max   : {np.max(eps_values):.4f}")

    print("=" * 60)


if __name__ == "__main__":
    main()
