"""
============================================================
GER
S29-E6.2

Report Module
============================================================

Builds the official report of S29-E6.2.

This module NEVER computes scientific quantities.

Persistence is delegated to the GER CORE.

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

from dataclasses import asdict

from GER.CORE.results_repository import ResultsRepository

from .statistics import StatisticsResults


# ============================================================
# REPORT BUILDERS
# ============================================================

def build_report(results: StatisticsResults) -> dict:
    """
    Complete machine-readable report.
    """

    return {

        "experiment": "S29-E6.2",

        "module": "Relational Signature Space",

        "version": "1.0",

        "results": asdict(results),

    }


def build_summary(results: StatisticsResults) -> str:
    """
    Human-readable summary.
    """

    s = results.summary
    d = results.distance
    t = results.topology

    lines = []

    lines.append("=" * 60)
    lines.append("GER")
    lines.append("S29-E6.2")
    lines.append("Relational Signature Space")
    lines.append("=" * 60)
    lines.append("")

    lines.append("Summary")
    lines.append("-" * 60)

    lines.append(f"Signatures            : {s.signature_count}")
    lines.append(f"Graph Nodes          : {s.graph_nodes}")
    lines.append(f"Graph Edges          : {s.graph_edges}")

    lines.append("")

    lines.append("Distance Statistics")
    lines.append("-" * 60)

    lines.append(f"Minimum              : {d.minimum:.6f}")
    lines.append(f"Maximum              : {d.maximum:.6f}")
    lines.append(f"Mean                 : {d.mean:.6f}")
    lines.append(f"Median               : {d.median:.6f}")
    lines.append(f"Standard Deviation   : {d.std:.6f}")

    lines.append("")

    lines.append("Topology")
    lines.append("-" * 60)

    lines.append(
        f"Connected            : {t.connectivity.connected}"
    )

    lines.append(
        f"Components           : {t.connectivity.connected_components}"
    )

    lines.append(
        f"Largest Component    : {t.connectivity.largest_component}"
    )

    lines.append(
        f"Isolated Nodes       : {t.summary.isolated}"
    )

    lines.append("")

    lines.append("Spectral")
    lines.append("-" * 60)

    lines.append(
        f"Lambda2              : {t.spectral.lambda2:.6f}"
    )

    lines.append(
        f"Spectral Gap         : {t.spectral.spectral_gap:.6f}"
    )

    lines.append("")

    lines.append("Descriptive")
    lines.append("-" * 60)

    lines.append(
        f"Clustering           : {t.descriptive.clustering:.6f}"
    )

    lines.append(
        f"Modularity           : {t.descriptive.modularity:.6f}"
    )

    return "\n".join(lines)


# ============================================================
# PUBLIC INTERFACE
# ============================================================

def run(
    results: StatisticsResults,
    repository: ResultsRepository,
):
    """
    Generates every official experiment output.
    """

    repository.save_json(

        "results",

        build_report(results),

    )

    repository.save_text(

        "summary",

        build_summary(results),

    )


# ============================================================
# PUBLIC SYMBOLS
# ============================================================

__all__ = [

    "build_report",

    "build_summary",

    "run",

]
