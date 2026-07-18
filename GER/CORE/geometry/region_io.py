"""
============================================================
GER
CORE
Geometry
Region IO
============================================================

Persistence utilities for the geometry package.

Responsibilities
----------------
- Save Region objects.
- Save SignatureSpace objects.
- Save RegionGraph objects.
- Load the same objects.
- Handle JSON serialization.

No scientific algorithms belong here.

Author
------
GER Project
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .region import Region
from .region_graph import RegionGraph
from .signature_space import SignatureSpace


class RegionIO:
    """
    Serialization utilities.

    All methods are stateless.
    """

    # ---------------------------------------------------------
    # Generic JSON
    # ---------------------------------------------------------

    @staticmethod
    def save_json(
        data: dict[str, Any],
        filename: str | Path,
        *,
        indent: int = 4,
    ) -> None:

        path = Path(filename)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                data,
                fp,
                indent=indent,
                ensure_ascii=False,
            )

    @staticmethod
    def load_json(
        filename: str | Path,
    ) -> dict[str, Any]:

        with Path(filename).open(
            "r",
            encoding="utf-8",
        ) as fp:

            return json.load(fp)

    # ---------------------------------------------------------
    # Region
    # ---------------------------------------------------------

    @staticmethod
    def save_region(
        region: Region,
        filename: str | Path,
    ) -> None:

        RegionIO.save_json(
            region.as_dict(),
            filename,
        )

    @staticmethod
    def load_region(
        filename: str | Path,
    ) -> Region:

        return Region.from_dict(
            RegionIO.load_json(filename)
        )

    # ---------------------------------------------------------
    # Signature Space
    # ---------------------------------------------------------

    @staticmethod
    def save_signature_space(
        space: SignatureSpace,
        filename: str | Path,
    ) -> None:

        RegionIO.save_json(
            space.as_dict(),
            filename,
        )

    @staticmethod
    def load_signature_space(
        filename: str | Path,
        signature_factory,
    ) -> SignatureSpace:

        return SignatureSpace.from_dict(
            RegionIO.load_json(filename),
            signature_factory,
        )

    # ---------------------------------------------------------
    # Region Graph
    # ---------------------------------------------------------

    @staticmethod
    def save_region_graph(
        graph: RegionGraph,
        filename: str | Path,
    ) -> None:

        RegionIO.save_json(
            graph.as_dict(),
            filename,
        )

    @staticmethod
    def load_region_graph(
        filename: str | Path,
        space: SignatureSpace,
    ) -> RegionGraph:

        return RegionGraph.from_dict(
            RegionIO.load_json(filename),
            space,
        )
