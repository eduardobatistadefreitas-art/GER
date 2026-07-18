"""
============================================================
GER S29-E4
Stability Region Topology
============================================================

Objective
---------
Study the global topology of the Stability Region Space (RSG).

Inputs
------
- regions.json
- intrinsic_geometry.json

Outputs
-------
- adjacency_matrix.csv
- adjacency_list.json
- topology_metrics.json
- region_centrality.csv
- topology_report.txt
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import networkx as nx

# ============================================================
# Paths
# ============================================================

BASE = Path("RESULTS/S29")
INPUT = BASE / "S29_E3_3"
OUTPUT = BASE / "S29_E4"

OUTPUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Load data
# ============================================================

with open(INPUT / "regions.json") as f:
    regions = json.load(f)

with open(INPUT / "intrinsic_geometry.json") as f:
    geometry = json.load(f)

centers = np.array(geometry["region_centers"])
labels = geometry["region_labels"]

N = len(labels)

# ============================================================
# Distance matrix
# ============================================================

D = np.zeros((N, N))

for i in range(N):
    for j in range(N):
        D[i, j] = np.linalg.norm(
            centers[i] - centers[j]
        )

# ============================================================
# Automatic threshold
# Median nearest-neighbour distance
# ============================================================

nearest = []

for i in range(N):
    d = np.sort(D[i][D[i] > 0])[0]
    nearest.append(d)

threshold = np.median(nearest)

# ============================================================
# Graph construction
# ============================================================

G = nx.Graph()

for i in range(N):
    G.add_node(i, label=labels[i])

for i in range(N):
    for j in range(i + 1, N):

        if D[i, j] <= threshold:

            G.add_edge(
                i,
                j,
                weight=float(D[i, j])
            )

# ============================================================
# Metrics
# ============================================================

metrics = {

    "nodes": G.number_of_nodes(),

    "edges": G.number_of_edges(),

    "connected_components":
        nx.number_connected_components(G),

    "average_degree":
        float(np.mean([d for _, d in G.degree()])),

    "maximum_degree":
        int(max(dict(G.degree()).values())),

    "density":
        nx.density(G)

}

if nx.is_connected(G):

    metrics["diameter"] = nx.diameter(G)

    metrics["average_shortest_path"] = \
        nx.average_shortest_path_length(G)

else:

    metrics["diameter"] = None
    metrics["average_shortest_path"] = None

metrics["clustering"] = nx.average_clustering(G)

# ============================================================
# Centralities
# ============================================================

bet = nx.betweenness_centrality(G)

clo = nx.closeness_centrality(G)

try:
    eig = nx.eigenvector_centrality(G, max_iter=1000)
except Exception:
    eig = {k: np.nan for k in G.nodes()}

centrality = pd.DataFrame({

    "Region": labels,

    "Degree":
        [G.degree(i) for i in G.nodes()],

    "Betweenness":
        [bet[i] for i in G.nodes()],

    "Closeness":
        [clo[i] for i in G.nodes()],

    "Eigenvector":
        [eig[i] for i in G.nodes()]

})

centrality.to_csv(
    OUTPUT / "region_centrality.csv",
    index=False
)

# ============================================================
# Adjacency
# ============================================================

adj = nx.to_numpy_array(G)

pd.DataFrame(adj).to_csv(
    OUTPUT / "adjacency_matrix.csv",
    index=False
)

adj_list = {
    labels[i]:
    [labels[j] for j in G.neighbors(i)]
    for i in G.nodes()
}

with open(
    OUTPUT / "adjacency_list.json",
    "w"
) as f:
    json.dump(adj_list, f, indent=4)

# ============================================================
# Save metrics
# ============================================================

with open(
    OUTPUT / "topology_metrics.json",
    "w"
) as f:
    json.dump(metrics, f, indent=4)

# ============================================================
# Bridges and articulation points
# ============================================================

bridges = list(nx.bridges(G))

articulations = list(nx.articulation_points(G))

# ============================================================
# Report
# ============================================================

with open(
    OUTPUT / "topology_report.txt",
    "w"
) as f:

    f.write("GER S29-E4\n")
    f.write("Stability Region Topology\n\n")

    for k, v in metrics.items():
        f.write(f"{k}: {v}\n")

    f.write("\n")

    f.write(f"Bridges: {len(bridges)}\n")
    f.write(f"Articulation points: {len(articulations)}\n")

    f.write("\n")

    f.write("Region ranking\n")
    f.write("====================\n\n")

    f.write(
        centrality.sort_values(
            "Betweenness",
            ascending=False
        ).to_string(index=False)
    )

print("\nDone.")
print("--------------------------------")
print(f"Regions : {N}")
print(f"Edges   : {G.number_of_edges()}")
print(f"Components : {metrics['connected_components']}")
print("--------------------------------")
