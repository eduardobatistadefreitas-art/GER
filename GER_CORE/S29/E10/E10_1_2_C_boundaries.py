"""
=============================================================
E10_1_2_C_boundaries.py
=============================================================

GER — Geometria da Superfície Relacional
E10.1.2.C — Surface Boundaries

Objetivo
--------
Identificar fronteiras geométricas na superfície relacional
produzida na E10.1.1.

Uma fronteira é definida como uma região onde ocorre uma
mudança significativa entre vizinhos da malha, indicando uma
transição estrutural local.

Esta etapa NÃO executa novas simulações.

Entradas
---------
signature_surface.parquet
grid.parquet

Saídas
------
boundary_surface.parquet
boundary_summary.json
boundary_summary.txt
boundary_maps.png

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
    / "E10_1_2_C_Boundaries"
)

FIGURES = OUTPUT / "FIGURES"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


# ============================================================
# ARQUIVOS
# ============================================================

SIGNATURE_FILE = ROOT / "signature_surface.parquet"
GRID_FILE = ROOT / "grid.parquet"

BOUNDARY_FILE = OUTPUT / "boundary_surface.parquet"

SUMMARY_JSON = OUTPUT / "boundary_summary.json"
SUMMARY_TXT = OUTPUT / "boundary_summary.txt"


# ============================================================
# PARÂMETROS
# ============================================================

# Limiar para caracterização de uma fronteira.
# Valores superiores a este limite serão classificados
# como pertencentes a uma região de transição.

BOUNDARY_THRESHOLD = 1e-10


# ============================================================
# LEITURA DOS DADOS
# ============================================================

print("=" * 60)
print("GER")
print("E10.1.2.C")
print("Surface Boundaries")
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

boundary_frames = []

summary = {

    "gamma_points": int(NG),
    "omega_points": int(NO),
    "threshold": float(BOUNDARY_THRESHOLD),
    "components": {},

}

# ============================================================
# DETECÇÃO DE FRONTEIRAS
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
    # Variações locais
    # --------------------------------------------------------

    delta_gamma = np.zeros_like(surface)
    delta_omega = np.zeros_like(surface)

    delta_gamma[:-1, :] = np.abs(
        surface[1:, :] - surface[:-1, :]
    )

    delta_omega[:, :-1] = np.abs(
        surface[:, 1:] - surface[:, :-1]
    )

    boundary_strength = np.maximum(
        delta_gamma,
        delta_omega,
    )

    boundary_mask = (
        boundary_strength >= BOUNDARY_THRESHOLD
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

    df["delta_gamma"] = delta_gamma.ravel()
    df["delta_omega"] = delta_omega.ravel()

    df["boundary_strength"] = (
        boundary_strength.ravel()
    )

    df["is_boundary"] = (
        boundary_mask.ravel()
    )

    boundary_frames.append(df)

    # --------------------------------------------------------
    # Estatísticas
    # --------------------------------------------------------

    summary["components"][component] = {

        "min_strength":
            float(np.min(boundary_strength)),

        "max_strength":
            float(np.max(boundary_strength)),

        "mean_strength":
            float(np.mean(boundary_strength)),

        "std_strength":
            float(np.std(boundary_strength)),

        "boundary_fraction":
            float(
                np.mean(boundary_mask)
            ),

        "interior_fraction":
            float(
                1.0 -
                np.mean(boundary_mask)
            ),

    }

print("\nFronteiras identificadas.")

# ============================================================
# DATAFRAME FINAL
# ============================================================

boundary_surface = pd.concat(

    boundary_frames,

    ignore_index=True,

)

print(
    f"Linhas produzidas : "
    f"{len(boundary_surface):,}"
)

print("=" * 60)

# ============================================================
# PERSISTÊNCIA DOS RESULTADOS
# ============================================================

print("\nGravando produtos...")

boundary_surface.to_parquet(
    BOUNDARY_FILE,
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
    fp.write("E10.1.2.C\n")
    fp.write("Surface Boundaries\n")
    fp.write("=" * 60 + "\n\n")

    fp.write(f"Pontos γ : {NG}\n")
    fp.write(f"Pontos ω : {NO}\n")
    fp.write(f"Limiar : {BOUNDARY_THRESHOLD:.2e}\n")
    fp.write(f"Componentes : {len(SIGNATURE_COLUMNS)}\n\n")

    for component in SIGNATURE_COLUMNS:

        s = summary["components"][component]

        fp.write("-" * 50 + "\n")
        fp.write(f"{component}\n")
        fp.write("-" * 50 + "\n")

        fp.write(f"Força mínima       : {s['min_strength']:.6e}\n")
        fp.write(f"Força máxima       : {s['max_strength']:.6e}\n")
        fp.write(f"Força média        : {s['mean_strength']:.6e}\n")
        fp.write(f"Desvio padrão      : {s['std_strength']:.6e}\n")
        fp.write(f"Fronteiras         : {100*s['boundary_fraction']:.2f}%\n")
        fp.write(f"Interior           : {100*s['interior_fraction']:.2f}%\n\n")

print("Resumo salvo.")

# ============================================================
# MAPAS DE FRONTEIRAS
# ============================================================

print("\nGerando mapas...")

for component in SIGNATURE_COLUMNS:

    subset = boundary_surface[
        boundary_surface["component"] == component
    ]

    surface = (
        subset
        .pivot(
            index="gamma",
            columns="omega",
            values="is_boundary",
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

    plt.colorbar(label="Boundary")

    plt.title(
        f"Boundary Map\n{component}"
    )

    plt.xlabel("ω")
    plt.ylabel("γ")

    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{component}_boundaries.png",
        dpi=200,
    )

    plt.close()

print("Mapas concluídos.")

# ============================================================
# RESUMO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("E10.1.2.C FINALIZADO")
print("=" * 60)

print(f"Componentes analisadas : {len(SIGNATURE_COLUMNS)}")
print(f"Arquivo principal      : {BOUNDARY_FILE.name}")
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
audit["boundary_rows"] = int(len(boundary_surface))

audit["gamma_points"] = int(NG)
audit["omega_points"] = int(NO)

audit["components"] = list(SIGNATURE_COLUMNS)

audit["expected_rows"] = int(
    len(signature) * len(SIGNATURE_COLUMNS)
)

audit["missing_values"] = int(
    boundary_surface.isna().sum().sum()
)

audit["duplicate_rows"] = int(
    boundary_surface.duplicated().sum()
)

audit["infinite_values"] = int(
    np.isinf(
        boundary_surface.select_dtypes(
            include=[np.number]
        )
    ).sum().sum()
)

audit["status"] = "PASS"

if audit["boundary_rows"] != audit["expected_rows"]:
    audit["status"] = "FAIL"

if audit["missing_values"] > 0:
    audit["status"] = "FAIL"

if audit["duplicate_rows"] > 0:
    audit["status"] = "FAIL"

if audit["infinite_values"] > 0:
    audit["status"] = "FAIL"

AUDIT_JSON = OUTPUT / "boundary_audit.json"

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

boundary_free = []
boundary_detected = []

for component in SIGNATURE_COLUMNS:

    s = summary["components"][component]

    if np.isclose(
        s["boundary_fraction"],
        0.0,
        atol=1e-12,
    ):

        boundary_free.append(component)

    else:

        boundary_detected.append(component)

print(
    f"Componentes sem fronteiras : "
    f"{len(boundary_free)}"
)

print(
    f"Componentes com fronteiras : "
    f"{len(boundary_detected)}"
)

if boundary_free:

    print("\nSem fronteiras:")

    for component in boundary_free:
        print(f"   • {component}")

if boundary_detected:

    print("\nCom fronteiras:")

    for component in boundary_detected:
        print(f"   • {component}")

# ============================================================
# CONCLUSÃO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("GER")
print("E10.1.2.C")
print("Surface Boundaries")
print("=" * 60)

print(f"Status da auditoria : {audit['status']}")
print(f"Linhas esperadas    : {audit['expected_rows']:,}")
print(f"Linhas produzidas   : {audit['boundary_rows']:,}")
print(f"Valores ausentes    : {audit['missing_values']}")
print(f"Duplicatas          : {audit['duplicate_rows']}")
print(f"Infinitos           : {audit['infinite_values']}")

print("\nProdutos gerados:")

print(f"  • {BOUNDARY_FILE.name}")
print(f"  • {SUMMARY_JSON.name}")
print(f"  • {SUMMARY_TXT.name}")
print(f"  • {AUDIT_JSON.name}")
print(f"  • {FIGURES}")

print("=" * 60)
print("Módulo E10.1.2.C concluído.")
print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():
    """
    O fluxo completo deste módulo é executado
    sequencialmente durante a importação.

    Esta função é mantida para padronização da série
    E10.1.2 e para permitir execução direta do módulo.
    """
    pass


if __name__ == "__main__":
    main()
