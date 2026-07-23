# ============================================================
# GER
#
# S27-R1.3
#
# External Snapshot
#
# First observational snapshot generated from
# an external dynamical system.
# ============================================================

import numpy as np

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)


# ------------------------------------------------------------
# Harmonic state
# ------------------------------------------------------------

def generate_harmonic_state(
    omega=1.0,
    amplitude=1.0,
    samples=2048,
    dt=1e-3,
):

    t = np.arange(samples) * dt

    gamma = amplitude * np.cos(
        omega * t
    )

    return gamma


# ------------------------------------------------------------
# Fourier basis
# ------------------------------------------------------------

def build_fourier_basis(n):

    return (
        np.fft.fft(np.eye(n))
        / np.sqrt(n)
    )


# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1.3")
    print("External Snapshot")
    print("=" * 60)
    print()

    gamma = generate_harmonic_state()

    basis = build_fourier_basis(
        len(gamma)
    )

    snapshot = build_observational_snapshot(
        gamma=gamma,
        eigenvectors=basis,
        step=0,
        time=0.0,
    )

    print("Snapshot fields")
    print("-" * 60)

    for key, value in snapshot.items():

        if np.isscalar(value):

            print(
                f"{key:<24}{value}"
            )

        else:

            print(
                f"{key:<24}"
                f"shape={np.shape(value)}"
            )

    print()

    print("Required fields")
    print("-" * 60)

    required = [

        "gamma",
        "probability",
        "participation_ratio",
        "modal_center",

    ]

    ok = True

    for field in required:

        exists = field in snapshot

        print(
            f"{field:<24}"
            f"{'PASS' if exists else 'FAIL'}"
        )

        ok &= exists

    print()

    print("=" * 60)

    if ok:

        print("STATUS : PASS")

    else:

        print("STATUS : FAIL")

    print("=" * 60)


if __name__ == "__main__":

    main()
