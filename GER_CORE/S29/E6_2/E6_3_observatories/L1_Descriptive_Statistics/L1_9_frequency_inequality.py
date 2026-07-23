"""
============================================================
GER
L1.9 Frequency Inequality Observatory
============================================================

Scientific Question
-------------------
How concentrated is the occupation of the Relational
Signature Space?

This observatory measures inequality and concentration
of the frequency spectrum.

Outputs
-------
report/
    inequality_report.txt

tables/
    inequality_metrics.csv

json/
    inequality.json

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

from ...statistics.descriptive import (
    compute_entropy,
    compute_gini,
)

TITLE = "GER\nL1.9 Frequency Inequality Observatory"


# ============================================================
# HHI
# ============================================================

def compute_hhi(values):

    values = np.asarray(values, dtype=float)

    total = values.sum()

    if total == 0:
        return 0.0

    p = values / total

    return float(np.sum(p ** 2))


# ============================================================
# SIMPSON
# ============================================================

def compute_simpson(values):

    return compute_hhi(values)


# ============================================================
# EFFECTIVE NUMBER
# ============================================================

def effective_number(values):

    hhi = compute_hhi(values)

    if hhi == 0:
        return 0.0

    return float(1.0 / hhi)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_concentration(gini):

    if gini < 0.30:
        return "LOW"

    if gini < 0.60:
        return "MODERATE"

    return "HIGH"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame):

    frequency = compute_frequency_table(df)

    values = frequency["Frequency"].values

    entropy = compute_entropy(values)

    gini = compute_gini(values)

    hhi = compute_hhi(values)

    simpson = compute_simpson(values)

    effective = effective_number(values)

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Entropy",

                "Gini",

                "HHI",

                "Simpson",

                "Effective Signatures",

                "Unique Signatures",

                "Total Occurrences",

            ],

            "Value": [

                entropy,

                gini,

                hhi,

                simpson,

                effective,

                len(values),

                int(values.sum()),

            ],

        }

    )

    summary = {

        "entropy": float(entropy),

        "gini": float(gini),

        "hhi": float(hhi),

        "simpson": float(simpson),

        "effective_signatures": float(effective),

        "unique_signatures": int(len(values)),

        "total_occurrences": int(values.sum()),

        "concentration": classify_concentration(gini),

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

        tables_folder / "inequality_metrics.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "inequality.json",

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

        "observatory": "L1.9",

        "title": "Frequency Inequality Observatory",

        "concentration": summary["concentration"],

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
L1.9 Frequency Inequality Observatory
============================================================

Entropy
{summary['entropy']:.6f}

Gini
{summary['gini']:.6f}

Herfindahl-Hirschman Index
{summary['hhi']:.6f}

Simpson Concentration Index
{summary['simpson']:.6f}

Effective Number of Signatures
{summary['effective_signatures']:.6f}

Unique Signatures
{summary['unique_signatures']}

Total Occurrences
{summary['total_occurrences']}

Concentration
{summary['concentration']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "inequality_report.txt",

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

        experiment="S29_E6_2_L1_9",

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
