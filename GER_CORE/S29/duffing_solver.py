"""
============================================================
RSG

S29

Duffing Solver

============================================================

Numerical integration of the forced Duffing oscillator.

This module is intentionally independent from the RSG CORE.

Its only responsibility is:

Parameters
        ↓
Trajectory

Nothing else.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "solve_duffing",
]

DUFFING_SOLVER_VERSION = "1.0"


# ==========================================================
# Duffing Dynamics
# ==========================================================

def _duffing(state, t,
             delta,
             beta,
             alpha,
             gamma,
             omega):

    x, y = state

    dx = y

    dy = (
        -delta * y
        -beta * x
        -alpha * x**3
        + gamma * np.cos(omega * t)
    )

    return np.array([dx, dy])


# ==========================================================
# Classical RK4
# ==========================================================

def solve_duffing(

    t_max=1000.0,

    dt=0.01,

    x0=0.1,

    y0=0.0,

    delta=0.3,

    beta=-1.0,

    alpha=1.0,

    gamma=0.5,

    omega=1.0,

):
    """
    Integrates the classical forced Duffing oscillator.

    Returns
    -------
    dict

        time

        trajectory
    """

    steps = int(t_max / dt)

    time = np.linspace(
        0.0,
        t_max,
        steps + 1,
    )

    trajectory = np.zeros(
        (
            steps + 1,
            2,
        )
    )

    trajectory[0] = [x0, y0]

    for i in range(steps):

        t = time[i]

        state = trajectory[i]

        k1 = _duffing(
            state,
            t,
            delta,
            beta,
            alpha,
            gamma,
            omega,
        )

        k2 = _duffing(
            state + 0.5 * dt * k1,
            t + 0.5 * dt,
            delta,
            beta,
            alpha,
            gamma,
            omega,
        )

        k3 = _duffing(
            state + 0.5 * dt * k2,
            t + 0.5 * dt,
            delta,
            beta,
            alpha,
            gamma,
            omega,
        )

        k4 = _duffing(
            state + dt * k3,
            t + dt,
            delta,
            beta,
            alpha,
            gamma,
            omega,
        )

        trajectory[i + 1] = (

            state

            + dt / 6.0

            * (

                k1

                + 2.0 * k2

                + 2.0 * k3

                + k4

            )

        )

    return {

        "time": time,

        "trajectory": trajectory,

    }


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("RSG")
    print("Duffing Solver")
    print("=" * 60)
    print()

    result = solve_duffing(
        t_max=20.0,
    )

    print("Integration finished.")
    print()

    print("Samples")

    print(len(result["time"]))

    print()

    print("Final state")

    print(result["trajectory"][-1])

    print()

    print("=" * 60)
    print("STATUS : DUFFING SOLVER READY")
    print("=" * 60)


if __name__ == "__main__":

    main()
