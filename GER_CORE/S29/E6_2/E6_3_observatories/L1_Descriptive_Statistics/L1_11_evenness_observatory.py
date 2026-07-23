"""
============================================================
GER
L1.11 Evenness Observatory
============================================================

Scientific Question
-------------------
How evenly are occurrences distributed across the
Relational Signature Space?

Outputs
-------
report/
    evenness_report.txt

tables/
    evenness_metrics.csv

json/
    evenness.json

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
)

TITLE = "GER\nL1.11 Evenness Observatory"


# ============================================================
# PIELOU EVENNESS
# ============================================================

def pielou_evenness(entropy, richness):

    if richness <= 1:
        return 0.0

    return float(entropy / np.log(richness))


# ============================================================
# SIMPSON DIVERSITY
# ============================================================

def simpson_diversity(values):

    values = np.asarray(values, dtype=float)

    total = values.sum()

    if total == 0:
        return 0.0

    p = values / total

    return float(1.0 - np.sum(p ** 2))


# ============================================================
# HILL NUMBERS
# ============================================================

def hill_q0(values):

    return int(len(values))


def hill_q1(entropy):

    return float(np.exp(entropy))


def hill_q2(values):

    values = np.asarray(values, dtype=float)

    total = values.sum()

    if total == 0:
        return 0.0

    p = values / total

    d = np.sum(p ** 2)

    if d == 0:
        return 0.0

    return float(1.0 / d)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_evenness(pielou):

    if pielou >= 0.90:
        return "HIGH"

    if pielou >= 0.70:
        return "MODERATE"

    return "LOW"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame):

    frequency = compute_frequency_table(df)

    values = frequency["Frequency"].values

    entropy = compute_entropy(values, base="e")

    richness = len(values)

    pielou = pielou_evenness(
        entropy,
        richness,
    )

    simpson = simpson_diversity(values)

    q0 = hill_q0(values)

    q1 = hill_q1(entropy)

    q2 = hill_q2(values)

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Pielou Evenness",

                "Simpson Diversity",

                "Hill q0",

                "Hill q1",

                "Hill q2",

            ],

            "Value": [

                pielou,

                simpson,

                q0,

                q1,

                q2,

            ],

        }

    )

    summary = {

        "pielou": float(pielou),

        "simpson_diversity": float(simpson),

        "hill_q0": int(q0),

        "hill_q1": float(q1),

        "hill_q2": float(q2),

        "uniformity": classify_evenness(
            pielou
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

        tables_folder / "evenness_metrics.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "evenness.json",

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

        "observatory": "L1.11",

        "title": "Evenness Observatory",

        "pielou": summary["pielou"],

        "simpson_diversity": summary["simpson_diversity"],

        "hill_q0": summary["hill_q0"],

        "hill_q1": summary["hill_q1"],

        "hill_q2": summary["hill_q2"],

        "uniformity": summary["uniformity"],

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
L1.11 Evenness Observatory
============================================================

Pielou Evenness
{summary['pielou']:.6f}

Simpson Diversity
{summary['simpson_diversity']:.6f}

Hill q0 (Richness)
{summary['hill_q0']}

Hill q1 (Shannon)
{summary['hill_q1']:.6f}

Hill q2 (Simpson)
{summary['hill_q2']:.6f}

Uniformity
{summary['uniformity']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "evenness_report.txt",

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

        experiment="S29_E6_2_L1_11",

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
