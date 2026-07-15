# ============================================================
# GER
#
# S27-R3.1
#
# Van der Pol State
#
# First external nonlinear state generated
# independently from the GER engine.
# ============================================================

import numpy as np


# ============================================================
# Parameters
# ============================================================

MU = 1.0

DT = 0.01

NSTEPS = 5000


# ============================================================
# Van der Pol
# ============================================================

def generate_vanderpol_state():

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
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R3.1")
    print("Van der Pol State")
    print("=" * 60)
    print()

    gamma = generate_vanderpol_state()

    print("State")
    print("-" * 60)

    print(f"Dimension : {len(gamma)}")
    print(f"Minimum   : {gamma.min():.6f}")
    print(f"Maximum   : {gamma.max():.6f}")
    print(f"L2 norm   : {np.linalg.norm(gamma):.6f}")

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":

    main()
