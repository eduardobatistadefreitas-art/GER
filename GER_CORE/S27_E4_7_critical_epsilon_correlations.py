# ============================================================
# GER
#
# S27-E4.7
#
# Critical Epsilon Correlations
#
# Investiga correlações entre o epsilon crítico
# e os demais observáveis da assinatura.
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


def correlation(x, y):

    if len(x) < 2:
        return np.nan

    return np.corrcoef(x, y)[0, 1]


def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.7")
    print("Critical Epsilon Correlations")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    eps = []

    diameter = []
    convergence = []
    drift = []

    beta = []
    sigma = []

    for row in results:

        if row["signature"].recurrence != 0.0:
            continue

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

        e = find_critical_epsilon(
            trajectory
        )

        if e is None:
            continue

        s = row["signature"]

        eps.append(e)
        diameter.append(s.diameter)
        convergence.append(s.convergence)
        drift.append(s.drift)
        beta.append(row["beta"])
        sigma.append(row["sigma"])

    print("Pearson correlations")
    print("-" * 40)

    print(f"Diameter     : {correlation(eps, diameter): .6f}")
    print(f"Convergence  : {correlation(eps, convergence): .6f}")
    print(f"Drift        : {correlation(eps, drift): .6f}")
    print(f"Beta         : {correlation(eps, beta): .6f}")
    print(f"Sigma        : {correlation(eps, sigma): .6f}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
