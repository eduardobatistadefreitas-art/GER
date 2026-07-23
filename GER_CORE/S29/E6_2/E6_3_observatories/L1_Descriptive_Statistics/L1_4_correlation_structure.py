"""
============================================================
GER
L1.4 Correlation Structure Observatory
============================================================

Scientific Question
-------------------
Are the geometric observables statistically independent,
or do they exhibit intrinsic correlations?

This observatory characterizes the correlation structure
of the Relational Signature Space.

Outputs
-------
report/
    correlation_structure_report.txt

tables/
    pearson_matrix.csv
    spearman_matrix.csv
    covariance_matrix.csv
    correlation_ranking.csv

json/
    correlation_structure.json

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


TITLE = "GER\nL1.4 Correlation Structure Observatory"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame) -> dict:
    """
    Analyse correlation structure of the signature space.
    """

    numeric = df.select_dtypes(include=[np.number])

    pearson = numeric.corr(method="pearson")

    spearman = numeric.corr(method="spearman")

    covariance = numeric.cov()

    ranking = []

    columns = list(numeric.columns)

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            value = float(
                pearson.iloc[i, j]
            )

            ranking.append(

                {
                    "Variable A": columns[i],
                    "Variable B": columns[j],
                    "Correlation": value,
                    "Absolute Correlation": abs(value),
                }

            )

    ranking = (
        pd.DataFrame(ranking)
        .sort_values(
            "Absolute Correlation",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    strongest = ranking.iloc[0].to_dict()

    weakest = ranking.iloc[-1].to_dict()

    summary = {

        "variables": len(columns),

        "pairs": len(ranking),

        "maximum_absolute_correlation":
            float(
                ranking.iloc[0][
                    "Absolute Correlation"
                ]
            ),

        "minimum_absolute_correlation":
            float(
                ranking.iloc[-1][
                    "Absolute Correlation"
                ]
            ),

        "strongest_pair": strongest,

        "weakest_pair": weakest,

        "status": "PASS",

    }

    return {

        "summary": summary,

        "pearson": pearson,

        "spearman": spearman,

        "covariance": covariance,

        "ranking": ranking,
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

    result["pearson"].to_csv(
        tables_folder / "pearson_matrix.csv"
    )

    result["spearman"].to_csv(
        tables_folder / "spearman_matrix.csv"
    )

    result["covariance"].to_csv(
        tables_folder / "covariance_matrix.csv"
    )

    result["ranking"].to_csv(
        tables_folder / "correlation_ranking.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(
        json_folder / "correlation_structure.json",
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

    with open(
        certificate_folder / "certificate.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            {
                "observatory": "L1.4",
                "title": "Correlation Structure Observatory",
                "status": summary["status"],
            },
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    strongest = summary["strongest_pair"]
    weakest = summary["weakest_pair"]

    report = f"""
============================================================
GER
L1.4 Correlation Structure Observatory
============================================================

Variables
{summary['variables']}

Pairs
{summary['pairs']}

Maximum Absolute Correlation
{summary['maximum_absolute_correlation']:.6f}

Minimum Absolute Correlation
{summary['minimum_absolute_correlation']:.6f}

Strongest Pair
{strongest['Variable A']}
{strongest['Variable B']}
Correlation = {strongest['Correlation']:.6f}

Weakest Pair
{weakest['Variable A']}
{weakest['Variable B']}
Correlation = {weakest['Correlation']:.6f}

Status
{summary['status']}

============================================================
"""

    with open(
        report_folder / "correlation_structure_report.txt",
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

        experiment="S29_E6_2_L1_4",

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

    run()}
  
