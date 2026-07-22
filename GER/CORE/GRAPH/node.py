"""
GER CORE
GRAPH

Immutable mathematical node.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True, slots=True)
class Node:
    """
    Immutable graph node.

    Parameters
    ----------
    id
        Unique node identifier.

    label
        Optional human-readable label.

    metadata
        Optional user-defined metadata.

    Notes
    -----
    Metadata is auxiliary information and does not participate
    in node identity. Two nodes are considered equal if their
    identifying fields are equal, regardless of metadata.
    """

    id: Any

    label: str | None = None

    metadata: Dict[str, Any] = field(
        default_factory=dict,
        compare=False,
    )

    def to_dict(self) -> dict:
        """
        Convert node to a dictionary.
        """
        return {
            "id": self.id,
            "label": self.label,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        """
        Create a node from a dictionary.
        """
        return cls(
            id=data["id"],
            label=data.get("label"),
            metadata=dict(data.get("metadata", {})),
        )
