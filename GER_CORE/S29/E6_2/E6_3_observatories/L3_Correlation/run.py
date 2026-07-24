"""
============================================================
GER

L3.1 Correlation Matrix

Main Runner

============================================================
"""

from pathlib import Path

from .correlation_observatory.analysis import (
    run_analysis,
    validate_results,
    build_summary,
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

from .correlation_observatory.io import (
    load_csv,
    save_csv,
    save_json,
)

from .correlation_observatory.config import *


# ============================================================
# Runner
# ============================================================

def run(dataset_file, output_folder):

    output = Path(output_folder)

    tables = output / TABLE_FOLDER
    json_dir = output / JSON_FOLDER
    report_dir = output / REPORT_FOLDER
    certificate_dir = output / CERTIFICATE_FOLDER

    df = load_csv(dataset_file)

    results = run_analysis(df)

    validate_results(results)

    summary = build_summary(results)

    certificate = build_certificate(results)

    # ========================================================
    # Export matrices
    # ========================================================

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

    # ========================================================
    # Export tables
    # ========================================================

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

    # ========================================================
    # JSON
    # ========================================================

    save_json(
        summary,
        json_dir / SUMMARY_JSON,
    )

    # ========================================================
    # Report
    # ========================================================

    write_report(
        summary,
        report_dir / REPORT_FILE,
    )

    # ========================================================
    # Certificate
    # ========================================================

    save_json(
        certificate,
        certificate_dir / CERTIFICATE_FILE,
    )

    # ========================================================
    # Dashboard
    # ========================================================

    print_dashboard(summary)

    return results


# ============================================================
# Main
# ============================================================

def main():

    DATASET = "observables.csv"

    OUTPUT = "RESULTS"

    run(

        DATASET,

        OUTPUT,

    )


if __name__ == "__main__":

    main()
