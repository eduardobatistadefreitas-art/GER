"""
============================================================
GER
L2.6 Density Estimation
============================================================

Scientific Objective
--------------------
Estimate the empirical probability density of each
numeric observable using non-parametric kernel density
estimation (KDE).

Unlike distribution fitting (L2.4), this observatory
does not assume any parametric family.

Outputs
-------
report/
    density_estimation_report.txt

tables/
    density_profile.csv
    density_grid.csv

json/
    density_estimation.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from scipy.integrate import trapezoid

from GER.CORE.ger_storage import ExperimentStorage

from ...statistical_observatory.io import load_signatures

from ...statistics import (
    density_grid,
    density_peak,
    effective_support,
)

TITLE = (
    "GER\n"
    "L2.6 Density Estimation"
)

# ============================================================
# CONSTANTS
# ============================================================

GRID_POINTS = 512

MAX_KDE_SAMPLE = 100_000

RANDOM_SEED = 42

# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    profile_rows = []

    density_rows = []

    total_observations = len(df)

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    for column in df.columns:

        series = (
            df[column]
            .dropna()
            .astype(float)
        )

        if len(series) < 2:

            continue

        values = series.to_numpy()

        # ----------------------------------------------------
        # KDE sample
        # ----------------------------------------------------

        if len(values) > MAX_KDE_SAMPLE:

            values_kde = rng.choice(
                values,
                size=MAX_KDE_SAMPLE,
                replace=False,
            )

        else:

            values_kde = values

        # ----------------------------------------------------
        # Density estimation
        # ----------------------------------------------------

        density_df = density_grid(
            values_kde,
            grid_size=GRID_POINTS,
        )

        grid = density_df["Value"].to_numpy()

        density = density_df["Density"].to_numpy()

        peak = density_peak(
            values_kde,
        )

        peak_location = float(
            peak["value"]
        )

        peak_density = float(
            peak["density"]
        )

        integral = float(
            trapezoid(
                density,
                grid,
            )
        )

        mean_density = float(
            np.mean(
                density
            )
        )

        support_info = effective_support(
            values_kde,
        )

        support = float(
            support_info["range"]
        )

        profile_rows.append(

            {

                "Variable":
                    column,

                "Sample Size":
                    len(values),

                "KDE Sample":
                    len(values_kde),

                "Grid Points":
                    GRID_POINTS,

                "Density Peak":
                    peak_density,

                "Peak Location":
                    peak_location,

                "Mean Density":
                    mean_density,

                "Density Integral":
                    integral,

                "Effective Support Width":
                    support,

            }

        )

        density_rows.extend(

            {

                "Variable":
                    column,

                "X":
                    float(x),

                "Density":
                    float(y),

            }

            for x, y in zip(
                grid,
                density,
            )

        )

    profile = pd.DataFrame(
        profile_rows
    )

    density_grid_table = pd.DataFrame(
        density_rows
    )

    summary = {

        "variables":
            len(profile),

        "grid_points":
            GRID_POINTS,

        "max_kde_sample":
            MAX_KDE_SAMPLE,

        "total_observations":
            total_observations,

        "status":
            "PASS",

    }

    return {

        "summary":
            summary,

        "profile":
            profile,

        "density_grid":
            density_grid_table,

    }

# ============================================================
# SAVE
# ============================================================

def save(
    storage: ExperimentStorage,
    results: dict,
):

    summary = results["summary"]

    storage.create_folder("report")
    storage.create_folder("tables")
    storage.create_folder("json")
    storage.create_folder("certificate")

    report_dir = storage.folder("report")
    tables_dir = storage.folder("tables")
    json_dir = storage.folder("json")
    certificate_dir = storage.folder("certificate")

    # --------------------------------------------------------
    # TABLES
    # --------------------------------------------------------

    results["profile"].to_csv(

        tables_dir / "density_profile.csv",

        index=False,

    )

    results["density_grid"].to_csv(

        tables_dir / "density_grid.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_dir / "density_estimation.json",

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

        "observatory":
            "L2.6",

        "title":
            "Density Estimation",

        "variables":
            summary["variables"],

        "grid_points":
            summary["grid_points"],

        "max_kde_sample":
            summary["max_kde_sample"],

        "total_observations":
            summary["total_observations"],

        "status":
            summary["status"],

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

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report = f"""
============================================================
GER
L2.6 Density Estimation
============================================================

Variables Analysed
{summary['variables']}

Total Observations
{summary['total_observations']}

KDE Grid Points
{summary['grid_points']}

Maximum KDE Sample
{summary['max_kde_sample']}

Outputs

density_profile.csv
density_grid.csv

Status
{summary['status']}

============================================================
"""

    with open(

        report_dir / "density_estimation_report.txt",

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

        experiment="S29_E6_2_L2_6",

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
