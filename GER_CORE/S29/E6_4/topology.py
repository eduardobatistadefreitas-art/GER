"""
============================================================
GER
S29-E6.4

Topology Analysis
============================================================

Topological analysis of the Relational Signature Space.

This module computes the intrinsic topological observables
of the Signature Graph.

It performs NO statistical aggregation and NO persistence.

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

from GER.CORE.GRAPH.graph_algorithms import (
    summary,
    degree_distribution,
    adjacency_matrix,
    laplacian_matrix,
    connected_components,
    largest_component,
)


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass(frozen=True)
class ConnectivityResults:

    connected_components: int

    largest_component: int

    connected: bool


@dataclass(frozen=True)
class SpectralResults:

    adjacency_matrix: list

    laplacian_matrix: list

    #
    # Filled in future versions
    #

    lambda2: float = 0.0

    spectral_gap: float = 0.0


@dataclass(frozen=True)
class DescriptiveResults:

    degree_distribution: dict

    clustering: float = 0.0

    modularity: float = 0.0


@dataclass(frozen=True)
class SummaryResults:

    nodes: int

    edges: int

    isolated: int


@dataclass(frozen=True)
class TopologyResults:

    summary: SummaryResults

    connectivity: ConnectivityResults

    descriptive: DescriptiveResults

    spectral: SpectralResults


# ============================================================
# MAIN ANALYSIS
# ============================================================

def run(graph) -> TopologyResults:
    """
    Computes every topological observable.
    """

    info = summary(graph)

    return TopologyResults(

        summary=SummaryResults(

            nodes=info["nodes"],

            edges=info["edges"],

            isolated=info["isolated"],

        ),

        connectivity=ConnectivityResults(

            connected_components=len(
                connected_components(graph)
            ),

            largest_component=len(
                largest_component(graph)
            ),

            connected=info["connected"],

        ),

        descriptive=DescriptiveResults(

            degree_distribution=degree_distribution(
                graph
            ),

        ),

        spectral=SpectralResults(

            adjacency_matrix=adjacency_matrix(
                graph
            ),

            laplacian_matrix=laplacian_matrix(
                graph
            ),

        ),

    )


# ============================================================
# PUBLIC SYMBOLS
# ============================================================

__all__ = [

    "ConnectivityResults",

    "SpectralResults",

    "DescriptiveResults",

    "SummaryResults",

    "TopologyResults",

    "run",

]
