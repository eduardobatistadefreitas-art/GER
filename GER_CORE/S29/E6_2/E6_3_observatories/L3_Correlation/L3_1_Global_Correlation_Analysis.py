"""
============================================================
GER

S29 • E6.2

L3.1 — Correlation Matrix

Experiment E1

GLOBAL CORRELATION ANALYSIS

Version: 1.0

============================================================

Scientific Goal
---------------

Characterize the complete correlation structure among all
GER observables.

This experiment is descriptive.

No hypothesis testing is performed.

============================================================
"""

from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from .correlation_observatory.analysis import (
    run_analysis,
    build_summary,
    validate_results,
)

from .correlation_observatory.dashboard import (
    print_dashboard,
)

from .correlation_observatory.report import (
    write_report,
)

from .correlation_observatory.certificate import (
    build_certificate,
)

from ...statistical_observatory.io import load_signatures

from .correlation_observatory.io import (
    save_csv,
    save_json,
)

from .correlation_observatory.config import *


# ============================================================
# Metadata
# ============================================================

EXPERIMENT = "L3.1_E1"

TITLE = "Global Correlation Analysis"

VERSION = "1.0"


# ============================================================
# Heatmap
# ============================================================

def generate_heatmap(
    matrix,
    title,
    filename,
):
    """
    Generates a heatmap from a correlation matrix.
    """

    plt.figure(figsize=(9, 8))

    plt.imshow(
        matrix,
        interpolation="nearest",
        aspect="auto",
    )

    plt.colorbar()

    plt.xticks(
        range(len(matrix.columns)),
        matrix.columns,
        rotation=90,
    )

    plt.yticks(
        range(len(matrix.columns)),
        matrix.columns,
    )

    plt.title(title)

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# ============================================================
# Histogram
# ============================================================

def generate_histogram(
    table,
    title,
    filename,
):
    """
    Histogram of correlation coefficients.
    """

    plt.figure(figsize=(8, 5))

    plt.hist(
        table["Correlation"],
        bins=30,
    )

    plt.title(title)

    plt.xlabel("Correlation")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# ============================================================
# Statistics
# ============================================================

def build_statistics(results):

    statistics = {}

    for method in METHODS:

        table = results[method]["table"]

        statistics[method] = {

            "pairs": len(table),

            "maximum": float(table["Correlation"].max()),

            "minimum": float(table["Correlation"].min()),

            "mean": float(table["Correlation"].mean()),

            "median": float(table["Correlation"].median()),

            "std": float(table["Correlation"].std()),

            "strong_positive":

                int((table["Correlation"] > 0.8).sum()),

            "strong_negative":

                int((table["Correlation"] < -0.8).sum()),

            "weak":

                int((table["Correlation"].abs() < 0.2).sum()),
        }

    return statistics


# ============================================================
# Figures
# ============================================================

def generate_figures(
    results,
    output_folder,
):

    figures = output_folder / "figures"

    figures.mkdir(
        parents=True,
        exist_ok=True,
    )

    generate_heatmap(

        results["pearson"]["matrix"],

        "Pearson Correlation",

        figures / "pearson_heatmap.png",

    )

    generate_heatmap(

        results["spearman"]["matrix"],

        "Spearman Correlation",

        figures / "spearman_heatmap.png",

    )

    generate_heatmap(

        results["kendall"]["matrix"],

        "Kendall Correlation",

        figures / "kendall_heatmap.png",

    )

    generate_histogram(

        results["pearson"]["table"],

        "Pearson Distribution",

        figures / "pearson_histogram.png",

    )

    generate_histogram(

        results["spearman"]["table"],

        "Spearman Distribution",

        figures / "spearman_histogram.png",

    )

    generate_histogram(

        results["kendall"]["table"],

        "Kendall Distribution",

        figures / "kendall_histogram.png",

    )


# ============================================================
# Scientific Report
# ============================================================

