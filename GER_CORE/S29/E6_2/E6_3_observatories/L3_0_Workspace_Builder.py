"""
GER_CORE/S29/E6_2/E6_3_observatories/L3_0_Workspace_Builder.py

GER - Geometria Espectral Relacional
S29 / E6.3

L3.0 - Observatory Workspace Builder

Objetivo
--------
Construir automaticamente um Workspace contendo um catálogo
completo dos artefatos produzidos pela E6.3.

Este módulo NÃO realiza análises científicas.
Sua função é preparar a infraestrutura para todos os
observatórios L3.x.

Autor: Eduardo Batista de Freitas
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

RESULTS_ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.3")

WORKSPACE_DIR = RESULTS_ROOT / "workspace"


# ============================================================
# UTILIDADES
# ============================================================

def discover_files(root: Path):

    exts = ("*.csv", "*.json", "*.txt")

    files = []

    for ext in exts:
        files.extend(root.rglob(ext))

    return sorted(files)


def classify_file(path: Path):

    name = path.name.lower()

    if "correlation" in name:
        return "Correlation"

    if "covariance" in name:
        return "Covariance"

    if "signature" in name:
        return "Signature"

    if "statistics" in name:
        return "Statistics"

    if "matrix" in name:
        return "Matrix"

    if "network" in name:
        return "Network"

    if "metadata" in name:
        return "Metadata"

    return "Unknown"


def inspect_csv(path: Path):

    try:

        df = pd.read_csv(path)

        return {

            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": {
                c: str(t)
                for c, t in df.dtypes.items()
            },
            "missing_values": int(df.isna().sum().sum()),
            "memory_bytes": int(df.memory_usage(deep=True).sum()),
            "status": "OK"

        }

    except Exception as exc:

        return {

            "rows": None,
            "columns": None,
            "column_names": [],
            "dtypes": {},
            "missing_values": None,
            "memory_bytes": None,
            "status": f"ERROR: {exc}"

        }


# ============================================================
# BUILDER
# ============================================================

def build_workspace():

    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    catalog = []

    files = discover_files(RESULTS_ROOT)

    for path in files:

        entry = {

            "name": path.name,
            "relative_path": str(path.relative_to(RESULTS_ROOT)),
            "extension": path.suffix,
            "size_bytes": path.stat().st_size,
            "category": classify_file(path)

        }

        if path.suffix == ".csv":

            info = inspect_csv(path)

            entry.update(info)

        catalog.append(entry)

    df = pd.DataFrame(catalog)

    df.to_csv(
        WORKSPACE_DIR / "workspace_catalog.csv",
        index=False
    )

    with open(
        WORKSPACE_DIR / "workspace_catalog.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            catalog,
            f,
            indent=4,
            ensure_ascii=False
        )

    summary = []

    summary.append("GER WORKSPACE BUILDER")
    summary.append("=" * 60)
    summary.append("")
    summary.append(f"Root : {RESULTS_ROOT}")
    summary.append("")
    summary.append(f"Arquivos encontrados : {len(catalog)}")
    summary.append(f"CSV : {sum(df.extension=='.csv')}")
    summary.append(f"JSON : {sum(df.extension=='.json')}")
    summary.append(f"TXT : {sum(df.extension=='.txt')}")
    summary.append("")
    summary.append("Categorias:")

    for cat, count in df.category.value_counts().items():

        summary.append(f"  {cat:<20} {count}")

    with open(
        WORKSPACE_DIR / "workspace_summary.txt",
        "w",
        encoding="utf8"
    ) as f:

        f.write("\n".join(summary))

    index = {

        row["name"]: row["relative_path"]

        for _, row in df.iterrows()

    }

    with open(
        WORKSPACE_DIR / "workspace_index.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            index,
            f,
            indent=4,
            ensure_ascii=False
        )

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print(" GER WORKSPACE BUILDER")
    print("=" * 60)

    df = build_workspace()

    print()
    print(df[[
        "name",
        "category",
        "rows",
        "columns",
        "status"
    ]])

    print()
    print("=" * 60)
    print("Workspace criado com sucesso.")
    print(WORKSPACE_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()
