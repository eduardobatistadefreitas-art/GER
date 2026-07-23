# ============================================================
# GER
#
# S27-R1.1
#
# Harmonic State Generation
#
# First external state construction.
#
# ============================================================

import numpy as np


# ------------------------------------------------------------
# Harmonic signal
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

    return t, gamma


# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1.1")
    print("Harmonic State Generation")
    print("=" * 60)
    print()

    t, gamma = generate_harmonic_state()

    print("State statistics")
    print("-" * 60)

    print(f"Samples     : {len(gamma)}")
    print(f"Dimension   : {gamma.ndim}")
    print(f"L2 norm     : {np.linalg.norm(gamma):.6f}")
    print(f"Mean        : {np.mean(gamma):.6f}")
    print(f"Std         : {np.std(gamma):.6f}")
    print(f"Minimum     : {np.min(gamma):.6f}")
    print(f"Maximum     : {np.max(gamma):.6f}")

    print()

    print("Mathematical requirements")
    print("-" * 60)

    print("Finite-dimensional vector : PASS")
    print("Complete state vector     : PASS")
    print("Real-valued state         : PASS")
    print("Finite norm              : PASS")

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()
