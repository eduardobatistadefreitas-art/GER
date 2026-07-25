"""
GER_CORE/S29/E6_2/E6_3_observatories/L3_Correlation/L3_0_Workspace.py

============================================================
GER
S29 - E6.3

L3.0 - Workspace Manager
============================================================

Responsabilidades

- Descobrir datasets
- Detectar datasets lógicos
- Suportar arquivo único e chunk_*.parquet
- Construir catálogo
- Disponibilizar API para todos os L3

"""

from __future__ import annotations

import json
import re

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E6.3"
)

WORKSPACE_DIR = RESULTS_ROOT / "workspace"


SUPPORTED_EXTENSIONS = (

    ".parquet",
    ".csv",
    ".json",
    ".txt",

)


CHUNK_PATTERN = re.compile(
    r"chunk_(\d+)\.parquet$",
    re.IGNORECASE
)


# ============================================================
# JSON SERIALIZER
# ============================================================

def json_serializer(obj):

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.bool_):
        return bool(obj)

    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()

    if isinstance(obj, pd.Timedelta):
        return str(obj)

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, set):
        return list(obj)

    return str(obj)


# ============================================================
# FILE DISCOVERY
# ============================================================

def discover_files(root: Path):

    files = []

    for ext in SUPPORTED_EXTENSIONS:

        files.extend(root.rglob(f"*{ext}"))

    return sorted(files)


# ============================================================
# FILE CLASSIFICATION
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

    if "checkpoint" in name:
        return "Checkpoint"

    if "metadata" in name:
        return "Metadata"

    if "network" in name:
        return "Network"

    if "matrix" in name:
        return "Matrix"

    if "log" in name:
        return "Log"

    return "Unknown"


# ============================================================
# DATASET DISCOVERY
# ============================================================

def discover_datasets(files):

    datasets = {}

    for file in files:

        # ----------------------------------------------------
        # chunk_XXXX.parquet
        # ----------------------------------------------------

        if CHUNK_PATTERN.match(file.name):

            dataset_name = file.parent.name

            if dataset_name not in datasets:

                datasets[dataset_name] = {

                    "name": dataset_name,
                    "logical": True,
                    "chunked": True,
                    "chunks": [],
                    "files": []

                }

            datasets[dataset_name]["chunks"].append(file)
            datasets[dataset_name]["files"].append(file)

            continue

        # ----------------------------------------------------
        # parquet único
        # ----------------------------------------------------

        if file.suffix == ".parquet":

            dataset_name = file.stem

            datasets[dataset_name] = {

                "name": dataset_name,
                "logical": True,
                "chunked": False,
                "chunks": [],
                "files": [file]

            }

            continue

        # ----------------------------------------------------
        # arquivos auxiliares
        # ----------------------------------------------------

        datasets[file.name] = {

            "name": file.name,
            "logical": False,
            "chunked": False,
            "chunks": [],
            "files": [file]

        }

    # ordenar chunks

    for dataset in datasets.values():

        dataset["chunks"] = sorted(dataset["chunks"])

    return datasets


# ============================================================
# DATAFRAME LOADER
# ============================================================

def load_single_dataframe(path: Path):

    if path.suffix == ".csv":
        return pd.read_csv(path)

    if path.suffix == ".parquet":
        return pd.read_parquet(path)

    return None


# ============================================================
# DATASET METADATA
# ============================================================

def build_dataset_metadata(dataset):

    files = dataset["files"]

    size = sum(
        f.stat().st_size
        for f in files
    )

    metadata = {

        "name": dataset["name"],

        "logical": dataset["logical"],

        "chunked": dataset["chunked"],

        "chunks": len(dataset["chunks"]),

        "files": len(files),

        "size_bytes": int(size),

        "category": classify_file(files[0]),

        "rows": None,

        "columns": None,

        "column_names": [],

        "dtypes": {},

        "missing_values": None,

        "memory_bytes": None,

        "status": "UNKNOWN"

    }

    return metadata

# ============================================================
# WORKSPACE
# ============================================================