def write_scientific_report(
    summary,
    statistics,
    filename,
):
    """
    Writes the scientific report.
    """

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as f:

        f.write("=" * 60 + "\n")

        f.write("GLOBAL CORRELATION ANALYSIS\n")

        f.write("=" * 60 + "\n\n")

        f.write(f"Version : {VERSION}\n")

        f.write(
            f"Generated : {datetime.now()}\n\n"
        )

        f.write(
            "GLOBAL SUMMARY\n\n"
        )

        for key, value in summary.items():

            f.write(f"{key}: {value}\n")

        f.write("\n")

        f.write(
            "=" * 60 + "\n"
        )

        f.write(
            "METHOD STATISTICS\n"
        )

        f.write(
            "=" * 60 + "\n\n"
        )

        for method, values in statistics.items():

            f.write(f"{method.upper()}\n")

            for k, v in values.items():

                f.write(f"   {k}: {v}\n")

            f.write("\n")

      # ============================================================
# Experiment
# ============================================================

def run_experiment(
    output_folder,
):

    df = load_signatures()
    """
    Runs the complete L3.1 Experiment E1.
    """

    output = Path(output_folder)

    tables = output / TABLE_FOLDER
    reports = output / REPORT_FOLDER
    certificates = output / CERTIFICATE_FOLDER
    json_dir = output / JSON_FOLDER

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_signatures()

    # --------------------------------------------------------
    # Analysis
    # --------------------------------------------------------

    results = run_analysis(df)

    validate_results(results)

    summary = build_summary(results)

    statistics = build_statistics(results)

    certificate = build_certificate(results)

    # --------------------------------------------------------
    # Export matrices
    # --------------------------------------------------------

    save_csv(
        results["pearson"]["matrix"],
        tables / PEARSON_MATRIX,
    )

    save_csv(
        results["spearman"]["matrix"],
        tables / SPEARMAN_MATRIX,
    )

    save_csv(
        results["kendall"]["matrix"],
        tables / KENDALL_MATRIX,
    )

    # --------------------------------------------------------
    # Export tables
    # --------------------------------------------------------

    save_csv(
        results["pearson"]["table"],
        tables / PEARSON_TABLE,
    )

    save_csv(
        results["spearman"]["table"],
        tables / SPEARMAN_TABLE,
    )

    save_csv(
        results["kendall"]["table"],
        tables / KENDALL_TABLE,
    )

    # --------------------------------------------------------
    # Figures
    # --------------------------------------------------------

    generate_figures(
        results,
        output,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    save_json(
        summary,
        json_dir / SUMMARY_JSON,
    )

    save_json(
        statistics,
        json_dir / "statistics.json",
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    write_report(
        summary,
        reports / REPORT_FILE,
    )

    write_scientific_report(
        summary,
        statistics,
        reports / "L3_1_E1_scientific_report.txt",
    )

    # --------------------------------------------------------
    # Certificate
    # --------------------------------------------------------

    save_json(
        certificate,
        certificates / CERTIFICATE_FILE,
    )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    print()

    print("=" * 60)
    print("GER")
    print("L3.1 — GLOBAL CORRELATION ANALYSIS")
    print("=" * 60)

    print_dashboard(summary)

    print()

    print("STATISTICS")

    print("-" * 60)

    for method in METHODS:

        s = statistics[method]

        print(method.upper())

        print(f"Pairs               : {s['pairs']}")
        print(f"Maximum             : {s['maximum']:.6f}")
        print(f"Minimum             : {s['minimum']:.6f}")
        print(f"Mean                : {s['mean']:.6f}")
        print(f"Median              : {s['median']:.6f}")
        print(f"Std                 : {s['std']:.6f}")
        print(f"Strong Positive     : {s['strong_positive']}")
        print(f"Strong Negative     : {s['strong_negative']}")
        print(f"Weak                : {s['weak']}")

        print()

    print("=" * 60)
    print("Experiment completed.")
    print("=" * 60)

    print()

    print("Results saved to:")

    print(output.resolve())

    print()

    return {

        "summary": summary,

        "statistics": statistics,

        "certificate": certificate,

        "results": results,

    }


# ============================================================
# Main
# ============================================================

def main():

    OUTPUT = "RESULTS/L3_1_E1"

    run_experiment(

        output_folder=OUTPUT,

    )

# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    main()
