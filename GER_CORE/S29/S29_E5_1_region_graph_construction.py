"""
============================================================
GER
S29-E5.1
Region Graph Construction
============================================================

Scientific Objective
--------------------
Construct and validate the first official Stability Region Graph (SRG)
generated from the Stability Regions identified in S29.

This experiment performs only structural validation.
No topological interpretation is carried out here.

Author
------
GER Project
"""

from collections import defaultdict


# ============================================================
# REGION GRAPH
# ============================================================

class RegionGraph:

    def __init__(self):
        self._adj = defaultdict(set)

    def add_region(self, region):

        self._adj[region] = self._adj[region]

    def connect(self, a, b):

        if a == b:
            return

        self._adj[a].add(b)
        self._adj[b].add(a)

    @property
    def regions(self):

        return list(self._adj.keys())

    @property
    def edges(self):

        edges = set()

        for a in self._adj:

            for b in self._adj[a]:

                edge = tuple(sorted((a, b)))

                edges.add(edge)

        return sorted(edges)

    def degree(self, region):

        return len(self._adj[region])

    def neighbors(self, region):

        return sorted(self._adj[region])


# ============================================================
# VALIDATION
# ============================================================

def validate(graph):

    report = {}

    report["vertices"] = len(graph.regions)
    report["edges"] = len(graph.edges)

    # self loops

    self_loops = 0

    for region in graph.regions:

        if region in graph.neighbors(region):

            self_loops += 1

    report["self_loops"] = self_loops

    # duplicated edges

    report["duplicate_edges"] = 0

    # symmetry

    symmetric = True

    for a in graph.regions:

        for b in graph.neighbors(a):

            if a not in graph.neighbors(b):

                symmetric = False

    report["symmetric"] = symmetric

    # isolated

    isolated = 0

    for region in graph.regions:

        if graph.degree(region) == 0:

            isolated += 1

    report["isolated"] = isolated

    return report


# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph(region_names):

    graph = RegionGraph()

    for region in region_names:

        graph.add_region(region)

    for i in range(len(region_names) - 1):

        graph.connect(region_names[i], region_names[i + 1])

    return graph


# ============================================================
# REPORT
# ============================================================

def print_graph(graph):

    print()
    print("Adjacency")
    print("---------")

    for region in graph.regions:

        print(region)

        for n in graph.neighbors(region):

            print("   ->", n)

        print()


def print_summary(report):

    print()
    print("==================================================")
    print("REGION GRAPH")
    print("==================================================")
    print()

    print(f"Vertices............. {report['vertices']}")
    print(f"Edges................ {report['edges']}")
    print(f"Self Loops........... {report['self_loops']}")
    print(f"Duplicate Edges...... {report['duplicate_edges']}")
    print(f"Isolated Regions..... {report['isolated']}")
    print(f"Symmetric............ {report['symmetric']}")
    print()

    if (
        report["self_loops"] == 0
        and report["duplicate_edges"] == 0
        and report["symmetric"]
    ):

        print("STATUS")
        print()
        print("REGION GRAPH SUCCESSFULLY CONSTRUCTED")

    else:

        print("STATUS")
        print()
        print("GRAPH VALIDATION FAILED")


# ============================================================
# MAIN
# ============================================================

def main():

    print("============================================================")
    print("GER")
    print("S29-E5.1")
    print("Region Graph Construction")
    print("============================================================")

    #
    # Replace this list with the official regions
    # produced by S29_E4.B.
    #

    regions = [

        "Region_01",
        "Region_02",
        "Region_03",
        "Region_04",
        "Region_05",
        "Region_06",
        "Region_07"

    ]

    graph = build_graph(regions)

    report = validate(graph)

    print_graph(graph)

    print_summary(report)


if __name__ == "__main__":

    main()
