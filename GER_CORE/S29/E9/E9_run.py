"""
=============================================================
S29_E9/run.py
=============================================================

Trajectory Relaxation Analysis

Main execution pipeline.

=============================================================
"""

from __future__ import annotations

from pathlib import Path

from .config import (
    EXPERIMENT_NAME,
    AVAILABLE_OBSERVABLES,
)

from .io import (
    load_dataset,
    prepare_output_directory,
    save_json,
)

from .fitting import (
    fit_all_models,
)

from .selection import (
    select_best_model,
    selection_summary,
)

from .statistics import (
    analyze_all_models,
)

from .dashboard import (
    build_dashboard,
)

from .report import (
    build_report,
)


# ============================================================
# Data Loading
# ============================================================

def load_experiment(
    input_file,
):
    """
    Load experimental dataset.
    """

    return load_dataset(

        input_file

    )


# ============================================================
# Model Fitting
# ============================================================

def execute_fitting(
    x,
    y,
):
    """
    Fit all registered models.
    """

    return fit_all_models(

        x,

        y,

    )


# ============================================================
# Statistical Analysis
# ============================================================

def execute_statistics(
    fit_results,
):
    """
    Analyze all fitted models.
    """

    return analyze_all_models(

        fit_results

    )


# ============================================================
# Model Selection
# ============================================================

def execute_selection(
    fit_results,
):
    """
    Select best model.
    """

    best = select_best_model(

        fit_results

    )

    summary = selection_summary(

        fit_results

    )

    return best, summary


# ============================================================
# Output Builders
# ============================================================

def build_outputs(
    fit_results,
):
    """
    Generate dashboard and report.
    """

    dashboard = build_dashboard(

        fit_results

    )

    report = build_report(

        fit_results

    )

    return dashboard, report

# ============================================================
# Main Pipeline
# ============================================================

def run_experiment(
    input_file,
):
    """
    Execute the complete experiment.
    """

    # --------------------------------------------------------
    # Load trajectory
    # --------------------------------------------------------

    data = load_experiment(

        input_file

    )

    x = data["sigma"]

    experiment_results = {}

    # --------------------------------------------------------
    # Analyze every observable
    # --------------------------------------------------------

    for observable in AVAILABLE_OBSERVABLES:

        print(

            f"Processing {observable}..."

        )

        y = data[observable]

        # ----------------------------------------------
        # Fit
        # ----------------------------------------------

        fit_results = execute_fitting(

            x,

            y,

        )

        # ----------------------------------------------
        # Statistics
        # ----------------------------------------------

        statistics = execute_statistics(

            fit_results

        )

        # ----------------------------------------------
        # Selection
        # ----------------------------------------------

        best_model, summary = execute_selection(

            fit_results

        )

        # ----------------------------------------------
        # Dashboard / Report
        # ----------------------------------------------

        dashboard, report = build_outputs(

            fit_results

        )

        experiment_results[observable] = {

            "best_model": best_model,

            "summary": summary,

            "statistics": statistics,

            "dashboard": dashboard,

            "report": report,

        }

    return experiment_results

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    data = load_experiment(

        input_file

    )

    x = data["x"]

    y = data["y"]

    # --------------------------------------------------------
    # Fit models
    # --------------------------------------------------------

    fit_results = execute_fitting(

        x,

        y,

    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    statistics = execute_statistics(

        fit_results

    )

    # --------------------------------------------------------
    # Selection
    # --------------------------------------------------------

    best_model, summary = execute_selection(

        fit_results

    )

    # --------------------------------------------------------
    # Build outputs
    # --------------------------------------------------------

    dashboard, report = build_outputs(

        fit_results

    )

    return {

        "best_model": best_model,

        "summary": summary,

        "statistics": statistics,

        "dashboard": dashboard,

        "report": report,

    }


# ============================================================
# Save Results
# ============================================================

def save_results(
    results,
    output_directory,
):
    """
    Save experiment outputs.
    """

    output_directory = prepare_output_directory(

        output_directory

    )

    save_json(

        results["dashboard"],

        Path(output_directory)

        / "dashboard.json",

    )

    save_json(

        results["summary"],

        Path(output_directory)

        / "summary.json",

    )

    report_path = (

        Path(output_directory)

        / "report.txt"

    )

    with open(

        report_path,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            results["report"]

        )

    return output_directory


# ============================================================
# Public Entry Point
# ============================================================

def run(
    input_file,
    output_directory,
):
    """
    Execute and save the experiment.
    """

    results = run_experiment(

        input_file

    )

    save_results(

        results,

        output_directory,

    )

    return results


# ============================================================
# Script Entry
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 60)

    print(EXPERIMENT_NAME)

    print("Trajectory Relaxation Analysis")

    print("=" * 60)

    print()

    INPUT_FILE = (
        "/content/drive/MyDrive/GER_RESULTS/"
        "S29/S29_E8/20260728_170754/trajectory.csv"
    )

    OUTPUT_DIRECTORY = (
        "/content/drive/MyDrive/GER_RESULTS/S29/S29_E9"
    )

    run(

        INPUT_FILE,

        OUTPUT_DIRECTORY,

    )
    
# ============================================================
# Public API
# ============================================================

__all__ = [

    "load_experiment",

    "execute_fitting",

    "execute_statistics",

    "execute_selection",

    "build_outputs",

    "run_experiment",

    "save_results",

    "run",

]
