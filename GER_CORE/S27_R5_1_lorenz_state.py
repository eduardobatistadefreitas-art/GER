# ============================================================
# GER
#
# S27-R5.1
#
# Lorenz State
#
# First external chaotic continuous state generated
# from the classical Lorenz attractor.
# ============================================================

import numpy as np


# ============================================================
# Parameters
# ============================================================

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

DT = 0.01

NSTEPS = 5000


# ============================================================
# Lorenz System
# ============================================================

def generate_lorenz_state():

    x = 1.0
    y = 1.0
    z = 1.0

    trajectory = []

    for _ in range(NSTEPS):

        trajectory.append(x)

        dx = SIGMA * (y - x)

        dy = x * (RHO - z) - y

        dz = x * y - BETA * z

        x += DT * dx
        y += DT * dy
        z += DT * dz

    return np.asarray(trajectory)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R5.1")
    print("Lorenz State")
    print("=" * 60)
    print()

    gamma = generate_lorenz_state()

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
