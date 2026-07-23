"""
============================================================
GER
L2.4 Distribution Fitting
============================================================

Scientific Objective
--------------------
Fit classical probability distributions to each
numeric variable of the Relational Signature dataset.

Each distribution is estimated using Maximum
Likelihood Estimation (MLE) and evaluated through the
Kolmogorov-Smirnov goodness-of-fit test.

Outputs
-------
report/
    distribution_fitting_report.txt

tables/
    distribution_fitting.csv
    best_fits.csv

json/
    distribution_fitting.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from scipy import stats

from GER.CORE.ger_storage import ExperimentStorage

from ...io import load_signatures


TITLE = (
    "GER\n"
    "L2.4 Distribution Fitting"
)


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    tested_models = [

        ("Normal", stats.norm),

        ("Uniform", stats.uniform),

        ("Exponential", stats.expon),

        ("Gamma", stats.gamma),

        ("Lognormal", stats.lognorm),

    ]

    fitting_rows = []

    best_rows = []

    total_observations = len(df)

    for column in df.columns:

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):

            continue

        values = series.dropna().to_numpy()

        results = []

        for name, distribution in tested_models:

            if name in ("Gamma", "Lognormal"):

                if np.any(values <= 0):

                    continue

            if name == "Exponential":

                if np.any(values < 0):

                    continue

            try:

                parameters = distribution.fit(values)

                ks_statistic, p_value = stats.kstest(

                    values,

                    distribution.name,

                    args=parameters,

                )

                accepted = (

                    "YES"

                    if ks_statistic <= 0.10

                    else "NO"

                )

                results.append(

                    {

                        "Variable":

                            column,

                        "Distribution":

                            name,

                        "KS Statistic":

                            float(ks_statistic),

                        "P Value":

                            float(p_value),

                        "Accepted":

                            accepted,

                    }

                )

            except Exception:

                continue

        if not results:

            continue

        results = sorted(

            results,

            key=lambda x: x["KS Statistic"],

        )

        for rank, row in enumerate(results, start=1):

            row["Rank"] = rank

            fitting_rows.append(row)

        best_rows.append(results[0])

    fitting = pd.DataFrame(fitting_rows)

    best = pd.DataFrame(best_rows)

    summary = {

        "variables":

            len(best),

        "tested_distributions":

            len(tested_models),

        "total_observations":

            total_observations,

        "status":

            "PASS",

    }

    return {

        "summary":

            summary,

        "fitting":

            fitting,

        "best":

            best,

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

    result["fitting"].to_csv(

        tables_folder / "distribution_fitting.csv",

        index=False,

    )

    result["best"].to_csv(

        tables_folder / "best_fits.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "distribution_fitting.json",

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

        "observatory": "L2.4",

        "title": "Distribution Fitting",

        "variables":
            summary["variables"],

        "tested_distributions":
            summary["tested_distributions"],

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
L2.4 Distribution Fitting
============================================================

Variables Analysed
{summary['variables']}

Tested Distributions
{summary['tested_distributions']}

Total Observations
{summary['total_observations']}

Status
{summary['status']}

------------------------------------------------------------
Methodological Notes
------------------------------------------------------------

The Kolmogorov-Smirnov statistic is used primarily
for comparative ranking between candidate models.

Because this dataset contains more than one million
observations, the KS p-values are expected to be
extremely small even for minor deviations from the
theoretical distributions.

The "Accepted" column is therefore an empirical
descriptor based on:

KS Statistic <= 0.10

It should not be interpreted as a formal hypothesis
acceptance criterion.

============================================================
"""

    with open(

        report_folder / "distribution_fitting_report.txt",

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

        experiment="S29_E6_2_L2_4",

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
