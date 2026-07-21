"""
========================================================================
GER CORE
Graph
========================================================================

Canonical graph representation for the Relational Spectral Geometry (RSG)
framework.

This module defines the fundamental graph objects used throughout the
scientific CORE.

The philosophy adopted here is intentionally minimal:

    • Graph is a mathematical object.
    • Graph contains no analysis algorithms.
    • Graph contains no topology algorithms.
    • Graph contains no spectral algorithms.
    • Graph contains no visualization code.

Those responsibilities belong to dedicated modules.

This module provides only:

    • Node
    • Edge
    • Graph

together with validation, serialization and structural consistency.

Design Principles
-----------------

- immutable value objects
- deterministic structure
- structural equality
- future-proof
- experiment independent
- no external dependencies
- reusable across every GER experiment

Future companion modules
------------------------

graph_builder.py
graph_algorithms.py
graph_operators.py
graph_adapter.py
topology.py

Author
------
GER Project
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from .node import Node
from .edge import Edge
from .graph import Graph

import hashlib
import json
    ##################################################################
    # Internal insertion
    ##################################################################

    def _insert_node(
        self,
        node: Node,
    ):

        if node.id in self._nodes:

            raise ValueError(
                f"Duplicate node '{node.id}'."
            )

        self._nodes[node.id] = node

    def _normalize_edge(

        self,

        source,

        target,

    ):

        if self._directed:

            return source, target

        return tuple(
            sorted(
                (source, target),
                key=repr,
            )
        )

    def _insert_edge(
        self,
        edge: Edge,
    ):

        if (
            not self._allow_self_loops
            and edge.source == edge.target
        ):

            raise ValueError(
                "Self-loops are disabled."
            )

        if edge.source not in self._nodes:

            raise KeyError(edge.source)

        if edge.target not in self._nodes:

            raise KeyError(edge.target)

        key = self._normalize_edge(

            edge.source,

            edge.target,
        )

        if key in self._edges:

            raise ValueError(
                f"Duplicate edge {key}."
            )

        self._edges[key] = edge
          ##################################################################
    # Validation
    ##################################################################

    def _validate(self):

        for edge in self._edges.values():

            if edge.source not in self._nodes:

                raise RuntimeError(
                    "Invalid graph."
                )

            if edge.target not in self._nodes:

                raise RuntimeError(
                    "Invalid graph."
                )
                  ##################################################################
    # Basic Properties
    ##################################################################

    @property
    def directed(self) -> bool:
        """Return whether the graph is directed."""
        return self._directed

    @property
    def allow_self_loops(self) -> bool:
        """Return whether self-loops are allowed."""
        return self._allow_self_loops

    @property
    def metadata(self) -> Dict[str, Any]:
        """Return a copy of graph metadata."""
        return dict(self._metadata)

    ##################################################################
    # Size
    ##################################################################

    def order(self) -> int:
        """
        Number of nodes.
        """
        return len(self._nodes)

    def size(self) -> int:
        """
        Number of edges.
        """
        return len(self._edges)

    number_of_nodes = order
    number_of_edges = size

    ##################################################################
    # Iteration
    ##################################################################

    def nodes(self) -> Tuple[Node, ...]:
        """
        Return all nodes.
        """
        return tuple(self._nodes.values())

    def edges(self) -> Tuple[Edge, ...]:
        """
        Return all edges.
        """
        return tuple(self._edges.values())

    def node_ids(self) -> Tuple[Any, ...]:
        """
        Return node identifiers.
        """
        return tuple(self._nodes.keys())

    ##################################################################
    # Membership
    ##################################################################

    def has_node(self, node_id: Any) -> bool:
        return node_id in self._nodes

    def has_edge(
        self,
        source: Any,
        target: Any,
    ) -> bool:

        key = self._normalize_edge(source, target)

        return key in self._edges

    ##################################################################
    # Access
    ##################################################################

    def get_node(
        self,
        node_id: Any,
    ) -> Node:

        return self._nodes[node_id]

    def get_edge(
        self,
        source: Any,
        target: Any,
    ) -> Edge:

        key = self._normalize_edge(source, target)

        return self._edges[key]

    ##################################################################
    # Neighbors
    ##################################################################

    def neighbors(
        self,
        node_id: Any,
    ) -> Tuple[Node, ...]:

        if node_id not in self._nodes:
            raise KeyError(node_id)

        result = []

        for edge in self._edges.values():

            if edge.source == node_id:

                result.append(
                    self._nodes[edge.target]
                )

            elif (
                not self._directed
                and edge.target == node_id
            ):

                result.append(
                    self._nodes[edge.source]
                )

        return tuple(result)

    ##################################################################
    # Degree
    ##################################################################

    def degree(
        self,
        node_id: Any,
    ) -> int:

        return len(
            self.neighbors(node_id)
        )

    ##################################################################
    # Density
    ##################################################################

    def density(self) -> float:
        """
        Graph density.
        """

        n = self.order()

        if n <= 1:
            return 0.0

        m = self.size()

        if self._directed:

            return m / (n * (n - 1))

        return (2.0 * m) / (n * (n - 1))

    ##################################################################
    # Adjacency
    ##################################################################

    def adjacency(self) -> Dict[Any, Tuple[Any, ...]]:
        """
        Return adjacency dictionary.
        """

        adj = {}

        for node in self._nodes:

            adj[node] = tuple(
                neighbor.id
                for neighbor in self.neighbors(node)
            )

        return adj

    ##################################################################
    # Copy
    ##################################################################

    def copy(self) -> "Graph":
        """
        Return an equivalent graph.
        """

        return Graph(
            nodes=self.nodes(),
            edges=self.edges(),
            directed=self._directed,
            allow_self_loops=self._allow_self_loops,
            metadata=self.metadata,
        )

    ##################################################################
    # Functional construction
    ##################################################################

    def with_node(
        self,
        node: Node,
    ) -> "Graph":
        """
        Return a new graph containing an additional node.
        """

        nodes = list(self.nodes())
        nodes.append(node)

        return Graph(
            nodes=nodes,
            edges=self.edges(),
            directed=self._directed,
            allow_self_loops=self._allow_self_loops,
            metadata=self.metadata,
        )

    def with_edge(
        self,
        edge: Edge,
    ) -> "Graph":
        """
        Return a new graph containing an additional edge.
        """

        edges = list(self.edges())
        edges.append(edge)

        return Graph(
            nodes=self.nodes(),
            edges=edges,
            directed=self._directed,
            allow_self_loops=self._allow_self_loops,
            metadata=self.metadata,
        )

    ##################################################################
    # Subgraph
    ##################################################################

    def subgraph(
        self,
        node_ids: Iterable[Any],
    ) -> "Graph":
        """
        Induced subgraph.
        """

        node_ids = set(node_ids)

        nodes = [
            node
            for node in self.nodes()
            if node.id in node_ids
        ]

        edges = []

        for edge in self.edges():

            if (
                edge.source in node_ids
                and edge.target in node_ids
            ):

                edges.append(edge)

        return Graph(
            nodes=nodes,
            edges=edges,
            directed=self._directed,
            allow_self_loops=self._allow_self_loops,
            metadata=self.metadata,
        )

    ##################################################################
    # Iteration protocol
    ##################################################################

    def __len__(self) -> int:
        return self.order()

    def __contains__(
        self,
        node_id: Any,
    ) -> bool:
        return self.has_node(node_id)

    def __iter__(self) -> Iterator[Node]:
        return iter(self._nodes.values())
          ##################################################################
    # Serialization
    ##################################################################

    def to_dict(self) -> Dict[str, Any]:
        """
        Deterministic dictionary representation.
        """

        return {

            "directed": self._directed,

            "allow_self_loops": self._allow_self_loops,

            "metadata": dict(self._metadata),

            "nodes": sorted(
                (
                    node.to_dict()
                    for node in self.nodes()
                ),
                key=lambda x: repr(x["id"]),
            ),

            "edges": sorted(
                (
                    edge.to_dict()
                    for edge in self.edges()
                ),
                key=lambda x: (
                    repr(x["source"]),
                    repr(x["target"]),
                ),
            ),
        }

    def to_json(
        self,
        indent: int | None = 4,
    ) -> str:

        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
            sort_keys=True,
        )

    ##################################################################
    # Edge List
    ##################################################################

    def to_edge_list(
        self,
    ) -> List[Tuple[Any, Any, float]]:

        return [

            (
                edge.source,
                edge.target,
                edge.weight,
            )

            for edge in self.edges()
        ]

    ##################################################################
    # Adjacency Matrix
    ##################################################################

    def to_adjacency_matrix(
        self,
    ) -> Tuple[List[Any], List[List[float]]]:
        """
        Returns

            labels

            matrix

        No external dependencies.
        """

        labels = sorted(
            self.node_ids(),
            key=repr,
        )

        index = {
            node: i
            for i, node in enumerate(labels)
        }

        n = len(labels)

        matrix = [

            [0.0] * n

            for _ in range(n)
        ]

        for edge in self.edges():

            i = index[edge.source]

            j = index[edge.target]

            matrix[i][j] = edge.weight

            if not self._directed:

                matrix[j][i] = edge.weight

        return labels, matrix

    ##################################################################
    # Structural Hash
    ##################################################################

    @property
    def structural_hash(
        self,
    ) -> str:

        payload = json.dumps(

            self.to_dict(),

            sort_keys=True,

            separators=(",", ":"),

            ensure_ascii=False,
        )

        return hashlib.sha256(

            payload.encode("utf-8")

        ).hexdigest()

    ##################################################################
    # Equality
    ##################################################################

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(other, Graph):

            return False

        return (

            self.to_dict()

            ==

            other.to_dict()
        )

    ##################################################################
    # Hash
    ##################################################################

    def __hash__(self) -> int:

        return hash(
            self.structural_hash
        )

    ##################################################################
    # Representation
    ##################################################################

    def summary(
        self,
    ) -> Dict[str, Any]:

        return {

            "nodes": self.order(),

            "edges": self.size(),

            "directed": self._directed,

            "weighted": any(
                edge.weight != 1.0
                for edge in self.edges()
            ),

            "density": self.density(),

            "hash": self.structural_hash,
        }

    def __repr__(self) -> str:

        weighted = any(
            edge.weight != 1.0
            for edge in self.edges()
        )

        return (
            "\n"
            "Graph\n"
            "-----\n"
            f"Nodes      : {self.order()}\n"
            f"Edges      : {self.size()}\n"
            f"Directed   : {self._directed}\n"
            f"Weighted   : {weighted}\n"
            f"Density    : {self.density():.6f}\n"
            f"Hash       : {self.structural_hash[:16]}"
        )
