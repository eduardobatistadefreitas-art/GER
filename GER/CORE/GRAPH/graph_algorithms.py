"""
============================================================
GER
GRAPH Algorithms
============================================================

Reusable graph algorithms for the GER framework.

These algorithms are completely independent of any
scientific experiment.

They operate on the generic Graph API.

Author
------
Eduardo Batista de Freitas

Framework
---------
GER

Version
-------
1.0
"""

from __future__ import annotations

from collections import deque


# ============================================================
# Basic access
# ============================================================

def nodes(graph):
    """
    Returns the list of nodes.
    """
    return list(graph.nodes())


def edges(graph):
    """
    Returns the list of edges.
    """
    return list(graph.edges())


# ============================================================
# Neighborhood
# ============================================================

def neighbors(graph, node):
    """
    Returns all neighbors of a node.
    """

    result = []

    for edge in graph.edges():

        if edge.source == node:
            result.append(edge.target)

        elif edge.target == node:
            result.append(edge.source)

    return result


def degree(graph, node):
    """
    Node degree.
    """
    return len(neighbors(graph, node))


def degree_distribution(graph):
    """
    Degree distribution.
    """
    return {
        node: degree(graph, node)
        for node in graph.nodes()
    }


# ============================================================
# Connectivity
# ============================================================

def connected_components(graph):
    """
    Connected components using BFS.
    """

    visited = set()
    components = []

    for node in graph.nodes():

        if node in visited:
            continue

        queue = deque([node])

        component = []

        visited.add(node)

        while queue:

            current = queue.popleft()

            component.append(current)

            for nxt in neighbors(graph, current):

                if nxt not in visited:

                    visited.add(nxt)

                    queue.append(nxt)

        components.append(component)

    return components


def number_of_connected_components(graph):

    return len(connected_components(graph))


def largest_component(graph):

    components = connected_components(graph)

    if not components:
        return []

    return max(
        components,
        key=len,
    )


def is_connected(graph):

    return (
        number_of_connected_components(graph)
        == 1
    )


# ============================================================
# Isolated vertices
# ============================================================

def isolated_nodes(graph):

    return [

        node

        for node in graph.nodes()

        if degree(graph, node) == 0

    ]


# ============================================================
# Matrices
# ============================================================

def adjacency_matrix(graph):

    nodes_list = list(graph.nodes())

    index = {

        node: i

        for i, node in enumerate(nodes_list)

    }

    n = len(nodes_list)

    A = [[0] * n for _ in range(n)]

    for edge in graph.edges():

        i = index[edge.source]

        j = index[edge.target]

        A[i][j] = 1

        A[j][i] = 1

    return A


def laplacian_matrix(graph):

    A = adjacency_matrix(graph)

    n = len(A)

    L = [[0] * n for _ in range(n)]

    for i in range(n):

        degree_i = sum(A[i])

        L[i][i] = degree_i

        for j in range(n):

            if i != j:

                L[i][j] = -A[i][j]

    return L


# ============================================================
# Convenience
# ============================================================

def summary(graph):

    return {

        "nodes":
            graph.number_of_nodes,

        "edges":
            graph.number_of_edges,

        "connected":
            is_connected(graph),

        "components":
            number_of_connected_components(graph),

        "largest_component":
            len(largest_component(graph)),

        "isolated":
            len(isolated_nodes(graph)),

    }


# ============================================================
# Public symbols
# ============================================================

__all__ = [

    "nodes",

    "edges",

    "neighbors",

    "degree",

    "degree_distribution",

    "connected_components",

    "number_of_connected_components",

    "largest_component",

    "is_connected",

    "isolated_nodes",

    "adjacency_matrix",

    "laplacian_matrix",

    "summary",

  ]
