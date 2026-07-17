"""
============================================================
RSG

S29

Snapshot Generator

============================================================

Converts an external trajectory into a sequence of
Standard Snapshots compatible with the RSG CORE.

Responsibilities

Trajectory
        ↓
Standard Snapshots

Nothing else.
"""

from __future__ import annotations

import numpy as np

from GER.CORE.snapshot_adapter import (
    SnapshotAdapter,
)

__all__ = [
    "generate_snapshots",
]

SNAPSHOT_GENERATOR_VERSION = "1.0"


def generate_snapshots(
    trajectory,
    eigenvectors,
    dt,
):
    """
    Builds Standard Snapshots from an external trajectory.

    Parameters
    ----------
    trajectory : ndarray

    eigenvectors : ndarray

    dt : float

    Returns
    -------
    list
    """

    adapter = SnapshotAdapter()

    snapshots = []

    for step, state in enumerate(trajectory):

        #
        # Current reference implementation:
        #
        # Position coordinate is used as the
        # modal state.
        #
        gamma = np.asarray(
            state,
            dtype=float,
        )

        snapshot = adapter.build(

            state=gamma,

            eigenvectors=eigenvectors,

            step=step,

            time=step * dt,

        )

        snapshots.append(
            snapshot
        )

    return snapshots


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("RSG")
    print("Snapshot Generator")
    print("=" * 60)
    print()

    print(
        "Module ready."
    )

    print()

    print("=" * 60)


if __name__ == "__main__":

    main()
