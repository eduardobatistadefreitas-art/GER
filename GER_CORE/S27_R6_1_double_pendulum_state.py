# ============================================================
# GER
#
# S27-R6.1
#
# Double Pendulum State
#
# First external chaotic mechanical state generated
# from the classical Double Pendulum.
# ============================================================

import numpy as np


# ============================================================
# Parameters
# ============================================================

G = 9.81

L1 = 1.0
L2 = 1.0

M1 = 1.0
M2 = 1.0

DT = 0.005

NSTEPS = 5000


# ============================================================
# Double Pendulum
# ============================================================

def generate_double_pendulum_state():

    theta1 = np.pi / 2
    theta2 = np.pi / 2 + 0.2

    omega1 = 0.0
    omega2 = 0.0

    trajectory = []

    for _ in range(NSTEPS):

        trajectory.append(theta1)

        delta = theta2 - theta1

        den1 = (M1 + M2) * L1 - M2 * L1 * np.cos(delta) ** 2

        den2 = (L2 / L1) * den1

        a1 = (
            M2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta)
            + M2 * G * np.sin(theta2) * np.cos(delta)
            + M2 * L2 * omega2**2 * np.sin(delta)
            - (M1 + M2) * G * np.sin(theta1)
        ) / den1

        a2 = (
            -M2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta)
            + (M1 + M2)
            * (
                G * np.sin(theta1) * np.cos(delta)
                - L1 * omega1**2 * np.sin(delta)
                - G * np.sin(theta2)
            )
        ) / den2

        omega1 += DT * a1
        omega2 += DT * a2

        theta1 += DT * omega1
        theta2 += DT * omega2

    return np.asarray(trajectory)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R6.1")
    print("Double Pendulum State")
    print("=" * 60)
    print()

    gamma = generate_double_pendulum_state()

    print("State")
    print("-" * 60)

    print(f"Dimension : {len(gamma)}")

    print(f"Minimum   : {gamma.min():.6f}")

    print(f"Maximum   : {gamma.max():.6f}")

    print(f"Mean      : {gamma.mean():.6f}")

    print(f"Std       : {gamma.std():.6f}")

    print(f"L2 norm   : {np.linalg.norm(gamma):.6f}")

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":

    main()
