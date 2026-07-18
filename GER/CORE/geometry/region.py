"""
============================================================
GER
CORE
Geometry
Region
============================================================

Permanent mathematical representation of a Region in the
Relational Spectral Geometry (RSG) framework.

A Region is a geometric entity of the Signature Space.

It is intentionally immutable and contains no analysis
algorithms.

Algorithms belong to:

    region_metrics.py
    region_graph.py
    region_io.py
    region_plot.py

Author
------
GER Project
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Region:
    """
    Immutable geometric region.

    A Region represents a subset of signatures belonging to the
    same geometric domain of the Signature Space.

    Notes
    -----
    * The Region is a mathematical object.
    * It does not perform calculations.
    * Scientific algorithms belong to external modules.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    id: str

    label: str | None = None

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    signature_ids: tuple[str, ...] = ()

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    centroid: tuple[float, ...] | None = None

    radius: float | None = None

    # ---------------------------------------------------------
    # Persistent attributes
    # ---------------------------------------------------------

    attributes: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Derived properties
    # ---------------------------------------------------------

    @property
    def dimension(self) -> int | None:
        """
        Intrinsic dimension inferred from the centroid.
        """

        if self.centroid is None:
            return None

        return len(self.centroid)

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def __len__(self) -> int:
        """
        Number of signatures in the region.
        """

        return len(self.signature_ids)

    def is_empty(self) -> bool:
        """
        Return True if the region has no signatures.
        """

        return len(self) == 0

    def contains(self, signature_id: str) -> bool:
        """
        Check whether a signature belongs to the region.
        """

        return signature_id in self.signature_ids

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:
        """
        Convert the region into a serializable dictionary.
        """

        return {

            "type": "Region",

            "version": 1,

            "id": self.id,

            "label": self.label,

            "signature_ids": list(self.signature_ids),

            "centroid": (
                list(self.centroid)
                if self.centroid is not None
                else None
            ),

            "radius": self.radius,

            "attributes": dict(self.attributes),

        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Region":
        """
        Construct a Region from a serialized dictionary.
        """

        centroid = data.get("centroid")

        return cls(

            id=data["id"],

            label=data.get("label"),

            signature_ids=tuple(
                data.get("signature_ids", ())
            ),

            centroid=(
                tuple(centroid)
                if centroid is not None
                else None
            ),

            radius=data.get("radius"),

            attributes=dict(
                data.get("attributes", {})
            ),

        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """
        Compact description of the region.
        """

        return {

            "id": self.id,

            "label": self.label,

            "size": len(self),

            "dimension": self.dimension,

            "radius": self.radius,

        }

    # ---------------------------------------------------------
    # Equality
    # ---------------------------------------------------------

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Region):
            return NotImplemented

        return self.id == other.id

    def __hash__(self) -> int:

        return hash(self.id)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"Region("
            f"id={self.id!r}, "
            f"size={len(self)}, "
            f"dimension={self.dimension}, "
            f"radius={self.radius})"

        )
