"""
=============================================================
S20_RELATIONAL_DYNAMICS.py
=============================================================

GER — CONSOLIDAÇÃO S16–S20

Dinâmica Relacional Local
Ação Variacional
Operador Δ_rel
Proxy Γ₂
Observatórios Estruturais

Resultados:

GER_RESULTS/
    S20/
        evolution.csv
        dynamics_summary.json
        dynamics_report.txt

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

SEED = 42

rng = np.random.default_rng(SEED)

# ------------------------------------------------------------
# Sistema
# ------------------------------------------------------------

NODES = 40
EDGE_PROBABILITY = 0.10

STEPS = 50

# ------------------------------------------------------------
# Parâmetros variacionais
# ------------------------------------------------------------

ALPHA = 0.50
BETA = 0.20
GAMMA = 0.30

LEARNING_RATE = 0.05

# ============================================================
# GERAÇÃO DA REDE
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
# κ_eff
#
# Proxy:
# número de caminhos simples
# até profundidade 3
# ============================================================

def compute_kappa(graph):

    n = graph.number_of_nodes()

    K = np.zeros((n, n), dtype=float)

    nodes = list(graph.nodes())

    index = {
        node: i
        for i, node in enumerate(nodes)
    }

    for source in nodes:

        for target in nodes:

            if source == target:
                continue

            try:

                paths = list(
                    nx.all_simple_paths(
                        graph,
                        source,
                        target,
                        cutoff=3
                    )
                )

                K[
                    index[source],
                    index[target]
                ] = len(paths)

            except nx.NetworkXNoPath:

                pass

    return K

# ============================================================
# Δ_rel
#
# Laplaciano relacional local
# ============================================================

def delta_rel(graph, K):

    n = graph.number_of_nodes()

    D = np.zeros_like(K)

    nodes = list(graph.nodes())

    for ia, node in enumerate(nodes):

        neigh = list(graph.neighbors(node))

        if len(neigh) == 0:
            continue

        idx = [nodes.index(x) for x in neigh]

        average = np.mean(
            K[idx],
            axis=0
        )

        D[ia] = average - K[ia]

    return D

# ============================================================
# Γ₂ proxy
#
# L K L
# ============================================================

def gamma2_proxy(graph, K):

    L = nx.laplacian_matrix(
        graph
    ).astype(float).toarray()

    return L @ K @ L

# ============================================================
# AÇÃO LOCAL
# ============================================================

def local_action(K, D, G2):

    term_curvature = np.sum(G2)

    term_smooth = ALPHA * np.sum(D**2)

    term_regularization = BETA * np.sum(K)

    return (
        term_curvature
        - term_smooth
        - term_regularization
    )

# ============================================================
# OBSERVATÓRIOS Γ₂
# ============================================================

def gamma2_observables(G2):

    eig = np.linalg.eigvals(G2)

    observables = {

        "mean":
            float(np.mean(G2)),

        "norm":
            float(
                np.linalg.norm(
                    G2,
                    ord="fro"
                )
            ),

        "variance":
            float(np.var(G2)),

        "maximum":
            float(
                np.max(
                    np.abs(G2)
                )
            ),

        "spectral_radius":
            float(
                np.max(
                    np.abs(eig)
                )
            ),

        "nonzero_fraction":
            float(
                np.count_nonzero(
                    np.abs(G2) > 1e-12
                ) / G2.size
            )

    }

    return observables

# ============================================================
# OBSERVATÓRIOS DA REDE
# ============================================================

def graph_observables(graph):

    density = nx.density(graph)

    degrees = np.array(
        [
            d
            for _, d
            in graph.degree()
        ]
    )

    return {

        "density":
            float(density),

        "mean_degree":
            float(np.mean(degrees)),

        "max_degree":
            int(np.max(degrees)),

        "min_degree":
            int(np.min(degrees))

    }

# ============================================================
# OBSERVATÓRIOS κ
# ============================================================

def kappa_observables(K):

    return {

        "mean":
            float(np.mean(K)),

        "variance":
            float(np.var(K)),

        "maximum":
            float(np.max(K)),

        "minimum":
            float(np.min(K))

    }

# ============================================================
# FERRAMENTA
# Conta alterações estruturais
# ============================================================

def edge_difference(old_graph, new_graph):

    old_edges = set(old_graph.edges())

    new_edges = set(new_graph.edges())

    return len(
        old_edges.symmetric_difference(
            new_edges
        )
    )

# ============================================================
# INICIALIZAÇÃO
# ============================================================

graph = create_graph()

history = []

print("=" * 60)
print("GER - S20")
print("Dinâmica Relacional Local")
print("=" * 60)
print(f"Nós: {graph.number_of_nodes()}")
print(f"Arestas: {graph.number_of_edges()}")
print("=" * 60)

# ============================================================
# EVOLUÇÃO DE κ_eff
#
# Feedback estrutural local
# ============================================================

def update_kappa(K, G2, D):

    force = (
        G2
        - ALPHA * D
        + GAMMA * K
    )

    K_new = K - LEARNING_RATE * force

    K_new = np.clip(K_new, 0.0, None)

    return K_new, force


# ============================================================
# EVOLUÇÃO DA REDE
#
# A conectividade é modificada segundo
# a intensidade da força estrutural.
# ============================================================

def update_graph(graph, force):

    new_graph = graph.copy()

    nodes = list(new_graph.nodes())

    n = len(nodes)

    threshold_add = np.percentile(force, 97)

    threshold_remove = np.percentile(force, 3)

    # --------------------------------------------------------
    # Adição de conexões
    # --------------------------------------------------------

    for i in range(n):

        for j in range(i + 1, n):

            if force[i, j] >= threshold_add:

                new_graph.add_edge(
                    nodes[i],
                    nodes[j]
                )

    # --------------------------------------------------------
    # Remoção de conexões
    # --------------------------------------------------------

    removable = list(new_graph.edges())

    for u, v in removable:

        iu = nodes.index(u)
        iv = nodes.index(v)

        if force[iu, iv] <= threshold_remove:

            if new_graph.degree(u) > 1 and new_graph.degree(v) > 1:

                new_graph.remove_edge(u, v)

    # --------------------------------------------------------
    # Mantém conectividade global
    # --------------------------------------------------------

    if not nx.is_connected(new_graph):

    # Mantém a topologia anterior caso a atualização
    # desconecte a rede.
        
        return graph.copy()


# ============================================================
# CLASSIFICAÇÃO LOCAL
# ============================================================

def classify_step(action_value, gamma_obs):

    if gamma_obs["norm"] < 1e-8:

        return "CONVERGENTE"

    if gamma_obs["variance"] < 1e-6:

        return "ESTACIONÁRIO"

    if gamma_obs["spectral_radius"] < 10:

        return "ATRATOR"

    return "INSTÁVEL"


# ============================================================
# EXECUÇÃO DA DINÂMICA
# ============================================================

print()

print("Iniciando evolução dinâmica...")

print()

current_graph = graph

# Campo efetivo inicial
current_kappa = compute_kappa(current_graph)

# Acoplamento entre κ efetivo e κ estrutural
RELAXATION = 0.15

for step in range(STEPS):

    previous_graph = current_graph.copy()

    # --------------------------------------------------------
    # Operadores fundamentais
    # --------------------------------------------------------

    K = current_kappa
    
    D = delta_rel(current_graph, K)
    
    G2 = gamma2_proxy(current_graph, K)

    # --------------------------------------------------------
    # Observatórios
    # --------------------------------------------------------

    gamma_obs = gamma2_observables(G2)

    graph_obs = graph_observables(current_graph)

    kappa_obs = kappa_observables(K)

    action_value = local_action(K, D, G2)

    # --------------------------------------------------------
    # Evolução local
    # --------------------------------------------------------

    current_kappa, force = update_kappa(
        current_kappa,
        G2,
        D
    )
    
    current_graph = update_graph(
        current_graph,
        force
    )
    
    # κ estrutural da nova rede
    kappa_graph = compute_kappa(current_graph)

    # Relaxação para manter coerência com a estrutura
    current_kappa = (
        (1.0 - RELAXATION) * current_kappa
        + RELAXATION * kappa_graph
    )

    # --------------------------------------------------------
    # Mudanças estruturais
    # --------------------------------------------------------

    changes = edge_difference(
        previous_graph,
        current_graph
    )

    # --------------------------------------------------------
    # Registro
    # --------------------------------------------------------

    history.append({

        "step":
            step,

        "action":
            float(action_value),

        "edge_changes":
            int(changes),

        "mean_kappa":
            kappa_obs["mean"],

        "var_kappa":
            kappa_obs["variance"],

        "max_kappa":
            kappa_obs["maximum"],

        "density":
            graph_obs["density"],

        "mean_degree":
            graph_obs["mean_degree"],

        "gamma_mean":
            gamma_obs["mean"],

        "gamma_norm":
            gamma_obs["norm"],

        "gamma_variance":
            gamma_obs["variance"],

        "gamma_max":
            gamma_obs["maximum"],

        "gamma_radius":
            gamma_obs["spectral_radius"],

        "gamma_support":
            gamma_obs["nonzero_fraction"],

        "classification":
            classify_step(
                action_value,
                gamma_obs
            )

    })

    # --------------------------------------------------------
    # Log
    # --------------------------------------------------------

    print(
        f"[{step + 1:03d}/{STEPS}]",
        f"A={action_value:12.4f}",
        f"κ={kappa_obs['mean']:8.4f}",
        f"||Γ₂||={gamma_obs['norm']:10.4f}",
        f"ρ={gamma_obs['spectral_radius']:10.4f}",
        f"ΔE={changes:4d}"
    )

print()

print("Dinâmica concluída.")

print("=" * 60)

# ============================================================
# ANÁLISE GLOBAL DA EVOLUÇÃO
# ============================================================

print()
print("=" * 60)
print("ANÁLISE GLOBAL")
print("=" * 60)

# ------------------------------------------------------------
# Conversão do histórico
# ------------------------------------------------------------

actions = np.array([h["action"] for h in history])

kappa_mean = np.array([h["mean_kappa"] for h in history])

kappa_var = np.array([h["var_kappa"] for h in history])

density = np.array([h["density"] for h in history])

changes = np.array([h["edge_changes"] for h in history])

gamma_mean = np.array([h["gamma_mean"] for h in history])

gamma_norm = np.array([h["gamma_norm"] for h in history])

gamma_var = np.array([h["gamma_variance"] for h in history])

gamma_radius = np.array([h["gamma_radius"] for h in history])

gamma_support = np.array([h["gamma_support"] for h in history])

# ============================================================
# ESTATÍSTICAS
# ============================================================

statistics = {

    "action_initial": float(actions[0]),
    "action_final": float(actions[-1]),
    "action_variation": float(actions[-1] - actions[0]),

    "kappa_initial": float(kappa_mean[0]),
    "kappa_final": float(kappa_mean[-1]),

    "density_initial": float(density[0]),
    "density_final": float(density[-1]),

    "gamma_norm_initial": float(gamma_norm[0]),
    "gamma_norm_final": float(gamma_norm[-1]),

    "gamma_radius_initial": float(gamma_radius[0]),
    "gamma_radius_final": float(gamma_radius[-1])

}

# ============================================================
# ESTABILIDADE
# ============================================================

window = max(5, STEPS // 5)

tail_norm = gamma_norm[-window:]

tail_radius = gamma_radius[-window:]

tail_density = density[-window:]

tail_kappa = kappa_mean[-window:]

tail_action = actions[-window:]

stability = {

    "gamma_norm_std":
        float(np.std(tail_norm)),

    "gamma_radius_std":
        float(np.std(tail_radius)),

    "density_std":
        float(np.std(tail_density)),

    "kappa_std":
        float(np.std(tail_kappa)),

    "action_std":
        float(np.std(tail_action))

}

# ============================================================
# ENERGIA ESTRUTURAL
# ============================================================

energy = {

    "gamma_energy":
        float(np.sum(gamma_norm ** 2)),

    "action_energy":
        float(np.sum(actions ** 2)),

    "network_activity":
        float(np.sum(changes))

}

# ============================================================
# CRITÉRIO DE CLASSIFICAÇÃO
# ============================================================

gamma_eps = 1e-8

if np.max(gamma_norm) < gamma_eps:

    regime = "CONVERGENTE"

elif (

    stability["gamma_norm_std"] <
    0.05 * np.mean(gamma_norm)

    and

    stability["density_std"] <
    0.02

):

    regime = "ATRATOR"

else:

    regime = "INSTÁVEL"

# ============================================================
# DIAGNÓSTICOS
# ============================================================

diagnostics = []

if np.max(gamma_norm) < gamma_eps:

    diagnostics.append(
        "Γ₂ praticamente nulo durante toda a evolução."
    )

else:

    diagnostics.append(
        "Γ₂ permaneceu estruturalmente ativo."
    )

if energy["network_activity"] == 0:

    diagnostics.append(
        "Nenhuma modificação estrutural detectada."
    )

else:

    diagnostics.append(
        f"{int(energy['network_activity'])} alterações estruturais registradas."
    )

if stability["kappa_std"] < 1e-6:

    diagnostics.append(
        "κ_eff estabilizado."
    )

else:

    diagnostics.append(
        "κ_eff continua evoluindo."
    )

if stability["density_std"] < 1e-6:

    diagnostics.append(
        "Densidade praticamente constante."
    )

else:

    diagnostics.append(
        "A densidade ainda apresenta variações."
    )

# ============================================================
# RESUMO FINAL
# ============================================================

summary = {

    "experiment":
        "S20_RELATIONAL_DYNAMICS",

    "seed":
        SEED,

    "nodes":
        current_graph.number_of_nodes(),

    "edges":
        current_graph.number_of_edges(),

    "steps":
        STEPS,

    "parameters": {

        "alpha": ALPHA,

        "beta": BETA,

        "gamma": GAMMA,

        "learning_rate": LEARNING_RATE

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
# IMPRESSÃO DO RESUMO
# ============================================================

print()

print("Resumo")

print("-" * 60)

print(f"Regime ............... {regime}")

print(f"Ação inicial ........ {statistics['action_initial']:.6f}")

print(f"Ação final .......... {statistics['action_final']:.6f}")

print(f"κ médio final ....... {statistics['kappa_final']:.6f}")

print(f"Densidade final ..... {statistics['density_final']:.6f}")

print(f"||Γ₂|| final ........ {statistics['gamma_norm_final']:.6f}")

print(f"Raio espectral ...... {statistics['gamma_radius_final']:.6f}")

print()

print("Diagnósticos:")

for item in diagnostics:

    print(" -", item)

print()

print("=" * 60)
print("Análise concluída.")
print("=" * 60)

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

csv_path = OUTPUT / "evolution.csv"

fieldnames = [

    "step",

    "action",

    "edge_changes",

    "mean_kappa",

    "var_kappa",

    "max_kappa",

    "density",

    "mean_degree",

    "gamma_mean",

    "gamma_norm",

    "gamma_variance",

    "gamma_max",

    "gamma_radius",

    "gamma_support",

    "classification"

]

with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.DictWriter(

        csvfile,

        fieldnames=fieldnames

    )

    writer.writeheader()

    for row in history:

        writer.writerow(row)

print("CSV salvo.")

# ============================================================
# JSON
# ============================================================

json_path = OUTPUT / "dynamics_summary.json"

with open(

    json_path,

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
# CERTIFICADO EXPERIMENTAL
# ============================================================

certificate = {

    "experiment": "S20",

    "title": "Relational Dynamics",

    "status": "COMPLETED",

    "nodes": current_graph.number_of_nodes(),

    "edges": current_graph.number_of_edges(),

    "steps": STEPS,

    "seed": SEED,

    "regime": regime,

    "files": {

        "csv": str(csv_path),

        "json": str(json_path),

        "report": str(
            OUTPUT / "dynamics_report.txt"
        )

    }

}

certificate_path = OUTPUT / "experiment_certificate.json"

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

    "output_directory": str(OUTPUT),

    "generated_files": [

        "evolution.csv",

        "dynamics_summary.json",

        "experiment_certificate.json",

        "dynamics_report.txt"

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
# VERIFICAÇÃO FINAL
# ============================================================

print()

print("Arquivos gerados:")

for file in sorted(OUTPUT.iterdir()):

    print(f"  ✓ {file.name}")

print()

print("=" * 60)
print("EXPORTAÇÃO FINALIZADA")
print("=" * 60)

# ============================================================
# RELATÓRIO CIENTÍFICO
# ============================================================

report_path = OUTPUT / "dynamics_report.txt"

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write("=" * 70 + "\n")
    f.write("GER - RELATIONAL DYNAMICS\n")
    f.write("CONSOLIDAÇÃO S16–S20\n")
    f.write("=" * 70 + "\n\n")

    f.write("CONFIGURAÇÃO\n")
    f.write("-" * 70 + "\n")

    f.write(f"Nós .................... {current_graph.number_of_nodes()}\n")
    f.write(f"Arestas ............... {current_graph.number_of_edges()}\n")
    f.write(f"Passos ................ {STEPS}\n")
    f.write(f"Seed .................. {SEED}\n\n")

    f.write("Parâmetros\n")

    f.write(f"  α = {ALPHA}\n")
    f.write(f"  β = {BETA}\n")
    f.write(f"  γ = {GAMMA}\n")
    f.write(f"  Learning Rate = {LEARNING_RATE}\n\n")

    f.write("RESULTADOS FINAIS\n")
    f.write("-" * 70 + "\n")

    f.write(f"Regime ................ {regime}\n")
    f.write(f"Ação inicial ......... {statistics['action_initial']:.6f}\n")
    f.write(f"Ação final ........... {statistics['action_final']:.6f}\n")
    f.write(f"Variação da ação ..... {statistics['action_variation']:.6f}\n\n")

    f.write(f"κ médio final ........ {statistics['kappa_final']:.6f}\n")
    f.write(f"Densidade final ...... {statistics['density_final']:.6f}\n\n")

    f.write("OBSERVATÓRIOS Γ₂\n")
    f.write("-" * 70 + "\n")

    f.write(f"Norma final .......... {statistics['gamma_norm_final']:.6f}\n")
    f.write(f"Raio espectral ....... {statistics['gamma_radius_final']:.6f}\n")
    f.write(f"Desvio ||Γ₂|| ........ {stability['gamma_norm_std']:.6f}\n")
    f.write(f"Desvio raio .......... {stability['gamma_radius_std']:.6f}\n\n")

    f.write("ENERGIA\n")
    f.write("-" * 70 + "\n")

    f.write(f"Energia Γ₂ ........... {energy['gamma_energy']:.6f}\n")
    f.write(f"Energia ação ......... {energy['action_energy']:.6f}\n")
    f.write(f"Atividade estrutural . {energy['network_activity']:.0f}\n\n")

    f.write("DIAGNÓSTICOS\n")
    f.write("-" * 70 + "\n")

    for item in diagnostics:
        f.write(f"- {item}\n")

    f.write("\n")

    f.write("INTERPRETAÇÃO\n")
    f.write("-" * 70 + "\n")

    if regime == "CONVERGENTE":

        f.write(
            "O sistema evoluiu para um estado aproximadamente "
            "estacionário segundo os observáveis implementados. "
            "Esse resultado deve ser interpretado apenas para o "
            "proxy de Γ₂ utilizado neste experimento.\n"
        )

    elif regime == "ATRATOR":

        f.write(
            "O sistema apresenta flutuações persistentes com "
            "estabilidade estatística, compatíveis com um regime "
            "de atrator relacional.\n"
        )

    else:

        f.write(
            "O sistema permaneceu em regime dinâmico sem evidência "
            "de estabilização durante o intervalo observado.\n"
        )

    f.write("\n")

    f.write("OBSERVAÇÃO DA AUDITORIA\n")
    f.write("-" * 70 + "\n")

    f.write(
        "Este experimento utiliza um proxy computacional para Γ₂. "
        "Os resultados validam exclusivamente o comportamento desse "
        "proxy, não constituindo demonstração do operador Γ₂ do "
        "formalismo matemático completo desenvolvido no GER.\n"
    )

print("Relatório salvo.")

# ============================================================
# ENCERRAMENTO
# ============================================================

print()
print("=" * 70)
print("GER - S20 FINALIZADO")
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

    """
    O experimento é executado durante a construção do módulo.
    O main() apenas encerra a execução de forma compatível com
    GitHub, Colab e execução local.
    """

    print()
    print("=" * 70)
    print("GER S20 - Execução concluída com sucesso.")
    print("=" * 70)


if __name__ == "__main__":
    main()
