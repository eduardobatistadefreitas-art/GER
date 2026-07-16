# ============================================================
# GER
#
# S27-R6.2
#
# Modal Representation
#
# Computes the modal representation of the first
# external Double Pendulum trajectory.
# ============================================================

import numpy as np

from GER_CORE.S27_R6_1_double_pendulum_state import (
    generate_double_pendulum_state,
)

from GER.CORE.ger_modal import (
    modal_projection,
)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R6.2")
    print("Modal Representation")
    print("=" * 60)
    print()

    gamma = generate_double_pendulum_state()

    eigenvectors = (

        np.fft.fft(
            np.eye(len(gamma))
        )

        / np.sqrt(len(gamma))

    )

    coefficients = modal_projection(

        gamma,

        eigenvectors,

    )

    print("Modal coefficients")
    print("-" * 60)

    print(f"Modes      : {len(coefficients)}")

    print(
        f"L2 norm    : "
        f"{np.linalg.norm(coefficients):.6f}"
    )

    dominant = np.argmax(
        np.abs(coefficients)
    )

    print(f"Peak mode  : {dominant}")

    print(
        f"Peak value : "
        f"{np.abs(coefficients[dominant]):.6f}"
    )

    energy = np.sum(
        np.abs(coefficients) ** 2
    )

    print(
        f"Modal energy : {energy:.6f}"
    )

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":

    main()
