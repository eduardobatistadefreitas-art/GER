"""
==============================================================================
GER S29-E6
Structural Graph Sampling
==============================================================================

Objective
---------
Construct the first experimental RegionGraph of the Signature Space.

Unlike the permanent CORE classes, this experiment defines the scientific
criterion used to connect Regions. The resulting graph is then persisted
using the public geometry API.

Inputs
------
RESULTS/S29_E5_signature_space.json

Outputs
-------
RESULTS/S29_E6_region_graph.json
RESULTS/S29_E6_adjacency_matrix.csv
RESULTS/S29_E6_adjacency_list.json
RESULTS/S29_E6_summary.txt

Author
------
GER Project
"""

from math import dist
from __future__ import annotations

from pathlib import Path
import csv
import json
from itertools import combinations

from GER.CORE.geometry.region_graph import RegionGraph
from GER.CORE.geometry.region_io import RegionIO


# =============================================================================
# Configuration
# =============================================================================

RESULTS = Path("RESULTS")

SIGNATURE_SPACE_FILE = (
    RESULTS / "S29_E5_signature_space.json"
)

GRAPH_FILE = (
    RESULTS / "S29_E6_region_graph.json"
)

ADJACENCY_LIST_FILE = (
    RESULTS / "S29_E6_adjacency_list.json"
)

ADJACENCY_MATRIX_FILE = (
    RESULTS / "S29_E6_adjacency_matrix.csv"
)

SUMMARY_FILE = (
    RESULTS / "S29_E6_summary.txt"
)


# =============================================================================
# Signature factory
# =============================================================================

class ExperimentalSignature:
    """
    Minimal signature representation required only for
    SignatureSpace deserialization.

    The scientific content of the signature is already frozen.
    The experiment only needs its identity and stored attributes.
    """

    def __init__(self, data):

        self.id = data["id"]
        self._data = dict(data)

    def as_dict(self):

        return dict(self._data)


def signature_factory(data):

    return ExperimentalSignature(data)


# =============================================================================
# Loading
# =============================================================================

def load_signature_space():

    if not SIGNATURE_SPACE_FILE.exists():
        raise FileNotFoundError(
            SIGNATURE_SPACE_FILE
        )

    print("=" * 72)
    print("Loading Signature Space")
    print("=" * 72)

    space = RegionIO.load_signature_space(
        SIGNATURE_SPACE_FILE,
        signature_factory,
    )

    print()

    summary = space.summary()

    print("Space ID        :", summary["id"])
    print("Signatures      :", summary["signatures"])
    print("Regions         :", summary["regions"])
    print("Assigned        :", summary["assigned"])
    print()

    return space


# =============================================================================
# Experimental adjacency criterion
# =============================================================================


def regions_are_adjacent(
    region_a,
    region_b,
):

    if region_a.centroid is None:
        return False

    if region_b.centroid is None:
        return False

    if region_a.radius is None:
        return False

    if region_b.radius is None:
        return False

    d = dist(
        region_a.centroid,
        region_b.centroid,
    )

    limit = (
        region_a.radius +
        region_b.radius
    )

    return d <= limit
    """
    Experimental adjacency criterion.

    IMPORTANT

    This function belongs to GER_CORE.

    The CORE never defines scientific hypotheses.

    Future versions of S29 may replace this criterion
    without modifying RegionGraph.
    """

    if (
        region_a.centroid is None
        or
        region_b.centroid is None
    ):
        return False

    if (
        region_a.radius is None
        or
        region_b.radius is None
    ):
        return False

    #
    # Placeholder.
    #
    # The experimental criterion will be refined during
    # the following S29 experiments.
    #

    return False


# =============================================================================
# Graph construction
# =============================================================================

def build_region_graph(space):

    print("=" * 72)
    print("Constructing Region Graph")
    print("=" * 72)

    graph = RegionGraph(space)

    region_ids = sorted(space.region_ids())

    total_pairs = 0
    total_edges = 0

    for region_a_id, region_b_id in combinations(
        region_ids,
        2,
    ):

        region_a = space.region(region_a_id)
        region_b = space.region(region_b_id)

        total_pairs += 1

        if regions_are_adjacent(
            region_a,
            region_b,
        ):

            graph.connect(
                region_a_id,
                region_b_id,
            )

            total_edges += 1

    print()

    print("Candidate pairs :", total_pairs)
    print("Connected edges :", total_edges)
    print()

    return graph
  # =============================================================================
# Statistics
# =============================================================================

