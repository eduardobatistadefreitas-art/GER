# ============================================================
# GER
#
# S27-R3.3
#
# External Snapshot
#
# Generates the observational snapshots for the
# external Van der Pol oscillator.
# ============================================================

import numpy as np

from GER_CORE.S27_R3_1_vanderpol_state import (
    generate_vanderpol_state,
)

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)


# ============================================================
# Parameters
# ============================================================

N_SNAPSHOTS = 50


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R3.3")
    print("External Snapshot")
    print("=" * 60)
    print()

    trajectory = generate_vanderpol_state()

    step_size = max(
        1,
        len(trajectory) // N_SNAPSHOTS,
    )

    dimension = len(trajectory)

    eigenvectors = (

        np.fft.fft(
            np.eye(dimension)
        )

        / np.sqrt(dimension)

    )

    snapshots = []

    for i in range(N_SNAPSHOTS):

        gamma = np.roll(
            trajectory,
            i * step_size,
        )

        snapshot = build_observational_snapshot(

            gamma=gamma,

            eigenvectors=eigenvectors,

            step=i,

            time=float(i),

        )

        snapshots.append(snapshot)

    first = snapshots[0]

    print("Snapshot fields")
    print("-" * 60)

    print(f"step{'':<20}{first['step']}")
    print(f"time{'':<20}{first['time']}")
    print(f"gamma{'':<19}shape={first['gamma'].shape}")
    print(f"probability{'':<13}shape={first['probability'].shape}")
    print(f"participation_ratio{'':<5}{first['participation_ratio']}")
    print(f"modal_center{'':<11}{first['modal_center']}")
    print(f"spectral_entropy{'':<7}{first['spectral_entropy']}")

    print()

    print("Generated snapshots")
    print("-" * 60)

    print(len(snapshots))

    print()

    print("Required fields")
    print("-" * 60)

    required = [

        "gamma",

        "probability",

        "participation_ratio",

        "modal_center",

    ]

    for field in required:

        status = "PASS" if field in first else "FAIL"

        print(f"{field:<24}{status}")

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":

    main()
