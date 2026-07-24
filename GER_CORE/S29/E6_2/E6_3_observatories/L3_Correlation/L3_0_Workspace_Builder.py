"""
GER_CORE/S29/E6_2/E6_3_observatories/L3_0_Workspace_Builder.py

GER - Geometria Espectral Relacional
S29 / E6.3

L3.0 - Observatory Workspace Builder

Constrói automaticamente um Workspace contendo um catálogo
completo dos artefatos produzidos pela E6.3.

Suporta:

    CSV
    PARQUET
    JSON
    TXT

Autor: Eduardo Batista de Freitas
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E6.3"
)

WORKSPACE_DIR = RESULTS_ROOT / "workspace"


# ============================================================
# DESCOBERTA
# ============================================================

SUPPORTED_EXTENSIONS = (

    "*.csv",
    "*.parquet",
    "*.json",
    "*.txt",

)


def discover_files(root: Path):

    files = []

    for pattern in SUPPORTED_EXTENSIONS:

        files.extend(root.rglob(pattern))

    return sorted(files)


# ============================================================
# CLASSIFICAÇÃO
# ============================================================

def classify_file(path: Path):

    name = path.name.lower()

    if "signature" in name:
        return "Signature"

    if "universe" in name:
        return "Universe"

    if "certificate" in name:
        return "Certificate"

    if "correlation" in name:
        return "Correlation"

    if "statistics" in name:
        return "Statistics"

    if "matrix" in name:
        return "Matrix"

    if "network" in name:
        return "Network"

    if "metadata" in name:
        return "Metadata"

    return "Unknown"


# ============================================================
# LEITURA
# ============================================================

def load_dataframe(path: Path):

    suffix = path.suffix.lower()

    if suffix == ".csv":

        return pd.read_csv(path)

    if suffix == ".parquet":

        return pd.read_parquet(path)

    return None


# ============================================================
# INSPEÇÃO
# ============================================================

def inspect_table(path: Path):

    try:

        df = load_dataframe(path)

        if df is None:

            return {

                "rows": None,
                "columns": None,
                "column_names": [],
                "dtypes": {},
                "missing_values": None,
                "memory_bytes": None,
                "preview": [],
                "status": "NOT_A_TABLE"

            }

        preview = (
            df
            .head(5)
            .to_dict(orient="records")
        )

        return {

            "rows": int(len(df)),

            "columns": int(len(df.columns)),

            "column_names": list(df.columns),

            "dtypes": {

                c: str(t)

                for c, t in df.dtypes.items()

            },

            "missing_values": int(
                df.isna().sum().sum()
            ),

            "memory_bytes": int(
                df.memory_usage(
                    deep=True
                ).sum()
            ),

            "preview": preview,

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
            "preview": [],
            "status": f"ERROR: {exc}"

        }

# ============================================================
# WORKSPACE BUILDER
# ============================================================

def build_workspace():

    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    files = discover_files(RESULTS_ROOT)

    catalog = []
    schemas = {}
    previews = {}

    for path in files:

        entry = {

            "name": path.name,
            "relative_path": str(path.relative_to(RESULTS_ROOT)),
            "extension": path.suffix.lower(),
            "category": classify_file(path),
            "size_bytes": path.stat().st_size

        }

        info = inspect_table(path)

        entry.update(info)

        catalog.append(entry)

        if info["status"] == "OK":

            schemas[path.name] = {

                "rows": info["rows"],
                "columns": info["columns"],
                "column_names": info["column_names"],
                "dtypes": info["dtypes"],
                "missing_values": info["missing_values"],
                "memory_bytes": info["memory_bytes"]

            }

            previews[path.name] = info["preview"]

    df = pd.DataFrame(catalog)

    # --------------------------------------------------------
    # CATÁLOGO CSV
    # --------------------------------------------------------

    df.to_csv(

        WORKSPACE_DIR / "workspace_catalog.csv",

        index=False

    )

    # --------------------------------------------------------
    # CATÁLOGO JSON
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # SCHEMA
    # --------------------------------------------------------

    with open(

        WORKSPACE_DIR / "workspace_schema.json",

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            schemas,

            f,

            indent=4,

            ensure_ascii=False

        )

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    with open(

        WORKSPACE_DIR / "workspace_preview.json",

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            previews,

            f,

            indent=4,

            ensure_ascii=False,

            default=str

        )

    # --------------------------------------------------------
    # INDEX
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = []

    summary.append("GER WORKSPACE BUILDER")
    summary.append("=" * 60)
    summary.append("")
    summary.append(f"ROOT : {RESULTS_ROOT}")
    summary.append("")
    summary.append(f"TOTAL FILES : {len(df)}")
    summary.append("")

    for ext in [".csv", ".parquet", ".json", ".txt"]:

        count = int((df["extension"] == ext).sum())

        summary.append(f"{ext:<10} : {count}")

    summary.append("")
    summary.append("CATEGORIES")
    summary.append("-" * 60)

    for cat, count in df["category"].value_counts().items():

        summary.append(f"{cat:<20} {count}")

    with open(

        WORKSPACE_DIR / "workspace_summary.txt",

        "w",

        encoding="utf8"

    ) as f:

        f.write("\n".join(summary))

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("GER WORKSPACE BUILDER")
    print("=" * 60)
    print()

    df = build_workspace()

    print("DATASETS")
    print("-" * 60)

    for _, row in df.iterrows():

        print()

        print(f"✓ {row['name']}")

        print(f"    Category : {row['category']}")

        print(f"    Type     : {row['extension']}")

        if pd.notna(row["rows"]):

            print(f"    Rows     : {int(row['rows'])}")

            print(f"    Columns  : {int(row['columns'])}")

            if isinstance(row["column_names"], list):

                print("")

                print("    Fields")

                for col in row["column_names"]:

                    print(f"       - {col}")

        else:

            print("    Non-tabular file")

    print()
    print("=" * 60)

    print("SUMMARY")

    print("=" * 60)

    print(f"Files       : {len(df)}")

    print(f"CSV         : {(df.extension=='.csv').sum()}")

    print(f"PARQUET     : {(df.extension=='.parquet').sum()}")

    print(f"JSON        : {(df.extension=='.json').sum()}")

    print(f"TXT         : {(df.extension=='.txt').sum()}")

    print()

    print("Workspace")

    print(WORKSPACE_DIR)

    print()

    print("Generated")

    print("   workspace_catalog.csv")

    print("   workspace_catalog.json")

    print("   workspace_schema.json")

    print("   workspace_preview.json")

    print("   workspace_index.json")

    print("   workspace_summary.txt")

    print()

    print("=" * 60)

    print("Workspace successfully built.")

    print("=" * 60)


if __name__ == "__main__":

    main()
