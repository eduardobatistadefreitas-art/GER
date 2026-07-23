"""
============================================================
GER
L2.5 Support Analysis
============================================================

Scientific Objective
--------------------
Characterize the effective support of each numeric
variable in the Relational Signature dataset.

This observatory investigates the occupied domain,
support continuity and the existence of gaps within
the observed interval.

Outputs
-------
report/
    support_analysis_report.txt

tables/
    support_analysis.csv

json/
    support_analysis.json

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
    "L2.5 Support Analysis"
)


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    rows = []

    total_observations = len(df)

    for column in df.columns:

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):

            continue

        values = np.sort(

            series.dropna().unique()

        )

        minimum = float(values.min())

        maximum = float(values.max())

        value_range = maximum - minimum

        unique_values = len(values)

        observed_values = unique_values

        is_integer = np.all(

            np.isclose(

                values,

                np.round(values),

            )

        )

        if is_integer:

            expected_values = int(

                round(maximum - minimum)

            ) + 1

            gap_count = (

                expected_values

                - unique_values

            )

        else:

            expected_values = unique_values

            gap_count = 0

        support_occupancy = (

            observed_values

            /

            expected_values

        )

        gap_ratio = (

            gap_count

            /

            expected_values

        )

        if support_occupancy >= 0.95:

            support_type = "Continuous"

        elif support_occupancy >= 0.50:

            support_type = "Discrete"

        else:

            support_type = "Sparse"

        rows.append(

            {

                "Variable":

                    column,

                "Minimum":

                    minimum,

                "Maximum":

                    maximum,

                "Range":

                    value_range,

                "Unique Values":

                    unique_values,

                "Observed Values":

                    observed_values,

                "Expected Values":

                    expected_values,

                "Support Occupancy":

                    support_occupancy,

                "Gap Count":

                    gap_count,

                "Gap Ratio":

                    gap_ratio,

                "Support Type":

                    support_type,

            }

        )

    support = pd.DataFrame(rows)

    summary = {

        "variables":

            len(support),

        "total_observations":

            total_observations,

        "status":

            "PASS",

    }

    return {

        "summary":

            summary,

        "support":

            support,

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

    result["support"].to_csv(

        tables_folder / "support_analysis.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "support_analysis.json",

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

        "observatory": "L2.5",

        "title": "Support Analysis",

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
L2.5 Support Analysis
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

        report_folder / "support_analysis_report.txt",

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

        experiment="S29_E6_2_L2_5",

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
