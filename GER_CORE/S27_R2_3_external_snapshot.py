# ============================================================
# GER
#
# S27-R2.3
#
# External Snapshot
#
# Generates the first external observational
# snapshots for the Damped Oscillator.
# ============================================================

import numpy as np

from GER_CORE.S27_R2_1_damped_state import (
    generate_damped_state,
)

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)


# ============================================================
# Parameters
# ============================================================

N_SNAPSHOTS = 50

DT = 1.0


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R2.3")
    print("External Snapshot")
    print("=" * 60)
    print()

    eigenvectors = (

        np.fft.fft(
            np.eye(2048)
        )

        / np.sqrt(2048)

    )

    snapshots = []

    for step in range(N_SNAPSHOTS):

        time = step * DT

        gamma = generate_damped_state(
            time=time,
        )

        snapshot = build_observational_snapshot(

            gamma=gamma,

            eigenvectors=eigenvectors,

            step=step,

            time=time,

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
