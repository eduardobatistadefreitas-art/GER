# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import json

import numpy as np
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

BASE_RESULTS = Path(
    "/content/drive/MyDrive/GER_RESULTS"
)

L30_FOLDER = (
    BASE_RESULTS /
    "S29_E6.3" /
    "L3_0_Universe_Builder"
)

RESULTS_DIR = (
    BASE_RESULTS /
    "S29_E6.3" /
    "L3_0_1_Universe_Dataset_Audit"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ============================================================
# DATASET DISCOVERY
# ============================================================

CANDIDATE_FILES = [

    L30_FOLDER / "universes.parquet",

    L30_FOLDER / "universes.csv",

    L30_FOLDER / "universes.feather",

]

# ============================================================
# FIND DATASET
# ============================================================

def locate_dataset():

    """
    Localiza automaticamente o dataset
    consolidado de universos.
    """

    for file in CANDIDATE_FILES:

        if file.exists():

            return file

    raise FileNotFoundError(

        "Universe dataset not found.\n\n"

        "Expected one of:\n"

        +

        "\n".join(

            str(f)

            for f in CANDIDATE_FILES

        )

    )

# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    """
    Carrega o dataset persistido.
    """

    dataset = locate_dataset()

    suffix = dataset.suffix.lower()

    if suffix == ".parquet":

        df = pd.read_parquet(dataset)

    elif suffix == ".csv":

        df = pd.read_csv(dataset)

    elif suffix == ".feather":

        df = pd.read_feather(dataset)

    else:

        raise ValueError(

            f"Unsupported format: {suffix}"

        )

    return dataset, df

# ============================================================
# BASIC SUMMARY
# ============================================================

def dataset_summary(df):

    """
    Estatísticas básicas do dataset.
    """

    summary = {

        "rows":

            int(len(df)),

        "columns":

            int(len(df.columns)),

        "memory_mb":

            float(

                df.memory_usage(

                    deep=True

                ).sum()

                /

                1024**2

            ),

        "column_names":

            list(df.columns),

    }

    return summary

# ============================================================
# PREVIEW
# ============================================================

def preview_dataset(df):

    """
    Pequena visualização do dataset.
    """

    return df.head(10).copy()

# ============================================================
# REPORT OBJECT
# ============================================================

def build_report():

    dataset_path, df = load_dataset()

    report = {

        "dataset_path":

            str(dataset_path),

        "summary":

            dataset_summary(df),

        "preview":

            preview_dataset(df),

        "dataframe":

            df,

    }

    return report

# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

def analyze_duplicates(df):

    """
    Analisa registros duplicados.
    """

    duplicated = int(df.duplicated().sum())

    return {

        "duplicated_rows": duplicated,

        "has_duplicates": duplicated > 0,

    }


# ============================================================
# MISSING VALUES
# ============================================================

def analyze_missing(df):

    """
    Analisa valores ausentes.
    """

    missing = (

        df.isna()

        .sum()

        .sort_values(

            ascending=False

        )

    )

    summary = pd.DataFrame({

        "column": missing.index,

        "missing": missing.values,

        "percentage":

            (

                missing.values

                /

                len(df)

                * 100

            )

    })

    return summary


# ============================================================
# DATA TYPES
# ============================================================

def analyze_dtypes(df):

    """
    Tipos das colunas.
    """

    return pd.DataFrame({

        "column": df.columns,

        "dtype":

            [

                str(x)

                for x

                in df.dtypes

            ]

    })


# ============================================================
# UNIQUE VALUES
# ============================================================

def analyze_uniques(df):

    """
    Cardinalidade das colunas.
    """

    return pd.DataFrame({

        "column": df.columns,

        "unique_values":

            [

                df[c].nunique(

                    dropna=False

                )

                for c

                in df.columns

            ]

    })


# ============================================================
# NUMERIC SUMMARY
# ============================================================

def analyze_numeric(df):

    """
    Estatísticas das colunas numéricas.
    """

    numeric = df.select_dtypes(

        include=np.number

    )

    if len(numeric.columns) == 0:

        return pd.DataFrame()

    summary = (

        numeric

        .describe()

        .T

    )

    summary.reset_index(

        inplace=True

    )

    summary.rename(

        columns={

            "index":

            "column"

        },

        inplace=True,

    )

    return summary


# ============================================================
# CONSTANT COLUMNS
# ============================================================

def analyze_constant_columns(df):

    """
    Detecta colunas constantes.
    """

    constants = []

    for column in df.columns:

        if df[column].nunique(

            dropna=False

        ) <= 1:

            constants.append(

                column

            )

    return constants


# ============================================================
# DATASET HEALTH
# ============================================================

def dataset_health(report):

    """
    Consolida indicadores
    de integridade.
    """

    df = report["dataframe"]

    duplicates = analyze_duplicates(

        df

    )

    missing = analyze_missing(

        df

    )

    dtypes = analyze_dtypes(

        df

    )

    uniques = analyze_uniques(

        df

    )

    numeric = analyze_numeric(

        df

    )

    constants = analyze_constant_columns(

        df

    )

    integrity = (

        duplicates["duplicated_rows"] == 0

        and

        missing["missing"].sum() == 0

    )

    certificate = {

        "rows":

            len(df),

        "columns":

            len(df.columns),

        "duplicated_rows":

            duplicates["duplicated_rows"],

        "missing_values":

            int(

                missing["missing"].sum()

            ),

        "constant_columns":

            len(constants),

        "integrity":

            integrity,

        "status":

            "PASS"

            if integrity

            else

            "FAIL",

    }

    report["duplicates"] = duplicates

    report["missing"] = missing

    report["dtypes"] = dtypes

    report["uniques"] = uniques

    report["numeric"] = numeric

    report["constant_columns"] = constants

    report["certificate"] = certificate

    return report

# ============================================================
# PERSISTENCE AUDIT
# ============================================================

import hashlib
from datetime import datetime

def compute_sha256(path, chunk_size=1024 * 1024):

    """
    Calcula SHA256 do arquivo.
    """

    sha = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(chunk_size)

            if not chunk:

                break

            sha.update(chunk)

    return sha.hexdigest()


def persistence_audit(report):

    """
    Auditoria do arquivo persistido.
    """

    dataset_path = Path(report["dataset_path"])

    stat = dataset_path.stat()

    persistence = {

        "file":

            str(dataset_path),

        "size_mb":

            stat.st_size / 1024**2,

        "modified":

            datetime.fromtimestamp(

                stat.st_mtime

            ).isoformat(),

        "sha256":

            compute_sha256(

                dataset_path

            ),

        "rows_loaded":

            int(

                len(

                    report["dataframe"]

                )

            ),

    }

    report["persistence"] = persistence

    return report


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(report):

    report["missing"].to_csv(

        RESULTS_DIR /

        "dataset_integrity.csv",

        index=False,

    )

    summary = pd.DataFrame({

        "metric": [

            "rows",

            "columns",

            "memory_mb",

        ],

        "value": [

            report["summary"]["rows"],

            report["summary"]["columns"],

            report["summary"]["memory_mb"],

        ]

    })

    summary.to_csv(

        RESULTS_DIR /

        "dataset_summary.csv",

        index=False,

    )

    report["preview"].to_csv(

        RESULTS_DIR /

        "dataset_preview.csv",

        index=False,

    )

    with open(

        RESULTS_DIR /

        "dataset_audit.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "summary":

                    report["summary"],

                "certificate":

                    report["certificate"],

                "persistence":

                    report["persistence"],

            },

            f,

            indent=4,

        )

    with open(

        RESULTS_DIR /

        "dataset_audit_summary.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            "GER\n"

            "S29 - E6.3\n"

            "L3.0.1\n"

            "Universe Dataset Audit\n\n"

        )

        f.write(

            "=" * 60 + "\n"

        )

        f.write(

            f"Dataset : {report['dataset_path']}\n"

        )

        f.write(

            f"Rows    : {report['summary']['rows']}\n"

        )

        f.write(

            f"Columns : {report['summary']['columns']}\n"

        )

        f.write(

            f"Memory  : {report['summary']['memory_mb']:.2f} MB\n\n"

        )

        f.write(

            "Integrity\n"

        )

        f.write(

            f"Status            : {report['certificate']['status']}\n"

        )

        f.write(

            f"Duplicated Rows   : {report['certificate']['duplicated_rows']}\n"

        )

        f.write(

            f"Missing Values    : {report['certificate']['missing_values']}\n"

        )

        f.write(

            f"Constant Columns  : {report['certificate']['constant_columns']}\n\n"

        )

        f.write(

            "Persistence\n"

        )

        f.write(

            f"File Size : {report['persistence']['size_mb']:.2f} MB\n"

        )

        f.write(

            f"Modified  : {report['persistence']['modified']}\n"

        )

        f.write(

            f"SHA256    : {report['persistence']['sha256']}\n"

        )


# ============================================================
# DASHBOARD
# ============================================================

def print_dashboard(report):

    s = report["summary"]
    c = report["certificate"]
    p = report["persistence"]

    print()

    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.0.1 - Universe Dataset Audit")
    print("=" * 60)
    print()

    print(f"Dataset : {report['dataset_path']}")
    print()

    print(f"Rows               : {s['rows']}")
    print(f"Columns            : {s['columns']}")
    print(f"Memory             : {s['memory_mb']:.2f} MB")
    print()

    print("Integrity")
    print("-" * 30)
    print(f"Status             : {c['status']}")
    print(f"Duplicated Rows    : {c['duplicated_rows']}")
    print(f"Missing Values     : {c['missing_values']}")
    print(f"Constant Columns   : {c['constant_columns']}")
    print()

    print("Persistence")
    print("-" * 30)
    print(f"File Size          : {p['size_mb']:.2f} MB")
    print(f"Rows Loaded        : {p['rows_loaded']}")
    print(f"Modified           : {p['modified']}")
    print()

    print("=" * 60)
    print("Generated Files")
    print("=" * 60)

    print("dataset_summary.csv")
    print("dataset_integrity.csv")
    print("dataset_preview.csv")
    print("dataset_audit.json")
    print("dataset_audit_summary.txt")

    print()

    print("Results")

    print(RESULTS_DIR)

    print()

    print("=" * 60)
    print("Experiment completed.")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print()

    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.0.1 - Universe Dataset Audit")
    print("=" * 60)
    print()

    print("Loading dataset...")

    report = build_report()

    print("Auditing dataset...")

    report = dataset_health(report)

    report = persistence_audit(report)

    print("Saving results...")

    save_results(report)

    print_dashboard(report)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