def compute_graph_statistics(graph):

    print("=" * 72)
    print("Graph Statistics")
    print("=" * 72)

    summary = graph.summary()

    vertices = graph.vertices()
    edges = graph.edges()

    degrees = {
        region_id: graph.degree(region_id)
        for region_id in vertices
    }

    if degrees:
        average_degree = (
            sum(degrees.values()) / len(degrees)
        )
    else:
        average_degree = 0.0

    density = 0.0

    n = len(vertices)

    if n > 1:
        density = (
            2.0 * len(edges)
        ) / (
            n * (n - 1)
        )

    statistics = {
        "vertices": len(vertices),
        "edges": len(edges),
        "connected": summary["connected"],
        "average_degree": average_degree,
        "density": density,
        "degrees": degrees,
        "maximum_degree": max(degrees.values()) if degrees else 0,
        "minimum_degree": min(degrees.values()) if degrees else 0,
    }

    print(f"Vertices .......... {statistics['vertices']}")
    print(f"Edges ............. {statistics['edges']}")
    print(f"Connected ......... {statistics['connected']}")
    print(f"Average degree .... {statistics['average_degree']:.3f}")
    print(f"Density ........... {statistics['density']:.6f}")
    print()

    return statistics


# =============================================================================
# Persistence
# =============================================================================

def save_adjacency_list(graph):

    adjacency = {}

    for region_id in graph.vertices():

        adjacency[region_id] = list(
            graph.neighbors(region_id)
        )

    with ADJACENCY_LIST_FILE.open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            adjacency,
            fp,
            indent=4,
            ensure_ascii=False,
        )


def save_adjacency_matrix(graph):

    vertices = list(
        graph.vertices()
    )

    with ADJACENCY_MATRIX_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fp:

        writer = csv.writer(fp)

        writer.writerow(
            ["Region"] + vertices
        )

        for row in vertices:

            values = []

            for column in vertices:

                values.append(
                    int(
                        graph.has_edge(
                            row,
                            column,
                        )
                    )
                )

            writer.writerow(
                [row] + values
            )


def save_summary(
    graph,
    statistics,
):

    with SUMMARY_FILE.open(
        "w",
        encoding="utf-8",
    ) as fp:

        fp.write(
            "============================================================\n"
        )
        fp.write(
            "GER S29-E6 Structural Graph Sampling\n"
        )
        fp.write(
            "============================================================\n\n"
        )

        fp.write(
            f"Vertices          : {statistics['vertices']}\n"
        )

        fp.write(
            f"Edges             : {statistics['edges']}\n"
        )

        fp.write(
            f"Connected         : {statistics['connected']}\n"
        )

        fp.write(
            f"Average Degree    : {statistics['average_degree']:.6f}\n"
        )

        fp.write(
            f"Density           : {statistics['density']:.6f}\n\n"
        )
        fp.write(
            f"Maximum Degree    : {statistics['maximum_degree']}\n"
        )

        fp.write(
            f"Minimum Degree    : {statistics['minimum_degree']}\n"
        )

        fp.write("Degrees\n")
        fp.write("-----------------------------\n")

        for region_id in sorted(
            statistics["degrees"]
        ):

            fp.write(
                f"{region_id:<12}"
                f"{statistics['degrees'][region_id]}\n"
            )

        fp.write("\n")

        fp.write("Edges\n")
        fp.write("-----------------------------\n")

        for edge in graph.edges():

            fp.write(
                f"{edge[0]} <-> {edge[1]}\n"
            )


def save_results(
    graph,
    statistics,
):

    print("=" * 72)
    print("Saving Results")
    print("=" * 72)

    RegionIO.save_region_graph(
        graph,
        GRAPH_FILE,
    )

    save_adjacency_list(graph)

    save_adjacency_matrix(graph)

    save_summary(
        graph,
        statistics,
    )

    print()

    print("Saved:")

    print("  ", GRAPH_FILE)
    print("  ", ADJACENCY_LIST_FILE)
    print("  ", ADJACENCY_MATRIX_FILE)
    print("  ", SUMMARY_FILE)
    print()
  # =============================================================================
# Main
# =============================================================================

def main():

    print()
    print("=" * 72)
    print("GER S29-E6")
    print("Structural Graph Sampling")
    print("=" * 72)
    print()

    RESULTS.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------------------
    # Load Signature Space
    # -------------------------------------------------------------------------

    space = load_signature_space()

    # -------------------------------------------------------------------------
    # Build Region Graph
    # -------------------------------------------------------------------------

    graph = build_region_graph(space)

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    statistics = compute_graph_statistics(graph)

    # -------------------------------------------------------------------------
    # Save
    # -------------------------------------------------------------------------

    save_results(
        graph,
        statistics,
    )

    # -------------------------------------------------------------------------
    # Final report
    # -------------------------------------------------------------------------

    print("=" * 72)
    print("Experiment Completed")
    print("=" * 72)
    print()

    print("Summary")
    print("-------")

    print(
        f"Regions ............ {statistics['vertices']}"
    )

    print(
        f"Connections ........ {statistics['edges']}"
    )

    print(
        f"Connected graph .... {statistics['connected']}"
    )

    print(
        f"Average degree ..... "
        f"{statistics['average_degree']:.3f}"
    )

    print(
        f"Density ............ "
        f"{statistics['density']:.6f}"
    )

    print()

    print("Generated files")

    print("  •", GRAPH_FILE.name)
    print("  •", ADJACENCY_LIST_FILE.name)
    print("  •", ADJACENCY_MATRIX_FILE.name)
    print("  •", SUMMARY_FILE.name)

    print()
    print("=" * 72)
    print("End")
    print("=" * 72)


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    main()
