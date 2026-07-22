"""
============================================================
GER
S29-E6.2

Statistical Analysis Module
============================================================

This module computes descriptive statistics for the
Relational Signature Space.

Input
-----
DistanceMatrix
TopologyResults

Output
------
StatisticsResults

This module NEVER interprets scientific results.
It only computes descriptive statistics.

Author : GER Project
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

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

def compute_distance_statistics(distance_matrix) -> DistanceStatistics:
    """
    Computes descriptive statistics of the distance matrix.
    """

    values = np.asarray(distance_matrix).flatten()

    return DistanceStatistics(
        minimum=float(np.min(values)),
        maximum=float(np.max(values)),
        mean=float(np.mean(values)),
        median=float(np.median(values)),
        std=float(np.std(values)),
    )


def compute_topology_statistics(topology) -> TopologyStatistics:
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


def compute_summary(distance_matrix, graph) -> StatisticsSummary:
    """
    Computes general experiment statistics.
    """

    return StatisticsSummary(
        signature_count=len(distance_matrix),
        graph_nodes=graph.number_of_nodes(),
        graph_edges=graph.number_of_edges(),
    )


# ============================================================
# PUBLIC INTERFACE
# ============================================================

def run(distance_matrix, graph, topology) -> StatisticsResults:
    """
    Executes the statistical analysis.

    Parameters
    ----------
    distance_matrix
        Pairwise distance matrix.

    graph
        Graph representation.

    topology
        TopologyResults object.

    Returns
    -------
    StatisticsResults
    """

    distance = compute_distance_statistics(distance_matrix)

    topology_stats = compute_topology_statistics(topology)

    summary = compute_summary(distance_matrix, graph)

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
