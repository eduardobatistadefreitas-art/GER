"""
============================================================
GER
S29 - E6.3 Observatory

L1.1 - Missing Values Observatory
============================================================

Scientific Question
-------------------
Are the generated signatures numerically complete and
internally consistent?

This observatory performs a complete integrity audit of the
signature dataset before any statistical analysis.

Checks
------
- Dataset dimensions
- Column names
- Data types
- Missing values
- Infinite values
- Duplicate rows

Outputs
-------
report/
    missing_values_report.txt

tables/
    missing_values_summary.csv

json/
    missing_values_summary.json

certificate/
    certificate.json

Author
------
Eduardo Batista de Freitas

Framework
---------
GER

Version
-------
1.0
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...io import load_signatures


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame) -> dict:

    summary = []

    numeric = df.select_dtypes(include=[np.number])

    for column in df.columns:

        values = df[column]

        info = {

            "column": column,
            "dtype": str(values.dtype),
            "rows": len(values),
            "missing": int(values.isna().sum()),
            "infinite": 0,
            "duplicate_values": int(values.duplicated().sum()),

        }

        if column in numeric.columns:

            info["infinite"] = int(
                np.isinf(values.to_numpy()).sum()
            )

        summary.append(info)

    duplicated_rows = int(df.duplicated().sum())

    status = "PASS"

    for item in summary:

        if item["missing"] > 0:
            status = "FAIL"

        if item["infinite"] > 0:
            status = "FAIL"

    return {

        "status": status,

        "rows": len(df),

        "columns": len(df.columns),

        "column_names": list(df.columns),

        "duplicated_rows": duplicated_rows,

        "duplicated_ratio": duplicated_rows / len(df),

        "summary": summary,

    }


# ============================================================
# SAVE
# ============================================================

def save(storage: ExperimentStorage, result: dict):

    storage.create_folder("report")
    storage.create_folder("tables")
    storage.create_folder("json")
    storage.create_folder("certificate")

    report_folder = storage.folder("report")
    tables_folder = storage.folder("tables")
    json_folder = storage.folder("json")
    certificate_folder = storage.folder("certificate")

    # ---------------- CSV ----------------

    table = pd.DataFrame(result["summary"])

    table.to_csv(
        tables_folder / "missing_values_summary.csv",
        index=False,
    )

    # ---------------- JSON ----------------

    with open(
        json_folder / "missing_values_summary.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
        )

    # ---------------- CERTIFICATE ----------------

    with open(
        certificate_folder / "certificate.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            {
                "observatory": "L1.1",
                "status": result["status"],
                "rows": result["rows"],
                "columns": result["columns"],
            },
            f,
            indent=4,
        )

    # ---------------- TXT ----------------

    report = []

    report.append("=" * 60)
    report.append("GER")
    report.append("L1.1 Missing Values Observatory")
    report.append("=" * 60)
    report.append("")

    report.append(f"Status : {result['status']}")
    report.append(f"Rows   : {result['rows']}")
    report.append(f"Columns: {result['columns']}")
    report.append("")

    report.append(
        f"Duplicated Rows : {result['duplicated_rows']}"
    )

    report.append(
        f"Duplicated Ratio: {result['duplicated_ratio']:.6f}"
    )

    report.append("")
    report.append("-" * 60)

    for item in result["summary"]:

        report.append(item["column"])
        report.append(f"    dtype      : {item['dtype']}")
        report.append(f"    missing    : {item['missing']}")
        report.append(f"    infinite   : {item['infinite']}")
        report.append(f"    duplicates : {item['duplicate_values']}")
        report.append("")

    with open(
        report_folder / "missing_values_report.txt",
        "w",
        encoding="utf-8",
    ) as f:

        f.write("\n".join(report))


# ============================================================
# MAIN
# ============================================================

def run():

    storage = ExperimentStorage(

        experiment="S29_E6_2_L1_1",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

    df = load_signatures()

    result = analyse(df)

    save(storage, result)

    print("=" * 60)
    print("GER")
    print("L1.1 Missing Values Observatory")
    print("=" * 60)
    print(f"Rows              : {result['rows']}")
    print(f"Columns           : {result['columns']}")
    print(f"Duplicated Rows   : {result['duplicated_rows']}")
    print(f"Status            : {result['status']}")
    print("=" * 60)
    from pathlib import Path

    print()
    print(storage.database)
    print(storage.database.exists())
    print(list(storage.database.iterdir()))

    return result


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
