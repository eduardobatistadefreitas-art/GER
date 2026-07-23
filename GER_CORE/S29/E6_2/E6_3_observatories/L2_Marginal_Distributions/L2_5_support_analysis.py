"""
============================================================
GER
L2.5 Support Analysis
============================================================

Scientific Objective
--------------------
Characterize the intrinsic geometry of the support of
each numeric variable.

Instead of analysing probability distributions, this
observatory studies how the observed values occupy
their domain.

Outputs
-------
report/
    support_analysis_report.txt

tables/
    support_analysis.csv
    spacing_distribution.csv

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

    spacing_rows = []

    total_observations = len(df)

    for column in df.columns:

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):

            continue

        values = np.sort(

            series
            .dropna()
            .unique()

        )

        minimum = float(values.min())

        maximum = float(values.max())

        value_range = maximum - minimum

        unique_values = len(values)

        if unique_values > 1:

            spacing = np.diff(values)

            minimum_spacing = float(

                spacing.min()

            )

            mean_spacing = float(

                spacing.mean()

            )

            maximum_spacing = float(

                spacing.max()

            )

            spacing_cv = (

                float(spacing.std())

                /

                float(spacing.mean())

                if spacing.mean() > 0

                else 0.0

            )

            regular = np.allclose(

                spacing,

                spacing[0],

                rtol=1e-6,

                atol=1e-12,

            )

        else:

            spacing = np.array([])

            minimum_spacing = 0.0

            mean_spacing = 0.0

            maximum_spacing = 0.0

            spacing_cv = 0.0

            regular = True

        if unique_values <= 20:

            support_type = "Discrete"

        elif regular:

            support_type = "Regular"

        else:

            support_type = "Irregular"

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

                "Minimum Resolution":

                    minimum_spacing,

                "Mean Spacing":

                    mean_spacing,

                "Maximum Spacing":

                    maximum_spacing,

                "Spacing CV":

                    spacing_cv,

                "Support Type":

                    support_type,

            }

        )

        for value in spacing:

            spacing_rows.append(

                {

                    "Variable":

                        column,

                    "Spacing":

                        float(value),

                }

            )

    support = pd.DataFrame(rows)

    spacing_distribution = pd.DataFrame(

        spacing_rows

    )

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

        "spacing_distribution":

            spacing_distribution,

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

    result["support"].to_csv(

        tables_folder / "support_analysis.csv",

        index=False,

    )

    result["spacing_distribution"].to_csv(

        tables_folder / "spacing_distribution.csv",

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

Outputs

support_analysis.csv
spacing_distribution.csv

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
