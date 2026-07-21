"""
GER CORE
GRAPH

Immutable mathematical edge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True, slots=True)
class Edge:
    """
    Immutable graph edge.

    Parameters
    ----------
    source
        Source node identifier.

    target
        Target node identifier.

    weight
        Edge weight.

    metadata
        Optional user-defined metadata.
    """

    source: Any
    target: Any
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """
        Convert edge to a dictionary.
        """
        return {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Edge":
        """
        Create an edge from a dictionary.
        """
        return cls(
            source=data["source"],
            target=data["target"],
            weight=data.get("weight", 1.0),
            metadata=dict(data.get("metadata", {})),
        )
