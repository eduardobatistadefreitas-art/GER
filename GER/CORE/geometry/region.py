"""
============================================================
GER
CORE
Geometry
Region
============================================================

Permanent mathematical representation of a Stability Region.

A Region is a fundamental object of the Relational Spectral
Geometry (RSG) framework.

A Region contains references to the signatures that belong to
the same stability domain together with its intrinsic geometric
properties.

This class intentionally contains no analysis algorithms.

Algorithms are implemented in:

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
    Permanent representation of a Stability Region.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    id: str

    label: str | None = None

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    signature_indices: tuple[int, ...] = ()

    centroid: tuple[float, ...] = ()

    dimension: int | None = None

    radius: float | None = None

    # ------------------------------------------------------------------
    # Scientific properties
    # ------------------------------------------------------------------

    properties: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:

        if self.dimension is None:
            object.__setattr__(self, "dimension", len(self.centroid))

    # ------------------------------------------------------------------
    # Basic properties
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Number of signatures contained in the region."""
        return len(self.signature_indices)

    def is_empty(self) -> bool:
        """Return True if the region contains no signatures."""
        return len(self.signature_indices) == 0

    def contains(self, signature_index: int) -> bool:
        """Check whether a signature belongs to this region."""
        return signature_index in self.signature_indices

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:
        """
        Convert the region into a serializable dictionary.
        """

        return {

            "id": self.id,

            "label": self.label,

            "signature_indices": list(self.signature_indices),

            "centroid": list(self.centroid),

            "dimension": self.dimension,

            "radius": self.radius,

            "properties": dict(self.properties),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Region":
        """
        Construct a Region from a dictionary.
        """

        return cls(

            id=data["id"],

            label=data.get("label"),

            signature_indices=tuple(
                data.get("signature_indices", ())
            ),

            centroid=tuple(
                data.get("centroid", ())
            ),

            dimension=data.get("dimension"),

            radius=data.get("radius"),

            properties=dict(
                data.get("properties", {})
            ),
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """
        Return a compact description of the region.
        """

        return {

            "id": self.id,

            "label": self.label,

            "size": len(self),

            "dimension": self.dimension,

            "radius": self.radius,
        }

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"Region("
            f"id={self.id!r}, "
            f"size={len(self)}, "
            f"dimension={self.dimension}, "
            f"radius={self.radius})"

        )
