"""
============================================================
GER
CORE
Geometry
Region Metrics
============================================================

Geometric metrics for Region objects.

This module contains pure functions.

No state is stored.

No Region is modified.

Author
------
GER Project
"""

from __future__ import annotations

from math import dist
from typing import Any

from .region import Region
from .signature_space import SignatureSpace


class RegionMetrics:
    """
    Static geometric measurements for Region objects.
    """

    # ---------------------------------------------------------
    # Basic
    # ---------------------------------------------------------

    @staticmethod
    def size(region: Region) -> int:
        """
        Number of signatures.
        """
        return len(region)

    @staticmethod
    def is_empty(region: Region) -> bool:

        return region.is_empty()

    @staticmethod
    def dimension(region: Region) -> int:

        return region.dimension

    @staticmethod
    def radius(region: Region) -> float | None:

        return region.radius

    @staticmethod
    def centroid(region: Region) -> tuple[float, ...] | None:

        return region.centroid

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    @staticmethod
    def contains(
        region: Region,
        signature_id: str,
    ) -> bool:

        return region.contains(signature_id)

    # ---------------------------------------------------------
    # Derived Geometry
    # ---------------------------------------------------------

    @staticmethod
    def centroid_norm(
        region: Region,
    ) -> float | None:
        """
        Euclidean norm of the centroid.
        """

        if region.centroid is None:
            return None

        origin = (0.0,) * len(region.centroid)

        return dist(origin, region.centroid)

    @staticmethod
    def bounding_diameter(
        region: Region,
    ) -> float | None:
        """
        Conservative geometric diameter.

        Uses:

            diameter = 2 * radius
        """

        if region.radius is None:
            return None

        return 2.0 * region.radius

    @staticmethod
    def density(
        region: Region,
    ) -> float | None:
        """
        Very simple density estimate.

        signatures / radius
        """

        if region.radius is None:

            return None

        if region.radius <= 0:

            return None

        return len(region) / region.radius

    # ---------------------------------------------------------
    # Global
    # ---------------------------------------------------------

    @staticmethod
    def occupancy(
        region: Region,
        space: SignatureSpace,
    ) -> float | None:
        """
        Fraction of signatures belonging to this region.
        """

        total = space.number_of_signatures()

        if total == 0:

            return None

        return len(region) / total

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    @staticmethod
    def summary(
        region: Region,
        space: SignatureSpace | None = None,
    ) -> dict[str, Any]:

        data = {

            "size": RegionMetrics.size(region),

            "dimension": RegionMetrics.dimension(region),

            "radius": RegionMetrics.radius(region),

            "diameter": RegionMetrics.bounding_diameter(region),

            "density": RegionMetrics.density(region),

            "centroid": RegionMetrics.centroid(region),

            "centroid_norm": RegionMetrics.centroid_norm(region),

        }

        if space is not None:

            data["occupancy"] = RegionMetrics.occupancy(
                region,
                space,
            )

        return data
