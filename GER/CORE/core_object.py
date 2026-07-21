"""
========================================================================
GER CORE
Core Scientific Object
========================================================================

Defines the abstract base class for every immutable scientific object
inside the Relational Spectral Geometry (RSG) framework.

Design principles
-----------------
- Immutable value objects
- Structural equality
- Deterministic serialization
- Canonical representation
- Future-ready certification support
- No experiment-specific logic
- No numerical algorithms

Every permanent mathematical object in the CORE should inherit from
CoreObject.

Examples
--------
- Signature
- SignatureCollection
- Graph
- Certificate
- Partition
- Snapshot (future)
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Any
from typing import Dict
from typing import Mapping

import hashlib
import json


class CoreObject(ABC):
    """
    Base class for every scientific object in the GER CORE.

    This class provides a common interface for:

    - deterministic serialization
    - structural equality
    - deterministic hashing
    - metadata handling
    - canonical representation

    Scientific subclasses only need to implement:

        to_dict()

    Everything else is automatically derived.
    """

    ####################################################################
    # Construction
    ####################################################################

    def __init__(self, metadata: Mapping[str, Any] | None = None):

        self._metadata: Dict[str, Any] = (
            dict(metadata)
            if metadata is not None
            else {}
        )

    ####################################################################
    # Abstract API
    ####################################################################

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Return a deterministic dictionary representation.

        The returned dictionary MUST contain only JSON-serializable
        objects.

        Ordering is irrelevant because canonicalization is performed
        automatically.
        """
        raise NotImplementedError

    ####################################################################
    # Metadata
    ####################################################################

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Immutable copy of metadata.
        """
        return dict(self._metadata)

    ####################################################################
    # Canonical representation
    ####################################################################

    def canonical_dict(self) -> Dict[str, Any]:
        """
        Canonical dictionary representation.

        Includes metadata.
        """

        return {
            "type": self.__class__.__name__,
            "data": self.to_dict(),
            "metadata": self.metadata,
        }

    def canonical_json(self) -> str:
        """
        Deterministic JSON representation.
        """

        return json.dumps(
            self.canonical_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    ####################################################################
    # Structural Certificate
    ####################################################################

    @property
    def structural_hash(self) -> str:
        """
        Deterministic SHA256 hash.

        Can later become the basis of the Structural Certificate.
        """

        return hashlib.sha256(
            self.canonical_json().encode("utf-8")
        ).hexdigest()

    ####################################################################
    # Equality
    ####################################################################

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, CoreObject):
            return False

        return (
            self.canonical_json()
            == other.canonical_json()
        )

    ####################################################################
    # Hashability
    ####################################################################

    def __hash__(self) -> int:
        """
        Hash based on deterministic structure.
        """

        return hash(self.structural_hash)

    ####################################################################
    # Representation
    ####################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(hash={self.structural_hash[:12]})"
        )

    ####################################################################
    # Convenience
    ####################################################################

    def to_json(self) -> str:
        """
        Alias for canonical_json().
        """

        return self.canonical_json()

    def summary(self) -> Dict[str, Any]:
        """
        Lightweight inspection.

        Subclasses may extend.
        """

        return {
            "type": self.__class__.__name__,
            "hash": self.structural_hash,
            "metadata": self.metadata,
        }
