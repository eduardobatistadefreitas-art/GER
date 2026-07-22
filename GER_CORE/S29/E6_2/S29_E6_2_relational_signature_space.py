"""
============================================================
GER
S29-E6.2

Intrinsic Geometry of the Relational Signature Space

Main Experiment
============================================================

Pipeline

Load Signatures
        │
        ▼
Distance Matrix
        │
        ▼
Graph Construction
        │
        ▼
Topology Analysis
        │
        ▼
Statistical Analysis
        │
        ▼
Report Generation

Author : GER Project
"""

from pathlib import Path

from .config import Config
from . import io
from . import metrics
from . import topology
from . import statistics
from . import report

# Graph is provided by GER CORE
from GER.CORE.graph import Graph


# ============================================================
# MAIN PIPELINE
# ============================================================

def run(config: Config | None = None):
    """
    Executes the complete S29-E6.2 experiment.

    Parameters
    ----------
    config
        Experiment configuration.

    Returns
    -------
    StatisticsResults
    """

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    if config is None:
        config = Config()

    print("=" * 60)
    print("GER")
    print("S29-E6.2")
    print("Intrinsic Geometry of the Relational Signature Space")
    print("=" * 60)

    # --------------------------------------------------------
    # Load signatures
    # --------------------------------------------------------

    print("\nLoading signatures...")

    signatures = io.load_signatures(config)

    print(f"Loaded signatures : {len(signatures)}")

    # --------------------------------------------------------
    # Distance Matrix
    # --------------------------------------------------------

    print("Computing distance matrix...")

    distance_matrix = metrics.run(
        signatures,
        config,
    )

    # --------------------------------------------------------
    # Graph Construction
    # --------------------------------------------------------

    print("Building graph...")

    graph = Graph.from_distance_matrix(
        distance_matrix,
        threshold=config.graph_threshold,
    )

    print(f"Nodes : {graph.number_of_nodes()}")
    print(f"Edges : {graph.number_of_edges()}")

    # --------------------------------------------------------
    # Topology
    # --------------------------------------------------------

    print("Computing topology...")

    topology_results = topology.run(
        graph,
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print("Computing statistics...")

    statistics_results = statistics.run(
        distance_matrix,
        graph,
        topology_results,
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print("Writing report...")

    report.run(
        statistics_results,
        config.output_directory,
    )

    print("\nExperiment completed.")

    return statistics_results


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
