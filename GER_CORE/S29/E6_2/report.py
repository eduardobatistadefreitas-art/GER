"""
============================================================
GER
S29-E6.2

Report Module
============================================================

Generates the official outputs of the experiment.

Input
-----
StatisticsResults

Output
------
JSON
CSV
TXT

This module NEVER computes scientific quantities.
It only exports results.

Author : GER Project
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import json
import csv


# ============================================================
# INTERNAL WRITERS
# ============================================================

def write_json(results, output_dir: Path) -> None:
    """
    Writes complete results in JSON format.
    """

    filepath = output_dir / "results.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            asdict(results),
            f,
            indent=4,
            ensure_ascii=False,
        )


def write_csv(results, output_dir: Path) -> None:
    """
    Writes flattened results in CSV format.
    """

    filepath = output_dir / "results.csv"

    flat = {}

    for section, values in asdict(results).items():
        for key, value in values.items():
            flat[f"{section}.{key}"] = value

    with open(filepath, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["Observable", "Value"])

        for key, value in flat.items():
            writer.writerow([key, value])


def write_summary(results, output_dir: Path) -> None:
    """
    Writes a human-readable summary.
    """

    filepath = output_dir / "summary.txt"

    s = results.summary
    d = results.distance
    t = results.topology

    with open(filepath, "w", encoding="utf-8") as f:

        f.write("========================================\n")
        f.write("GER\n")
        f.write("S29-E6.2\n")
        f.write("Relational Signature Space\n")
        f.write("========================================\n\n")

        f.write("Summary\n")
        f.write("----------------------------------------\n")
        f.write(f"Signatures           : {s.signature_count}\n")
        f.write(f"Graph Nodes          : {s.graph_nodes}\n")
        f.write(f"Graph Edges          : {s.graph_edges}\n\n")

        f.write("Distance Statistics\n")
        f.write("----------------------------------------\n")
        f.write(f"Minimum              : {d.minimum:.6f}\n")
        f.write(f"Maximum              : {d.maximum:.6f}\n")
        f.write(f"Mean                 : {d.mean:.6f}\n")
        f.write(f"Median               : {d.median:.6f}\n")
        f.write(f"Std                  : {d.std:.6f}\n\n")

        f.write("Topology\n")
        f.write("----------------------------------------\n")
        f.write(f"Connected Components : {t.connected_components}\n")
        f.write(f"Largest Component    : {t.largest_component}\n")
        f.write(f"Lambda2              : {t.lambda2:.6f}\n")
        f.write(f"Clustering           : {t.clustering:.6f}\n")
        f.write(f"Modularity           : {t.modularity:.6f}\n")


def write_metadata(output_dir: Path) -> None:
    """
    Writes execution metadata.
    """

    filepath = output_dir / "metadata.json"

    metadata = {
        "experiment": "S29-E6.2",
        "module": "Relational Signature Space",
        "version": "1.0",
    }

    with open(filepath, "w", encoding="utf-8") as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False,
        )


# ============================================================
# PUBLIC INTERFACE
# ============================================================

def run(results, output_dir) -> None:
    """
    Generates every experiment output.
    """

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_json(results, output_dir)

    write_csv(results, output_dir)

    write_summary(results, output_dir)

    write_metadata(output_dir)


# ============================================================
# PUBLIC SYMBOLS
# ============================================================

__all__ = [
    "run",
]
