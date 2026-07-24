"""
============================================================
GER
L2.7 Distribution Comparison
============================================================

Scientific Objective
--------------------
Compare the marginal distributions of every numeric
observable using complementary statistical distances.

Unlike previous observatories that characterize each
variable independently, this observatory studies the
relationships between marginal distributions.

Outputs
-------
report/
    distribution_comparison_report.txt

tables/
    wasserstein_matrix.csv
    ks_distance_matrix.csv
    ks_pvalue_matrix.csv
    js_matrix.csv
    overlap_matrix.csv

json/
    distribution_comparison.json

certificate/
    certificate.json

============================================================
"""

from __future__ import annotations

import json

import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...statistical_observatory.io import (
    load_signatures,
)

from ...statistics.distribution_comparison import (

    pairwise_wasserstein,

    pairwise_ks,

    pairwise_js,

    pairwise_overlap,

    summary_statistics,

)

TITLE = (

    "GER\n"

    "L2.7 Distribution Comparison"

)

# ============================================================
# ANALYSIS
# ============================================================


def analyse(
    df: pd.DataFrame,
):

    wasserstein = pairwise_wasserstein(
        df,
    )

    ks_distance, ks_pvalue = pairwise_ks(
        df,
    )

    js = pairwise_js(
        df,
    )

    overlap = pairwise_overlap(
        df,
    )

    summary = {

        "wasserstein":
            summary_statistics(
                wasserstein,
            ),

        "ks":
            summary_statistics(
                ks_distance,
            ),

        "js":
            summary_statistics(
                js,
            ),

        "overlap":
            summary_statistics(
                overlap,
            ),

        "variables":
            len(
                wasserstein.columns
            ),

        "comparisons":
            summary_statistics(
                wasserstein,
            )["comparisons"],

        "status":
            "PASS",

    }

    return {

        "summary":
            summary,

        "wasserstein":
            wasserstein,

        "ks_distance":
            ks_distance,

        "ks_pvalue":
            ks_pvalue,

        "js":
            js,

        "overlap":
            overlap,

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

    results["wasserstein"].to_csv(

        tables_dir / "wasserstein_matrix.csv",

        index=True,

    )

    results["ks_distance"].to_csv(

        tables_dir / "ks_distance_matrix.csv",

        index=True,

    )

    results["ks_pvalue"].to_csv(

        tables_dir / "ks_pvalue_matrix.csv",

        index=True,

    )

    results["js"].to_csv(

        tables_dir / "js_matrix.csv",

        index=True,

    )

    results["overlap"].to_csv(

        tables_dir / "overlap_matrix.csv",

        index=True,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_dir / "distribution_comparison.json",

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
            "L2.7",

        "title":
            "Distribution Comparison",

        "variables":
            summary["variables"],

        "comparisons":
            summary["comparisons"],

        "metrics": [

            "Wasserstein",

            "Kolmogorov-Smirnov",

            "Jensen-Shannon",

            "Overlap",

        ],

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
L2.7 Distribution Comparison
============================================================

Variables
{summary['variables']}

Comparisons
{summary['comparisons']}

------------------------------------------------------------
Wasserstein

Minimum
{summary['wasserstein']['minimum']}

Maximum
{summary['wasserstein']['maximum']}

Mean
{summary['wasserstein']['mean']}

------------------------------------------------------------
Kolmogorov-Smirnov

Minimum
{summary['ks']['minimum']}

Maximum
{summary['ks']['maximum']}

Mean
{summary['ks']['mean']}

------------------------------------------------------------
Jensen-Shannon

Minimum
{summary['js']['minimum']}

Maximum
{summary['js']['maximum']}

Mean
{summary['js']['mean']}

------------------------------------------------------------
Overlap

Minimum
{summary['overlap']['minimum']}

Maximum
{summary['overlap']['maximum']}

Mean
{summary['overlap']['mean']}

------------------------------------------------------------

Outputs

wasserstein_matrix.csv
ks_distance_matrix.csv
ks_pvalue_matrix.csv
js_matrix.csv
overlap_matrix.csv

Status
{summary['status']}

============================================================
"""

    with open(

        report_dir / "distribution_comparison_report.txt",

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

        experiment="S29_E6_2_L2_7",

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
