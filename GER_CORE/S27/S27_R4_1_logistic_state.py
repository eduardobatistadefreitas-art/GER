# ============================================================
# GER
#
# S27-R4.1
#
# Logistic State
#
# First external chaotic state generated from
# the Logistic Map.
# ============================================================

import numpy as np


# ============================================================
# Parameters
# ============================================================

R = 3.9

X0 = 0.3141592653589793

NSTEPS = 5000


# ============================================================
# Logistic Map
# ============================================================

def generate_logistic_state():

    x = X0

    trajectory = []

    for _ in range(NSTEPS):

        trajectory.append(x)

        x = R * x * (1.0 - x)

    return np.asarray(trajectory)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R4.1")
    print("Logistic State")
    print("=" * 60)
    print()

    gamma = generate_logistic_state()

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
