"""
=============================================================
E10_1_2_D_connected_regions.py
=============================================================

GER — Geometria da Superfície Relacional
E10.1.2.D — Connected Regions

Objetivo
--------
Identificar regiões conectadas da superfície relacional.

Cada região corresponde a um conjunto máximo de pontos
adjacentes que pertencem ao mesmo domínio estrutural.

Esta etapa NÃO executa novas simulações.

Entradas
---------
signature_surface.parquet
grid.parquet

Saídas
------
connected_regions.parquet
connected_regions_summary.json
connected_regions_summary.txt
connected_regions_maps.png

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
    / "E10_1_2_D_ConnectedRegions"
)

FIGURES = OUTPUT / "FIGURES"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


# ============================================================
# ARQUIVOS
# ============================================================

SIGNATURE_FILE = ROOT / "signature_surface.parquet"
GRID_FILE = ROOT / "grid.parquet"

CONNECTED_FILE = OUTPUT / "connected_regions.parquet"

SUMMARY_JSON = OUTPUT / "connected_regions_summary.json"
SUMMARY_TXT = OUTPUT / "connected_regions_summary.txt"


# ============================================================
# PARÂMETROS
# ============================================================

# Tolerância para considerar dois pontos pertencentes
# à mesma região conectada.

CONNECTIVITY_TOLERANCE = 1e-12


# ============================================================
# LEITURA DOS DADOS
# ============================================================

print("=" * 60)
print("GER")
print("E10.1.2.D")
print("Connected Regions")
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

connected_frames = []

summary = {

    "gamma_points": int(NG),
    "omega_points": int(NO),
    "tolerance": float(CONNECTIVITY_TOLERANCE),
    "components": {},

}

# ============================================================
# IDENTIFICAÇÃO DAS REGIÕES CONECTADAS
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

    nrows, ncols = surface.shape

    region_map = -np.ones(
        (nrows, ncols),
        dtype=int,
    )

    region_id = 0

    # --------------------------------------------------------
    # Flood-fill por conectividade 4-neighbors
    # --------------------------------------------------------

    for i in range(nrows):

        for j in range(ncols):

            if region_map[i, j] >= 0:
                continue

            seed_value = surface[i, j]

            stack = [(i, j)]

            region_map[i, j] = region_id

            while stack:

                x, y = stack.pop()

                for dx, dy in (
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1),
                ):

                    xx = x + dx
                    yy = y + dy

                    if (
                        xx < 0
                        or xx >= nrows
                        or yy < 0
                        or yy >= ncols
                    ):
                        continue

                    if region_map[xx, yy] >= 0:
                        continue

                    if np.abs(
                        surface[xx, yy] - seed_value
                    ) <= CONNECTIVITY_TOLERANCE:

                        region_map[xx, yy] = region_id
                        stack.append((xx, yy))

            region_id += 1

    # --------------------------------------------------------
    # Estatísticas das regiões
    # --------------------------------------------------------

    unique_regions, counts = np.unique(
        region_map,
        return_counts=True,
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

    df["region_id"] = region_map.ravel()

    connected_frames.append(df)

    summary["components"][component] = {

        "number_of_regions":
            int(len(unique_regions)),

        "largest_region":
            int(np.max(counts)),

        "smallest_region":
            int(np.min(counts)),

        "mean_region_size":
            float(np.mean(counts)),

        "std_region_size":
            float(np.std(counts)),

    }

print("\nRegiões conectadas identificadas.")

# ============================================================
# DATAFRAME FINAL
# ============================================================

connected_regions = pd.concat(

    connected_frames,

    ignore_index=True,

)

print(
    f"Linhas produzidas : "
    f"{len(connected_regions):,}"
)

print("=" * 60)

# ============================================================
# PERSISTÊNCIA DOS RESULTADOS
# ============================================================

print("\nGravando produtos...")

connected_regions.to_parquet(
    CONNECTED_FILE,
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
    fp.write("E10.1.2.D\n")
    fp.write("Connected Regions\n")
    fp.write("=" * 60 + "\n\n")

    fp.write(f"Pontos γ : {NG}\n")
    fp.write(f"Pontos ω : {NO}\n")
    fp.write(f"Tolerância : {CONNECTIVITY_TOLERANCE:.2e}\n")
    fp.write(f"Componentes : {len(SIGNATURE_COLUMNS)}\n\n")

    for component in SIGNATURE_COLUMNS:

        s = summary["components"][component]

        fp.write("-" * 50 + "\n")
        fp.write(f"{component}\n")
        fp.write("-" * 50 + "\n")

        fp.write(
            f"Número de regiões     : {s['number_of_regions']}\n"
        )

        fp.write(
            f"Maior região          : {s['largest_region']}\n"
        )

        fp.write(
            f"Menor região          : {s['smallest_region']}\n"
        )

        fp.write(
            f"Tamanho médio         : {s['mean_region_size']:.4f}\n"
        )

        fp.write(
            f"Desvio padrão         : {s['std_region_size']:.4f}\n\n"
        )

print("Resumo salvo.")

# ============================================================
# MAPAS DAS REGIÕES CONECTADAS
# ============================================================

print("\nGerando mapas...")

for component in SIGNATURE_COLUMNS:

    subset = connected_regions[
        connected_regions["component"] == component
    ]

    surface = (
        subset
        .pivot(
            index="gamma",
            columns="omega",
            values="region_id",
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

    plt.colorbar(label="Region ID")

    plt.title(
        f"Connected Regions\n{component}"
    )

    plt.xlabel("ω")
    plt.ylabel("γ")

    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{component}_connected_regions.png",
        dpi=200,
    )

    plt.close()

print("Mapas concluídos.")

# ============================================================
# RESUMO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("E10.1.2.D FINALIZADO")
print("=" * 60)

print(f"Componentes analisadas : {len(SIGNATURE_COLUMNS)}")
print(f"Arquivo principal      : {CONNECTED_FILE.name}")
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
audit["connected_rows"] = int(len(connected_regions))

audit["gamma_points"] = int(NG)
audit["omega_points"] = int(NO)

audit["components"] = list(SIGNATURE_COLUMNS)

audit["expected_rows"] = int(
    len(signature) * len(SIGNATURE_COLUMNS)
)

audit["missing_values"] = int(
    connected_regions.isna().sum().sum()
)

audit["duplicate_rows"] = int(
    connected_regions.duplicated().sum()
)

audit["infinite_values"] = int(
    np.isinf(
        connected_regions.select_dtypes(
            include=[np.number]
        )
    ).sum().sum()
)

audit["status"] = "PASS"

if audit["connected_rows"] != audit["expected_rows"]:
    audit["status"] = "FAIL"

if audit["missing_values"] > 0:
    audit["status"] = "FAIL"

if audit["duplicate_rows"] > 0:
    audit["status"] = "FAIL"

if audit["infinite_values"] > 0:
    audit["status"] = "FAIL"

AUDIT_JSON = OUTPUT / "connected_regions_audit.json"

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

single_region = []
multiple_regions = []

for component in SIGNATURE_COLUMNS:

    s = summary["components"][component]

    if s["number_of_regions"] == 1:

        single_region.append(component)

    else:

        multiple_regions.append(component)

print(
    f"Componentes com uma única região : "
    f"{len(single_region)}"
)

print(
    f"Componentes com múltiplas regiões : "
    f"{len(multiple_regions)}"
)

if single_region:

    print("\nRegião única:")

    for component in single_region:
        print(f"   • {component}")

if multiple_regions:

    print("\nMúltiplas regiões:")

    for component in multiple_regions:
        print(f"   • {component}")

# ============================================================
# CONCLUSÃO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("GER")
print("E10.1.2.D")
print("Connected Regions")
print("=" * 60)

print(f"Status da auditoria : {audit['status']}")
print(f"Linhas esperadas    : {audit['expected_rows']:,}")
print(f"Linhas produzidas   : {audit['connected_rows']:,}")
print(f"Valores ausentes    : {audit['missing_values']}")
print(f"Duplicatas          : {audit['duplicate_rows']}")
print(f"Infinitos           : {audit['infinite_values']}")

print("\nProdutos gerados:")

print(f"  • {CONNECTED_FILE.name}")
print(f"  • {SUMMARY_JSON.name}")
print(f"  • {SUMMARY_TXT.name}")
print(f"  • {AUDIT_JSON.name}")
print(f"  • {FIGURES}")

print("=" * 60)
print("Módulo E10.1.2.D concluído.")
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