class Workspace:

    def __init__(self, root: Path = RESULTS_ROOT):

        self.root = Path(root)

        self.files = discover_files(self.root)

        self.datasets = discover_datasets(self.files)

        self.metadata = {}

        self._inspect_all()

    # ========================================================
    # INTERNAL
    # ========================================================

    def _inspect_all(self):

        for name, dataset in self.datasets.items():

            self.metadata[name] = self._inspect_dataset(dataset)

    # --------------------------------------------------------

    def _inspect_dataset(self, dataset):

        metadata = build_dataset_metadata(dataset)

        try:

            # ------------------------------------------------
            # DATASET NÃO TABULAR
            # ------------------------------------------------

            first = dataset["files"][0]

            if first.suffix not in (".csv", ".parquet"):

                metadata["status"] = "NOT_A_TABLE"

                return metadata

            # ------------------------------------------------
            # CHUNKED DATASET
            # ------------------------------------------------

            if dataset["chunked"]:

                total_rows = 0

                first_chunk = None

                for chunk in dataset["chunks"]:

                    df = pd.read_parquet(chunk)

                    total_rows += len(df)

                    if first_chunk is None:

                        first_chunk = df

                metadata["rows"] = int(total_rows)

                metadata["columns"] = int(
                    len(first_chunk.columns)
                )

                metadata["column_names"] = list(
                    first_chunk.columns
                )

                metadata["dtypes"] = {

                    c: str(t)

                    for c, t in first_chunk.dtypes.items()

                }

                metadata["missing_values"] = int(

                    first_chunk.isna().sum().sum()

                )

                metadata["memory_bytes"] = int(

                    first_chunk.memory_usage(
                        deep=True
                    ).sum()

                )

                metadata["status"] = "OK"

                return metadata

            # ------------------------------------------------
            # DATASET ÚNICO
            # ------------------------------------------------

            df = load_single_dataframe(first)

            metadata["rows"] = int(len(df))

            metadata["columns"] = int(len(df.columns))

            metadata["column_names"] = list(df.columns)

            metadata["dtypes"] = {

                c: str(t)

                for c, t in df.dtypes.items()

            }

            metadata["missing_values"] = int(

                df.isna().sum().sum()

            )

            metadata["memory_bytes"] = int(

                df.memory_usage(
                    deep=True
                ).sum()

            )

            metadata["status"] = "OK"

            return metadata

        except Exception as exc:

            metadata["status"] = f"ERROR: {exc}"

            return metadata

    # ========================================================
    # PUBLIC API
    # ========================================================

    def list_datasets(self):

        return sorted(self.datasets.keys())

    # --------------------------------------------------------

    def get_metadata(self, dataset):

        return self.metadata[dataset]

    # --------------------------------------------------------

    def exists(self, dataset):

        return dataset in self.datasets

    # --------------------------------------------------------

    def load_dataframe(self, dataset):

        info = self.datasets[dataset]

        # --------------------------------------------
        # DATASET CHUNKED
        # --------------------------------------------

        if info["chunked"]:

            frames = []

            for chunk in info["chunks"]:

                frames.append(
                    pd.read_parquet(chunk)
                )

            return pd.concat(
                frames,
                ignore_index=True
            )

        # --------------------------------------------
        # DATASET ÚNICO
        # --------------------------------------------

        return load_single_dataframe(
            info["files"][0]
        )

    # --------------------------------------------------------

    def iter_chunks(self, dataset):

        info = self.datasets[dataset]

        if info["chunked"]:

            for chunk in info["chunks"]:

                yield pd.read_parquet(chunk)

        else:

            yield self.load_dataframe(dataset)

    # --------------------------------------------------------

    def load_preview(
        self,
        dataset,
        rows=5
    ):

        df = self.load_dataframe(dataset)

        return json.loads(

            json.dumps(

                df.head(rows).to_dict(
                    orient="records"
                ),

                default=json_serializer

            )

        )

    # --------------------------------------------------------

    def dataset_shape(self, dataset):

        meta = self.get_metadata(dataset)

        return (

            meta["rows"],

            meta["columns"]

        )

    # --------------------------------------------------------

    def dataset_columns(self, dataset):

        return self.get_metadata(
            dataset
        )["column_names"]

    # --------------------------------------------------------

    def summary(self):

        report = []

        report.append("=" * 60)

        report.append("WORKSPACE SUMMARY")

        report.append("=" * 60)

        report.append("")

        for name in self.list_datasets():

            meta = self.get_metadata(name)

            report.append(name)

            report.append(
                f"  status   : {meta['status']}"
            )

            report.append(
                f"  rows     : {meta['rows']}"
            )

            report.append(
                f"  columns  : {meta['columns']}"
            )

            report.append(
                f"  chunked  : {meta['chunked']}"
            )

            report.append(
                f"  chunks   : {meta['chunks']}"
            )

            report.append("")

        return "\n".join(report)

