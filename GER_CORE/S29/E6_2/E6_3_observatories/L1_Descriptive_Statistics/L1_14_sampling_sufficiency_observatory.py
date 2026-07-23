"""
============================================================
GER
L1.14 Sampling Sufficiency Observatory
============================================================

Scientific Question
-------------------
Is the current sample size sufficient to provide a stable
representation of the observed Relational Signature Space?

Outputs
-------
report/
    sampling_sufficiency_report.txt

tables/
    sampling_sufficiency_metrics.csv

json/
    sampling_sufficiency.json

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
    "L1.14 Sampling Sufficiency Observatory"
)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_sampling(
    index: float,
) -> str:

    if index >= 0.15:
        return "HIGH"

    if index >= 0.08:
        return "MODERATE"

    return "LOW"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    frequency = compute_frequency_table(df)

    values = (
        frequency["Frequency"]
        .values
        .astype(float)
    )

    total_occurrences = int(
        values.sum()
    )

    unique_signatures = len(values)

    observation_ratio = (

        total_occurrences

        / unique_signatures

    )

    mean_samples = float(

        np.mean(values)

    )

    median_samples = float(

        np.median(values)

    )

    minimum_samples = int(

        np.min(values)

    )

    maximum_samples = int(

        np.max(values)

    )

    std_samples = float(

        np.std(

            values,

            ddof=0,

        )

    )

    coefficient_variation = (

        std_samples

        / mean_samples

    )


    # --------------------------------------------------------
    # Minimum Coverage
    # --------------------------------------------------------

    minimum_coverage = (

        minimum_samples

        /

        mean_samples

    )

    # --------------------------------------------------------
    # Sampling Sufficiency Index
    # --------------------------------------------------------

    sampling_index = (

        minimum_coverage

        /

        (

            1.0

            + coefficient_variation

        )

    )

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Total Observations",

                "Unique Signatures",

                "Observation Ratio",

                "Mean Samples",

                "Median Samples",

                "Minimum Samples",

                "Maximum Samples",

                "Std Samples",

                "Coefficient of Variation",

                "Minimum Coverage",

                "Sampling Sufficiency Index",

            ],

            "Value": [

                total_occurrences,

                unique_signatures,

                observation_ratio,

                mean_samples,

                median_samples,

                minimum_samples,

                maximum_samples,

                std_samples,

                coefficient_variation,

                minimum_coverage,

                sampling_index,

            ],

        }

    )

    summary = {

        "total_observations":

            total_occurrences,

        "unique_signatures":

            unique_signatures,

        "observation_ratio":

            observation_ratio,

        "mean_samples":

            mean_samples,

        "median_samples":

            median_samples,

        "minimum_samples":

            minimum_samples,

        "maximum_samples":

            maximum_samples,

        "std_samples":

            std_samples,

        "coefficient_variation":

            coefficient_variation,

        "minimum_coverage":

            minimum_coverage,

        "sampling_sufficiency_index":

            sampling_index,

        "sampling":

            classify_sampling(

                sampling_index,

            ),

        "status":

            "PASS",

    }

    return {

        "summary":

            summary,

        "metrics":

            metrics,

    }    
    
# ============================================================
# SAVE
# ============================================================

def save(
    storage: ExperimentStorage,
    result: dict,
):

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

        tables_folder / "sampling_sufficiency_metrics.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "sampling_sufficiency.json",

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

        "observatory": "L1.14",

        "title": "Sampling Sufficiency Observatory",

        "sampling_sufficiency_index":
            summary["sampling_sufficiency_index"],

        "observation_ratio":
            summary["observation_ratio"],

        "mean_samples":
            summary["mean_samples"],

        "median_samples":
            summary["median_samples"],

        "minimum_samples":
            summary["minimum_samples"],

        "maximum_samples":
            summary["maximum_samples"],
        
        "minimum_coverage":
            summary["minimum_coverage"],

        "coefficient_variation":
            summary["coefficient_variation"],

        "sampling":
            summary["sampling"],

        "status":
            summary["status"],

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
L1.14 Sampling Sufficiency Observatory
============================================================

Total Observations
{summary['total_observations']}

Unique Signatures
{summary['unique_signatures']}

Observation Ratio
{summary['observation_ratio']:.6f}

Mean Samples
{summary['mean_samples']:.6f}

Median Samples
{summary['median_samples']:.6f}

Minimum Samples
{summary['minimum_samples']}

Maximum Samples
{summary['maximum_samples']}

Coefficient of Variation
{summary['coefficient_variation']:.6f}

Minimum Coverage
{summary['minimum_coverage']:.6f}

Sampling Sufficiency Index
{summary['sampling_sufficiency_index']:.6f}

Sampling
{summary['sampling']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "sampling_sufficiency_report.txt",

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

        experiment="S29_E6_2_L1_14",

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

    save(

        storage,

        result,

    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
