"""
============================================================
GER
L2.2 Marginal Distribution
============================================================

Scientific Objective
--------------------
Describe the empirical marginal distribution of each
variable in the Relational Signature dataset.

This observatory provides a non-parametric description of
each variable without assuming any probability model.

Outputs
-------
report/
    marginal_distribution_report.txt

tables/
    marginal_profiles.csv
    marginal_distributions.csv

json/
    marginal_distribution.json

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


TITLE = (
    "GER\n"
    "L2.2 Marginal Distribution"
)


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    profiles = []

    distributions = []

    total_observations = len(df)

    for column in df.columns:

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):

            continue

        values = series.dropna()

        profile = {

            "Variable":

                column,

            "Count":

                int(values.count()),

            "Unique":

                int(values.nunique()),

            "Min":

                float(values.min()),

            "Q25":

                float(values.quantile(0.25)),

            "Median":

                float(values.median()),

            "Q75":

                float(values.quantile(0.75)),

            "Max":

                float(values.max()),

            "IQR":

                float(

                    values.quantile(0.75)

                    -

                    values.quantile(0.25)

                ),

        }

        profiles.append(
            profile
        )

        frequency = (

            values

            .value_counts(

                dropna=False,

            )

            .sort_index()

        )

        relative = (

            frequency

            /

            frequency.sum()

        )

        distribution = pd.DataFrame(

            {

                "Variable":

                    column,

                "Value":

                    frequency.index,

                "Frequency":

                    frequency.values,

                "Relative Frequency":

                    relative.values,

            }

        )

        distributions.append(
            distribution
        )

    profiles = pd.DataFrame(
        profiles
    )

    distributions = pd.concat(

        distributions,

        ignore_index=True,

    )

    summary = {

        "variables":

            len(profiles),

        "total_observations":

            total_observations,

        "status":

            "PASS",

    }

    return {

        "summary":

            summary,

        "profiles":

            profiles,

        "distributions":

            distributions,

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
    # TABLES
    # --------------------------------------------------------

    result["profiles"].to_csv(

        tables_folder / "marginal_profiles.csv",

        index=False,

    )

    result["distributions"].to_csv(

        tables_folder / "marginal_distributions.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "marginal_distribution.json",

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

        "observatory": "L2.2",

        "title": "Marginal Distribution",

        "variables":
            summary["variables"],

        "total_observations":
            summary["total_observations"],

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
L2.2 Marginal Distribution
============================================================

Variables Analysed
{summary['variables']}

Total Observations
{summary['total_observations']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "marginal_distribution_report.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

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

        experiment="S29_E6_2_L2_2",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

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
