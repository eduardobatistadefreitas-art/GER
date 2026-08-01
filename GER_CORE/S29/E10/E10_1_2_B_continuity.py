"""
=============================================================
E10_1_2_B_continuity.py
=============================================================

GER — Geometria da Superfície Relacional
E10.1.2.B — Surface Continuity

Objetivo
--------
Analisar a continuidade local e global da superfície
relacional construída na E10.1.1.

Esta etapa NÃO executa novas simulações.

Ela apenas verifica se componentes vizinhas da superfície
apresentam variações compatíveis com uma superfície contínua.

Entradas
---------
signature_surface.parquet
grid.parquet

Saídas
------
continuity_surface.parquet
continuity_summary.json
continuity_summary.txt
continuity_maps.png

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
    / "E10_1_2_B_Continuity"
)

FIGURES = OUTPUT / "FIGURES"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


# ============================================================
# ARQUIVOS
# ============================================================

SIGNATURE_FILE = ROOT / "signature_surface.parquet"
GRID_FILE = ROOT / "grid.parquet"

CONTINUITY_FILE = OUTPUT / "continuity_surface.parquet"

SUMMARY_JSON = OUTPUT / "continuity_summary.json"
SUMMARY_TXT = OUTPUT / "continuity_summary.txt"


# ============================================================
# PARÂMETROS
# ============================================================

# Tolerância para considerar continuidade local.
# Mantida explícita para facilitar auditorias futuras.
CONTINUITY_TOLERANCE = 1e-12


# ============================================================
# LEITURA DOS DADOS
# ============================================================

print("=" * 60)
print("GER")
print("E10.1.2.B")
print("Surface Continuity")
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

continuity_frames = []

summary = {

    "gamma_points": int(NG),
    "omega_points": int(NO),
    "tolerance": float(CONTINUITY_TOLERANCE),
    "components": {},

}

# ============================================================
# ANÁLISE DE CONTINUIDADE
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
    # Diferenças locais
    # --------------------------------------------------------

    delta_gamma = np.zeros_like(surface)
    delta_omega = np.zeros_like(surface)

    delta_gamma[:-1, :] = np.abs(
        surface[1:, :] - surface[:-1, :]
    )

    delta_omega[:, :-1] = np.abs(
        surface[:, 1:] - surface[:, :-1]
    )

    max_delta = np.maximum(
        delta_gamma,
        delta_omega,
    )

    continuity_mask = (
        max_delta <= CONTINUITY_TOLERANCE
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

    df["max_delta"] = max_delta.ravel()

    df["continuous"] = continuity_mask.ravel()

    continuity_frames.append(df)

    # --------------------------------------------------------
    # Estatísticas
    # --------------------------------------------------------

    summary["components"][component] = {

        "min_delta":
            float(np.min(max_delta)),

        "max_delta":
            float(np.max(max_delta)),

        "mean_delta":
            float(np.mean(max_delta)),

        "std_delta":
            float(np.std(max_delta)),

        "continuous_fraction":
            float(
                np.mean(
                    continuity_mask
                )
            ),

        "discontinuous_fraction":
            float(
                1.0 -
                np.mean(
                    continuity_mask
                )
            ),

    }

print("\nContinuidade analisada.")

# ============================================================
# DATAFRAME FINAL
# ============================================================

continuity_surface = pd.concat(

    continuity_frames,

    ignore_index=True,

)

print(
    f"Linhas produzidas : "
    f"{len(continuity_surface):,}"
)

print("=" * 60)
# ============================================================
# PERSISTÊNCIA DOS RESULTADOS
# ============================================================

print("\nGravando produtos...")

continuity_surface.to_parquet(
    CONTINUITY_FILE,
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
    fp.write("E10.1.2.B\n")
    fp.write("Surface Continuity\n")
    fp.write("=" * 60 + "\n\n")

    fp.write(f"Pontos γ : {NG}\n")
    fp.write(f"Pontos ω : {NO}\n")
    fp.write(f"Tolerância : {CONTINUITY_TOLERANCE:.2e}\n")
    fp.write(f"Componentes : {len(SIGNATURE_COLUMNS)}\n\n")

    for component in SIGNATURE_COLUMNS:

        s = summary["components"][component]

        fp.write("-" * 50 + "\n")
        fp.write(f"{component}\n")
        fp.write("-" * 50 + "\n")

        fp.write(f"Δ mínimo            : {s['min_delta']:.6e}\n")
        fp.write(f"Δ máximo            : {s['max_delta']:.6e}\n")
        fp.write(f"Δ médio             : {s['mean_delta']:.6e}\n")
        fp.write(f"Desvio padrão       : {s['std_delta']:.6e}\n")
        fp.write(f"Continuidade        : {100*s['continuous_fraction']:.2f}%\n")
        fp.write(f"Descontinuidade     : {100*s['discontinuous_fraction']:.2f}%\n\n")

print("Resumo salvo.")

# ============================================================
# MAPAS DE CONTINUIDADE
# ============================================================

print("\nGerando mapas...")

for component in SIGNATURE_COLUMNS:

    subset = continuity_surface[
        continuity_surface["component"] == component
    ]

    surface = (
        subset
        .pivot(
            index="gamma",
            columns="omega",
            values="continuous",
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

    plt.colorbar(label="Continuidade")

    plt.title(
        f"Continuity Map\n{component}"
    )

    plt.xlabel("ω")
    plt.ylabel("γ")

    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{component}_continuity.png",
        dpi=200,
    )

    plt.close()

print("Mapas concluídos.")

# ============================================================
# RESUMO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("E10.1.2.B FINALIZADO")
print("=" * 60)

print(f"Componentes analisadas : {len(SIGNATURE_COLUMNS)}")
print(f"Arquivo principal      : {CONTINUITY_FILE.name}")
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
audit["continuity_rows"] = int(len(continuity_surface))

audit["gamma_points"] = int(NG)
audit["omega_points"] = int(NO)

audit["components"] = list(SIGNATURE_COLUMNS)

audit["expected_rows"] = int(
    len(signature) * len(SIGNATURE_COLUMNS)
)

audit["missing_values"] = int(
    continuity_surface.isna().sum().sum()
)

audit["duplicate_rows"] = int(
    continuity_surface.duplicated().sum()
)

audit["infinite_values"] = int(
    np.isinf(
        continuity_surface.select_dtypes(
            include=[np.number]
        )
    ).sum().sum()
)

audit["status"] = "PASS"

if audit["continuity_rows"] != audit["expected_rows"]:
    audit["status"] = "FAIL"

if audit["missing_values"] > 0:
    audit["status"] = "FAIL"

if audit["duplicate_rows"] > 0:
    audit["status"] = "FAIL"

if audit["infinite_values"] > 0:
    audit["status"] = "FAIL"

AUDIT_JSON = OUTPUT / "continuity_audit.json"

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

fully_continuous = []
partially_discontinuous = []

for component in SIGNATURE_COLUMNS:

    s = summary["components"][component]

    if np.isclose(
        s["continuous_fraction"],
        1.0,
        atol=1e-12,
    ):

        fully_continuous.append(component)

    else:

        partially_discontinuous.append(component)

print(
    f"Componentes totalmente contínuas : "
    f"{len(fully_continuous)}"
)

print(
    f"Componentes com descontinuidades : "
    f"{len(partially_discontinuous)}"
)

if fully_continuous:

    print("\nContínuas:")

    for component in fully_continuous:
        print(f"   • {component}")

if partially_discontinuous:

    print("\nCom descontinuidades:")

    for component in partially_discontinuous:
        print(f"   • {component}")

# ============================================================
# CONCLUSÃO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("GER")
print("E10.1.2.B")
print("Surface Continuity")
print("=" * 60)

print(f"Status da auditoria : {audit['status']}")
print(f"Linhas esperadas    : {audit['expected_rows']:,}")
print(f"Linhas produzidas   : {audit['continuity_rows']:,}")
print(f"Valores ausentes    : {audit['missing_values']}")
print(f"Duplicatas          : {audit['duplicate_rows']}")
print(f"Infinitos           : {audit['infinite_values']}")

print("\nProdutos gerados:")

print(f"  • {CONTINUITY_FILE.name}")
print(f"  • {SUMMARY_JSON.name}")
print(f"  • {SUMMARY_TXT.name}")
print(f"  • {AUDIT_JSON.name}")
print(f"  • {FIGURES}")

print("=" * 60)
print("Módulo E10.1.2.B concluído.")
print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():
    """
    O fluxo completo do módulo é executado sequencialmente
    durante a importação deste arquivo.

    Esta função existe para manter a padronização da série
    E10.1.2 e permitir execução direta do módulo.
    """
    pass


if __name__ == "__main__":
    main()
