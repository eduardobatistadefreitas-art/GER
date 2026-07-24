"""
============================================================
GER
L2.10
Marginal Certificate
============================================================

Scientific Objective
--------------------

Consolidate the complete Marginal Distributions module.

This observatory performs no statistical analysis.

Instead, it validates that every observatory belonging to
Layer L2 completed successfully and emitted a valid
certificate.

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
# CONFIGURATION
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS"
)

OBSERVATORIES = [

    (
        "L2.1",
        "S29_E6_2_L2_1",
        "Location"
    ),

    (
        "L2.2",
        "S29_E6_2_L2_2",
        "Dispersion"
    ),

    (
        "L2.3",
        "S29_E6_2_L2_3",
        "Shape"
    ),

    (
        "L2.4",
        "S29_E6_2_L2_4",
        "Quantiles"
    ),

    (
        "L2.5",
        "S29_E6_2_L2_5",
        "Distribution Summary"
    ),

    (
        "L2.6",
        "S29_E6_2_L2_6",
        "Marginal Dashboard"
    ),

    (
        "L2.7",
        "S29_E6_2_L2_7",
        "Distribution Comparison"
    ),

    (
        "L2.7.1",
        "S29_E6_2_L2_7_1",
        "Normalized Comparison"
    ),

    (
        "L2.8",
        "S29_E6_2_L2_8",
        "Tail Behaviour"
    ),

    (
        "L2.9",
        "S29_E6_2_L2_9",
        "Marginal Stability"
    ),

]

# ============================================================
# HELPERS
# ============================================================


def certificate_path(
    experiment: str,
):

    return (

        RESULTS_ROOT

        / experiment

        / "certificate"

        / "certificate.json"

    )


def load_certificate(
    experiment: str,
):

    path = certificate_path(
        experiment
    )

    if not path.exists():

        return {

            "exists": False,

            "status": "MISSING",

            "certificate": None,

            "path": str(path),

        }

    try:

        with open(

            path,

            "r",

            encoding="utf-8",

        ) as f:

            data = json.load(f)

    except Exception:

        return {

            "exists": True,

            "status": "INVALID",

            "certificate": None,

            "path": str(path),

        }

    return {

        "exists": True,

        "status": data.get(
            "status",
            "UNKNOWN",
        ),

        "certificate": data,

        "path": str(path),

    }


# ============================================================
# ANALYSIS
# ============================================================


def analyse():

    rows = []

    total = len(
        OBSERVATORIES
    )

    found = 0

    passed = 0

    failed = 0

    missing = 0

    for (

        observatory,

        experiment,

        description,

    ) in OBSERVATORIES:

        cert = load_certificate(
            experiment
        )

        if cert["exists"]:

            found += 1

        else:

            missing += 1

        status = cert["status"]

        if status == "PASS":

            passed += 1

        elif status != "MISSING":

            failed += 1

        rows.append({

            "observatory":
                observatory,

            "experiment":
                experiment,

            "description":
                description,

            "exists":
                cert["exists"],

            "status":
                status,

            "certificate":
                cert["path"],

        })

    summary = pd.DataFrame(
        rows
    )

    return {

        "summary":
            summary,

        "total":
            total,

        "found":
            found,

        "passed":
            passed,

        "failed":
            failed,

        "missing":
            missing,

        "status":

            "PASS"

            if (

                passed == total

                and

                missing == 0

                and

                failed == 0

            )

            else

            "INCOMPLETE",

    }

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

        "expected_observatories":
            results["total"],

        "found":
            results["found"],

        "passed":
            results["passed"],

        "failed":
            results["failed"],

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

        "expected":
            results["total"],

        "passed":
            results["passed"],

        "failed":
            results["failed"],

        "missing":
            results["missing"],

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

    report.append("Certified Observatories")
    report.append("-" * 60)

    for _, row in summary.iterrows():

        symbol = (

            "✓"

            if row["status"] == "PASS"

            else "✗"

        )

        report.append(

            f"{symbol} "

            f"{row['observatory']:<7}"

            f"{row['description']:<30}"

            f"{row['status']}"

        )

    report.append("")
    report.append("-" * 60)
    report.append("")

    report.append("Module Summary")
    report.append("")

    report.append(
        f"Expected : {results['total']}"
    )

    report.append(
        f"Found    : {results['found']}"
    )

    report.append(
        f"Passed   : {results['passed']}"
    )

    report.append(
        f"Failed   : {results['failed']}"
    )

    report.append(
        f"Missing  : {results['missing']}"
    )

    report.append("")
    report.append("-" * 60)
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
    report.append("-" * 60)
    report.append("")

    report.append(
        f"FINAL STATUS : {results['status']}"
    )

    if results["status"] == "PASS":

        report.append("")

        report.append(
            "Marginal Distributions module successfully certified."
        )

    else:

        report.append("")

        report.append(
            "Marginal Distributions module is incomplete."
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

    results = analyse()

    save(

        storage,

        results,

    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
