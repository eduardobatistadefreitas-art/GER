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
SignatureCollection
Graph
TopologyResults

Output
------
StatisticsResults

This module NEVER computes topology or graph operators.

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

from dataclasses import dataclass

import numpy as np

from .topology import TopologyResults


# ============================================================
# RESULT STRUCTURES
# ============================================================

@dataclass(frozen=True)
class DistanceStatistics:

    minimum: float

    maximum: float

    mean: float

    median: float

    std: float


@dataclass(frozen=True)
class SummaryStatistics:

    signature_count: int

    graph_nodes: int

    graph_edges: int


@dataclass(frozen=True)
class StatisticsResults:

    distance: DistanceStatistics

    topology: TopologyResults

    summary: SummaryStatistics


# ============================================================
# INTERNAL COMPUTATIONS
# ============================================================

def compute_distance_statistics(collection):

    D = collection.distance_matrix()

    values = D[np.triu_indices_from(D, k=1)]

    return DistanceStatistics(

        minimum=float(np.min(values)),

        maximum=float(np.max(values)),

        mean=float(np.mean(values)),

        median=float(np.median(values)),

        std=float(np.std(values)),

    )


def compute_summary(collection, graph):

    return SummaryStatistics(

        signature_count=len(collection),

        graph_nodes=graph.number_of_nodes(),

        graph_edges=graph.number_of_edges(),

    )


# ============================================================
# PUBLIC INTERFACE
# ============================================================

def run(
    collection,
    graph,
    topology: TopologyResults,
) -> StatisticsResults:
    """
    Executes the statistical analysis.
    """

    distance = compute_distance_statistics(
        collection
    )

    summary = compute_summary(
        collection,
        graph,
    )

    return StatisticsResults(

        distance=distance,

        topology=topology,

        summary=summary,

    )


# ============================================================
# PUBLIC SYMBOLS
# ============================================================

__all__ = [

    "DistanceStatistics",

    "SummaryStatistics",

    "StatisticsResults",

    "run",

]
