"""
============================================================
GER
L2.10
Marginal Certificate
============================================================

Scientific Objective
--------------------

Consolidate the complete marginal distribution analysis.

This observatory does not perform new statistical analyses.

Instead, it validates the completeness of the Marginal
Distributions module and produces a unified certificate.

Certified observatories

    L2.1
    L2.2
    L2.3
    L2.4
    L2.5
    L2.6
    L2.7
    L2.7.1
    L2.8
    L2.9

Outputs
-------

report/
    marginal_certificate_report.txt

tables/
    marginal_summary.csv

json/
    marginal_certificate.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage


TITLE = (
    "GER\n"
    "L2.10 Marginal Certificate"
)

# ============================================================
# OBSERVATORIES
# ============================================================

OBSERVATORIES = [

    (
        "L2.1",
        "Location"
    ),

    (
        "L2.2",
        "Dispersion"
    ),

    (
        "L2.3",
        "Shape"
    ),

    (
        "L2.4",
        "Quantiles"
    ),

    (
        "L2.5",
        "Distribution Summary"
    ),

    (
        "L2.6",
        "Marginal Dashboard"
    ),

    (
        "L2.7",
        "Distribution Comparison"
    ),

    (
        "L2.7.1",
        "Normalized Comparison"
    ),

    (
        "L2.8",
        "Tail Behaviour"
    ),

    (
        "L2.9",
        "Marginal Stability"
    ),

]

# ============================================================
# HELPERS
# ============================================================


def find_certificate_files(
    root: Path,
):

    certificates = {}

    for observatory, _ in OBSERVATORIES:

        matches = list(

            root.rglob(

                f"{observatory}/**/certificate.json"

            )

        )

        if not matches:

            matches = list(

                root.rglob(

                    f"*{observatory}*/**/certificate.json"

                )

            )

        certificates[
            observatory
        ] = matches

    return certificates


def analyse(
    root: Path,
):

    certificates = find_certificate_files(
        root
    )

    summary = []

    completed = 0

    for observatory, description in OBSERVATORIES:

        files = certificates[
            observatory
        ]

        status = (
            "PASS"
            if files
            else "MISSING"
        )

        if files:

            completed += 1

        summary.append({

            "observatory":
                observatory,

            "description":
                description,

            "status":
                status,

            "files_found":
                len(files),

        })

    results = {

        "summary":
            pd.DataFrame(
                summary
            ),

        "completed":
            completed,

        "missing":
            len(
                OBSERVATORIES
            ) - completed,

        "status":
            (
                "PASS"
                if completed == len(
                    OBSERVATORIES
                )
                else "INCOMPLETE"
            ),

    }

    return results

# ============================================================
# SAVE
# ============================================================

def save(
    storage: ExperimentStorage,
    results: dict,
):

    storage.create_folder("report")
    storage.create_folder("tables")
    storage.create_folder("json")
    storage.create_folder("certificate")

    report_dir = storage.folder("report")
    tables_dir = storage.folder("tables")
    json_dir = storage.folder("json")
    certificate_dir = storage.folder("certificate")

    summary = results["summary"]

    summary.to_csv(
        tables_dir / "marginal_summary.csv",
        index=False,
    )

    json_output = {

        "module":
            "Marginal Distributions",

        "version":
            "1.0",

        "total_observatories":
            len(OBSERVATORIES),

        "completed":
            results["completed"],

        "missing":
            results["missing"],

        "status":
            results["status"],

        "observatories":
            summary.to_dict(
                orient="records"
            ),

    }

    with open(

        json_dir /
        "marginal_certificate.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            json_output,

            f,

            indent=4,

        )

    certificate = {

        "observatory":
            "L2.10",

        "title":
            "Marginal Certificate",

        "module":
            "Marginal Distributions",

        "status":
            results["status"],

        "completed":
            results["completed"],

        "total":
            len(
                OBSERVATORIES
            ),

    }

    with open(

        certificate_dir /
        "certificate.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4,

        )

    report = []

    report.append("=" * 60)
    report.append("GER")
    report.append("L2.10")
    report.append("Marginal Certificate")
    report.append("=" * 60)
    report.append("")

    report.append(
        "Certified Observatories"
    )

    report.append(
        "-" * 40
    )

    for _, row in summary.iterrows():

        symbol = (
            "✓"
            if row["status"] == "PASS"
            else "✗"
        )

        report.append(

            f"{symbol} "

            f"{row['observatory']}"

            f"  "

            f"{row['description']}"

        )

    report.append("")
    report.append("-" * 40)
    report.append("")

    report.append(
        "Marginal characterization includes"
    )

    report.append("")

    report.append("• Central tendency")
    report.append("• Dispersion")
    report.append("• Shape")
    report.append("• Quantiles")
    report.append("• Distribution summary")
    report.append("• Distribution comparison")
    report.append("• Normalized comparison")
    report.append("• Tail behaviour")
    report.append("• Sampling stability")

    report.append("")
    report.append("-" * 40)
    report.append("")

    report.append(
        f"Completed : {results['completed']}/{len(OBSERVATORIES)}"
    )

    report.append(
        f"Missing   : {results['missing']}"
    )

    report.append("")

    report.append(
        f"STATUS : {results['status']}"
    )

    with open(

        report_dir /
        "marginal_certificate_report.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(
            "\n".join(report)
        )

    print(
        "\n".join(report)
    )


# ============================================================
# RUN
# ============================================================

def run():

    print("=" * 60)
    print(TITLE)
    print("=" * 60)
    print()

    storage = ExperimentStorage(

        experiment="S29_E6_2_L2_10",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

    results_root = Path(
        storage.base_output.parent
    )

    results = analyse(
        results_root
    )

    save(
        storage,
        results,
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
