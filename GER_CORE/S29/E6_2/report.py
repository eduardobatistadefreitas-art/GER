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
GER — Geometria Espectral Relacional

Version
-------
1.0
"""

from __future__ import annotations

from dataclasses import asdict

# CORE persistence
from GER.CORE.results_repository import ResultsRepository


# ============================================================
# Internal helpers
# ============================================================

def build_report(results) -> dict:
    """
    Builds the complete report dictionary.
    """

    return {

        "experiment": "S29-E6.2",

        "module": "Relational Signature Space",

        "version": "1.0",

        "results": asdict(results),

    }


def build_summary(results) -> str:
    """
    Human-readable summary.
    """

    s = results.summary
    d = results.distance
    t = results.topology

    lines = []

    lines.append("=" * 40)
    lines.append("GER")
    lines.append("S29-E6.2")
    lines.append("Relational Signature Space")
    lines.append("=" * 40)
    lines.append("")

    lines.append("Summary")
    lines.append("-" * 40)
    lines.append(f"Signatures        : {s.signature_count}")
    lines.append(f"Graph Nodes       : {s.graph_nodes}")
    lines.append(f"Graph Edges       : {s.graph_edges}")
    lines.append("")

    lines.append("Distance")
    lines.append("-" * 40)
    lines.append(f"Minimum           : {d.minimum:.6f}")
    lines.append(f"Maximum           : {d.maximum:.6f}")
    lines.append(f"Mean              : {d.mean:.6f}")
    lines.append(f"Median            : {d.median:.6f}")
    lines.append(f"Std               : {d.std:.6f}")
    lines.append("")

    lines.append("Topology")
    lines.append("-" * 40)
    lines.append(
        f"Connected Components : {t.connected_components}"
    )
    lines.append(
        f"Largest Component    : {t.largest_component}"
    )
    lines.append(
        f"Lambda2              : {t.lambda2:.6f}"
    )
    lines.append(
        f"Clustering           : {t.clustering:.6f}"
    )
    lines.append(
        f"Modularity           : {t.modularity:.6f}"
    )

    return "\n".join(lines)


# ============================================================
# Public interface
# ============================================================

def run(results, repository: ResultsRepository):
    """
    Generates every experiment output.

    The actual persistence is performed by the GER CORE.
    """

    report = build_report(results)

    summary = build_summary(results)

    repository.save_json(
        "results",
        report,
    )

    repository.save_text(
        "summary",
        summary,
    )


# ============================================================
# Public symbols
# ============================================================

__all__ = [
    "run",
]
