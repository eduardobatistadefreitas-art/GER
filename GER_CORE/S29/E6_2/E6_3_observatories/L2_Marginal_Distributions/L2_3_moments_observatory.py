"""
============================================================
GER
L2.3 Moments Observatory
============================================================

Scientific Objective
--------------------
Compute the fundamental statistical moments of each
numeric variable in the Relational Signature dataset.

This observatory characterizes the central tendency,
dispersion and shape of the empirical distributions
without assuming any probability model.

Outputs
-------
report/
    moments_report.txt

tables/
    moments.csv

json/
    moments.json

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
    "L2.3 Moments Observatory"
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

        values = series.dropna()

        mean = float(values.mean())

        std = float(values.std())

        variance = float(values.var())

        median = float(values.median())

        cv = (

            std / abs(mean)

            if abs(mean) > 1e-12

            else np.nan

        )

        skewness = float(values.skew())

        kurtosis = float(values.kurt())

        rows.append(

            {

                "Variable":

                    column,

                "Count":

                    int(values.count()),

                "Mean":

                    mean,

                "Median":

                    median,

                "Variance":

                    variance,

                "Standard Deviation":

                    std,

                "Coefficient of Variation":

                    cv,

                "Skewness":

                    skewness,

                "Kurtosis":

                    kurtosis,

            }

        )

    moments = pd.DataFrame(rows)

    cv_values = moments[
        "Coefficient of Variation"
    ].replace(

        [np.inf, -np.inf],

        np.nan,

    )

    summary = {

        "variables":

            len(moments),

        "total_observations":

            total_observations,

        "average_cv":

            float(cv_values.mean()),

        "maximum_cv":

            float(cv_values.max()),

        "minimum_cv":

            float(cv_values.min()),

        "status":

            "PASS",

    }

    return {

        "summary":

            summary,

        "moments":

            moments,

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

    result["moments"].to_csv(

        tables_folder / "moments.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "moments.json",

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

        "observatory": "L2.3",

        "title": "Moments Observatory",

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
L2.3 Moments Observatory
============================================================

Variables Analysed
{summary['variables']}

Total Observations
{summary['total_observations']}

Average CV
{summary['average_cv']:.6f}

Maximum CV
{summary['maximum_cv']:.6f}

Minimum CV
{summary['minimum_cv']:.6f}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "moments_report.txt",

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

        experiment="S29_E6_2_L2_3",

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
