"""
============================================================
GER
L1.3 Distribution Shape Observatory
============================================================

Scientific Question
-------------------
What is the statistical shape of the signature multiplicity
distribution?

This observatory characterizes the intrinsic statistical
structure of the Relational Signature Space.

Outputs
-------
report/
    distribution_shape_report.txt

tables/
    distribution_statistics.csv
    multiplicity_distribution.csv

json/
    distribution_shape.json

certificate/
    certificate.json

Author
------
Eduardo Batista de Freitas

Framework
---------
GER

Version
-------
1.0
============================================================
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...io import load_signatures


TITLE = "GER\nL1.3 Distribution Shape Observatory"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame) -> dict:
    """
    Analyse the statistical shape of the multiplicity
    distribution.
    """

    grouped = (
        df.groupby(list(df.columns))
        .size()
        .reset_index(name="Multiplicity")
        .sort_values("Multiplicity", ascending=False)
        .reset_index(drop=True)
    )

    multiplicity = grouped["Multiplicity"].to_numpy(dtype=float)

    probabilities = multiplicity / multiplicity.sum()

    entropy = float(
        -np.sum(
            probabilities * np.log2(probabilities)
        )
    )

    q1 = float(np.percentile(multiplicity, 25))
    median = float(np.median(multiplicity))
    q3 = float(np.percentile(multiplicity, 75))

    iqr = q3 - q1

    mean = float(np.mean(multiplicity))
    std = float(np.std(multiplicity))
    variance = float(np.var(multiplicity))

    minimum = float(np.min(multiplicity))
    maximum = float(np.max(multiplicity))
    data_range = maximum - minimum

    cv = std / mean if mean > 0 else 0.0

    skewness = float(
        pd.Series(multiplicity).skew()
    )

    kurtosis = float(
        pd.Series(multiplicity).kurt()
    )

    sorted_values = np.sort(multiplicity)

    n = len(sorted_values)

    gini = (
        (
            np.sum(
                (2 * np.arange(1, n + 1) - n - 1)
                * sorted_values
            )
        )
        /
        (n * np.sum(sorted_values))
    )

    summary = {

        "unique_signatures": int(len(grouped)),

        "mean": mean,

        "median": median,

        "std": std,

        "variance": variance,

        "minimum": minimum,

        "maximum": maximum,

        "range": data_range,

        "q1": q1,

        "q3": q3,

        "iqr": iqr,

        "coefficient_variation": float(cv),

        "skewness": skewness,

        "kurtosis": kurtosis,

        "entropy_bits": entropy,

        "gini": float(gini),

        "status": "PASS",

    }

    statistics = pd.DataFrame(
        [
            {
                "Metric": key,
                "Value": value,
            }
            for key, value in summary.items()
        ]
    )

    return {

        "summary": summary,

        "statistics": statistics,

        "distribution": grouped,

  }
  # ============================================================
# SAVE
# ============================================================

def save(storage: ExperimentStorage, result: dict) -> None:

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
    # TABLES
    # --------------------------------------------------------

    result["statistics"].to_csv(
        tables_folder / "distribution_statistics.csv",
        index=False,
    )

    result["distribution"].to_csv(
        tables_folder / "multiplicity_distribution.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(
        json_folder / "distribution_shape.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(summary, f, indent=4)

    # --------------------------------------------------------
    # CERTIFICATE
    # --------------------------------------------------------

    with open(
        certificate_folder / "certificate.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            {
                "observatory": "L1.3",
                "title": "Distribution Shape Observatory",
                "status": summary["status"],
            },
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report = f"""
============================================================
GER
L1.3 Distribution Shape Observatory
============================================================

Unique Signatures
{summary['unique_signatures']}

Mean
{summary['mean']:.6f}

Median
{summary['median']:.6f}

Standard Deviation
{summary['std']:.6f}

Variance
{summary['variance']:.6f}

Minimum
{summary['minimum']:.6f}

Maximum
{summary['maximum']:.6f}

Range
{summary['range']:.6f}

Q1
{summary['q1']:.6f}

Q3
{summary['q3']:.6f}

Interquartile Range
{summary['iqr']:.6f}

Coefficient of Variation
{summary['coefficient_variation']:.6f}

Skewness
{summary['skewness']:.6f}

Kurtosis
{summary['kurtosis']:.6f}

Entropy (bits)
{summary['entropy_bits']:.6f}

Gini Coefficient
{summary['gini']:.6f}

Status
{summary['status']}

============================================================
"""

    with open(
        report_folder / "distribution_shape_report.txt",
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

        experiment="S29_E6_2_L1_3",

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
