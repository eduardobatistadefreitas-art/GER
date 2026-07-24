"""
============================================================
GER
L2.8 Tail Behaviour
============================================================

Scientific Objective
--------------------
Characterize the tail behaviour of the marginal
distributions associated with the Geometric Signature
observables.

This observatory evaluates:

    • Skewness
    • Excess Kurtosis
    • Quantiles
    • Interquartile Range
    • Median Absolute Deviation
    • Tail Ratios
    • Tukey Outlier Rates

Outputs
-------

report/
    tail_behaviour_report.txt

tables/
    tail_summary.csv
    tail_quantiles.csv
    tail_ratios.csv
    tail_outliers.csv

json/
    tail_behaviour.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json

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
    "L2.8 Tail Behaviour"
)

# ============================================================
# HELPERS
# ============================================================


def median_absolute_deviation(values):

    values = np.asarray(values)

    median = np.median(values)

    return np.median(
        np.abs(values - median)
    )


def tail_statistics(
    series: pd.Series,
):

    values = series.to_numpy()

    q01 = np.percentile(values, 1)
    q05 = np.percentile(values, 5)
    q25 = np.percentile(values, 25)
    q50 = np.percentile(values, 50)
    q75 = np.percentile(values, 75)
    q95 = np.percentile(values, 95)
    q99 = np.percentile(values, 99)
    q999 = np.percentile(values, 99.9)

    iqr = q75 - q25

    mad = median_absolute_deviation(
        values
    )

    lower = q25 - 1.5 * iqr
    upper = q75 + 1.5 * iqr

    outliers = np.logical_or(
        values < lower,
        values > upper,
    )

    outlier_count = int(
        np.sum(outliers)
    )

    outlier_rate = (
        outlier_count / len(values)
    )

    return {

        "count":
            len(values),

        "mean":
            float(np.mean(values)),

        "std":
            float(np.std(values)),

        "median":
            float(q50),

        "skewness":
            float(skew(values)),

        "kurtosis":
            float(
                kurtosis(
                    values,
                    fisher=True,
                )
            ),

        "iqr":
            float(iqr),

        "mad":
            float(mad),

        "quantiles":{

            "1%":float(q01),
            "5%":float(q05),
            "25%":float(q25),
            "50%":float(q50),
            "75%":float(q75),
            "95%":float(q95),
            "99%":float(q99),
            "99.9%":float(q999),

        },

        "tail_ratios":{

            "P95/P50":
                float(
                    q95/(q50+1e-12)
                ),

            "P99/P50":
                float(
                    q99/(q50+1e-12)
                ),

            "P99.9/P50":
                float(
                    q999/(q50+1e-12)
                ),

        },

        "outliers":{

            "count":
                outlier_count,

            "rate":
                float(
                    outlier_rate
                ),

        },

    }


# ============================================================
# ANALYSIS
# ============================================================


def analyse(
    df: pd.DataFrame,
):

    results = {}

    for column in df.columns:

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):
            continue

        results[column] = tail_statistics(
            df[column]
        )

    return results

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

    summary_rows = []
    quantile_rows = []
    ratio_rows = []
    outlier_rows = []

    report = []

    report.append("=" * 60)
    report.append("GER")
    report.append("L2.8 Tail Behaviour")
    report.append("=" * 60)
    report.append("")

    for observable, stats in results.items():

        summary_rows.append({

            "observable": observable,
            "count": stats["count"],
            "mean": stats["mean"],
            "std": stats["std"],
            "median": stats["median"],
            "skewness": stats["skewness"],
            "kurtosis": stats["kurtosis"],
            "iqr": stats["iqr"],
            "mad": stats["mad"],

        })

        q = stats["quantiles"]

        quantile_rows.append({

            "observable": observable,

            **q,

        })

        r = stats["tail_ratios"]

        ratio_rows.append({

            "observable": observable,

            **r,

        })

        outlier_rows.append({

            "observable": observable,

            "count": stats["outliers"]["count"],

            "rate": stats["outliers"]["rate"],

        })

        report.append(observable.upper())
        report.append("-" * 40)

        report.append(
            f"Mean      : {stats['mean']:.6f}"
        )

        report.append(
            f"Std       : {stats['std']:.6f}"
        )

        report.append(
            f"Median    : {stats['median']:.6f}"
        )

        report.append(
            f"Skewness  : {stats['skewness']:.6f}"
        )

        report.append(
            f"Kurtosis  : {stats['kurtosis']:.6f}"
        )

        report.append(
            f"IQR        : {stats['iqr']:.6f}"
        )

        report.append(
            f"MAD        : {stats['mad']:.6f}"
        )

        report.append("")

        report.append("Quantiles")

        for name, value in q.items():

            report.append(
                f"  {name:<6}: {value:.6f}"
            )

        report.append("")

        report.append("Tail Ratios")

        for name, value in r.items():

            report.append(
                f"  {name:<12}: {value:.6f}"
            )

        report.append("")

        report.append(
            f"Outliers : {stats['outliers']['count']:,}"
        )

        report.append(
            f"Rate     : {100*stats['outliers']['rate']:.4f}%"
        )

        report.append("")
        report.append("")

    pd.DataFrame(
        summary_rows
    ).to_csv(

        tables_dir / "tail_summary.csv",

        index=False,

    )

    pd.DataFrame(
        quantile_rows
    ).to_csv(

        tables_dir / "tail_quantiles.csv",

        index=False,

    )

    pd.DataFrame(
        ratio_rows
    ).to_csv(

        tables_dir / "tail_ratios.csv",

        index=False,

    )

    pd.DataFrame(
        outlier_rows
    ).to_csv(

        tables_dir / "tail_outliers.csv",

        index=False,

    )

    with open(

        json_dir / "tail_behaviour.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            results,

            f,

            indent=4,

        )

    certificate = {

        "observatory": "L2.8",

        "title": "Tail Behaviour",

        "variables": len(results),

        "status": "PASS",

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

    with open(

        report_dir / "tail_behaviour_report.txt",

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

        experiment="S29_E6_2_L2_8",

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
