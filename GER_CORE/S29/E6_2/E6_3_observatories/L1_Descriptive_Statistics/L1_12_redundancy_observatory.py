"""
============================================================
GER
L1.12 Redundancy Observatory
============================================================

Scientific Question
-------------------
How much of the observed dataset corresponds to repeated
Relational Signatures?

Outputs
-------
report/
    redundancy_report.txt

tables/
    redundancy_metrics.csv

json/
    redundancy.json

certificate/
    certificate.json
============================================================
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...io import load_signatures

from ...statistics.spectrum import (
    compute_frequency_table,
)

TITLE = "GER\nL1.12 Redundancy Observatory"


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_redundancy(ratio):

    if ratio < 0.50:
        return "LOW"

    if ratio < 0.90:
        return "MODERATE"

    return "HIGH"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame):

    frequency = compute_frequency_table(df)

    values = frequency["Frequency"].values.astype(float)

    total_occurrences = int(values.sum())

    unique_signatures = int(len(values))

    redundancy_ratio = (
        (total_occurrences - unique_signatures)
        / total_occurrences
    )

    novelty_ratio = (
        unique_signatures
        / total_occurrences
    )

    mean_repetition = float(values.mean())

    median_repetition = float(np.median(values))

    maximum_repetition = int(values.max())

    minimum_repetition = int(values.min())

    std_repetition = float(values.std(ddof=0))

    repeat_excess = float(mean_repetition - 1.0)

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Total Occurrences",

                "Unique Signatures",

                "Redundancy Ratio",

                "Novelty Ratio",

                "Mean Repetition",

                "Median Repetition",

                "Maximum Repetition",

                "Minimum Repetition",

                "Std Repetition",

                "Repeat Excess",

            ],

            "Value": [

                total_occurrences,

                unique_signatures,

                redundancy_ratio,

                novelty_ratio,

                mean_repetition,

                median_repetition,

                maximum_repetition,

                minimum_repetition,

                std_repetition,

                repeat_excess,

            ],

        }

    )

    summary = {

        "total_occurrences": total_occurrences,

        "unique_signatures": unique_signatures,

        "redundancy_ratio": float(redundancy_ratio),

        "novelty_ratio": float(novelty_ratio),

        "mean_repetition": float(mean_repetition),

        "median_repetition": float(median_repetition),

        "maximum_repetition": maximum_repetition,

        "minimum_repetition": minimum_repetition,

        "std_repetition": float(std_repetition),

        "repeat_excess": float(repeat_excess),

        "redundancy": classify_redundancy(
            redundancy_ratio
        ),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "metrics": metrics,

    }

# ============================================================
# SAVE
# ============================================================

def save(storage: ExperimentStorage, result: dict):

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
    # TABLE
    # --------------------------------------------------------

    result["metrics"].to_csv(

        tables_folder / "redundancy_metrics.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "redundancy.json",

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

    certificate = {

        "observatory": "L1.12",

        "title": "Redundancy Observatory",

        "redundancy_ratio": summary["redundancy_ratio"],

        "novelty_ratio": summary["novelty_ratio"],

        "mean_repetition": summary["mean_repetition"],

        "median_repetition": summary["median_repetition"],

        "maximum_repetition": summary["maximum_repetition"],

        "minimum_repetition": summary["minimum_repetition"],

        "std_repetition": summary["std_repetition"],

        "repeat_excess": summary["repeat_excess"],

        "redundancy": summary["redundancy"],

        "status": summary["status"],

    }

    with open(

        certificate_folder / "certificate.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4,

        )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report = f"""
============================================================
GER
L1.12 Redundancy Observatory
============================================================

Total Occurrences
{summary['total_occurrences']}

Unique Signatures
{summary['unique_signatures']}

Redundancy Ratio
{summary['redundancy_ratio']:.6f}

Novelty Ratio
{summary['novelty_ratio']:.6f}

Mean Repetition
{summary['mean_repetition']:.6f}

Median Repetition
{summary['median_repetition']:.6f}

Maximum Repetition
{summary['maximum_repetition']}

Minimum Repetition
{summary['minimum_repetition']}

Std Repetition
{summary['std_repetition']:.6f}

Repeat Excess
{summary['repeat_excess']:.6f}

Redundancy
{summary['redundancy']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "redundancy_report.txt",

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

        experiment="S29_E6_2_L1_12",

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
