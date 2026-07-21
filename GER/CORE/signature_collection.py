"""
=========================================================
GER CORE
signature_collection.py
=========================================================

Mathematical representation of a collection of Geometric
Signatures.

This module is intentionally independent from:

- Reference Universes
- Persistence
- Providers
- Experiments

It simply provides an immutable collection-like interface
for manipulating sets of Geometric Signatures.

Future experimental series (S29, S30, RH, ...) should
exchange SignatureCollection objects instead of raw lists.

=========================================================
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Iterator, Sequence

import numpy as np

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

from GER.CORE.signature_api import Signature

__all__ = [
    "SignatureCollection",
]

SIGNATURE_COLLECTION_VERSION = "1.0"


class SignatureCollection:
    """
    Immutable collection of Geometric Signatures.
    """

    def __init__(
        self,
        signatures: Iterable[Signature],
        names: Iterable[str] | None = None,
    ):
        self._signatures = tuple(signatures)

        if names is None:
            self._names = tuple(
                f"Signature {i + 1}"
                for i in range(len(self._signatures))
            )
        else:
            self._names = tuple(names)

        if len(self._names) != len(self._signatures):
            raise ValueError(
                "Number of names must match number of signatures."
            )

    # =====================================================
    # Basic Collection Interface
    # =====================================================

    def __len__(self) -> int:
        return len(self._signatures)

    def __iter__(self) -> Iterator[Signature]:
        return iter(self._signatures)

    def __getitem__(self, item):
        return self._signatures[item]

    def __repr__(self):
        return (
            f"SignatureCollection("
            f"{len(self)} signatures)"
        )

    # =====================================================
    # Metadata
    # =====================================================

    def names(self):
        return list(self._names)

    def signature_names(self):
        return self.names()

    def dimension(self):
        if len(self) == 0:
            return 0

        return len(asdict(self._signatures[0]))

    # =====================================================
    # Access
    # =====================================================

    def get(self, name: str) -> Signature:
        try:
            index = self._names.index(name)
        except ValueError:
            raise KeyError(
                f"Unknown signature '{name}'."
            )

        return self._signatures[index]

    # =====================================================
    # Numeric Representations
    # =====================================================

    def matrix(self) -> np.ndarray:
        if len(self) == 0:
            return np.empty((0, 0))

        return np.asarray(
            [
                list(asdict(signature).values())
                for signature in self._signatures
            ],
            dtype=float,
        )

    def to_numpy(self):
        return self.matrix()

    # =====================================================
    # Statistics
    # =====================================================

    def centroid(self):
        X = self.matrix()

        if X.size == 0:
            return np.empty(0)

        return np.mean(
            X,
            axis=0,
        )

    def distance_matrix(self):
        X = self.matrix()

        n = len(X)

        D = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):

                d = np.linalg.norm(
                    X[i] - X[j]
                )

                D[i, j] = d
                D[j, i] = d

        return D

    # =====================================================
    # Export
    # =====================================================

    def as_dataframe(self):
        if pd is None:
            raise ImportError(
                "pandas is required."
            )

        return pd.DataFrame(
            self.matrix(),
            index=self._names,
            columns=[
                "Diameter",
                "Convergence",
                "Recurrence",
                "Drift",
            ],
        )

    # =====================================================
    # Utilities
    # =====================================================

    def copy(self):
        return SignatureCollection(
            self._signatures,
            self._names,
        )

    def subset(
        self,
        indices: Sequence[int],
    ):
        return SignatureCollection(
            [self._signatures[i] for i in indices],
            [self._names[i] for i in indices],
        )

    def to_dict(self):
        return {
            name: asdict(signature)
            for name, signature in zip(
                self._names,
                self._signatures,
            )
        }