# ============================================================
# WORKSPACE BUILDER
# ============================================================

def build_workspace():

    WORKSPACE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    ws = Workspace()

    catalog = []
    schemas = {}
    previews = {}

    for dataset in ws.list_datasets():

        meta = dict(ws.get_metadata(dataset))

        catalog.append(meta)

        if meta["status"] == "OK":

            schemas[dataset] = {

                "rows": meta["rows"],
                "columns": meta["columns"],
                "column_names": meta["column_names"],
                "dtypes": meta["dtypes"],
                "missing_values": meta["missing_values"],
                "memory_bytes": meta["memory_bytes"],
                "chunked": meta["chunked"],
                "chunks": meta["chunks"]

            }

            previews[dataset] = ws.load_preview(dataset)

    df = pd.DataFrame(catalog)

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    df.to_csv(

        WORKSPACE_DIR / "workspace_catalog.csv",

        index=False

    )

    # --------------------------------------------------------
    # JSON
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

            ensure_ascii=False,

            default=json_serializer

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

            ensure_ascii=False,

            default=json_serializer

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

            default=json_serializer

        )

    # --------------------------------------------------------
    # INDEX
    # --------------------------------------------------------

    index = {}

    for dataset in ws.list_datasets():

        index[dataset] = ws.get_metadata(dataset)

    with open(

        WORKSPACE_DIR / "workspace_index.json",

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            index,

            f,

            indent=4,

            ensure_ascii=False,

            default=json_serializer

        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    lines = []

    lines.append("=" * 60)
    lines.append("GER WORKSPACE")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Root : {RESULTS_ROOT}")
    lines.append("")

    lines.append(f"Datasets : {len(ws.list_datasets())}")
    lines.append("")

    for dataset in ws.list_datasets():

        meta = ws.get_metadata(dataset)

        lines.append(dataset)

        lines.append(f"    Status      : {meta['status']}")
        lines.append(f"    Rows        : {meta['rows']}")
        lines.append(f"    Columns     : {meta['columns']}")
        lines.append(f"    Chunked     : {meta['chunked']}")
        lines.append(f"    Chunks      : {meta['chunks']}")
        lines.append(f"    Category    : {meta['category']}")
        lines.append("")

    with open(

        WORKSPACE_DIR / "workspace_summary.txt",

        "w",

        encoding="utf8"

    ) as f:

        f.write("\n".join(lines))

    return ws


# ============================================================
# DASHBOARD
# ============================================================

def print_dashboard(ws):

    print("=" * 60)
    print("GER WORKSPACE")
    print("=" * 60)
    print()

    for dataset in ws.list_datasets():

        meta = ws.get_metadata(dataset)

        print(f"✓ {dataset}")

        print(f"    Status      : {meta['status']}")
        print(f"    Category    : {meta['category']}")
        print(f"    Chunked     : {meta['chunked']}")
        print(f"    Chunks      : {meta['chunks']}")

        if meta["rows"] is not None:

            print(f"    Rows        : {meta['rows']}")
            print(f"    Columns     : {meta['columns']}")

            if meta["column_names"]:

                print()

                print("    Fields")

                for c in meta["column_names"]:

                    print(f"       - {c}")

        else:

            print("    Non-tabular dataset")

        print()

    print("=" * 60)

    print("Datasets")

    for dataset in ws.list_datasets():

        print(f"   {dataset}")

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
    print("Workspace ready.")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    ws = build_workspace()

    print_dashboard(ws)


if __name__ == "__main__":

    main()
