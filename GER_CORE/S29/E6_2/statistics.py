"""
============================================================
GER
S29-E6.2
Statistical Analysis Module
============================================================

Computes descriptive statistics for the
Relational Signature Space.

Input
-----

Distance Matrix
TopologyResults

Output
------

StatisticsResults

This module NEVER interprets scientific results.

Author
------
Eduardo Batista de Freitas

Framework
---------
GER — Geometria Espectral Relacional

Version
-------
1.0
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# ============================================================
# RESULT STRUCTURES
# ============================================================

@dataclass(frozen=True)
class DistanceStatistics:
    """
    Statistics computed directly from the distance matrix.
    """

    minimum: float
    maximum: float
    mean: float
    median: float
    std: float


@dataclass(frozen=True)
class TopologyStatistics:
    """
    Statistical summary of topological observables.
    """

    connected_components: int
    largest_component: int
    lambda2: float
    clustering: float
    modularity: float


@dataclass(frozen=True)
class StatisticsSummary:
    """
    Global experiment summary.
    """

    signature_count: int
    graph_nodes: int
    graph_edges: int


@dataclass(frozen=True)
class StatisticsResults:
    """
    Complete statistical report.
    """

    distance: DistanceStatistics
    topology: TopologyStatistics
    summary: StatisticsSummary


# ============================================================
# INTERNAL COMPUTATIONS
# ============================================================

def compute_distance_statistics(distance_matrix):
    """
    Computes descriptive statistics of the distance matrix.
    """

    values = np.asarray(distance_matrix)

    #
    # Ignore the diagonal (distance = 0)
    #

    values = values[np.triu_indices_from(values, k=1)]

    return DistanceStatistics(
        minimum=float(np.min(values)),
        maximum=float(np.max(values)),
        mean=float(np.mean(values)),
        median=float(np.median(values)),
        std=float(np.std(values)),
    )


def compute_topology_statistics(topology):
    """
    Extracts statistical values from TopologyResults.
    """

    return TopologyStatistics(
        connected_components=topology.connectivity.connected_components,
        largest_component=topology.connectivity.largest_component,
        lambda2=topology.spectral.lambda2,
        clustering=topology.descriptive.clustering,
        modularity=topology.descriptive.modularity,
    )


def compute_summary(collection, graph):
    """
    Computes general experiment statistics.
    """

    return StatisticsSummary(
        signature_count=len(collection),
        graph_nodes=graph.number_of_nodes(),
        graph_edges=graph.number_of_edges(),
    )


# ============================================================
# PUBLIC INTERFACE
# ============================================================

def run(collection, graph, topology):
    """
    Executes the statistical analysis.

    Parameters
    ----------
    collection
        SignatureCollection.

    graph
        Graph representation.

    topology
        TopologyResults.

    Returns
    -------
    StatisticsResults
    """

    distance = compute_distance_statistics(
        collection.distance_matrix()
    )

    topology_stats = compute_topology_statistics(
        topology
    )

    summary = compute_summary(
        collection,
        graph,
    )

    return StatisticsResults(
        distance=distance,
        topology=topology_stats,
        summary=summary,
    )


# ============================================================
# PUBLIC SYMBOLS
# ============================================================

__all__ = [
    "DistanceStatistics",
    "TopologyStatistics",
    "StatisticsSummary",
    "StatisticsResults",
    "run",
]
