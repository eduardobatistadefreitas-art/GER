"""
============================================================
GER
S29-E6.2-L1.9
Frequency Inequality Observatory
============================================================

Scientific Question
-------------------
How concentrated is the occupation of the Signature Space?

This observatory measures the inequality of the frequency
distribution using complementary concentration indices.

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

from GER_CORE.S29.E6_2.storage import ExperimentStorage

from GER_CORE.S29.E6_2.io import load_signatures

from GER_CORE.S29.E6_2.statistics.spectrum import (
    compute_frequency_table,
)

from GER_CORE.S29.E6_2.statistics.descriptive import (
    compute_entropy,
    compute_gini,
)


# ============================================================
# HHI
# ============================================================

def compute_hhi(values):

    values = np.asarray(values, dtype=float)

    p = values / values.sum()

    return float(np.sum(p ** 2))


# ============================================================
# SIMPSON
# ============================================================

def compute_simpson(values):

    values = np.asarray(values, dtype=float)

    p = values / values.sum()

    return float(np.sum(p ** 2))


# ============================================================
# EFFECTIVE NUMBER
# ============================================================

def effective_number(values):

    hhi = compute_hhi(values)

    if hhi == 0:
        return 0.0

    return float(1.0 / hhi)


# ============================================================
# CONCENTRATION CLASS
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

def analyse():

    df = load_signatures()

    frequency = compute_frequency_table(df)

    values = frequency["Frequency"].values

    entropy = compute_entropy(values)

    gini = compute_gini(values)

    hhi = compute_hhi(values)

    simpson = compute_simpson(values)

    effective = effective_number(values)

    metrics = pd.DataFrame(
        [

            {
                "Metric": "Entropy",
                "Value": entropy,
            },

            {
                "Metric": "Gini",
                "Value": gini,
            },

            {
                "Metric": "HHI",
                "Value": hhi,
            },

            {
                "Metric": "Simpson",
                "Value": simpson,
            },

            {
                "Metric": "Effective Signatures",
                "Value": effective,
            },

        ]

    )

    certificate = {

        "entropy": entropy,

        "gini": gini,

        "hhi": hhi,

        "simpson": simpson,

        "effective_signatures": effective,

        "concentration": classify_concentration(gini),

        "status": "PASS",

    }

    return {

        "metrics": metrics,

        "certificate": certificate,

    }


# ============================================================
# SAVE
# ============================================================

def save(storage, result):

    result["metrics"].to_csv(

        storage.path(
            "tables",
            "inequality_metrics.csv",
        ),

        index=False,

    )

    with open(

        storage.path(
            "json",
            "inequality.json",
        ),

        "w",

    ) as f:

        json.dump(

            result["certificate"],

            f,

            indent=4,

        )

    with open(

        storage.path(
            "certificate",
            "certificate.json",
        ),

        "w",

    ) as f:

        json.dump(

            result["certificate"],

            f,

            indent=4,

        )

    with open(

        storage.path(
            "report",
            "inequality_report.txt",
        ),

        "w",

    ) as f:

        f.write(
            "==================================================\n"
        )
        f.write(
            "GER\n"
        )
        f.write(
            "Frequency Inequality Observatory\n"
        )
        f.write(
            "==================================================\n\n"
        )

        for _, row in result["metrics"].iterrows():

            f.write(

                f"{row['Metric']:<30}"

                f"{row['Value']:.6f}\n"

            )

        f.write("\n")

        f.write(
            f"Concentration : {result['certificate']['concentration']}\n"
        )

        f.write(
            f"Status        : {result['certificate']['status']}\n"
        )


# ============================================================
# RUN
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

    result = analyse()

    save(storage, result)

    print("=" * 60)
    print("GER")
    print("Frequency Inequality Observatory")
    print("=" * 60)

    print()

    print(result["metrics"])

    print()

    print("Concentration :", result["certificate"]["concentration"])

    print("Status        :", result["certificate"]["status"])


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
