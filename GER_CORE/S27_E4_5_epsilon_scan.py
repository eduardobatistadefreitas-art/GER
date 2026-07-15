# ============================================================
# GER
#
# S27-E4.5
#
# Epsilon Scan
#
# Mede a robustez da recorrência em função
# do parâmetro epsilon.
# ============================================================

import numpy as np

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
    build_trajectory,
    compute_recurrence,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER.CORE.ger_engine import run_engine


EPS_FACTORS = [
    0.01,
    0.02,
    0.05,
    0.10,
    0.20,
]


def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.5")
    print("Epsilon Scan")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    zero_cases = [

        row

        for row in results

        if row["signature"].recurrence == 0.0

    ]

    print(f"Zero-recurrence signatures : {len(zero_cases)}")
    print()

    header = "ID".ljust(4)

    for f in EPS_FACTORS:

        header += f"{f:>10.2f}"

    print(header)

    print("-" * len(header))

    robust = 0

    for row in zero_cases:

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

        sigma = np.std(trajectory)

        values = []

        for factor in EPS_FACTORS:

            r = compute_recurrence(
                trajectory,
                epsilon=factor * sigma,
            )

            values.append(r)

        line = f"{row['simulation_id']:02d}"

        still_zero = True

        for r in values:

            line += f"{r:10.6f}"

            if r != 0.0:
                still_zero = False

        print(line)

        if still_zero:
            robust += 1

    print()
    print("=" * 60)
    print(f"Robustly zero : {robust}/{len(zero_cases)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
