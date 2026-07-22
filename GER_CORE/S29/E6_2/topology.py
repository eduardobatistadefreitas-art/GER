"""
============================================================
GER
S29-E6.2
Topology Analysis
============================================================

Topological analysis of the Relational Signature Space.

This module consumes the generic graph algorithms provided
by GER.CORE.GRAPH and computes the structural observables
used by S29-E6.2.

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

from GER.CORE.GRAPH.graph_algorithms import (
    summary,
    degree_distribution,
    adjacency_matrix,
    laplacian_matrix,
)


# ============================================================
# Analysis
# ============================================================

def run(graph):
    """
    Compute topological observables.
    """

    graph_summary = summary(graph)

    degree_stats = degree_distribution(graph)

    adjacency = adjacency_matrix(graph)

    laplacian = laplacian_matrix(graph)

    return {

        "summary":
            graph_summary,

        "degree_distribution":
            degree_stats,

        "adjacency_matrix":
            adjacency,

        "laplacian_matrix":
            laplacian,

    }


# ============================================================
# Convenience
# ============================================================

def compute_summary(graph):
    """
    Alias for report generation.
    """

    return run(graph)


__all__ = [

    "run",

    "compute_summary",

]
