"""
============================================================
GER
CORE
Geometry
Region Plot
============================================================

Visualization utilities for Region objects.

This module depends only on the public API of the geometry
package and matplotlib.

No scientific algorithms belong here.

Author
------
GER Project
"""

from __future__ import annotations

from math import cos, pi, sin
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle

from .region_graph import RegionGraph
from .signature_space import SignatureSpace


class RegionPlot:
    """
    Plot utilities for the geometry package.
    """

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    @staticmethod
    def _axes(ax: Axes | None) -> Axes:

        if ax is not None:
            return ax

        fig, ax = plt.subplots(figsize=(8, 8))
        return ax

    @staticmethod
    def _positions(space: SignatureSpace) -> dict[str, tuple[float, float]]:

        positions = {}

        for region_id in space.region_ids():

            region = space.region(region_id)

            if region.centroid is not None and len(region.centroid) >= 2:

                positions[region_id] = (
                    float(region.centroid[0]),
                    float(region.centroid[1]),
                )

            else:

                positions[region_id] = (0.0, 0.0)

        return positions

    # ---------------------------------------------------------
    # Centroids
    # ---------------------------------------------------------

    @staticmethod
    def centroids(
        space: SignatureSpace,
        *,
        ax: Axes | None = None,
        show_labels: bool = True,
    ) -> Axes:

        ax = RegionPlot._axes(ax)

        positions = RegionPlot._positions(space)

        for region_id, (x, y) in positions.items():

            ax.scatter(x, y)

            if show_labels:

                ax.text(
                    x,
                    y,
                    region_id,
                )

        ax.set_title("Region Centroids")
        ax.set_aspect("equal")

        return ax

    # ---------------------------------------------------------
    # Radius
    # ---------------------------------------------------------

    @staticmethod
    def radius(
        space: SignatureSpace,
        *,
        ax: Axes | None = None,
        show_labels: bool = True,
    ) -> Axes:

        ax = RegionPlot._axes(ax)

        positions = RegionPlot._positions(space)

        for region_id in space.region_ids():

            region = space.region(region_id)

            x, y = positions[region_id]

            ax.scatter(x, y)

            if region.radius is not None:

                circle = Circle(
                    (x, y),
                    region.radius,
                    fill=False,
                )

                ax.add_patch(circle)

            if show_labels:

                ax.text(
                    x,
                    y,
                    region_id,
                )

        ax.set_title("Region Radius")
        ax.set_aspect("equal")

        return ax

    # ---------------------------------------------------------
    # Graph
    # ---------------------------------------------------------

    @staticmethod
    def graph(
        graph: RegionGraph,
        *,
        ax: Axes | None = None,
        show_labels: bool = True,
    ) -> Axes:

        ax = RegionPlot._axes(ax)

        space = graph._space

        positions = RegionPlot._positions(space)

        for a, b in graph.edges():

            xa, ya = positions[a]
            xb, yb = positions[b]

            ax.plot(
                [xa, xb],
                [ya, yb],
            )

        for region_id, (x, y) in positions.items():

            ax.scatter(x, y)

            if show_labels:

                ax.text(
                    x,
                    y,
                    region_id,
                )

        ax.set_title("Region Graph")
        ax.set_aspect("equal")

        return ax

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    @staticmethod
    def summary(
        space: SignatureSpace,
        graph: RegionGraph | None = None,
        *,
        ax: Axes | None = None,
    ) -> Axes:

        ax = RegionPlot._axes(ax)

        RegionPlot.radius(
            space,
            ax=ax,
            show_labels=True,
        )

        if graph is not None:

            positions = RegionPlot._positions(space)

            for a, b in graph.edges():

                xa, ya = positions[a]
                xb, yb = positions[b]

                ax.plot(
                    [xa, xb],
                    [ya, yb],
                )

        ax.set_title("Geometry Summary")
        ax.set_aspect("equal")

        return ax

    # ---------------------------------------------------------
    # Circular Layout
    # ---------------------------------------------------------

    @staticmethod
    def circular_layout(
        graph: RegionGraph,
        *,
        radius: float = 1.0,
        ax: Axes | None = None,
        show_labels: bool = True,
    ) -> Axes:
        """
        Draw the graph using a simple circular layout.
        Useful when regions do not have centroids.
        """

        ax = RegionPlot._axes(ax)

        vertices = graph.vertices()

        n = len(vertices)

        if n == 0:

            return ax

        positions = {}

        for i, region_id in enumerate(vertices):

            angle = 2.0 * pi * i / n

            positions[region_id] = (
                radius * cos(angle),
                radius * sin(angle),
            )

        for a, b in graph.edges():

            xa, ya = positions[a]
            xb, yb = positions[b]

            ax.plot(
                [xa, xb],
                [ya, yb],
            )

        for region_id, (x, y) in positions.items():

            ax.scatter(x, y)

            if show_labels:

                ax.text(
                    x,
                    y,
                    region_id,
                )

        ax.set_title("Region Graph (Circular Layout)")
        ax.set_aspect("equal")

        return ax
