"""
=============================================================
S20B_SPECTRAL_PHASE_DIAGRAM.py
=============================================================

GER — S20B

Spectral Phase Diagram

Reconstrução do experimento observacional S20.

Objetivo
--------

Construir o espaço de fase relacional definido pelos
observáveis

    (κ_eff, Γ₂, ρ)

durante a evolução estrutural de uma rede relacional.

Neste experimento κ_eff NÃO é tratado como variável
dinâmica.

Todos os observáveis são recalculados diretamente a
partir da estrutura da rede em cada passo temporal.

Resultados

GER_RESULTS/
    S20B/

        phase_space.csv
        phase_summary.json
        regime_certificate.json
        inventory.json
        phase_report.txt

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

OUTPUT = Path("/content/drive/MyDrive/GER_RESULTS/S20B")
OUTPUT.mkdir(parents=True, exist_ok=True)

SEED = 42

rng = np.random.default_rng(SEED)

# ============================================================
# PARÂMETROS
# ============================================================

NODES = 50

EDGE_PROBABILITY = 0.08

STEPS = 20

PERTURBATION_RATE = 0.02

# ============================================================
# CONSTRUÇÃO DA REDE
# ============================================================

def create_graph():

    graph = nx.erdos_renyi_graph(
        NODES,
        EDGE_PROBABILITY,
        seed=SEED
    )

    if not nx.is_connected(graph):

        largest = max(
            nx.connected_components(graph),
            key=len
        )

        graph = graph.subgraph(
            largest
        ).copy()

    return graph

# ============================================================
# MATRIZ DE ADJACÊNCIA
# ============================================================

def adjacency_matrix(graph):

    return nx.to_numpy_array(
        graph,
        dtype=float
    )

# ============================================================
# κ_eff
#
# Proxy:
# Betweenness Centrality média
# ============================================================

def compute_kappa(graph):

    centrality = nx.betweenness_centrality(graph)

    values = np.array(
        list(
            centrality.values()
        ),
        dtype=float
    )

    return {

        "mean":
            float(np.mean(values)),

        "variance":
            float(np.var(values)),

        "maximum":
            float(np.max(values)),

        "minimum":
            float(np.min(values))

    }

# ============================================================
# LAPLACIANO
# ============================================================

def laplacian(graph):

    return nx.laplacian_matrix(
        graph
    ).astype(float).toarray()

# ============================================================
# Γ₂ (proxy)
#
# tr(L Lᵀ)/N²
# ============================================================

def compute_gamma2(graph):

    L = laplacian(graph)

    gamma = float(

        np.trace(
            L @ L.T
        ) /

        (graph.number_of_nodes() ** 2)

    )

    eig = np.linalg.eigvals(L)

    return {

        "mean":
            gamma,

        "norm":
            float(
                np.linalg.norm(
                    L,
                    ord="fro"
                )
            ),

        "spectral_radius":
            float(
                np.max(
                    np.abs(eig)
                )
            )

    }

# ============================================================
# OBSERVÁVEIS DA REDE
# ============================================================

def graph_observables(graph):

    degrees = np.array(

        [
            d
            for _, d
            in graph.degree()
        ],

        dtype=float

    )

    return {

        "density":
            float(
                nx.density(graph)
            ),

        "mean_degree":
            float(
                np.mean(degrees)
            ),

        "max_degree":
            int(
                np.max(degrees)
            ),

        "min_degree":
            int(
                np.min(degrees)
            )

    }

# ============================================================
# PERTURBAÇÃO ESTRUTURAL
#
# Evolução apenas da rede.
#
# κ e Γ₂ nunca são integrados.
# ============================================================

def perturb_graph(graph):

    new_graph = graph.copy()

    nodes = list(
        new_graph.nodes()
    )

    n = len(nodes)

    trials = max(
        1,
        int(
            PERTURBATION_RATE * n * n
        )
    )

    for _ in range(trials):

        i = rng.integers(n)
        j = rng.integers(n)

        if i == j:
            continue

        u = nodes[i]
        v = nodes[j]

        if new_graph.has_edge(u, v):

            if (
                new_graph.degree(u) > 1
                and
                new_graph.degree(v) > 1
            ):

                new_graph.remove_edge(u, v)

        else:

            new_graph.add_edge(u, v)

    if not nx.is_connected(new_graph):

        largest = max(
            nx.connected_components(new_graph),
            key=len
        )

        new_graph = new_graph.subgraph(
            largest
        ).copy()

    return new_graph

# ============================================================
# HISTÓRICO
# ============================================================

history = []

graph = create_graph()

print("=" * 60)
print("GER — S20B")
print("Spectral Phase Diagram")
print("=" * 60)
print(f"Nós ............ {graph.number_of_nodes()}")
print(f"Arestas ........ {graph.number_of_edges()}")
print("=" * 60)
print()
print("Iniciando evolução observacional...")
print()

# ============================================================
# CLASSIFICAÇÃO DE REGIME
# ============================================================

GAMMA_EPS = 1e-4
KAPPA_VAR_EPS = 1e-4

def classify_regime(kappa_obs, gamma_obs):

    gamma_norm = gamma_obs["norm"]

    kappa_var = kappa_obs["variance"]

    if (
        gamma_norm < GAMMA_EPS
        and
        kappa_var < KAPPA_VAR_EPS
    ):

        return "COLAPSO_ESPECTRAL"

    if gamma_norm >= GAMMA_EPS:

        return "FLUTUACAO_CRITICA"

    return "BORDA_CRITICA"

# ============================================================
# EVOLUÇÃO OBSERVACIONAL
# ============================================================

for step in range(STEPS):

    # --------------------------------------------------------
    # Evolução exclusivamente estrutural
    # --------------------------------------------------------

    graph = perturb_graph(graph)

    # --------------------------------------------------------
    # Observáveis
    # --------------------------------------------------------

    kappa_obs = compute_kappa(graph)

    gamma_obs = compute_gamma2(graph)

    network_obs = graph_observables(graph)

    # --------------------------------------------------------
    # Vetor do espaço de fase
    # --------------------------------------------------------

    phase_point = {

        "step":
            step,

        "kappa_mean":
            kappa_obs["mean"],

        "kappa_variance":
            kappa_obs["variance"],

        "kappa_max":
            kappa_obs["maximum"],

        "kappa_min":
            kappa_obs["minimum"],

        "gamma_mean":
            gamma_obs["mean"],

        "gamma_norm":
            gamma_obs["norm"],

        "gamma_radius":
            gamma_obs["spectral_radius"],

        "density":
            network_obs["density"],

        "mean_degree":
            network_obs["mean_degree"],

        "max_degree":
            network_obs["max_degree"],

        "min_degree":
            network_obs["min_degree"],

        "classification":
            classify_regime(
                kappa_obs,
                gamma_obs
            )

    }

    history.append(phase_point)

    # --------------------------------------------------------
    # Log
    # --------------------------------------------------------

    print(

        f"[{step + 1:03d}/{STEPS}]",

        f"κ={phase_point['kappa_mean']:.6f}",

        f"Varκ={phase_point['kappa_variance']:.6e}",

        f"Γ₂={phase_point['gamma_mean']:.6f}",

        f"||Γ₂||={phase_point['gamma_norm']:.6f}",

        f"ρ={phase_point['density']:.4f}",

        f"{phase_point['classification']}"

    )

print()

print("Evolução concluída.")

print("=" * 60)

# ============================================================
# CONVERSÃO PARA ARRAYS
# ============================================================

kappa_mean = np.array(
    [
        h["kappa_mean"]
        for h in history
    ]
)

kappa_variance = np.array(
    [
        h["kappa_variance"]
        for h in history
    ]
)

gamma_mean = np.array(
    [
        h["gamma_mean"]
        for h in history
    ]
)

gamma_norm = np.array(
    [
        h["gamma_norm"]
        for h in history
    ]
)

gamma_radius = np.array(
    [
        h["gamma_radius"]
        for h in history
    ]
)

density = np.array(
    [
        h["density"]
        for h in history
    ]
)

mean_degree = np.array(
    [
        h["mean_degree"]
        for h in history
    ]
)

labels = [
    h["classification"]
    for h in history
]

# ============================================================
# ESPAÇO DE FASE
# ============================================================

phase_space = np.column_stack(

    [

        kappa_mean,

        gamma_mean,

        density

    ]

)

print()

print("=" * 60)
print("ESPAÇO DE FASE")
print("=" * 60)

print()

print("Primeiros pontos:")

for point in phase_space[:5]:

    print(point)

print()

# ============================================================
# ANÁLISE GLOBAL
# ============================================================

print()
print("=" * 60)
print("ANÁLISE GLOBAL")
print("=" * 60)

# ============================================================
# ESTATÍSTICAS
# ============================================================

statistics = {

    "kappa_initial":
        float(kappa_mean[0]),

    "kappa_final":
        float(kappa_mean[-1]),

    "kappa_variation":
        float(kappa_mean[-1] - kappa_mean[0]),

    "gamma_initial":
        float(gamma_mean[0]),

    "gamma_final":
        float(gamma_mean[-1]),

    "gamma_variation":
        float(gamma_mean[-1] - gamma_mean[0]),

    "density_initial":
        float(density[0]),

    "density_final":
        float(density[-1]),

    "density_variation":
        float(density[-1] - density[0])

}

# ============================================================
# ESTABILIDADE
# ============================================================

window = max(5, STEPS // 5)

stability = {

    "kappa_std":
        float(
            np.std(
                kappa_mean[-window:]
            )
        ),

    "gamma_std":
        float(
            np.std(
                gamma_mean[-window:]
            )
        ),

    "density_std":
        float(
            np.std(
                density[-window:]
            )
        )

}

# ============================================================
# ENERGIA OBSERVACIONAL
# ============================================================

energy = {

    "kappa_energy":
        float(
            np.sum(
                kappa_mean ** 2
            )
        ),

    "gamma_energy":
        float(
            np.sum(
                gamma_mean ** 2
            )
        ),

    "density_energy":
        float(
            np.sum(
                density ** 2
            )
        )

}

# ============================================================
# REGIME GLOBAL
# ============================================================

from collections import Counter

counter = Counter(labels)

regime = counter.most_common(1)[0][0]

# ============================================================
# DIAGNÓSTICOS
# ============================================================

diagnostics = []

if stability["kappa_std"] < 1e-6:

    diagnostics.append(
        "κ_eff apresentou alta estabilidade temporal."
    )

else:

    diagnostics.append(
        "κ_eff permaneceu em evolução durante a observação."
    )

if stability["gamma_std"] < 1e-6:

    diagnostics.append(
        "Γ₂ permaneceu praticamente constante."
    )

else:

    diagnostics.append(
        "Γ₂ permaneceu estruturalmente ativo."
    )

if stability["density_std"] < 1e-6:

    diagnostics.append(
        "A densidade estrutural permaneceu praticamente constante."
    )

else:

    diagnostics.append(
        "A densidade apresentou evolução estrutural."
    )

diagnostics.append(
    f"Regime predominante: {regime}."
)

# ============================================================
# RESUMO
# ============================================================

summary = {

    "experiment":
        "S20B_SPECTRAL_PHASE_DIAGRAM",

    "seed":
        SEED,

    "nodes":
        graph.number_of_nodes(),

    "edges":
        graph.number_of_edges(),

    "steps":
        STEPS,

    "parameters": {

        "edge_probability":
            EDGE_PROBABILITY,

        "perturbation_rate":
            PERTURBATION_RATE

    },

    "statistics":
        statistics,

    "stability":
        stability,

    "energy":
        energy,

    "regime":
        regime,

    "diagnostics":
        diagnostics

}

# ============================================================
# IMPRESSÃO
# ============================================================

print()

print("Resumo")

print("-" * 60)

print(f"Regime ............... {regime}")

print(f"κ inicial ............ {statistics['kappa_initial']:.6f}")
print(f"κ final .............. {statistics['kappa_final']:.6f}")

print(f"Γ₂ inicial ........... {statistics['gamma_initial']:.6f}")
print(f"Γ₂ final ............. {statistics['gamma_final']:.6f}")

print(f"Densidade inicial .... {statistics['density_initial']:.6f}")
print(f"Densidade final ...... {statistics['density_final']:.6f}")

print()

print("Diagnósticos:")

for item in diagnostics:

    print(" -", item)

# ============================================================
# EXPORTAÇÃO
# ============================================================

print()
print("=" * 60)
print("SALVANDO RESULTADOS")
print("=" * 60)

# ============================================================
# CSV
# ============================================================

csv_path = OUTPUT / "phase_space.csv"

fieldnames = list(history[0].keys())

with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as fp:

    writer = csv.DictWriter(
        fp,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(history)

print("CSV salvo.")

# ============================================================
# JSON
# ============================================================

summary_path = OUTPUT / "phase_summary.json"

with open(
    summary_path,
    "w",
    encoding="utf-8"
) as fp:

    json.dump(
        summary,
        fp,
        indent=4,
        ensure_ascii=False
    )

print("JSON salvo.")

# ============================================================
# CERTIFICADO
# ============================================================

certificate = {

    "experiment":
        "S20B",

    "title":
        "Spectral Phase Diagram",

    "status":
        "COMPLETED",

    "nodes":
        graph.number_of_nodes(),

    "edges":
        graph.number_of_edges(),

    "steps":
        STEPS,

    "seed":
        SEED,

    "regime":
        regime,

    "files": {

        "csv":
            str(csv_path),

        "summary":
            str(summary_path),

        "report":
            str(
                OUTPUT / "phase_report.txt"
            )

    }

}

certificate_path = OUTPUT / "regime_certificate.json"

with open(
    certificate_path,
    "w",
    encoding="utf-8"
) as fp:

    json.dump(
        certificate,
        fp,
        indent=4,
        ensure_ascii=False
    )

print("Certificado salvo.")

# ============================================================
# INVENTÁRIO
# ============================================================

inventory = {

    "output_directory":
        str(OUTPUT),

    "generated_files": [

        "phase_space.csv",

        "phase_summary.json",

        "regime_certificate.json",

        "inventory.json",

        "phase_report.txt"

    ]

}

inventory_path = OUTPUT / "inventory.json"

with open(
    inventory_path,
    "w",
    encoding="utf-8"
) as fp:

    json.dump(
        inventory,
        fp,
        indent=4,
        ensure_ascii=False
    )

print("Inventário salvo.")

# ============================================================
# RELATÓRIO
# ============================================================

report_path = OUTPUT / "phase_report.txt"

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write("=" * 70 + "\n")
    f.write("GER - S20B\n")
    f.write("SPECTRAL PHASE DIAGRAM\n")
    f.write("=" * 70 + "\n\n")

    f.write("CONFIGURAÇÃO\n")
    f.write("-" * 70 + "\n")

    f.write(f"Nós ................ {graph.number_of_nodes()}\n")
    f.write(f"Arestas ............ {graph.number_of_edges()}\n")
    f.write(f"Passos ............. {STEPS}\n")
    f.write(f"Seed ............... {SEED}\n\n")

    f.write("ESTATÍSTICAS\n")
    f.write("-" * 70 + "\n")

    for key, value in statistics.items():
        f.write(f"{key:25s} {value}\n")

    f.write("\n")

    f.write("ESTABILIDADE\n")
    f.write("-" * 70 + "\n")

    for key, value in stability.items():
        f.write(f"{key:25s} {value}\n")

    f.write("\n")

    f.write("ENERGIA OBSERVACIONAL\n")
    f.write("-" * 70 + "\n")

    for key, value in energy.items():
        f.write(f"{key:25s} {value}\n")

    f.write("\n")

    f.write("REGIME GLOBAL\n")
    f.write("-" * 70 + "\n")

    f.write(f"{regime}\n\n")

    f.write("DIAGNÓSTICOS\n")
    f.write("-" * 70 + "\n")

    for item in diagnostics:
        f.write(f"- {item}\n")

    f.write("\n")

    f.write("INTERPRETAÇÃO\n")
    f.write("-" * 70 + "\n")

    f.write(
        "O experimento caracteriza o espaço de fase observacional "
        "do sistema relacional utilizando κ_eff, Γ₂ e densidade "
        "estrutural como coordenadas. Nenhuma dinâmica explícita "
        "é imposta a κ_eff; todos os observáveis são recalculados "
        "diretamente a partir da topologia da rede em cada passo. "
        "As conclusões deste experimento referem-se exclusivamente "
        "ao comportamento observacional do sistema sob perturbações "
        "estruturais controladas.\n"
    )

print("Relatório salvo.")

# ============================================================
# ENCERRAMENTO
# ============================================================

print()

print("=" * 70)
print("GER - S20B FINALIZADO")
print("=" * 70)

print(f"Diretório : {OUTPUT}")

print()

for file in sorted(OUTPUT.iterdir()):

    print(f"✓ {file.name}")

print()

print("Experimento concluído.")

print("=" * 70)

# ============================================================
# MAIN
# ============================================================

def main():

    print()

    print("=" * 70)

    print("GER S20B - Execução concluída com sucesso.")

    print("=" * 70)


if __name__ == "__main__":
    main()
