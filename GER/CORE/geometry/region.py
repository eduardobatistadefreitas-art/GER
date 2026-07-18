"""
============================================================
GER
CORE
Geometry
Region
============================================================

Mathematical representation of a Stability Region.

A Region is a permanent geometric object of the RSG framework.
It represents a subset of the Signature Space containing
geometric signatures that belong to the same stability domain.

This class intentionally performs no geometric analysis.
Algorithms belong to:

    region_metrics.py
    region_graph.py
    region_plot.py
    region_io.py

Author:
GER Project
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Region:
    """
    Permanent representation of a Stability Region.
    """

    id: str

    name: str | None = None

    signature_indices: list[int] = field(default_factory=list)

    centroid: tuple[float, ...] = field(default_factory=tuple)

    radius: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        """Number of signatures contained in the region."""
        return len(self.signature_indices)

    def dimension(self) -> int:
        """Dimension of the centroid."""
        return len(self.centroid)

    def is_empty(self) -> bool:
        """Return True if the region contains no signatures."""
        return len(self.signature_indices) == 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize the region into a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "signature_indices": list(self.signature_indices),
            "centroid": list(self.centroid),
            "radius": self.radius,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Region":
        """Create a Region from a dictionary."""
        return cls(
            id=data["id"],
            name=data.get("name"),
            signature_indices=list(data.get("signature_indices", [])),
            centroid=tuple(data.get("centroid", ())),
            radius=data.get("radius"),
            metadata=dict(data.get("metadata", {})),
        )

    def summary(self) -> dict[str, Any]:
        """Return a compact summary of the region."""
        return {
            "id": self.id,
            "name": self.name,
            "size": len(self),
            "dimension": self.dimension(),
            "radius": self.radius,
        }

    def __repr__(self) -> str:
        return (
            f"Region("
            f"id={self.id!r}, "
            f"size={len(self)}, "
            f"dimension={self.dimension()}, "
            f"radius={self.radius})"
        )
