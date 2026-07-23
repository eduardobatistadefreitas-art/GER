"""
============================================================
GER
L1.15 Coverage Saturation Observatory
============================================================

Scientific Question
-------------------
Is the Relational Signature Space approaching saturation,
or are new signatures still being discovered as sampling
continues?

Outputs
-------
report/
    coverage_saturation_report.txt

tables/
    coverage_saturation_metrics.csv
    coverage_progression.csv

json/
    coverage_saturation.json

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


TITLE = (
    "GER\n"
    "L1.15 Coverage Saturation Observatory"
)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_saturation(
    ratio: float,
    discovery_rate: float,
) -> str:

    if (
        ratio >= 0.99
        and discovery_rate <= 0.001
    ):
        return "HIGH"

    if (
        ratio >= 0.95
        and discovery_rate <= 0.01
    ):
        return "MODERATE"

    return "LOW"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    total_observations = len(df)

    checkpoints = [

        0.01,
        0.02,
        0.05,
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70,
        0.80,
        0.90,
        1.00,

    ]

    progression = []

    previous_unique = 0

    for fraction in checkpoints:

        n = max(
            1,
            int(
                total_observations
                * fraction
            ),
        )

        subset = df.iloc[:n]

        frequency = compute_frequency_table(
            subset
        )

        unique = len(frequency)

        discovery = (

            unique

            - previous_unique

        )

        progression.append(

            {

                "Fraction":

                    fraction,

                "Observations":

                    n,

                "Unique Signatures":

                    unique,

                "New Signatures":

                    discovery,

            }

        )

        previous_unique = unique

    progression = pd.DataFrame(
        progression
    )

    unique_final = int(

        progression[
            "Unique Signatures"
        ].iloc[-1]

    )

    unique_90 = int(

        progression[
            "Unique Signatures"
        ].iloc[-2]

    )

    saturation_ratio = (

        unique_90

        /

        unique_final

    )

    final_new = int(

        progression[
            "New Signatures"
        ].iloc[-1]

    )

    final_observations = (

        progression[
            "Observations"
        ].iloc[-1]

        -

        progression[
            "Observations"
        ].iloc[-2]

    )

    discovery_rate = (

        final_new

        /

        final_observations

    )

    plateau_score = (

        1.0

        -

        discovery_rate

    )

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Total Observations",

                "Unique Signatures",

                "Saturation Ratio",

                "Final Discovery Rate",

                "Plateau Score",

            ],

            "Value": [

                total_observations,

                unique_final,

                saturation_ratio,

                discovery_rate,

                plateau_score,

            ],

        }

    )

    summary = {

        "total_observations":

            total_observations,

        "unique_signatures":

            unique_final,

        "saturation_ratio":

            saturation_ratio,

        "final_discovery_rate":

            discovery_rate,

        "plateau_score":

            plateau_score,

        "coverage":

            classify_saturation(

                saturation_ratio,

                discovery_rate,

            ),

        "status":

            "PASS",

    }

    return {

        "summary":

            summary,

        "metrics":

            metrics,

        "progression":

            progression,

    }

# ============================================================
# SAVE
# ============================================================

def save(
    storage: ExperimentStorage,
    results,
):

    summary = results["summary"]

    metrics = results["metrics"]

    progression = results["progression"]

    metrics.to_csv(

        storage.path(

            "tables",
            "coverage_saturation_metrics.csv",

        ),

        index=False,

    )

    progression.to_csv(

        storage.path(

            "tables",
            "coverage_progression.csv",

        ),

        index=False,

    )

    with open(

        storage.path(

            "json",
            "coverage_saturation.json",

        ),

        "w",

    ) as fp:

        json.dump(

            summary,

            fp,

            indent=4,

        )

    with open(

        storage.path(

            "certificate",
            "certificate.json",

        ),

        "w",

    ) as fp:

        json.dump(

            summary,

            fp,

            indent=4,

        )

    report = f"""
============================================================
GER
L1.15 Coverage Saturation Observatory
============================================================

Total Observations
{summary['total_observations']}

Unique Signatures
{summary['unique_signatures']}

Saturation Ratio
{summary['saturation_ratio']:.6f}

Final Discovery Rate
{summary['final_discovery_rate']:.6f}

Plateau Score
{summary['plateau_score']:.6f}

Coverage Saturation
{summary['coverage']}

Status
{summary['status']}

============================================================
"""

    with open(

        storage.path(

            "report",
            "coverage_saturation_report.txt",

        ),

        "w",

    ) as fp:

        fp.write(report)

    print(report)


# ============================================================
# RUN
# ============================================================

def run():

    print("=" * 60)

    print(TITLE)

    print("=" * 60)
    print()

    storage = ExperimentStorage(

        experiment="S29_E6_2_L1_15",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

    df = load_signatures()

    results = analyse(df)

    save(

        storage,

        results,

    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
