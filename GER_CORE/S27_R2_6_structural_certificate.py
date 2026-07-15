# ============================================================
# GER
#
# S27-R2.6
#
# Structural Certificate
#
# First external Structural Certificate
# generated for the Damped Oscillator.
# ============================================================

import numpy as np

from GER.CORE.signature_api import (
    Signature,
)

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

OMEGA = 1.0
GAMMA = 0.15

DIMENSION = 2048

N_SNAPSHOTS = 50

DT = 1.0


# ============================================================
# Damped oscillator
# ============================================================

def generate_state(time):

    theta = np.linspace(

        0.0,

        2.0 * np.pi,

        DIMENSION,

        endpoint=False,

    )

    amplitude = np.exp(

        -GAMMA * time

    )

    return amplitude * np.cos(

        theta + OMEGA * time

    )


# ============================================================
# Signature
# ============================================================

def generate_signature():

    eigenvectors = (

        np.fft.fft(

            np.eye(DIMENSION)

        )

        / np.sqrt(DIMENSION)

    )

    snapshots = []

    for step in range(N_SNAPSHOTS):

        t = step * DT

        gamma = generate_state(t)

        snapshots.append(

            build_observational_snapshot(

                gamma=gamma,

                eigenvectors=eigenvectors,

                step=step,

                time=t,

            )

        )

    observables = run_persistence_observatory(

        snapshots,

        DT,

    )

    trajectory = build_trajectory(

        observables

    )

    diameter = compute_confinement(

        trajectory

    )

    convergence = compute_convergence(

        trajectory,

        DT,

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
    print("S27-R2.6")
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
    print("STATUS : FIRST DAMPED STRUCTURAL CERTIFICATE")
    print("=" * 60)


if __name__ == "__main__":

    main()
