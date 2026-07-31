"""
=============================================================
E10_1_2_E_dimension.py
=============================================================

GER — Geometria da Superfície Relacional
E10.1.2.E — Effective Dimension

Objetivo
--------
Estimar a dimensionalidade efetiva da superfície relacional
produzida na E10.1.1.

Esta etapa quantifica a complexidade geométrica da superfície,
fornecendo medidas globais da organização espacial obtida
pelos operadores anteriores.

Esta etapa NÃO executa novas simulações.

Entradas
---------
signature_surface.parquet
grid.parquet

Saídas
------
effective_dimension.parquet
effective_dimension_summary.json
effective_dimension_summary.txt
effective_dimension_maps.png

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
    / "E10_1_2_E_Dimension"
)

FIGURES = OUTPUT / "FIGURES"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


# ============================================================
# ARQUIVOS
# ============================================================

SIGNATURE_FILE = ROOT / "signature_surface.parquet"
GRID_FILE = ROOT / "grid.parquet"

DIMENSION_FILE = OUTPUT / "effective_dimension.parquet"

SUMMARY_JSON = OUTPUT / "effective_dimension_summary.json"
SUMMARY_TXT = OUTPUT / "effective_dimension_summary.txt"


# ============================================================
# PARÂMETROS
# ============================================================

# Tolerância numérica utilizada nas estimativas
# de dimensionalidade efetiva.

DIMENSION_TOLERANCE = 1e-12


# ============================================================
# LEITURA DOS DADOS
# ============================================================

print("=" * 60)
print("GER")
print("E10.1.2.E")
print("Effective Dimension")
print("=" * 60)

print("\nCarregando superfície...")

signature = pd.read_parquet(SIGNATURE_FILE)
grid = pd.read_parquet(GRID_FILE)

print(f"Assinaturas      : {len(signature):,}")
print(f"Pontos da malha  : {len(grid):,}")

if len(signature) != len(grid):
    raise RuntimeError(
        "Número de assinaturas diferente da grade."
    )

print("\nSuperfície carregada com sucesso.")


# ============================================================
# COMPONENTES DA ASSINATURA
# ============================================================

RESERVED_COLUMNS = {
    "id",
    "i",
    "j",
    "gamma",
    "omega",
}

SIGNATURE_COLUMNS = [

    column

    for column in signature.columns

    if column not in RESERVED_COLUMNS

]

print("\nComponentes analisadas:")

for component in SIGNATURE_COLUMNS:
    print(f"   • {component}")

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

dimension_frames = []

summary = {

    "gamma_points": int(NG),
    "omega_points": int(NO),
    "tolerance": float(DIMENSION_TOLERANCE),
    "components": {},

}

# ============================================================
# ESTIMATIVA DA DIMENSÃO EFETIVA
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

    # --------------------------------------------------------
    # Dimensões ativas
    # --------------------------------------------------------

    gamma_variation = np.ptp(surface, axis=1)
    omega_variation = np.ptp(surface, axis=0)

    gamma_active = (
        gamma_variation > DIMENSION_TOLERANCE
    )

    omega_active = (
        omega_variation > DIMENSION_TOLERANCE
    )

    active_gamma = int(np.sum(gamma_active))
    active_omega = int(np.sum(omega_active))

    effective_dimension = int(
        (active_gamma > 0)
        +
        (active_omega > 0)
    )

    # --------------------------------------------------------
    # Reconstrução tabular
    # --------------------------------------------------------

    df = (
        pivot
        .stack()
        .reset_index(name="value")
    )

    df["component"] = component

    df["effective_dimension"] = effective_dimension

    df["gamma_active"] = active_gamma

    df["omega_active"] = active_omega

    dimension_frames.append(df)

    # --------------------------------------------------------
    # Estatísticas
    # --------------------------------------------------------

    summary["components"][component] = {

        "effective_dimension":
            effective_dimension,

        "active_gamma_lines":
            active_gamma,

        "active_omega_lines":
            active_omega,

        "inactive_gamma_lines":
            int(NG - active_gamma),

        "inactive_omega_lines":
            int(NO - active_omega),

    }

print("\nDimensionalidade estimada.")

# ============================================================
# DATAFRAME FINAL
# ============================================================

effective_dimension = pd.concat(

    dimension_frames,

    ignore_index=True,

)

print(
    f"Linhas produzidas : "
    f"{len(effective_dimension):,}"
)

print("=" * 60)
# ============================================================
# PERSISTÊNCIA DOS RESULTADOS
# ============================================================

print("\nGravando produtos...")

effective_dimension.to_parquet(
    DIMENSION_FILE,
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

print("Produtos gravados.")

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
    fp.write("E10.1.2.E\n")
    fp.write("Effective Dimension\n")
    fp.write("=" * 60 + "\n\n")

    fp.write(f"Pontos γ : {NG}\n")
    fp.write(f"Pontos ω : {NO}\n")
    fp.write(f"Tolerância : {DIMENSION_TOLERANCE:.2e}\n")
    fp.write(f"Componentes : {len(SIGNATURE_COLUMNS)}\n\n")

    for component in SIGNATURE_COLUMNS:

        s = summary["components"][component]

        fp.write("-" * 50 + "\n")
        fp.write(f"{component}\n")
        fp.write("-" * 50 + "\n")

        fp.write(
            f"Dimensão efetiva     : {s['effective_dimension']}\n"
        )

        fp.write(
            f"Linhas γ ativas      : {s['active_gamma_lines']}\n"
        )

        fp.write(
            f"Linhas ω ativas      : {s['active_omega_lines']}\n"
        )

        fp.write(
            f"Linhas γ inativas    : {s['inactive_gamma_lines']}\n"
        )

        fp.write(
            f"Linhas ω inativas    : {s['inactive_omega_lines']}\n\n"
        )

print("Resumo salvo.")

# ============================================================
# MAPAS DA DIMENSÃO EFETIVA
# ============================================================

print("\nGerando mapas...")

for component in SIGNATURE_COLUMNS:

    subset = effective_dimension[
        effective_dimension["component"] == component
    ]

    surface = (
        subset
        .pivot(
            index="gamma",
            columns="omega",
            values="effective_dimension",
        )
        .sort_index()
        .sort_index(axis=1)
    )

    plt.figure(figsize=(7, 6))

    plt.imshow(
        surface.to_numpy(dtype=float),
        origin="lower",
        aspect="auto",
        interpolation="nearest",
    )

    plt.colorbar(label="Effective Dimension")

    plt.title(
        f"Effective Dimension\n{component}"
    )

    plt.xlabel("ω")
    plt.ylabel("γ")

    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{component}_effective_dimension.png",
        dpi=200,
    )

    plt.close()

print("Mapas concluídos.")

# ============================================================
# RESUMO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("E10.1.2.E FINALIZADO")
print("=" * 60)

print(f"Componentes analisadas : {len(SIGNATURE_COLUMNS)}")
print(f"Arquivo principal      : {DIMENSION_FILE.name}")
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
audit["dimension_rows"] = int(len(effective_dimension))

audit["gamma_points"] = int(NG)
audit["omega_points"] = int(NO)

audit["components"] = list(SIGNATURE_COLUMNS)

audit["expected_rows"] = int(
    len(signature) * len(SIGNATURE_COLUMNS)
)

audit["missing_values"] = int(
    effective_dimension.isna().sum().sum()
)

audit["duplicate_rows"] = int(
    effective_dimension.duplicated().sum()
)

audit["infinite_values"] = int(
    np.isinf(
        effective_dimension.select_dtypes(
            include=[np.number]
        )
    ).sum().sum()
)

audit["status"] = "PASS"

if audit["dimension_rows"] != audit["expected_rows"]:
    audit["status"] = "FAIL"

if audit["missing_values"] > 0:
    audit["status"] = "FAIL"

if audit["duplicate_rows"] > 0:
    audit["status"] = "FAIL"

if audit["infinite_values"] > 0:
    audit["status"] = "FAIL"

AUDIT_JSON = OUTPUT / "effective_dimension_audit.json"

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

dimension0 = []
dimension1 = []
dimension2 = []

for component in SIGNATURE_COLUMNS:

    d = summary["components"][component]["effective_dimension"]

    if d == 0:
        dimension0.append(component)

    elif d == 1:
        dimension1.append(component)

    else:
        dimension2.append(component)

print(
    f"Componentes dimensão 0 : {len(dimension0)}"
)

print(
    f"Componentes dimensão 1 : {len(dimension1)}"
)

print(
    f"Componentes dimensão 2 : {len(dimension2)}"
)

if dimension0:

    print("\nDimensão 0:")

    for component in dimension0:
        print(f"   • {component}")

if dimension1:

    print("\nDimensão 1:")

    for component in dimension1:
        print(f"   • {component}")

if dimension2:

    print("\nDimensão 2:")

    for component in dimension2:
        print(f"   • {component}")

# ============================================================
# CONCLUSÃO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("GER")
print("E10.1.2.E")
print("Effective Dimension")
print("=" * 60)

print(f"Status da auditoria : {audit['status']}")
print(f"Linhas esperadas    : {audit['expected_rows']:,}")
print(f"Linhas produzidas   : {audit['dimension_rows']:,}")
print(f"Valores ausentes    : {audit['missing_values']}")
print(f"Duplicatas          : {audit['duplicate_rows']}")
print(f"Infinitos           : {audit['infinite_values']}")

print("\nProdutos gerados:")

print(f"  • {DIMENSION_FILE.name}")
print(f"  • {SUMMARY_JSON.name}")
print(f"  • {SUMMARY_TXT.name}")
print(f"  • {AUDIT_JSON.name}")
print(f"  • {FIGURES}")

print("=" * 60)
print("Módulo E10.1.2.E concluído.")
print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():
    """
    O fluxo completo deste módulo é executado
    sequencialmente durante a importação.

    Esta função é mantida para padronização da série
    E10.1.2 e permitir execução direta do módulo.
    """
    pass


if __name__ == "__main__":
    main()
