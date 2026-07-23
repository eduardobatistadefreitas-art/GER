"""
============================================================
GER
L1.6 Cumulative Coverage Observatory
============================================================

Scientific Question
-------------------
How many unique signatures are required to explain most
of the observed universe?

This observatory measures cumulative coverage and determines
the minimum number of signatures necessary to reach several
coverage thresholds.

Outputs
-------
report/
    cumulative_coverage_report.txt

tables/
    cumulative_coverage.csv
    coverage_thresholds.csv

json/
    cumulative_coverage.json

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
============================================================
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...io import load_signatures


TITLE = "GER\nL1.6 Cumulative Coverage Observatory"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame) -> dict:

    grouped = (
        df.groupby(list(df.columns))
        .size()
        .reset_index(name="Frequency")
        .sort_values(
            "Frequency",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    total = int(grouped["Frequency"].sum())

    grouped["Rank"] = np.arange(
        1,
        len(grouped) + 1,
    )

    grouped["Cumulative Frequency"] = (
        grouped["Frequency"].cumsum()
    )

    grouped["Coverage (%)"] = (
        100.0
        * grouped["Cumulative Frequency"]
        / total
    )

    thresholds = []

    for target in [50, 80, 90, 95, 99]:

        idx = np.argmax(
            grouped["Coverage (%)"] >= target
        )

        thresholds.append({

            "Target (%)": target,

            "Required Signatures": int(
                grouped.iloc[idx]["Rank"]
            ),

            "Fraction of Signature Space (%)":
            100.0
            * grouped.iloc[idx]["Rank"]
            / len(grouped),

            "Achieved Coverage (%)":
            float(
                grouped.iloc[idx]["Coverage (%)"]
            ),

        })

    thresholds = pd.DataFrame(thresholds)

    summary = {

        "total_signatures": total,

        "unique_signatures": int(
            len(grouped)
        ),

        "coverage_50": int(
            thresholds.iloc[0]["Required Signatures"]
        ),

        "coverage_80": int(
            thresholds.iloc[1]["Required Signatures"]
        ),

        "coverage_90": int(
            thresholds.iloc[2]["Required Signatures"]
        ),

        "coverage_95": int(
            thresholds.iloc[3]["Required Signatures"]
        ),

        "coverage_99": int(
            thresholds.iloc[4]["Required Signatures"]
        ),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "coverage": grouped,

        "thresholds": thresholds,

    }

# ============================================================
# SAVE
# ============================================================

def save(storage: ExperimentStorage, result: dict) -> None:

    summary = result["summary"]

    storage.create_folder("report")
    storage.create_folder("tables")
    storage.create_folder("json")
    storage.create_folder("certificate")

    report_folder = storage.folder("report")
    tables_folder = storage.folder("tables")
    json_folder = storage.folder("json")
    certificate_folder = storage.folder("certificate")

    # --------------------------------------------------------
    # TABLES
    # --------------------------------------------------------

    result["coverage"].to_csv(
        tables_folder / "cumulative_coverage.csv",
        index=False,
    )

    result["thresholds"].to_csv(
        tables_folder / "coverage_thresholds.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(
        json_folder / "cumulative_coverage.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            summary,
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # CERTIFICATE
    # --------------------------------------------------------

    with open(
        certificate_folder / "certificate.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            {
                "observatory": "L1.6",
                "title": "Cumulative Coverage Observatory",
                "status": summary["status"],
            },
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report = f"""
============================================================
GER
L1.6 Cumulative Coverage Observatory
============================================================

Total Signatures
{summary['total_signatures']}

Unique Signatures
{summary['unique_signatures']}

Signatures Required for 50% Coverage
{summary['coverage_50']}

Signatures Required for 80% Coverage
{summary['coverage_80']}

Signatures Required for 90% Coverage
{summary['coverage_90']}

Signatures Required for 95% Coverage
{summary['coverage_95']}

Signatures Required for 99% Coverage
{summary['coverage_99']}

Status
{summary['status']}

============================================================
"""

    with open(
        report_folder / "cumulative_coverage_report.txt",
        "w",
        encoding="utf-8",
    ) as f:

        f.write(report)

    print(report)


# ============================================================
# MAIN
# ============================================================

def run():

    storage = ExperimentStorage(

        experiment="S29_E6_2_L1_6",

        folders=[
            "report",
            "tables",
            "json",
            "certificate",
        ],

    )

    print("=" * 60)
    print(TITLE)
    print("=" * 60)

    df = load_signatures()

    result = analyse(df)

    save(storage, result)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
