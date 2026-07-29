"""
=============================================================
S20_RELATIONAL_DYNAMICS.py
=============================================================

Consolidação experimental do bloco S16–S20.

Produz:

/content/drive/MyDrive/GER_RESULTS/S20/

    dynamics_summary.json
    dynamics_report.txt
    evolution.csv

=============================================================
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import networkx as nx
import numpy as np

# ============================================================
# CONFIGURAÇÃO
# ============================================================

OUTPUT = Path("/content/drive/MyDrive/GER_RESULTS/S20")
OUTPUT.mkdir(parents=True, exist_ok=True)

N = 40
P = 0.10
STEPS = 20

ALPHA = 0.50
BETA = 0.20
GAMMA = 0.30
LR = 0.05

rng = np.random.default_rng(42)

# ============================================================
# GRAFO
# ============================================================

G = nx.erdos_renyi_graph(N, P, seed=42)

if not nx.is_connected(G):
    largest = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest).copy()

N = G.number_of_nodes()

# ============================================================
# κ_eff
# Proxy: número de caminhos simples até profundidade 3
# ============================================================

def kappa_eff(graph):

    K = np.zeros((N, N))

    for i in graph.nodes():
        for j in graph.nodes():

            if i == j:
                continue

            try:
                paths = list(
                    nx.all_simple_paths(
                        graph,
                        i,
                        j,
                        cutoff=3
                    )
                )

                K[i, j] = len(paths)

            except nx.NetworkXNoPath:
                K[i, j] = 0

    return K

# ============================================================
# Δ_rel
# ============================================================

def delta_rel(graph, K):

    D = np.zeros_like(K)

    for a in graph.nodes():

        neigh = list(graph.neighbors(a))

        if len(neigh) == 0:
            continue

        avg = np.mean(K[neigh], axis=0)

        D[a] = avg - K[a]

    return D

# ============================================================
# Γ2 proxy
# ============================================================

def gamma2_proxy(graph, K):

    L = nx.laplacian_matrix(graph).astype(float).toarray()

    return L @ K @ L

# ============================================================
# AÇÃO
# ============================================================

def action(K, D, G2):

    return (
        np.sum(G2)
        - ALPHA * np.sum(D**2)
        - BETA * np.sum(K)
    )

# ============================================================
# EVOLUÇÃO
# ============================================================

history = []

previous_edges = set(G.edges())

for step in range(STEPS):

    K = kappa_eff(G)

    D = delta_rel(G, K)

    G2 = gamma2_proxy(G, K)

    S = action(K, D, G2)

    mean_kappa = float(np.mean(K))

    mean_gamma2 = float(np.mean(G2))

    density = nx.density(G)

    # força local simplificada

    force = G2 - ALPHA * D + GAMMA * K

    threshold = np.mean(force)

    # remove aresta aleatória

    if G.number_of_edges() > 0:

        edge = list(G.edges())[rng.integers(G.number_of_edges())]

        G.remove_edge(*edge)

    # adiciona aresta segundo força

    i, j = np.unravel_index(
        np.argmax(force),
        force.shape
    )

    if i != j:
        G.add_edge(int(i), int(j))

    current_edges = set(G.edges())

    changes = len(previous_edges.symmetric_difference(current_edges))

    previous_edges = current_edges

    history.append({

        "step": step,

        "action": float(S),

        "mean_kappa": mean_kappa,

        "mean_gamma2": mean_gamma2,

        "density": density,

        "edge_changes": changes

    })

# ============================================================
# CSV
# ============================================================

csv_file = OUTPUT / "evolution.csv"

with open(csv_file, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=history[0].keys()
    )

    writer.writeheader()

    writer.writerows(history)

# ============================================================
# CLASSIFICAÇÃO
# ============================================================

gamma_series = np.array(
    [h["mean_gamma2"] for h in history]
)

variation = float(np.std(gamma_series))

if variation < 1e-6:
    regime = "CONVERGENTE"

elif variation < 5.0:
    regime = "ATRATOR"

else:
    regime = "INSTÁVEL"

summary = {

    "experiment": "S20_RELATIONAL_DYNAMICS",

    "nodes": N,

    "steps": STEPS,

    "mean_final_kappa": history[-1]["mean_kappa"],

    "mean_final_gamma2": history[-1]["mean_gamma2"],

    "density_final": history[-1]["density"],

    "gamma2_std": variation,

    "regime": regime

}

# ============================================================
# JSON
# ============================================================

with open(
    OUTPUT / "dynamics_summary.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

# ============================================================
# TXT
# ============================================================

with open(
    OUTPUT / "dynamics_report.txt",
    "w"
) as f:

    f.write("=" * 60 + "\n")
    f.write("GER - S16–S20\n")
    f.write("DINÂMICA RELACIONAL\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Nós: {N}\n")
    f.write(f"Passos: {STEPS}\n\n")

    f.write(f"κ médio final: {summary['mean_final_kappa']:.6f}\n")
    f.write(f"Γ₂ médio final: {summary['mean_final_gamma2']:.6f}\n")
    f.write(f"Densidade final: {summary['density_final']:.6f}\n")
    f.write(f"Desvio de Γ₂: {summary['gamma2_std']:.6f}\n")
    f.write(f"Regime identificado: {summary['regime']}\n\n")

    f.write("Interpretação:\n")

    if regime == "ATRATOR":
        f.write(
            "- O sistema apresenta flutuações persistentes de Γ₂,\n"
            "compatíveis com um regime atrator, sem convergência\n"
            "para um vácuo estrito.\n"
        )

    elif regime == "CONVERGENTE":
        f.write(
            "- O sistema converge para um estado estacionário.\n"
        )

    else:
        f.write(
            "- O sistema apresenta grande variabilidade dinâmica,\n"
            "sem estabilização durante o intervalo observado.\n"
        )

print("=" * 60)
print("S16–S20 FINALIZADO")
print("Resultados salvos em:")
print(OUTPUT)
print("=" * 60)
