"""
GER CORE
GRAPH

Core graph implementation.
"""

from __future__ import annotations

from typing import Any

from .node import Node
from .edge import Edge


class Graph:
    """
    Mathematical graph.

    The graph is responsible for storing nodes and edges and
    defining the graph topology.
    """

    def __init__(self) -> None:
        self._nodes: dict[Any, Node] = {}
        self._edges: list[Edge] = []

    # ==========================================================
    # Nodes
    # ==========================================================

    def add_node(self, node: Node) -> None:
        """
        Add a node to the graph.
        """
        self._nodes[node.id] = node

    def has_node(self, node_id: Any) -> bool:
        """
        Return True if the node exists.
        """
        return node_id in self._nodes

    def get_node(self, node_id: Any) -> Node:
        """
        Return a node by its identifier.
        """
        return self._nodes[node_id]

    @property
    def nodes(self) -> tuple[Node, ...]:
        """
        Immutable view of graph nodes.
        """
        return tuple(self._nodes.values())

    # ==========================================================
    # Edges
    # ==========================================================

    def add_edge(self, edge: Edge) -> None:
        """
        Add an edge to the graph.

        Both endpoints must already exist.
        """
        if edge.source not in self._nodes:
            raise ValueError(f"Unknown node: {edge.source}")

        if edge.target not in self._nodes:
            raise ValueError(f"Unknown node: {edge.target}")

        self._edges.append(edge)

    @property
    def edges(self) -> tuple[Edge, ...]:
        """
        Immutable view of graph edges.
        """
        return tuple(self._edges)

    # ==========================================================
    # Basic properties
    # ==========================================================

    @property
    def number_of_nodes(self) -> int:
        return len(self._nodes)

    @property
    def number_of_edges(self) -> int:
        return len(self._edges)

    def clear(self) -> None:
        """
        Remove all graph contents.
        """
        self._nodes.clear()
        self._edges.clear()

    # ==========================================================
    # Python protocol
    # ==========================================================

    def __len__(self) -> int:
        return self.number_of_nodes

    def __contains__(self, node_id: Any) -> bool:
        return self.has_node(node_id)

    def __iter__(self):
        return iter(self._nodes.values())

    def __repr__(self) -> str:
        return (
            f"Graph("
            f"nodes={self.number_of_nodes}, "
            f"edges={self.number_of_edges})"
        )
