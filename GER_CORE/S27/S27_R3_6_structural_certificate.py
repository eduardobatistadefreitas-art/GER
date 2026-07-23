# ============================================================
# GER
#
# S27-R3.6
#
# Structural Certificate
#
# First external Structural Certificate
# generated for the Van der Pol Oscillator.
# ============================================================

import numpy as np

from GER.CORE.signature_api import Signature

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (
    build_trajectory,
    compute_confinement,
    compute_convergence,
    compute_recurrence,
    compute_drift,
)

from GER_CORE.S26_B36_stationary_scan import (
    stationary_scan,
)


# ============================================================
# Parameters
# ============================================================

MU = 1.0

DT = 0.01

NSTEPS = 5000

N_SNAPSHOTS = 50


# ============================================================
# Van der Pol trajectory
# ============================================================

def generate_trajectory():

    x = 1.0
    y = 0.0

    trajectory = []

    for _ in range(NSTEPS):

        trajectory.append(x)

        dx = y
        dy = MU * (1.0 - x**2) * y - x

        x += DT * dx
        y += DT * dy

    return np.asarray(trajectory)


# ============================================================
# Signature generation
# ============================================================

def generate_signature():

    trajectory = generate_trajectory()

    dimension = len(trajectory)

    step_size = max(
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
            step * step_size,
        )

        snapshots.append(

            build_observational_snapshot(

                gamma=gamma,

                eigenvectors=eigenvectors,

                step=step,

                time=float(step),

            )

        )

    observables = run_persistence_observatory(

        snapshots,

        dt=1.0,

    )

    trajectory = build_trajectory(
        observables
    )

    diameter = compute_confinement(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        1.0,
    )

    recurrence = compute_recurrence(
        trajectory
    )

    drift, _ = compute_drift(
        trajectory
    )

    return Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R3.6")
    print("Structural Certificate")
    print("=" * 60)
    print()

    signature = generate_signature()

    certificate = stationary_scan(
        signature
    )

    print("Signature")
    print("-" * 60)

    print(signature)

    print()

    print("Certificate summary")
    print("-" * 60)

    print(
        certificate["summary"]
    )

    print()

    print("Deductions")
    print("-" * 60)

    for deduction in certificate["deductions"]:

        print(deduction)

    print()

    print("=" * 60)
    print("STATUS : FIRST VAN DER POL STRUCTURAL CERTIFICATE")
    print("=" * 60)


if __name__ == "__main__":

    main()
