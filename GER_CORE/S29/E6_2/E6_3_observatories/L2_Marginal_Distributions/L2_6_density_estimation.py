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

        # ----------------------------------------
        # KDE sample (for scalability)
        # ----------------------------------------

        if len(values) > MAX_KDE_SAMPLE:

            values_kde = rng.choice(

                values,

                size=MAX_KDE_SAMPLE,

                replace=False,

            )

        else:

            values_kde = values

        # ----------------------------------------
        # Density estimation
        # ----------------------------------------

        density_df = density_grid(
   
            values_kde,
            
            grid_size=GRID_POINTS,
            
        )
        grid = density_df["Value"].to_numpy()
        
        density = density_df["Density"].to_numpy()

        peak_location, peak_density = density_peak(

            grid,

            density,

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

        support = float(

            effective_support(

                values_kde,

            )

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
    results,
):

    storage = ExperimentStorage()

    storage.create_folder(

        "S29/E6_2/L2_6_density_estimation"

    )

    folder = storage.folder(

        "S29/E6_2/L2_6_density_estimation"

    )

    report_dir = folder / "report"
    tables_dir = folder / "tables"
    json_dir = folder / "json"
    certificate_dir = folder / "certificate"

    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    tables_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    certificate_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Tables
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

            results["summary"],

            f,

            indent=4,

        )

    # --------------------------------------------------------
    # Certificate
    # --------------------------------------------------------

    certificate = {

        "title": TITLE,

        "status": results["summary"]["status"],

        "variables": results["summary"]["variables"],

        "grid_points": results["summary"]["grid_points"],

        "max_kde_sample": results["summary"]["max_kde_sample"],

        "total_observations": results["summary"]["total_observations"],

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
    # Report
    # --------------------------------------------------------

    report = []

    report.append("=" * 60)
    report.append("GER")
    report.append("L2.6 Density Estimation")
    report.append("=" * 60)
    report.append("")

    for key, value in results["summary"].items():

        report.append(

            f"{key:25s}: {value}"

        )

    report.append("")
    report.append("Density profiles computed successfully.")

    with open(

        report_dir / "density_estimation_report.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

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

    df = load_signatures()

    print(

        f"Loaded signatures : {len(df):,}"

    )

    print()

    results = analyse(

        df,

    )

    save(

        results,

    )

    print()

    print("Density estimation completed.")

    print(

        f"Variables analysed : {results['summary']['variables']}"

    )

    print(

        f"KDE grid points    : {results['summary']['grid_points']}"

    )

    print()

    print("Status : PASS")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run()
