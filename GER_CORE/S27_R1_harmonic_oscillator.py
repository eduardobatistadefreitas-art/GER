# ============================================================
# GER
#
# S27-R1
#
# Harmonic Oscillator
#
# First external validation experiment.
#
# The GER framework is used without modification.
# ============================================================

import numpy as np

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (
    build_trajectory,
    compute_confinement,
    compute_convergence,
    compute_recurrence,
    compute_drift,
    Signature,
)


def generate_harmonic_oscillator(

    omega=1.0,
    amplitude=1.0,
    timesteps=2000,
    dt=2.5e-4,

):

    t = np.arange(timesteps) * dt

    x = amplitude * np.cos(omega * t)

    v = -amplitude * omega * np.sin(omega * t)

    snapshots = []

    for xi, vi in zip(x, v):

        snapshots.append(

            {

                "gamma": np.array([xi]),

                "velocity": np.array([vi]),

            }

        )

    return snapshots


def main():

    print("=" * 60)
    print("GER")
    print("S27-R1")
    print("Harmonic Oscillator")
    print("=" * 60)
    print()

    dt = 2.5e-4

    snapshots = generate_harmonic_oscillator(
        dt=dt
    )

    observables = run_persistence_observatory(
        snapshots,
        dt,
    )

    trajectory = build_trajectory(
        observables
    )

    diameter = compute_confinement(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        dt,
    )

    recurrence = compute_recurrence(
        trajectory
    )

    drift, length = compute_drift(
        trajectory
    )

    signature = Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )

    print("Signature")
    print("-" * 60)

    print(f"Diameter    : {signature.diameter:.6f}")
    print(f"Convergence : {signature.convergence:.6f}")
    print(f"Recurrence  : {signature.recurrence:.6f}")
    print(f"Drift       : {signature.drift:.6f}")

    print()

    print("=" * 60)
    print("STATUS : EXTERNAL OBSERVATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
