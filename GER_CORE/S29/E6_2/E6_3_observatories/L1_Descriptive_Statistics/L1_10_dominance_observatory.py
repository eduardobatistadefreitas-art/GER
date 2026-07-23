"""
============================================================
GER
L1.10 Dominance Observatory
============================================================

Scientific Question
-------------------
Is the Signature Space dominated by a small number of
high-frequency signatures?

Outputs
-------
report/
    dominance_report.txt

tables/
    dominance_metrics.csv

json/
    dominance.json

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

TITLE = "GER\nL1.10 Dominance Observatory"


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_dominance(dominance):

    if dominance < 0.10:
        return "LOW"

    if dominance < 0.25:
        return "MODERATE"

    return "HIGH"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame):

    frequency = compute_frequency_table(df)

    values = frequency["Frequency"].values

    total = values.sum()

    top1 = int(values[0])

    top5 = int(values[:5].sum())

    top10 = int(values[:10].sum())

    mean = float(np.mean(values))

    median = float(np.median(values))

    dominance = top1 / total

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Top-1 Frequency",

                "Top-5 Frequency",

                "Top-10 Frequency",

                "Top-1 Coverage",

                "Top-5 Coverage",

                "Top-10 Coverage",

                "Top-1 / Mean",

                "Top-1 / Median",

            ],

            "Value": [

                top1,

                top5,

                top10,

                dominance,

                top5 / total,

                top10 / total,

                top1 / mean,

                top1 / median,

            ],

        }

    )

    summary = {

        "top1_frequency": top1,

        "top5_frequency": top5,

        "top10_frequency": top10,

        "top1_coverage": float(dominance),

        "top5_coverage": float(top5 / total),

        "top10_coverage": float(top10 / total),

        "top1_mean_ratio": float(top1 / mean),

        "top1_median_ratio": float(top1 / median),

        "dominance": classify_dominance(dominance),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "metrics": metrics,

    }

"""
============================================================
GER
L1.10 Dominance Observatory
============================================================

Scientific Question
-------------------
Is the Signature Space dominated by a small number of
high-frequency signatures?

Outputs
-------
report/
    dominance_report.txt

tables/
    dominance_metrics.csv

json/
    dominance.json

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

TITLE = "GER\nL1.10 Dominance Observatory"


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_dominance(dominance):

    if dominance < 0.10:
        return "LOW"

    if dominance < 0.25:
        return "MODERATE"

    return "HIGH"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame):

    frequency = compute_frequency_table(df)

    values = frequency["Frequency"].values

    total = values.sum()

    top1 = int(values[0])

    top5 = int(values[:5].sum())

    top10 = int(values[:10].sum())

    mean = float(np.mean(values))

    median = float(np.median(values))

    dominance = top1 / total

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Top-1 Frequency",

                "Top-5 Frequency",

                "Top-10 Frequency",

                "Top-1 Coverage",

                "Top-5 Coverage",

                "Top-10 Coverage",

                "Top-1 / Mean",

                "Top-1 / Median",

            ],

            "Value": [

                top1,

                top5,

                top10,

                dominance,

                top5 / total,

                top10 / total,

                top1 / mean,

                top1 / median,

            ],

        }

    )

    summary = {

        "top1_frequency": top1,

        "top5_frequency": top5,

        "top10_frequency": top10,

        "top1_coverage": float(dominance),

        "top5_coverage": float(top5 / total),

        "top10_coverage": float(top10 / total),

        "top1_mean_ratio": float(top1 / mean),

        "top1_median_ratio": float(top1 / median),

        "dominance": classify_dominance(dominance),

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

        tables_folder / "dominance_metrics.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "dominance.json",

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

        "observatory": "L1.10",

        "title": "Dominance Observatory",

        "dominance": summary["dominance"],

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
L1.10 Dominance Observatory
============================================================

Top-1 Frequency
{summary['top1_frequency']}

Top-5 Frequency
{summary['top5_frequency']}

Top-10 Frequency
{summary['top10_frequency']}

Top-1 Coverage
{summary['top1_coverage']:.6f}

Top-5 Coverage
{summary['top5_coverage']:.6f}

Top-10 Coverage
{summary['top10_coverage']:.6f}

Top-1 / Mean
{summary['top1_mean_ratio']:.6f}

Top-1 / Median
{summary['top1_median_ratio']:.6f}

Dominance
{summary['dominance']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "dominance_report.txt",

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

        experiment="S29_E6_2_L1_10",

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
