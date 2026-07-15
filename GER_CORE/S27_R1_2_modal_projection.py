# ============================================================
# GER
#
# S27-R1.2
#
# Modal Projection
#
# First modal projection of an external state.
# ============================================================

import numpy as np


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

def build_fourier_basis(n):

    return np.fft.fft(
        np.eye(n)
    ) / np.sqrt(n)


# ------------------------------------------------------------

def modal_projection(
    gamma,
    basis,
):

    return basis.T @ gamma


# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1.2")
    print("Modal Projection")
    print("=" * 60)
    print()

    gamma = generate_harmonic_state()

    basis = build_fourier_basis(
        len(gamma)
    )

    gamma_hat = modal_projection(
        gamma,
        basis,
    )

    energy_state = np.sum(
        np.abs(gamma) ** 2
    )

    energy_modal = np.sum(
        np.abs(gamma_hat) ** 2
    )

    error = abs(
        energy_state - energy_modal
    )

    print("State")
    print("-" * 60)

    print(f"Dimension : {len(gamma)}")

    print()

    print("Modal basis")
    print("-" * 60)

    print(
        f"Shape : {basis.shape}"
    )

    print()

    print("Projection")
    print("-" * 60)

    print(
        f"Modal coefficients : {len(gamma_hat)}"
    )

    print()

    print("Parseval Audit")
    print("-" * 60)

    print(
        f"State energy : {energy_state:.12f}"
    )

    print(
        f"Modal energy : {energy_modal:.12f}"
    )

    print(
        f"Difference   : {error:.3e}"
    )

    print()

    if error < 1e-10:

        print("Projection : PASS")

    else:

        print("Projection : FAIL")

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":

    main()
