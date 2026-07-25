"""
GER_CORE/S29/E6_2/E6_3_observatories/L3_Correlation/L3_0_Workspace.py

============================================================
GER
S29 - E6.3

L3.0 - Workspace Manager
============================================================

Responsabilidades

• Descobrir datasets
• Detectar datasets lógicos
• Suportar Parquet único
• Suportar chunk_*.parquet
• Construir catálogo
• Disponibilizar API para todos os L3

Esta é a única camada de acesso aos dados da série L3.

Todos os observatórios devem utilizar exclusivamente
a classe Workspace.

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

    if "statistics" in name:
        return "Statistics"

    if "correlation" in name:
        return "Correlation"

    if "checkpoint" in name:
        return "Checkpoint"

    if "network" in name:
        return "Network"

    if "matrix" in name:
        return "Matrix"

    if "metadata" in name:
        return "Metadata"

    if "workspace" in name:
        return "Workspace"

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
        # chunk_000001.parquet
        # ----------------------------------------------------

        if CHUNK_PATTERN.match(file.name):

            dataset_name = file.parent.name

            if dataset_name not in datasets:

                datasets[dataset_name] = {

                    "name": dataset_name,

                    "logical": True,

                    "files": [],

                    "chunks": []

                }

            datasets[dataset_name]["files"].append(file)

            datasets[dataset_name]["chunks"].append(file)

            continue

        # ----------------------------------------------------
        # parquet único
        # ----------------------------------------------------

        if file.suffix == ".parquet":

            dataset_name = file.stem

            if dataset_name not in datasets:

                datasets[dataset_name] = {

                    "name": dataset_name,

                    "logical": True,

                    "files": [],

                    "chunks": []

                }

            datasets[dataset_name]["files"].append(file)

            continue

        # ----------------------------------------------------
        # auxiliares
        # ----------------------------------------------------

        datasets[file.name] = {

            "name": file.name,

            "logical": False,

            "files": [file],

            "chunks": []

        }

    # --------------------------------------------------------
    # normalização
    # --------------------------------------------------------

    for dataset in datasets.values():

        dataset["chunks"] = sorted(dataset["chunks"])

        dataset["chunked"] = (

            len(dataset["chunks"]) > 0

        )

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

    return {

        "name": dataset["name"],

        "logical": dataset["logical"],

        "chunked": len(dataset["chunks"]) > 0,

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

# ============================================================
# WORKSPACE
# ============================================================

class Workspace:

    """
    Camada única de acesso aos dados da série L3.

    Observatórios NÃO devem acessar arquivos diretamente.
    """

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

            first_file = dataset["files"][0]

            # ------------------------------------------------
            # NÃO TABULAR
            # ------------------------------------------------

            if first_file.suffix not in (".csv", ".parquet"):

                metadata["status"] = "NOT_A_TABLE"

                return metadata

            # ------------------------------------------------
            # DATASET CHUNKED
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

            df = load_single_dataframe(first_file)

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

    def exists(self, dataset):

        return dataset in self.datasets

    # --------------------------------------------------------

    def get_metadata(self, dataset):

        return self.metadata[dataset]

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

    def load_dataframe(self, dataset):

        """
        Carrega o dataset completo.

        Recomendado apenas para datasets pequenos ou médios.

        Para grandes datasets utilizar iter_chunks().
        """

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

        """
        Iterador para processamento streaming.

        Deve ser o método preferido pelos observatórios L3.
        """

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

        """
        Retorna apenas uma pequena amostra.

        Nunca concatena todos os chunks.
        """

        info = self.datasets[dataset]

        if info["chunked"]:

            df = pd.read_parquet(

                info["chunks"][0]

            )

        else:

            df = load_single_dataframe(

                info["files"][0]

            )

        return json.loads(

            json.dumps(

                df.head(rows).to_dict(

                    orient="records"

                ),

                default=json_serializer

            )

        )

    # --------------------------------------------------------

    def summary(self):

        report = []

        report.append("=" * 60)

        report.append("WORKSPACE SUMMARY")

        report.append("=" * 60)

        report.append("")

        for dataset in self.list_datasets():

            meta = self.get_metadata(dataset)

            report.append(dataset)

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

    manifest = {}

    index = {}

    # --------------------------------------------------------
    # BUILD
    # --------------------------------------------------------

    for dataset in ws.list_datasets():

        meta = dict(

            ws.get_metadata(dataset)

        )

        catalog.append(meta)

        index[dataset] = meta

        manifest[dataset] = {

            "category": meta["category"],

            "logical": meta["logical"],

            "status": meta["status"],

            "chunked": meta["chunked"],

            "chunks": meta["chunks"],

            "rows": meta["rows"],

            "columns": meta["columns"]

        }

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

    # ========================================================
    # CATALOG CSV
    # ========================================================

    pd.DataFrame(catalog).to_csv(

        WORKSPACE_DIR / "workspace_catalog.csv",

        index=False

    )

    # ========================================================
    # CATALOG JSON
    # ========================================================

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

    # ========================================================
    # SCHEMA
    # ========================================================

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

    # ========================================================
    # PREVIEW
    # ========================================================

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

    # ========================================================
    # INDEX
    # ========================================================

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

    # ========================================================
    # MANIFEST
    # ========================================================

    with open(

        WORKSPACE_DIR / "workspace_manifest.json",

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            manifest,

            f,

            indent=4,

            ensure_ascii=False,

            default=json_serializer

        )

    # ========================================================
    # SUMMARY
    # ========================================================

    lines = []

    lines.append("=" * 60)
    lines.append("GER WORKSPACE")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Root : {RESULTS_ROOT}")
    lines.append("")

    lines.append(

        f"Datasets : {len(ws.list_datasets())}"

    )

    lines.append("")

    for dataset in ws.list_datasets():

        meta = ws.get_metadata(dataset)

        lines.append(dataset)

        lines.append(

            f"    Status      : {meta['status']}"

        )

        lines.append(

            f"    Category    : {meta['category']}"

        )

        lines.append(

            f"    Logical     : {meta['logical']}"

        )

        lines.append(

            f"    Rows        : {meta['rows']}"

        )

        lines.append(

            f"    Columns     : {meta['columns']}"

        )

        lines.append(

            f"    Chunked     : {meta['chunked']}"

        )

        lines.append(

            f"    Chunks      : {meta['chunks']}"

        )

        lines.append("")

    with open(

        WORKSPACE_DIR / "workspace_summary.txt",

        "w",

        encoding="utf8"

    ) as f:

        f.write(

            "\n".join(lines)

        )

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
        print(f"    Logical     : {meta['logical']}")
        print(f"    Chunked     : {meta['chunked']}")
        print(f"    Chunks      : {meta['chunks']}")

        if meta["rows"] is not None:

            print(f"    Rows        : {meta['rows']}")
            print(f"    Columns     : {meta['columns']}")

            if meta["column_names"]:

                print()
                print("    Fields")

                for column in meta["column_names"]:

                    print(f"       - {column}")

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

    generated = [

        "workspace_catalog.csv",
        "workspace_catalog.json",
        "workspace_schema.json",
        "workspace_preview.json",
        "workspace_index.json",
        "workspace_manifest.json",
        "workspace_summary.txt",

    ]

    for file in generated:

        print(f"   {file}")

    print()

    print("=" * 60)
    print("Workspace ready.")
    print("=" * 60)

# ============================================================
# PUBLIC API
# ============================================================

def get_workspace():
    """
    Builds and returns the complete workspace dictionary.
    """
    return build_workspace()


def load_dataset(name: str):
    """
    Loads a dataset from the workspace.

    Parameters
    ----------
    name : str
        Dataset logical name.

    Returns
    -------
    pandas.DataFrame
    """

    workspace = build_workspace()

    datasets = workspace["datasets"]

    if name not in datasets:
        raise KeyError(f"Dataset '{name}' not found.")

    dataset = datasets[name]

    if dataset["status"] != "OK":
        raise RuntimeError(
            f"Dataset '{name}' is not available."
        )

    return dataset["data"]

# ============================================================
# MAIN
# ============================================================

def main():

    ws = build_workspace()

    print_dashboard(ws)


if __name__ == "__main__":

    main()
