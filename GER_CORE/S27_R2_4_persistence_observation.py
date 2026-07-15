# ============================================================
# GER
#
# S27-R2.4
#
# Persistence Observation
#
# Runs the official GER Persistence Observatory
# on the external Damped Oscillator.
# ============================================================

import numpy as np

from GER_CORE.S27_R2_1_damped_state import (
    generate_damped_state,
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

DT = 1.0


# ============================================================
# Snapshot generation
# ============================================================

def generate_snapshots():

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

    return snapshots


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R2.4")
    print("Persistence Observation")
    print("=" *
