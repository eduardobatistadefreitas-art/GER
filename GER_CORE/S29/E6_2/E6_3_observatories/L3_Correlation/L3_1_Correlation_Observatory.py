"""
============================================================
GER
S29 - E6.3

L3.1 - Correlation Observatory

Observational Layer

This experiment characterizes the complete correlation
structure of the Geometric Signature Space.

Input
-----
Workspace
    signatures

Output
------
correlation_matrix.csv
covariance_matrix.csv
absolute_correlation.csv
pair_correlation_ranking.csv
pair_strength.csv
independent_pairs.csv
redundant_pairs.csv
correlation_statistics.json
correlation_certificate.json
correlation_certificate.txt

============================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .L3_0_Workspace_Manager import WorkspaceManager


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_FOLDER = "L3_1_Correlation"

CORRELATION_FIELDS = [

    "diameter",
    "convergence",
    "recurrence",
    "drift",

]

PAIR_THRESHOLDS = {

    "Very Strong": 0.90,
    "Strong": 0.70,
    "Moderate": 0.50,
    "Weak": 0.30,
    "Negligible": 0.00,

}


# ============================================================
# HELPERS
# ============================================================

def banner():

    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.1 - Correlation Observatory")
    print("=" * 60)
    print()


def classify_strength(value: float) -> str:

    value = abs(float(value))

    if value >= PAIR_THRESHOLDS["Very Strong"]:
        return "Very Strong"

    if value >= PAIR_THRESHOLDS["Strong"]:
        return "Strong"

    if value >= PAIR_THRESHOLDS["Moderate"]:
        return "Moderate"

    if value >= PAIR_THRESHOLDS["Weak"]:
        return "Weak"

    return "Negligible"


# ============================================================
# LOAD SIGNATURES
# ============================================================

def load_signatures(workspace):

    print("Loading signatures...")

    df = workspace.load("signatures")

    df = df[CORRELATION_FIELDS].copy()

    print(f"Rows : {len(df):,}")
    print(f"Cols : {len(df.columns)}")
    print()

    return df


# ============================================================
# CORRELATION MATRICES
# ============================================================

def compute_matrices(df):

    correlation = df.corr(
        method="pearson",
        numeric_only=True,
    )

    covariance = df.cov(
        numeric_only=True,
    )

    absolute = correlation.abs()

    return correlation, covariance, absolute


# ============================================================
# PAIR TABLE
# ============================================================

def build_pair_table(correlation):

    rows = []

    columns = list(correlation.columns)

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            a = columns[i]
            b = columns[j]

            value = float(correlation.loc[a, b])

            rows.append(

                {

                    "observable_1": a,
                    "observable_2": b,
                    "correlation": value,
                    "absolute_correlation": abs(value),
                    "strength": classify_strength(value),

                }

            )

    table = pd.DataFrame(rows)

    return table

# ============================================================
# GLOBAL STATISTICS
# ============================================================

def compute_statistics(pair_table):

    values = pair_table["correlation"].to_numpy()
    abs_values = np.abs(values)

    statistics = {
        "number_of_observables": int(len(CORRELATION_FIELDS)),
        "number_of_pairs": int(len(pair_table)),
        "maximum_correlation": float(values.max()),
        "minimum_correlation": float(values.min()),
        "maximum_absolute_correlation": float(abs_values.max()),
        "minimum_absolute_correlation": float(abs_values.min()),
        "mean_correlation": float(values.mean()),
        "mean_absolute_correlation": float(abs_values.mean()),
        "median_correlation": float(np.median(values)),
        "median_absolute_correlation": float(np.median(abs_values)),
        "std_correlation": float(values.std()),
        "std_absolute_correlation": float(abs_values.std()),
    }

    return statistics


# ============================================================
# RANKINGS
# ============================================================

def build_rankings(pair_table):

    correlation_ranking = (
        pair_table
        .sort_values("absolute_correlation", ascending=False)
        .reset_index(drop=True)
    )

    independent_pairs = (
        pair_table
        .sort_values("absolute_correlation", ascending=True)
        .reset_index(drop=True)
    )

    redundant_pairs = (
        pair_table
        .sort_values("absolute_correlation", ascending=False)
        .reset_index(drop=True)
    )

    return (
        correlation_ranking,
        independent_pairs,
        redundant_pairs,
    )


# ============================================================
# CERTIFICATE
# ============================================================

def build_certificate(pair_table, statistics):

    strongest = (
        pair_table
        .sort_values("absolute_correlation", ascending=False)
        .iloc[0]
    )

    weakest = (
        pair_table
        .sort_values("absolute_correlation", ascending=True)
        .iloc[0]
    )

    strength_count = (
        pair_table["strength"]
        .value_counts()
        .to_dict()
    )

    certificate = {
        "number_of_observables": statistics["number_of_observables"],
        "number_of_pairs": statistics["number_of_pairs"],
        "average_absolute_correlation": statistics["mean_absolute_correlation"],
        "maximum_absolute_correlation": statistics["maximum_absolute_correlation"],
        "minimum_absolute_correlation": statistics["minimum_absolute_correlation"],
        "strongest_pair": {
            "observable_1": strongest["observable_1"],
            "observable_2": strongest["observable_2"],
            "correlation": float(strongest["correlation"]),
        },
        "weakest_pair": {
            "observable_1": weakest["observable_1"],
            "observable_2": weakest["observable_2"],
            "correlation": float(weakest["correlation"]),
        },
        "strength_distribution": strength_count,
    }

    return certificate

# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    workspace,
    correlation,
    covariance,
    absolute,
    pair_ranking,
    independent_pairs,
    redundant_pairs,
    statistics,
    certificate,
):

    output = workspace.create_output_folder(OUTPUT_FOLDER)

    correlation.to_csv(
        output / "correlation_matrix.csv",
        index=True,
    )

    covariance.to_csv(
        output / "covariance_matrix.csv",
        index=True,
    )

    absolute.to_csv(
        output / "absolute_correlation.csv",
        index=True,
    )

    pair_ranking.to_csv(
        output / "pair_correlation_ranking.csv",
        index=False,
    )

    pair_ranking[
        [
            "observable_1",
            "observable_2",
            "strength",
        ]
    ].to_csv(
        output / "pair_strength.csv",
        index=False,
    )

    independent_pairs.to_csv(
        output / "independent_pairs.csv",
        index=False,
    )

    redundant_pairs.to_csv(
        output / "redundant_pairs.csv",
        index=False,
    )

    with open(
        output / "correlation_statistics.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            statistics,
            f,
            indent=4,
        )

    with open(
        output / "correlation_certificate.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            certificate,
            f,
            indent=4,
        )

    with open(
        output / "correlation_certificate.txt",
        "w",
        encoding="utf-8",
    ) as f:

        f.write("GER\n")
        f.write("S29 - E6.3\n")
        f.write("L3.1 - Correlation Observatory\n\n")

        f.write(
            f"Number of observables : {certificate['number_of_observables']}\n"
        )

        f.write(
            f"Number of pairs       : {certificate['number_of_pairs']}\n"
        )

        f.write(
            f"Average |ρ|           : {certificate['average_absolute_correlation']:.6f}\n"
        )

        f.write(
            f"Maximum |ρ|           : {certificate['maximum_absolute_correlation']:.6f}\n"
        )

        f.write(
            f"Minimum |ρ|           : {certificate['minimum_absolute_correlation']:.6f}\n\n"
        )

        pair = certificate["strongest_pair"]

        f.write("Strongest pair\n")
        f.write(
            f"    {pair['observable_1']} × {pair['observable_2']}\n"
        )
        f.write(
            f"    correlation = {pair['correlation']:.6f}\n\n"
        )

        pair = certificate["weakest_pair"]

        f.write("Weakest pair\n")
        f.write(
            f"    {pair['observable_1']} × {pair['observable_2']}\n"
        )
        f.write(
            f"    correlation = {pair['correlation']:.6f}\n\n"
        )

        f.write("Strength distribution\n")

        for key, value in certificate["strength_distribution"].items():

            f.write(f"    {key:<15} : {value}\n")

    print()
    print("=" * 60)
    print("Results")
    print("=" * 60)
    print(output)
    print()

    print("Generated")
    print("   correlation_matrix.csv")
    print("   covariance_matrix.csv")
    print("   absolute_correlation.csv")
    print("   pair_correlation_ranking.csv")
    print("   pair_strength.csv")
    print("   independent_pairs.csv")
    print("   redundant_pairs.csv")
    print("   correlation_statistics.json")
    print("   correlation_certificate.json")
    print("   correlation_certificate.txt")
    print()

# ============================================================
# MAIN
# ============================================================

def main():

    banner()

    workspace = WorkspaceManager()

    workspace.load_workspace()



    signatures = load_signatures(

        workspace

    )



    correlation, covariance, absolute = (

        compute_matrices(

            signatures

        )

    )



    pair_table = build_pair_table(

        correlation

    )



    statistics = compute_statistics(

        pair_table

    )



    (

        pair_ranking,

        independent_pairs,

        redundant_pairs,

    ) = build_rankings(

        pair_table

    )



    certificate = build_certificate(

        pair_table,

        statistics,

    )



    save_results(

        workspace,

        correlation,

        covariance,

        absolute,

        pair_ranking,

        independent_pairs,

        redundant_pairs,

        statistics,

        certificate,

    )



    print("=" * 60)

    print("Experiment completed.")

    print("=" * 60)

    print()



if __name__ == "__main__":

    main()
