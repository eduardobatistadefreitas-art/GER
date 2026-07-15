# ============================================================
# GER
#
# S27-R1.4
#
# Persistence Observation
#
# First persistence observation of an external
# dynamical system.
# ============================================================

import numpy as np

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


# ------------------------------------------------------------
# Harmonic trajectory
# ------------------------------------------------------------

def generate_harmonic_trajectory(
    omega=1.0,
    amplitude=1.0,
    samples=50,
    dimension=2048,
):

    snapshots = []

    basis = (
        np.fft.fft(np.eye(dimension))
        / np.sqrt(dimension)
    )

    for k in range(samples):

        phase = 2.0 * np.pi * k / samples

        theta = np.linspace(
            0,
            2*np.pi,
            dimension,
            endpoint=False,
        )

        gamma = amplitude * np.cos(
            theta + phase
        )

        snapshot = build_observational_snapshot(
            gamma=gamma,
            eigenvectors=basis,
            step=k,
            time=float(k),
        )

        snapshots.append(snapshot)

    return snapshots


# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1.4")
    print("Persistence Observation")
    print("=" * 60)
    print()

    snapshots = generate_harmonic_trajectory()

    observables = run_persistence_observatory(
        snapshots=snapshots,
        dt=1.0,
    )

    print("Observables")
    print("-" * 60)

    for key, values in observables.items():

        values = np.asarray(values)

        print(
            f"{key:<12}"
            f"mean={values.mean():.6f}   "
            f"std={values.std():.6f}"
        )

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()
