"""
==========================================================
GER S0
Nascimento do Operador Relacional
==========================================================

Produz:

GER_RESULTS/
    S0/
        summary.json
        results.txt
        diameter.csv
        diameter_evolution.png

==========================================================
"""

from pathlib import Path
import json
import csv

import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------------------
# Diretório
# -------------------------------------------------------

OUTPUT = Path("/content/drive/MyDrive/GER_RESULTS/S0")
OUTPUT.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# Grafo inicial
# -------------------------------------------------------

N = 100

G = nx.path_graph(N)

# -------------------------------------------------------
# Funções
# -------------------------------------------------------

def diameter_safe(graph):
    if nx.is_connected(graph):
        return nx.diameter(graph)
    c = max(nx.connected_components(graph), key=len)
    return nx.diameter(graph.subgraph(c))

def closure_step(graph):
    H = graph.copy()

    new_edges = []

    for b in graph.nodes():

        pred = list(graph.neighbors(b))

        for a in pred:
            for c in pred:

                if a == c:
                    continue

                if not H.has_edge(a, c):
                    new_edges.append((a, c))

    H.add_edges_from(new_edges)

    return H

# -------------------------------------------------------
# Fechamento total
# -------------------------------------------------------

G_full = G.copy()

diam_full = [diameter_safe(G_full)]

for _ in range(8):

    G_full = closure_step(G_full)
    diam_full.append(diameter_safe(G_full))

# -------------------------------------------------------
# Fechamento estratificado simples
# (limita novas arestas por passo)
# -------------------------------------------------------

G_strat = G.copy()

diam_strat = [diameter_safe(G_strat)]

for _ in range(8):

    H = G_strat.copy()

    added = 0

    for b in G_strat.nodes():

        neigh = list(G_strat.neighbors(b))

        for a in neigh:
            for c in neigh:

                if a == c:
                    continue

                if H.has_edge(a, c):
                    continue

                H.add_edge(a, c)

                added += 1

                if added >= N:
                    break

            if added >= N:
                break

        if added >= N:
            break

    G_strat = H

    diam_strat.append(diameter_safe(G_strat))

# -------------------------------------------------------
# CSV
# -------------------------------------------------------

with open(OUTPUT/"diameter.csv","w",newline="") as f:

    w = csv.writer(f)

    w.writerow([
        "step",
        "transitive",
        "stratified"
    ])

    for i in range(len(diam_full)):

        w.writerow([
            i,
            diam_full[i],
            diam_strat[i]
        ])

# -------------------------------------------------------
# Figura
# -------------------------------------------------------

plt.figure(figsize=(7,4))

plt.plot(diam_full,label="Transitivo")

plt.plot(diam_strat,label="Estratificado")

plt.xlabel("Passo")

plt.ylabel("Diâmetro")

plt.title("Evolução do Diâmetro Relacional")

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(OUTPUT/"diameter_evolution.png")

plt.close()

# -------------------------------------------------------
# JSON
# -------------------------------------------------------

summary = {

    "experiment":"GER_S0",

    "nodes":N,

    "initial_diameter":diam_full[0],

    "transitive_final":diam_full[-1],

    "stratified_final":diam_strat[-1],

    "observation":
        "Comparação entre fechamento transitivo e fechamento estratificado."
}

with open(OUTPUT/"summary.json","w") as f:

    json.dump(summary,f,indent=4)

# -------------------------------------------------------
# TXT
# -------------------------------------------------------

with open(OUTPUT/"results.txt","w") as f:

    f.write("GER S0\n")
    f.write("="*50+"\n\n")

    f.write(f"Nós: {N}\n\n")

    f.write(f"Diâmetro inicial : {diam_full[0]}\n")
    f.write(f"Transitivo final : {diam_full[-1]}\n")
    f.write(f"Estratificado final : {diam_strat[-1]}\n\n")

    f.write("Conclusão\n")
    f.write("O fechamento transitivo reduz rapidamente o diâmetro da rede.\n")
    f.write("O fechamento estratificado preserva maior profundidade estrutural,\n")
    f.write("representando a ideia consolidada ao final do ciclo S0–S10.\n")

print("="*60)
print("GER S0 FINALIZADO")
print("Resultados salvos em:")
print(OUTPUT)
print("="*60)
