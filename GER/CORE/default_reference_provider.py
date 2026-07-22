"""
=========================================================
GER CORE

default_reference_provider.py

=========================================================

Default implementation of the ReferenceProvider interface.

This provider loads persisted Reference Universes generated
by GER experiments.

Current backend:
    - signatures.parquet
    - universes.parquet (optional)

Future implementations may replace the persistence backend
without changing the public API.
=========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from GER.CORE.reference_provider import ReferenceProvider
from GER.CORE.signature_api import Signature
from GER.CORE.signature_collection import SignatureCollection


__all__ = [
    "DefaultReferenceProvider",
]

DEFAULT_REFERENCE_PROVIDER_VERSION = "1.0"


class DefaultReferenceProvider(ReferenceProvider):

    def __init__(
        self,
        signatures_path,
        universes_path=None,
        reference_name="Reference Universe",
    ):

        self._signatures_path = Path(signatures_path)

        self._universes_path = (
            Path(universes_path)
            if universes_path is not None
            else None
        )

        self._reference_name = reference_name

        self._collection = None
        self._metadata = None

    # =====================================================
    # Internal
    # =====================================================

    def _load(self):

        if self._collection is not None:
            return

        if not self._signatures_path.exists():

            raise FileNotFoundError(
                f"Signature database not found:\n"
                f"{self._signatures_path}"
            )

        df = pd.read_parquet(
            self._signatures_path
        )

        required = [
            "diameter",
            "convergence",
            "recurrence",
            "drift",
        ]

        missing = [
            column
            for column in required
            if column not in df.columns
        ]

        if missing:

            raise RuntimeError(
                "Invalid signature database.\n"
                f"Missing columns: {missing}"
            )

        signatures = [

            Signature(
                diameter=float(row.diameter),
                convergence=float(row.convergence),
                recurrence=float(row.recurrence),
                drift=float(row.drift),
            )

            for row in df.itertuples(index=False)

        ]

        names = None

        metadata = {}

        if (
            self._universes_path is not None
            and self._universes_path.exists()
        ):

            udf = pd.read_parquet(
                self._universes_path
            )

            if "UniverseID" in udf.columns:

                names = [
                    f"Universe {uid}"
                    for uid in udf["UniverseID"]
                ]

            metadata = {

                "universes": len(udf),

                "columns": list(
                    udf.columns
                ),

            }

        self._collection = SignatureCollection(
            signatures,
            names,
        )

        metadata.update({

            "reference_name":
                self._reference_name,

            "signature_count":
                len(self._collection),

            "dimension":
                self._collection.dimension(),

            "source":
                str(self._signatures_path),

        })

        self._metadata = metadata

    # =====================================================
    # ReferenceProvider API
    # =====================================================

    def load_signatures(self):

        self._load()

        return self._collection

    def available_signatures(self):

        self._load()

        return len(self._collection)

    def signature_names(self):

        self._load()

        return self._collection.signature_names()

    def signature_dimension(self):

        self._load()

        return self._collection.dimension()

    def reference_name(self):

        return self._reference_name

    def metadata(self):

        self._load()

        return dict(self._metadata)

    def summary(self):

        self._load()

        return (
            f"{self._reference_name}\n"
            f"Signatures : {len(self._collection)}\n"
            f"Dimension  : "
            f"{self._collection.dimension()}"
        )
