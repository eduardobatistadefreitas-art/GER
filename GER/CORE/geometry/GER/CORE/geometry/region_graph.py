"""
============================================================
GER
CORE
Geometry
Region Graph
============================================================

Permanent topological graph of Regions in the
Relational Spectral Geometry (RSG) framework.

The RegionGraph represents adjacency relationships between
regions belonging to a SignatureSpace.

Responsibilities
----------------
- Store region adjacencies.
- Maintain graph consistency.
- Provide topological queries.
- Serialize the graph.

No graph algorithms belong here.

Algorithms such as:
    - shortest paths
    - spanning trees
    - connected components
    - centrality
    - clustering

must be implemented in independent modules.

Author
------
GER Project
"""

from __future__ import annotations

from typing import Any

from .signature_space import SignatureSpace


class RegionGraph:
    """
    Undirected graph of regions.
    """

    def __init__(self, space: SignatureSpace):

        self._space = space

        self._adjacency: dict[str, set[str]] = {
            region_id: set()
            for region_id in space.region_ids()
        }

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _check_region(self, region_id: str) -> None:

        if not self._space.has_region(region_id):
            raise KeyError(f"Unknown region '{region_id}'.")

        self._adjacency.setdefault(region_id, set())

    # ---------------------------------------------------------
    # Edge management
    # ---------------------------------------------------------

    def connect(
        self,
        region_a: str,
        region_b: str,
    ) -> None:

        self._check_region(region_a)
        self._check_region(region_b)

        if region_a == region_b:
            raise ValueError(
                "Self-loops are not allowed."
            )

        self._adjacency[region_a].add(region_b)
        self._adjacency[region_b].add(region_a)

    def disconnect(
        self,
        region_a: str,
        region_b: str,
    ) -> None:

        self._check_region(region_a)
        self._check_region(region_b)

        self._adjacency[region_a].discard(region_b)
        self._adjacency[region_b].discard(region_a)

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def neighbors(
        self,
        region_id: str,
    ) -> tuple[str, ...]:

        self._check_region(region_id)

        return tuple(sorted(self._adjacency[region_id]))

    def degree(
        self,
        region_id: str,
    ) -> int:

        self._check_region(region_id)

        return len(self._adjacency[region_id])

    def has_edge(
        self,
        region_a: str,
        region_b: str,
    ) -> bool:

        self._check_region(region_a)
        self._check_region(region_b)

        return region_b in self._adjacency[region_a]

    # ---------------------------------------------------------
    # Collections
    # ---------------------------------------------------------

    def vertices(self) -> tuple[str, ...]:

        return tuple(sorted(self._adjacency.keys()))

    def edges(self) -> tuple[tuple[str, str], ...]:

        edges = set()

        for a, neighbors in self._adjacency.items():

            for b in neighbors:

                edge = tuple(sorted((a, b)))

                edges.add(edge)

        return tuple(sorted(edges))

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def number_of_vertices(self) -> int:

        return len(self._adjacency)

    def number_of_edges(self) -> int:

        return len(self.edges())

    def is_connected(self) -> bool:
        """
        Returns True if the graph is connected.

        Empty graphs and graphs with one vertex are considered
        connected.
        """

        vertices = self.vertices()

        if len(vertices) <= 1:
            return True

        visited = set()

        stack = [vertices[0]]

        while stack:

            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            stack.extend(
                self._adjacency[current] - visited
            )

        return len(visited) == len(vertices)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def as_dict(self) -> dict[str, Any]:

        return {

            "type": "RegionGraph",

            "version": 1,

            "adjacency": {

                region: sorted(neighbors)

                for region, neighbors in self._adjacency.items()

            },

        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        space: SignatureSpace,
    ) -> "RegionGraph":

        graph = cls(space)

        graph._adjacency.clear()

        for region, neighbors in data.get(
            "adjacency",
            {},
        ).items():

            graph._adjacency[region] = set(neighbors)

        return graph

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self) -> dict[str, Any]:

        return {

            "vertices": self.number_of_vertices(),

            "edges": self.number_of_edges(),

            "connected": self.is_connected(),

        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            "RegionGraph("
            f"vertices={self.number_of_vertices()}, "
            f"edges={self.number_of_edges()})"

        )
