"""
============================================================
GER
L1.5 Signature Frequency Observatory
============================================================

Scientific Question
-------------------
How are signature frequencies distributed throughout the
Relational Signature Space?

This observatory characterizes the frequency spectrum of
all unique geometric signatures.

Outputs
-------
report/
    signature_frequency_report.txt

tables/
    signature_frequency.csv
    cumulative_frequency.csv

json/
    signature_frequency.json

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


TITLE = "GER\nL1.5 Signature Frequency Observatory"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame) -> dict:
    """
    Analyse signature frequency distribution.
    """

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

    grouped["Relative Frequency"] = (
        grouped["Frequency"] / total
    )

    grouped["Relative Frequency (%)"] = (
        100.0
        * grouped["Relative Frequency"]
    )

    grouped["Cumulative Frequency"] = (
        grouped["Frequency"].cumsum()
    )

    grouped["Cumulative (%)"] = (
        100.0
        * grouped["Cumulative Frequency"]
        / total
    )

    cumulative = grouped[
        [
            "Rank",
            "Frequency",
            "Relative Frequency (%)",
            "Cumulative Frequency",
            "Cumulative (%)",
        ]
    ].copy()

    summary = {

        "total_signatures": total,

        "unique_signatures": int(
            len(grouped)
        ),

        "maximum_frequency": int(
            grouped["Frequency"].max()
        ),

        "minimum_frequency": int(
            grouped["Frequency"].min()
        ),

        "mean_frequency": float(
            grouped["Frequency"].mean()
        ),

        "median_frequency": float(
            grouped["Frequency"].median()
        ),

        "top1_percent": float(
            grouped.iloc[0]["Cumulative (%)"]
        ),

        "top5_percent": float(
            grouped.iloc[
                min(4, len(grouped)-1)
            ]["Cumulative (%)"]
        ),

        "top10_percent": float(
            grouped.iloc[
                min(9, len(grouped)-1)
            ]["Cumulative (%)"]
        ),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "frequency": grouped,

        "cumulative": cumulative,

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

    result["frequency"].to_csv(
        tables_folder / "signature_frequency.csv",
        index=False,
    )

    result["cumulative"].to_csv(
        tables_folder / "cumulative_frequency.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(
        json_folder / "signature_frequency.json",
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
                "observatory": "L1.5",
                "title": "Signature Frequency Observatory",
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
L1.5 Signature Frequency Observatory
============================================================

Total Signatures
{summary['total_signatures']}

Unique Signatures
{summary['unique_signatures']}

Maximum Frequency
{summary['maximum_frequency']}

Minimum Frequency
{summary['minimum_frequency']}

Mean Frequency
{summary['mean_frequency']:.6f}

Median Frequency
{summary['median_frequency']:.6f}

Coverage by Top-1 Signature (%)
{summary['top1_percent']:.6f}

Coverage by Top-5 Signatures (%)
{summary['top5_percent']:.6f}

Coverage by Top-10 Signatures (%)
{summary['top10_percent']:.6f}

Status
{summary['status']}

============================================================
"""

    with open(
        report_folder / "signature_frequency_report.txt",
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

        experiment="S29_E6_2_L1_5",

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
