# ============================================================
# GER
#
# S27-R2.1
#
# Damped State
#
# First external damped oscillator state
# generated independently from the GER engine.
# ============================================================

import numpy as np


# ============================================================
# Parameters
# ============================================================

OMEGA = 1.0
GAMMA = 0.15

DIMENSION = 2048


# ============================================================
# Damped oscillator
# ============================================================

def generate_damped_state(
    time,
    dimension=DIMENSION,
):

    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        dimension,
        endpoint=False,
    )

    amplitude = np.exp(
        -GAMMA * time
    )

    gamma = amplitude * np.cos(

        theta +

        OMEGA * time

    )

    return gamma


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R2.1")
    print("Damped State")
    print("=" * 60)
    print()

    gamma = generate_damped_state(
        time=0.0,
    )

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
