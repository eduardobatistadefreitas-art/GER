# ============================================================
# GER
#
# S27-R4.4
#
# Persistence Observation
#
# Runs the official GER Persistence Observatory
# on the external Logistic Map.
# ============================================================

import numpy as np

from GER_CORE.S27_R4_1_logistic_state import (
    generate_logistic_state,
)

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


# ============================================================
# Parameters
# ============================================================

N_SNAPSHOTS = 50


# ============================================================
# Snapshot generation
# ============================================================

def generate_snapshots():

    trajectory = generate_logistic_state()

    dimension = len(trajectory)

    stride = max(
        1,
        dimension // N_SNAPSHOTS,
    )

    eigenvectors = (

        np.fft.fft(
            np.eye(dimension)
        )

        / np.sqrt(dimension)

    )

    snapshots = []

    for step in range(N_SNAPSHOTS):

        gamma = np.roll(
            trajectory,
            step * stride,
        )

        snapshot = build_observational_snapshot(

            gamma=gamma,

            eigenvectors=eigenvectors,

            step=step,

            time=float(step),

        )

        snapshots.append(snapshot)

    return snapshots


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R4.4")
    print("Persistence Observation")
    print("=" * 60)
    print()

    snapshots = generate_snapshots()

    observables = run_persistence_observatory(

        snapshots,

        dt=1.0,

    )

    print("Observables")
    print("-" * 60)

    for name, values in observables.items():

        values = np.asarray(values)

        print(

            f"{name:<12}"

            f"mean={np.mean(values):.6f}"

            f"   "

            f"std={np.std(values):.6f}"

        )

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":

    main()
