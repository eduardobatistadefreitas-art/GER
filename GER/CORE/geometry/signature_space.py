"""
============================================================
GER
CORE
Geometry
Signature Space
============================================================

Permanent representation of a Signature Space in the
Relational Spectral Geometry (RSG) framework.

The SignatureSpace is the root geometric container of the
framework.

Responsibilities
----------------
- Store signatures.
- Store regions.
- Maintain membership consistency.
- Provide queries.
- Serialize the complete space.

No scientific algorithms belong here.

Algorithms belong to:

    region_metrics.py
    region_graph.py
    region_plot.py
    region_io.py

Author
------
GER Project
"""

from __future__ import annotations

from typing import Any

from .region import Region


class SignatureSpace:
    """
    Root geometric container of the RSG framework.

    The SignatureSpace owns all signatures and regions and
    guarantees their consistency.
    """

    def __init__(
        self,
        *,
        id: str,
        label: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> None:

        self.id = id
        self.label = label

        self._attributes = dict(attributes or {})

        self._signatures: dict[str, Any] = {}

        self._regions: dict[str, Region] = {}

        self._signature_to_region: dict[str, str | None] = {}

    # ---------------------------------------------------------
    # Signature management
    # ---------------------------------------------------------

    def add_signature(
        self,
        signature: Any,
    ) -> None:

        signature_id = signature.id

        if signature_id in self._signatures:
            raise ValueError(
                f"Signature '{signature_id}' already exists."
            )

        self._signatures[signature_id] = signature
        self._signature_to_region[signature_id] = None

    def remove_signature(
        self,
        signature_id: str,
    ) -> None:

        if signature_id not in self._signatures:
            raise KeyError(signature_id)

        del self._signatures[signature_id]
        del self._signature_to_region[signature_id]

    # ---------------------------------------------------------
    # Region management
    # ---------------------------------------------------------

    def add_region(
        self,
        region: Region,
    ) -> None:

        if region.id in self._regions:
            raise ValueError(
                f"Region '{region.id}' already exists."
            )

        self._regions[region.id] = region

    def remove_region(
        self,
        region_id: str,
    ) -> None:

        if region_id not in self._regions:
            raise KeyError(region_id)

        del self._regions[region_id]

        for signature_id, current in self._signature_to_region.items():

            if current == region_id:
                self._signature_to_region[signature_id] = None

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    def assign_signature(
        self,
        signature_id: str,
        region_id: str,
    ) -> None:

        if signature_id not in self._signatures:
            raise KeyError(signature_id)

        if region_id not in self._regions:
            raise KeyError(region_id)

        self._signature_to_region[signature_id] = region_id

    def unassign_signature(
        self,
        signature_id: str,
    ) -> None:

        if signature_id not in self._signatures:
            raise KeyError(signature_id)

        self._signature_to_region[signature_id] = None

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def signature(
        self,
        signature_id: str,
    ) -> Any:

        return self._signatures[signature_id]

    def region(
        self,
        region_id: str,
    ) -> Region:

        return self._regions[region_id]

    def region_of(
        self,
        signature_id: str,
    ) -> Region | None:

        region_id = self._signature_to_region[signature_id]

        if region_id is None:
            return None

        return self._regions[region_id]

    def has_signature(
        self,
        signature_id: str,
    ) -> bool:

        return signature_id in self._signatures

    def has_region(
        self,
        region_id: str,
    ) -> bool:

        return region_id in self._regions

    # ---------------------------------------------------------
    # Collections
    # ---------------------------------------------------------

    def signature_ids(self) -> tuple[str, ...]:

        return tuple(self._signatures.keys())

    def region_ids(self) -> tuple[str, ...]:

        return tuple(self._regions.keys())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def number_of_signatures(self) -> int:

        return len(self._signatures)

    def number_of_regions(self) -> int:

        return len(self._regions)

    def is_empty(self) -> bool:

        return (
            self.number_of_signatures() == 0
            and self.number_of_regions() == 0
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:

        return {

            "type": "SignatureSpace",

            "version": 1,

            "id": self.id,

            "label": self.label,

            "attributes": dict(self._attributes),

            "signatures": [
                signature.as_dict()
                for signature in self._signatures.values()
            ],

            "regions": [
                region.as_dict()
                for region in self._regions.values()
            ],

            "membership": dict(
                self._signature_to_region
            ),

        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        signature_factory,
    ) -> "SignatureSpace":

        space = cls(

            id=data["id"],

            label=data.get("label"),

            attributes=data.get("attributes", {}),

        )

        for signature_data in data.get("signatures", ()):

            signature = signature_factory(signature_data)

            space.add_signature(signature)

        for region_data in data.get("regions", ()):

            region = Region.from_dict(region_data)

            space.add_region(region)

        for signature_id, region_id in data.get(
            "membership",
            {},
        ).items():

            if region_id is not None:

                space.assign_signature(
                    signature_id,
                    region_id,
                )

        return space

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self) -> dict[str, Any]:

        assigned = sum(
            region is not None
            for region in self._signature_to_region.values()
        )

        return {

            "id": self.id,

            "label": self.label,

            "signatures": self.number_of_signatures(),

            "regions": self.number_of_regions(),

            "assigned": assigned,

        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            "SignatureSpace("
            f"id={self.id!r}, "
            f"signatures={self.number_of_signatures()}, "
            f"regions={self.number_of_regions()})"

          )
