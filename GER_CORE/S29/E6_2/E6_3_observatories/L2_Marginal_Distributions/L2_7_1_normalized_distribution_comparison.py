"""
============================================================
GER
L2.7.1 Normalized Distribution Comparison
============================================================

Scientific Objective
--------------------
Evaluate whether pairwise distribution comparisons are
dominated by differences in physical scale.

The complete L2.7 analysis is repeated after applying
two independent normalization strategies:

    • Min-Max Normalization
    • Z-Score Normalization

The resulting metrics are compared with the original
(non-normalized) analysis.

Outputs
-------

report/
    normalized_distribution_report.txt
    comparison_original_vs_normalized.txt

tables/

    minmax/
        wasserstein_matrix.csv
        ks_distance_matrix.csv
        ks_pvalue_matrix.csv
        js_matrix.csv
        overlap_matrix.csv

    zscore/
        wasserstein_matrix.csv
        ks_distance_matrix.csv
        ks_pvalue_matrix.csv
        js_matrix.csv
        overlap_matrix.csv

json/
    normalized_distribution.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json

import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...statistical_observatory.io import (
    load_signatures,
)

from ...statistics.distribution_comparison import (

    pairwise_wasserstein,

    pairwise_ks,

    pairwise_js,

    pairwise_overlap,

    summary_statistics,

)

TITLE = (

    "GER\n"

    "L2.7.1 Normalized Distribution Comparison"

)

# ============================================================
# NORMALIZATION
# ============================================================


def normalize_minmax(
    df: pd.DataFrame,
):

    normalized = df.copy()

    for column in normalized.columns:

        if not pd.api.types.is_numeric_dtype(
            normalized[column]
        ):
            continue

        minimum = normalized[column].min()

        maximum = normalized[column].max()

        if maximum == minimum:

            normalized[column] = 0.0

        else:

            normalized[column] = (

                normalized[column] - minimum

            ) / (

                maximum - minimum

            )

    return normalized


def normalize_zscore(
    df: pd.DataFrame,
):

    normalized = df.copy()

    for column in normalized.columns:

        if not pd.api.types.is_numeric_dtype(
            normalized[column]
        ):
            continue

        mean = normalized[column].mean()

        std = normalized[column].std()

        if std == 0:

            normalized[column] = 0.0

        else:

            normalized[column] = (

                normalized[column] - mean

            ) / std

    return normalized


# ============================================================
# ANALYSIS
# ============================================================


def analyse_single(
    df: pd.DataFrame,
):

    wasserstein = pairwise_wasserstein(
        df,
    )

    ks_distance, ks_pvalue = pairwise_ks(
        df,
    )

    js = pairwise_js(
        df,
    )

    overlap = pairwise_overlap(
        df,
    )

    return {

        "wasserstein": wasserstein,

        "ks_distance": ks_distance,

        "ks_pvalue": ks_pvalue,

        "js": js,

        "overlap": overlap,

        "summary": {

            "wasserstein":
                summary_statistics(
                    wasserstein,
                ),

            "ks":
                summary_statistics(
                    ks_distance,
                ),

            "js":
                summary_statistics(
                    js,
                ),

            "overlap":
                summary_statistics(
                    overlap,
                ),

        },

    }


def analyse(
    df: pd.DataFrame,
):

    original = analyse_single(
        df,
    )

    minmax = analyse_single(

        normalize_minmax(
            df,
        )

    )

    zscore = analyse_single(

        normalize_zscore(
            df,
        )

    )

    return {

        "original": original,

        "minmax": minmax,

        "zscore": zscore,

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

    for mode in [

        "minmax",

        "zscore",

    ]:

        storage.create_folder(
            f"tables/{mode}"
        )

        mode_dir = storage.folder(
            f"tables/{mode}"
        )

        r = results[mode]

        r["wasserstein"].to_csv(
            mode_dir / "wasserstein_matrix.csv"
        )

        r["ks_distance"].to_csv(
            mode_dir / "ks_distance_matrix.csv"
        )

        r["ks_pvalue"].to_csv(
            mode_dir / "ks_pvalue_matrix.csv"
        )

        r["js"].to_csv(
            mode_dir / "js_matrix.csv"
        )

        r["overlap"].to_csv(
            mode_dir / "overlap_matrix.csv"
        )

    with open(

        json_dir / "normalized_distribution.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "original":

                    results["original"]["summary"],

                "minmax":

                    results["minmax"]["summary"],

                "zscore":

                    results["zscore"]["summary"],

            },

            f,

            indent=4,

        )

    certificate = {

        "observatory":

            "L2.7.1",

        "title":

            "Normalized Distribution Comparison",

        "normalizations": [

            "minmax",

            "zscore",

        ],

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

    report.append("L2.7.1 Normalized Distribution Comparison")

    report.append("=" * 60)

    report.append("")

    for mode in [

        "original",

        "minmax",

        "zscore",

    ]:

        s = results[mode]["summary"]

        report.append(mode.upper())

        report.append("-" * 40)

        report.append("")

        for metric in [

            "wasserstein",

            "ks",

            "js",

            "overlap",

        ]:

            report.append(metric.upper())

            report.append(

                f"Minimum : {s[metric]['minimum']}"

            )

            report.append(

                f"Maximum : {s[metric]['maximum']}"

            )

            report.append(

                f"Mean    : {s[metric]['mean']}"

            )

            report.append("")

    with open(

        report_dir / "normalized_distribution_report.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            "\n".join(report)

        )

    comparison = []

    comparison.append("=" * 60)

    comparison.append(

        "Comparison Original vs Normalized"

    )

    comparison.append("=" * 60)

    comparison.append("")

    for metric in [

        "wasserstein",

        "ks",

        "js",

        "overlap",

    ]:

        comparison.append(metric.upper())

        comparison.append(

            f"Original Mean : {results['original']['summary'][metric]['mean']}"

        )

        comparison.append(

            f"MinMax Mean   : {results['minmax']['summary'][metric]['mean']}"

        )

        comparison.append(

            f"ZScore Mean   : {results['zscore']['summary'][metric]['mean']}"

        )

        comparison.append("")

    with open(

        report_dir / "comparison_original_vs_normalized.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            "\n".join(comparison)

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

        experiment="S29_E6_2_L2_7_1",

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

        df,

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
