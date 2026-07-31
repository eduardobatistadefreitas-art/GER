"""
=============================================================
E10_1_2_A_gradient.py
=============================================================

GER — Geometria da Superfície Relacional
E10.1.2.A — Gradient Field

Objetivo
--------
Calcular o campo discreto de gradientes da superfície relacional
produzida na E10.1.1.

Esta etapa NÃO executa novas simulações.

Ela apenas analisa os produtos gerados pela
E10.1.1.

Entradas
---------
signature_surface.parquet
grid.parquet

Saídas
------
gradient_surface.parquet
gradient_summary.json
gradient_summary.txt
gradient_maps.png

=============================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


# ============================================================
# CONFIGURAÇÃO
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
    / "E10_1_1"
)

OUTPUT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
    / "E10_1_2_A_Gradient"
)

FIGURES = OUTPUT / "FIGURES"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


# ============================================================
# ARQUIVOS
# ============================================================

SIGNATURE_FILE = ROOT / "signature_surface.parquet"
GRID_FILE = ROOT / "grid.parquet"

GRADIENT_FILE = OUTPUT / "gradient_surface.parquet"

SUMMARY_JSON = OUTPUT / "gradient_summary.json"
SUMMARY_TXT = OUTPUT / "gradient_summary.txt"


# ============================================================
# LEITURA DOS DADOS
# ============================================================

print("=" * 60)
print("GER")
print("E10.1.2.A")
print("Gradient Field")
print("=" * 60)

print("\nCarregando superfície...")

signature = pd.read_parquet(SIGNATURE_FILE)
grid = pd.read_parquet(GRID_FILE)

print(f"Assinaturas : {len(signature):,}")
print(f"Pontos da malha : {len(grid):,}")

if len(signature) != len(grid):
    raise RuntimeError(
        "Número de assinaturas diferente da grade."
    )

print("\nSuperfície carregada com sucesso.")

# ============================================================
# COLUNAS DA ASSINATURA
# ============================================================

RESERVED_COLUMNS = {
    "id",
    "i",
    "j",
    "gamma",
    "omega",
}

SIGNATURE_COLUMNS = [
    c
    for c in signature.columns
    if c not in RESERVED_COLUMNS
]

print("\nComponentes da assinatura:")

for name in SIGNATURE_COLUMNS:
    print(f"   • {name}")

print("\nPreparação concluída.")
print("=" * 60)

# ============================================================
# RECONSTRUÇÃO DA SUPERFÍCIE
# ============================================================

print("\nReconstruindo superfície relacional...")

gamma_values = np.sort(signature["gamma"].unique())
omega_values = np.sort(signature["omega"].unique())

NG = len(gamma_values)
NO = len(omega_values)

print(f"Pontos em γ : {NG}")
print(f"Pontos em ω : {NO}")

gradient_frames = []

summary = {
    "gamma_points": int(NG),
    "omega_points": int(NO),
    "components": {},
}

# ============================================================
# CÁLCULO DOS GRADIENTES
# ============================================================

for component in SIGNATURE_COLUMNS:

    print(f"\nProcessando: {component}")

    pivot = (
        signature
        .pivot(
            index="gamma",
            columns="omega",
            values=component,
        )
        .sort_index()
        .sort_index(axis=1)
    )

    surface = pivot.to_numpy(dtype=float)

    # --------------------------------------------
    # Gradientes discretos
    # --------------------------------------------

    grad_gamma, grad_omega = np.gradient(surface)

    grad_norm = np.sqrt(
        grad_gamma ** 2 +
        grad_omega ** 2
    )

    # --------------------------------------------
    # Reconstrução em formato tabular
    # --------------------------------------------

    df = (
        pivot
        .stack()
        .reset_index(name="value")
    )

    df["component"] = component

    df["grad_gamma"] = grad_gamma.ravel()
    df["grad_omega"] = grad_omega.ravel()
    df["grad_norm"] = grad_norm.ravel()

    gradient_frames.append(df)

    # --------------------------------------------
    # Estatísticas básicas
    # --------------------------------------------

    summary["components"][component] = {

        "min_gradient":
            float(np.min(grad_norm)),

        "max_gradient":
            float(np.max(grad_norm)),

        "mean_gradient":
            float(np.mean(grad_norm)),

        "std_gradient":
            float(np.std(grad_norm)),

        "zero_fraction":
            float(
                np.mean(
                    np.isclose(
                        grad_norm,
                        0.0,
                        atol=1e-12,
                    )
                )
            ),
    }

print("\nGradientes calculados.")

# ============================================================
# DATAFRAME FINAL
# ============================================================

gradient_surface = pd.concat(
    gradient_frames,
    ignore_index=True,
)

print(f"Linhas produzidas : {len(gradient_surface):,}")

print("=" * 60)

# ============================================================
# PERSISTÊNCIA DOS RESULTADOS
# ============================================================

print("\nGravando produtos...")

gradient_surface.to_parquet(
    GRADIENT_FILE,
    index=False,
)

with open(
    SUMMARY_JSON,
    "w",
    encoding="utf-8",
) as fp:

    json.dump(
        summary,
        fp,
        indent=4,
        ensure_ascii=False,
    )

# ============================================================
# RELATÓRIO TEXTO
# ============================================================

with open(
    SUMMARY_TXT,
    "w",
    encoding="utf-8",
) as fp:

    fp.write("=" * 60 + "\n")
    fp.write("GER\n")
    fp.write("E10.1.2.A\n")
    fp.write("Gradient Field\n")
    fp.write("=" * 60 + "\n\n")

    fp.write(f"Pontos γ : {NG}\n")
    fp.write(f"Pontos ω : {NO}\n")
    fp.write(f"Componentes : {len(SIGNATURE_COLUMNS)}\n\n")

    for component in SIGNATURE_COLUMNS:

        s = summary["components"][component]

        fp.write("-" * 50 + "\n")
        fp.write(f"{component}\n")
        fp.write("-" * 50 + "\n")

        fp.write(f"Gradiente mínimo : {s['min_gradient']:.6e}\n")
        fp.write(f"Gradiente máximo : {s['max_gradient']:.6e}\n")
        fp.write(f"Gradiente médio  : {s['mean_gradient']:.6e}\n")
        fp.write(f"Desvio padrão    : {s['std_gradient']:.6e}\n")
        fp.write(f"Fração nula      : {100*s['zero_fraction']:.2f}%\n\n")

print("Resumo salvo.")

# ============================================================
# MAPAS DE GRADIENTE
# ============================================================

print("\nGerando mapas...")

for component in SIGNATURE_COLUMNS:

    subset = gradient_surface[
        gradient_surface["component"] == component
    ]

    surface = (
        subset
        .pivot(
            index="gamma",
            columns="omega",
            values="grad_norm",
        )
        .sort_index()
        .sort_index(axis=1)
    )

    plt.figure(figsize=(7, 6))

    plt.imshow(
        surface.to_numpy(),
        origin="lower",
        aspect="auto",
    )

    plt.colorbar(label="||∇S||")

    plt.title(
        f"Gradient Norm\n{component}"
    )

    plt.xlabel("ω")

    plt.ylabel("γ")

    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{component}_gradient.png",
        dpi=200,
    )

    plt.close()

print("Mapas concluídos.")

# ============================================================
# RESUMO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("E10.1.2.A FINALIZADO")
print("=" * 60)

print(f"Componentes analisadas : {len(SIGNATURE_COLUMNS)}")
print(f"Arquivo principal      : {GRADIENT_FILE.name}")
print(f"Resumo JSON            : {SUMMARY_JSON.name}")
print(f"Resumo TXT             : {SUMMARY_TXT.name}")
print(f"Figuras                : {FIGURES}")

print("=" * 60)

# ============================================================
# AUDITORIA OPERACIONAL
# ============================================================

print("\nExecutando auditoria...")

audit = {}

audit["signature_rows"] = int(len(signature))
audit["gradient_rows"] = int(len(gradient_surface))

audit["gamma_points"] = int(NG)
audit["omega_points"] = int(NO)

audit["components"] = list(SIGNATURE_COLUMNS)

audit["expected_rows"] = int(
    len(signature) * len(SIGNATURE_COLUMNS)
)

audit["missing_values"] = int(
    gradient_surface.isna().sum().sum()
)

audit["duplicate_rows"] = int(
    gradient_surface.duplicated().sum()
)

audit["infinite_values"] = int(
    np.isinf(
        gradient_surface.select_dtypes(
            include=[np.number]
        )
    ).sum().sum()
)

audit["status"] = "PASS"

if audit["gradient_rows"] != audit["expected_rows"]:
    audit["status"] = "FAIL"

if audit["missing_values"] > 0:
    audit["status"] = "FAIL"

if audit["duplicate_rows"] > 0:
    audit["status"] = "FAIL"

if audit["infinite_values"] > 0:
    audit["status"] = "FAIL"

AUDIT_JSON = OUTPUT / "gradient_audit.json"

with open(
    AUDIT_JSON,
    "w",
    encoding="utf-8",
) as fp:

    json.dump(
        audit,
        fp,
        indent=4,
        ensure_ascii=False,
    )

print("Auditoria concluída.")

# ============================================================
# DIAGNÓSTICO CIENTÍFICO
# ============================================================

print("\nDiagnóstico:")

constant_components = []

variable_components = []

for component in SIGNATURE_COLUMNS:

    g = summary["components"][component]

    if np.isclose(
        g["max_gradient"],
        0.0,
        atol=1e-12,
    ):

        constant_components.append(component)

    else:

        variable_components.append(component)

print(f"Componentes constantes : {len(constant_components)}")
print(f"Componentes variáveis  : {len(variable_components)}")

if constant_components:

    print("\nConstantes:")

    for c in constant_components:
        print(f"   • {c}")

if variable_components:

    print("\nVariáveis:")

    for c in variable_components:
        print(f"   • {c}")

# ============================================================
# CONCLUSÃO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("GER")
print("E10.1.2.A")
print("Gradient Field")
print("=" * 60)

print(f"Status da auditoria : {audit['status']}")
print(f"Linhas esperadas    : {audit['expected_rows']:,}")
print(f"Linhas produzidas   : {audit['gradient_rows']:,}")
print(f"Valores ausentes    : {audit['missing_values']}")
print(f"Duplicatas          : {audit['duplicate_rows']}")
print(f"Infinitos           : {audit['infinite_values']}")

print("\nProdutos gerados:")

print(f"  • {GRADIENT_FILE.name}")
print(f"  • {SUMMARY_JSON.name}")
print(f"  • {SUMMARY_TXT.name}")
print(f"  • {AUDIT_JSON.name}")
print(f"  • {FIGURES}")

print("=" * 60)
print("Módulo E10.1.2.A concluído.")
print("=" * 60)

def main():

    ...
    # fluxo completo do módulo

if __name__ == "__main__":
    main()
