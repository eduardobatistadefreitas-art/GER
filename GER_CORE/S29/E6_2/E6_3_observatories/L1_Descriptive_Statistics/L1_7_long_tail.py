"""
============================================================
GER
L1.7 Long Tail Observatory
============================================================

Scientific Question
-------------------
Does the Relational Signature Space exhibit a long-tail
distribution?

This observatory quantifies the population of rare,
uncommon and dominant signatures.

Outputs
-------
report/
    long_tail_report.txt

tables/
    frequency_classes.csv
    rarity_thresholds.csv

json/
    long_tail.json

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


TITLE = "GER\nL1.7 Long Tail Observatory"


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

    total_occurrences = int(grouped["Frequency"].sum())
    total_signatures = len(grouped)

    percentiles = grouped["Frequency"].quantile(
        [0.10, 0.25, 0.50, 0.75, 0.90]
    )

    rarity_table = pd.DataFrame({

        "Criterion": [
            "Frequency <= 10",
            "Frequency <= 100",
            "Frequency <= 1000",
            "Bottom 10%",
            "Bottom 25%",
            "Top 10%",
        ],

        "Number of Signatures": [

            int((grouped["Frequency"] <= 10).sum()),

            int((grouped["Frequency"] <= 100).sum()),

            int((grouped["Frequency"] <= 1000).sum()),

            int(
                (
                    grouped["Frequency"]
                    <= percentiles.loc[0.10]
                ).sum()
            ),

            int(
                (
                    grouped["Frequency"]
                    <= percentiles.loc[0.25]
                ).sum()
            ),

            int(
                (
                    grouped["Frequency"]
                    >= percentiles.loc[0.90]
                ).sum()
            ),

        ]

    })

    grouped["Class"] = pd.cut(

        grouped["Frequency"],

        bins=[
            -1,
            percentiles.loc[0.25],
            percentiles.loc[0.75],
            np.inf,
        ],

        labels=[
            "Rare",
            "Common",
            "Frequent",
        ],

    )

    class_summary = (

        grouped
        .groupby("Class")
        .agg(

            Signatures=("Frequency", "count"),

            TotalOccurrences=("Frequency", "sum"),

        )
        .reset_index()

    )

    class_summary["Occurrence (%)"] = (

        100
        * class_summary["TotalOccurrences"]
        / total_occurrences

    )

    class_summary["Signature (%)"] = (

        100
        * class_summary["Signatures"]
        / total_signatures

    )

    summary = {

        "total_signatures": total_signatures,

        "total_occurrences": total_occurrences,

        "rare_signatures": int(

            class_summary.loc[
                class_summary["Class"] == "Rare",
                "Signatures",
            ].iloc[0]

        ),

        "frequent_signatures": int(

            class_summary.loc[
                class_summary["Class"] == "Frequent",
                "Signatures",
            ].iloc[0]

        ),

        "rare_occurrence_percent": float(

            class_summary.loc[
                class_summary["Class"] == "Rare",
                "Occurrence (%)",
            ].iloc[0]

        ),

        "frequent_occurrence_percent": float(

            class_summary.loc[
                class_summary["Class"] == "Frequent",
                "Occurrence (%)",
            ].iloc[0]

        ),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "classes": class_summary,

        "rarity": rarity_table,

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

    result["classes"].to_csv(
        tables_folder / "frequency_classes.csv",
        index=False,
    )

    result["rarity"].to_csv(
        tables_folder / "rarity_thresholds.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(
        json_folder / "long_tail.json",
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
                "observatory": "L1.7",
                "title": "Long Tail Observatory",
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
L1.7 Long Tail Observatory
============================================================

Total Occurrences
{summary['total_occurrences']}

Unique Signatures
{summary['total_signatures']}

Rare Signatures
{summary['rare_signatures']}

Frequent Signatures
{summary['frequent_signatures']}

Occurrences Represented by Rare Signatures (%)
{summary['rare_occurrence_percent']:.6f}

Occurrences Represented by Frequent Signatures (%)
{summary['frequent_occurrence_percent']:.6f}

Status
{summary['status']}

============================================================
"""

    with open(
        report_folder / "long_tail_report.txt",
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

        experiment="S29_E6_2_L1_7",

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
