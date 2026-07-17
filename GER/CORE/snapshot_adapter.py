"""
=========================================================
GER CORE

snapshot_adapter.py

=========================================================

Snapshot Adapter

Official boundary between external systems and the
RSG CORE.

The SnapshotAdapter converts an external temporal
representation into a Standard Snapshot compatible
with the CORE.

The internal mathematical representation used to
perform this conversion is intentionally hidden from
the public interface.

Responsibilities
----------------

Trajectory
        ↓
Standard Snapshot

Nothing else.

This component does not know:

- Duffing
- Lorenz
- ECG
- Fourier
- Wavelets
- Koopman
- POD

Those are implementation details.
"""

from __future__ import annotations

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

__all__ = [
    "SnapshotAdapter",
]

SNAPSHOT_ADAPTER_VERSION = "1.0"


class SnapshotAdapter:
    """
    Official adapter between external trajectories
    and the RSG CORE.
    """

    def build(
        self,
        state,
        eigenvectors,
        *,
        step=0,
        time=0.0,
    ):
        """
        Produces one Standard Snapshot.

        Parameters
        ----------
        state
            External state representation.

        eigenvectors
            Modal basis compatible with the
            current CORE implementation.

        step
            Simulation step.

        time
            Physical time.

        Returns
        -------
        dict
            Standard Snapshot.
        """

        return build_observational_snapshot(
            gamma=state,
            eigenvectors=eigenvectors,
            step=step,
            time=time,
        )
