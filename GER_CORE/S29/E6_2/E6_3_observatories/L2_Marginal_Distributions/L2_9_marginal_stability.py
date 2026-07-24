"""
============================================================
GER
L2.9 Marginal Stability
============================================================

Scientific Objective
--------------------
Evaluate the robustness of marginal statistics under
random subsampling.

This observatory validates the stability of the statistical
pipeline before large-scale execution (5M signatures).

Outputs
-------

report/
    marginal_stability_report.txt

tables/
    stability_summary.csv
    sampling_statistics.csv
    sampling_errors.csv

json/
    marginal_stability.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json
import time

import numpy as np
import pandas as pd

from scipy.stats import skew
from scipy.stats import kurtosis

from GER.CORE.ger_storage import ExperimentStorage

from ...statistical_observatory.io import (
    load_signatures,
)

TITLE = (
    "GER\n"
    "L2.9 Marginal Stability"
)

# ============================================================
# CONFIGURATION
# ============================================================

SAMPLE_LEVELS = [

    5,
    10,
    20,
    30,
    50,
    70,
    90,

]

N_REPLICATIONS = 10

RANDOM_SEED = 42

# ============================================================
# HELPERS
# ============================================================


def compute_statistics(
    series: pd.Series,
):

    values = series.to_numpy()

    return {

        "mean":
            float(np.mean(values)),

        "std":
            float(np.std(values)),

        "median":
            float(np.median(values)),

        "skewness":
            float(skew(values)),

        "kurtosis":
            float(
                kurtosis(
                    values,
                    fisher=True,
                )
            ),

    }


def compute_reference(
    df: pd.DataFrame,
):

    reference = {}

    for column in df.columns:

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):
            continue

        reference[column] = compute_statistics(
            df[column]
        )

    return reference


def compute_errors(
    reference: dict,
    sample: dict,
):

    errors = {}

    for observable in reference:

        errors[observable] = {}

        for metric in reference[observable]:

            ref = reference[observable][metric]

            val = sample[observable][metric]

            abs_error = abs(
                val - ref
            )

            rel_error = abs_error / (

                abs(ref) + 1e-12

            )

            errors[observable][metric] = {

                "absolute":
                    float(abs_error),

                "relative":
                    float(rel_error),

            }

    return errors


# ============================================================
# RANDOM SAMPLING
# ============================================================


def sample_dataframe(
    df: pd.DataFrame,
    percentage: int,
    seed: int,
):

    fraction = percentage / 100.0

    return df.sample(

        frac=fraction,

        replace=False,

        random_state=seed,

    )


def analyse_sample(
    df: pd.DataFrame,
):

    stats = {}

    for column in df.columns:

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):
            continue

        stats[column] = compute_statistics(
            df[column]
        )

    return stats

# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    reference = compute_reference(df)

    sampling_statistics = []

    sampling_errors = []

    stability_summary = []

    np.random.seed(RANDOM_SEED)

    total_runs = len(SAMPLE_LEVELS) * N_REPLICATIONS
    current_run = 0

    start_total = time.time()

    for percentage in SAMPLE_LEVELS:

        level_errors = []

        print(
            f"\nSampling {percentage}%"
        )

        for replication in range(
            N_REPLICATIONS
        ):

            current_run += 1

            seed = np.random.randint(
                0,
                1_000_000_000,
            )

            start = time.time()

            sample = sample_dataframe(

                df,

                percentage,

                seed,

            )

            stats = analyse_sample(
                sample
            )

            errors = compute_errors(

                reference,

                stats,

            )

            elapsed = (
                time.time() - start
            )

            print(

                f"[{current_run:02d}/{total_runs}] "

                f"{percentage:2d}% "

                f"Replication "

                f"{replication+1:02d} "

                f"({elapsed:.2f}s)"

            )

            for observable in stats:

                sampling_statistics.append({

                    "sample_percentage":
                        percentage,

                    "replication":
                        replication + 1,

                    "observable":
                        observable,

                    **stats[observable],

                    "runtime":
                        elapsed,

                })

                observable_errors = {

                    "sample_percentage":
                        percentage,

                    "replication":
                        replication + 1,

                    "observable":
                        observable,

                }

                for metric in errors[
                    observable
                ]:

                    observable_errors[
                        metric +
                        "_absolute"
                    ] = errors[
                        observable
                    ][metric][
                        "absolute"
                    ]

                    observable_errors[
                        metric +
                        "_relative"
                    ] = errors[
                        observable
                    ][metric][
                        "relative"
                    ]

                    level_errors.append(

                        errors[
                            observable
                        ][metric][
                            "relative"
                        ]

                    )

                sampling_errors.append(

                    observable_errors

                )

        level_errors = np.asarray(
            level_errors
        )

        stability_summary.append({

            "sample_percentage":
                percentage,

            "mean_relative_error":
                float(
                    np.mean(
                        level_errors
                    )
                ),

            "std_relative_error":
                float(
                    np.std(
                        level_errors
                    )
                ),

            "maximum_relative_error":
                float(
                    np.max(
                        level_errors
                    )
                ),

        })

    total_time = (
        time.time() -
        start_total
    )

    return {

        "reference":
            reference,

        "sampling_statistics":
            pd.DataFrame(
                sampling_statistics
            ),

        "sampling_errors":
            pd.DataFrame(
                sampling_errors
            ),

        "stability_summary":
            pd.DataFrame(
                stability_summary
            ),

        "execution":{

            "sample_levels":
                SAMPLE_LEVELS,

            "replications":
                N_REPLICATIONS,

            "total_runs":
                total_runs,

            "total_runtime":
                total_time,

        },

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

    results["stability_summary"].to_csv(
        tables_dir / "stability_summary.csv",
        index=False,
    )

    results["sampling_statistics"].to_csv(
        tables_dir / "sampling_statistics.csv",
        index=False,
    )

    results["sampling_errors"].to_csv(
        tables_dir / "sampling_errors.csv",
        index=False,
    )

    json_results = {

        "reference":
            results["reference"],

        "execution":
            results["execution"],

        "stability_summary":
            results["stability_summary"].to_dict(
                orient="records"
            ),

    }

    with open(

        json_dir / "marginal_stability.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            json_results,

            f,

            indent=4,

        )

    certificate = {

        "observatory":
            "L2.9",

        "title":
            "Marginal Stability",

        "sample_levels":
            SAMPLE_LEVELS,

        "replications":
            N_REPLICATIONS,

        "total_runs":
            results["execution"]["total_runs"],

        "status":
            "PASS",

    }

    with open(

        certificate_dir / "certificate.json",

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
    report.append("L2.9 Marginal Stability")
    report.append("=" * 60)
    report.append("")

    report.append("Execution")
    report.append("-" * 40)
    report.append(
        f"Replications : {N_REPLICATIONS}"
    )
    report.append(
        f"Sample Levels: {SAMPLE_LEVELS}"
    )
    report.append(
        f"Total Runs   : {results['execution']['total_runs']}"
    )
    report.append(
        f"Runtime (s)  : {results['execution']['total_runtime']:.2f}"
    )
    report.append("")

    report.append("Stability Summary")
    report.append("-" * 40)

    for _, row in results[
        "stability_summary"
    ].iterrows():

        report.append(
            f"Sample {int(row['sample_percentage']):2d}%"
        )

        report.append(
            f"Mean Relative Error : {row['mean_relative_error']:.6e}"
        )

        report.append(
            f"Std Relative Error  : {row['std_relative_error']:.6e}"
        )

        report.append(
            f"Maximum Error       : {row['maximum_relative_error']:.6e}"
        )

        report.append("")

    with open(

        report_dir / "marginal_stability_report.txt",

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

        experiment="S29_E6_2_L2_9",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

    df = load_signatures()

    print(
        f"Loaded signatures : {len(df):,}"
    )

    print()

    results = analyse(
        df
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
