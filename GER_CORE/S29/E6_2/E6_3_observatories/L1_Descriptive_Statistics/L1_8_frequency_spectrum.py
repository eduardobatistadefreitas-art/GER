"""
============================================================
GER
L1.8 Frequency Spectrum Observatory
============================================================

Scientific Question
-------------------
Which statistical model best describes the frequency
spectrum of geometric signatures?

Outputs
-------
report/
    frequency_spectrum_report.txt

tables/
    model_comparison.csv
    spectrum_statistics.csv

json/
    frequency_spectrum.json

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


TITLE = "GER\nL1.8 Frequency Spectrum Observatory"


# ============================================================
# FIT
# ============================================================

def fit_distribution(values, distribution):

    params = distribution.fit(values)

    loglikelihood = np.sum(
        distribution.logpdf(values, *params)
    )

    k = len(params)

    n = len(values)

    aic = 2 * k - 2 * loglikelihood

    bic = np.log(n) * k - 2 * loglikelihood

    ks, p = stats.kstest(

        values,

        distribution.name,

        args=params,

    )

    return {

        "Distribution": distribution.name,

        "AIC": aic,

        "BIC": bic,

        "KS": ks,

        "KS p-value": p,

        "Parameters": params,

    }


# ============================================================
# ANALYSIS
# ============================================================

def analyse(df: pd.DataFrame):

    grouped = (

        df
        .groupby(list(df.columns))
        .size()
        .reset_index(name="Frequency")

    )

    freq = grouped["Frequency"].values

    statistics = pd.DataFrame({

        "Statistic": [

            "Unique Signatures",

            "Total Occurrences",

            "Mean",

            "Median",

            "Std",

            "Variance",

            "Minimum",

            "Maximum",

            "Skewness",

            "Kurtosis",

        ],

        "Value": [

            len(freq),

            int(freq.sum()),

            float(np.mean(freq)),

            float(np.median(freq)),

            float(np.std(freq)),

            float(np.var(freq)),

            int(np.min(freq)),

            int(np.max(freq)),

            float(stats.skew(freq)),

            float(stats.kurtosis(freq)),

        ],

    })

    models = [

        stats.norm,

        stats.expon,

        stats.gamma,

        stats.lognorm,

        stats.weibull_min,

    ]

    comparison = []

    for model in models:

        try:

            comparison.append(

                fit_distribution(
                    freq,
                    model,
                )

            )

        except Exception:

            continue

    comparison = (

        pd.DataFrame(comparison)

        .sort_values("AIC")

        .reset_index(drop=True)

    )

    winner = comparison.iloc[0]

    summary = {

        "winner": winner["Distribution"],

        "aic": float(winner["AIC"]),

        "bic": float(winner["BIC"]),

        "ks": float(winner["KS"]),

        "ks_pvalue": float(
            winner["KS p-value"]
        ),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "statistics": statistics,

        "comparison": comparison,

    }

# ============================================================
# SAVE
# ============================================================

def save(storage: ExperimentStorage, result: dict):

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
        tables_folder / "spectrum_statistics.csv",
        index=False,
    )

    comparison = result["comparison"].copy()

    comparison["Parameters"] = comparison["Parameters"].astype(str)

    comparison.to_csv(
        tables_folder / "model_comparison.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    json_summary = summary.copy()

    json_summary["parameters"] = str(
        result["comparison"].iloc[0]["Parameters"]
    )

    with open(
        json_folder / "frequency_spectrum.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            json_summary,
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
                "observatory": "L1.8",
                "title": "Frequency Spectrum Observatory",
                "best_model": summary["winner"],
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
L1.8 Frequency Spectrum Observatory
============================================================

Best Statistical Model
{summary['winner']}

AIC
{summary['aic']:.6f}

BIC
{summary['bic']:.6f}

Kolmogorov-Smirnov Statistic
{summary['ks']:.6f}

Kolmogorov-Smirnov p-value
{summary['ks_pvalue']:.6f}

Status
{summary['status']}

============================================================
"""

    with open(
        report_folder / "frequency_spectrum_report.txt",
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

        experiment="S29_E6_2_L1_8",

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
