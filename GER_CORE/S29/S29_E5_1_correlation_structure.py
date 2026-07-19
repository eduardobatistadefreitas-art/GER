#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==========================================================================
GER
S29-E5.1
Correlation Structure of the Stability Region Space
==========================================================================

Objective
---------
Construct the complete correlation structure of the Stability Region Space,
identifying:

    • Independent observables
    • Redundant observables
    • Linear correlations
    • Monotonic correlations
    • Nonlinear dependencies
    • Observable families

Input
-----
GER_CORE/S29/geometric_database/
    region_database/

Outputs
-------
GER_RESULTS/S29_E5.1/

Author
------
GER Scientific Framework
"""

import os
import json
import shutil
import warnings

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from scipy.stats import spearmanr

from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram

from scipy.spatial.distance import squareform

from sklearn.feature_selection import mutual_info_regression

warnings.filterwarnings("ignore")

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = "/content/GER"

DATABASE = os.path.join(
    PROJECT_ROOT,
    "GER_CORE",
    "S29",
    "geometric_database"
)

REGION_DATABASE = os.path.join(
    DATABASE,
    "region_database"
)

RESULTS = "/content/drive/MyDrive/GER_RESULTS/S29_E5.1"

os.makedirs(RESULTS, exist_ok=True)

# ============================================================
# FILES
# ============================================================

FILES = {

    "local_geometry":
        os.path.join(
            REGION_DATABASE,
            "local_geometry.csv"
        ),

    "comparison":
        os.path.join(
            REGION_DATABASE,
            "comparison.csv"
        ),

    "global_geometry":
        os.path.join(
            REGION_DATABASE,
            "global_geometry.json"
        ),

    "mst_statistics":
        os.path.join(
            REGION_DATABASE,
            "mst_statistics.json"
        ),

    "mst_topology":
        os.path.join(
            REGION_DATABASE,
            "mst_topology.json"
        ),

    "consensus_topology":
        os.path.join(
            REGION_DATABASE,
            "consensus_topology.json"
        )

}

# ============================================================
# PRINT
# ============================================================

def line():

    print("=" * 70)


def header():

    line()

    print("GER")

    print("S29-E5.1")

    print("Correlation Structure of the Stability Region Space")

    line()

# ============================================================
# VALIDATION
# ============================================================

def validate_database():

    print()

    print("Checking database...")

    missing = []

    for key, path in FILES.items():

        if os.path.exists(path):

            print(f"[OK] {key}")

        else:

            print(f"[ERROR] {key}")

            missing.append(path)

    if len(missing) > 0:

        print()

        print("Missing required database files:")

        for f in missing:

            print(f)

        raise FileNotFoundError()

# ============================================================
# LOADERS
# ============================================================

def load_csv(path):

    return pd.read_csv(path)


def load_json(path):

    with open(path, "r") as f:

        return json.load(f)

# ============================================================
# BUILD TABLE
# ============================================================

def build_observable_table():

    """
    Creates one unified table containing all numerical
    observables available for each Stability Region.
    """

    print()

    print("Loading region database...")

    local = load_csv(FILES["local_geometry"])

    comparison = load_csv(FILES["comparison"])

    global_geometry = load_json(FILES["global_geometry"])

    mst_statistics = load_json(FILES["mst_statistics"])

    mst_topology = load_json(FILES["mst_topology"])

    consensus_topology = load_json(FILES["consensus_topology"])

    df = local.copy()

    # -------------------------------------------------------

    if "Backbone" in comparison.columns:

        comparison = comparison.drop(columns=["Backbone"])

    # merge if possible

    common = list(

        set(df.columns)

        &

        set(comparison.columns)

    )

    if "Region" in comparison.columns:

        common = ["Region"]

    if len(common) > 0:

        df = df.merge(

            comparison,

            on=common,

            how="left"

        )

    # -------------------------------------------------------
    # Append global scalar metrics
    # -------------------------------------------------------

    scalar_values = {}

    for key, value in global_geometry.items():

        if isinstance(value, (int, float)):

            scalar_values[f"global_{key}"] = value

    for key, value in mst_statistics.items():

        if isinstance(value, (int, float)):

            scalar_values[f"mst_{key}"] = value

    for key, value in mst_topology.items():

        if isinstance(value, (int, float)):

            scalar_values[f"mstTopology_{key}"] = value

    for key, value in consensus_topology.items():

        if isinstance(value, (int, float)):

            scalar_values[f"consensusTopology_{key}"] = value

    for key, value in scalar_values.items():

        df[key] = value

    print()

    print(f"Regions loaded : {len(df)}")

    print(f"Columns loaded : {len(df.columns)}")

    output = os.path.join(

        RESULTS,

        "correlation_table.csv"

    )

    df.to_csv(

        output,

        index=False

    )

    return df

# ============================================================
# DATA VALIDATION
# ============================================================

def validate_dataframe(df):

    report = []

    report.append("DATA VALIDATION REPORT")
    report.append("")

    report.append(f"Rows    : {len(df)}")
    report.append(f"Columns : {len(df.columns)}")
    report.append("")

    numeric = df.select_dtypes(include=np.number)

    report.append(
        f"Numeric variables : {len(numeric.columns)}"
    )

    report.append("")

    # ------------------------------------------

    nan_columns = []

    inf_columns = []

    constant_columns = []

    empty_columns = []

    for column in numeric.columns:

        values = numeric[column].values

        if np.isnan(values).any():

            nan_columns.append(column)

        if np.isinf(values).any():

            inf_columns.append(column)

        if len(np.unique(values)) == 1:

            constant_columns.append(column)

        if np.all(pd.isna(values)):

            empty_columns.append(column)

    report.append(
        f"NaN columns : {len(nan_columns)}"
    )

    report.append(
        f"Infinite columns : {len(inf_columns)}"
    )

    report.append(
        f"Constant columns : {len(constant_columns)}"
    )

    report.append(
        f"Empty columns : {len(empty_columns)}"
    )

    report.append("")

    if len(nan_columns):

        report.append("NaN")

        report.extend(nan_columns)

        report.append("")

    if len(inf_columns):

        report.append("Infinite")

        report.extend(inf_columns)

        report.append("")

    if len(constant_columns):

        report.append("Constant")

        report.extend(constant_columns)

        report.append("")

    if len(empty_columns):

        report.append("Empty")

        report.extend(empty_columns)

        report.append("")

    with open(

        os.path.join(

            RESULTS,

            "validation_report.txt"

        ),

        "w"

    ) as f:

        f.write("\n".join(report))

    return numeric

# ============================================================
# SUMMARY STATISTICS
# ============================================================

def compute_statistics(numeric):

    print()

    print("Computing summary statistics...")

    rows = []

    for column in numeric.columns:

        values = numeric[column].dropna()

        if len(values) == 0:
            continue

        mean = values.mean()
        median = values.median()
        std = values.std()
        var = values.var()

        if abs(mean) > 1e-12:
            cv = std / abs(mean)
        else:
            cv = np.nan

        rows.append({

            "Observable": column,
            "Mean": mean,
            "Median": median,
            "Std": std,
            "Variance": var,
            "CoefficientVariation": cv,
            "Minimum": values.min(),
            "Maximum": values.max()

        })

    statistics = pd.DataFrame(rows)

    statistics.to_csv(

        os.path.join(
            RESULTS,
            "observable_statistics.csv"
        ),

        index=False

    )

    return statistics


# ============================================================
# PEARSON MATRIX
# ============================================================

def compute_pearson_matrix(numeric):

    print()

    print("Computing Pearson correlation matrix...")

    columns = list(numeric.columns)

    matrix = np.zeros(

        (len(columns), len(columns))

    )

    for i in range(len(columns)):

        for j in range(len(columns)):

            x = numeric[columns[i]]

            y = numeric[columns[j]]

            valid = (

                (~x.isna())
                &
                (~y.isna())

            )

            if valid.sum() < 2:

                value = np.nan

            else:

                try:

                    value = pearsonr(

                        x[valid],

                        y[valid]

                    )[0]

                except Exception:

                    value = np.nan

            matrix[i, j] = value

    pearson = pd.DataFrame(

        matrix,

        columns=columns,

        index=columns

    )

    pearson.to_csv(

        os.path.join(

            RESULTS,

            "pearson_matrix.csv"

        )

    )

    return pearson


# ============================================================
# SPEARMAN MATRIX
# ============================================================

def compute_spearman_matrix(numeric):

    print()

    print("Computing Spearman correlation matrix...")

    columns = list(numeric.columns)

    matrix = np.zeros(

        (len(columns), len(columns))

    )

    for i in range(len(columns)):

        for j in range(len(columns)):

            x = numeric[columns[i]]

            y = numeric[columns[j]]

            valid = (

                (~x.isna())

                &

                (~y.isna())

            )

            if valid.sum() < 2:

                value = np.nan

            else:

                try:

                    value = spearmanr(

                        x[valid],

                        y[valid]

                    )[0]

                except Exception:

                    value = np.nan

            matrix[i, j] = value

    spearman = pd.DataFrame(

        matrix,

        columns=columns,

        index=columns

    )

    spearman.to_csv(

        os.path.join(

            RESULTS,

            "spearman_matrix.csv"

        )

    )

    return spearman


# ============================================================
# HEATMAP
# ============================================================

def draw_heatmap(

    matrix,

    title,

    filename

):

    print(

        f"Generating {filename}..."

    )

    plt.figure(

        figsize=(14, 12)

    )

    image = plt.imshow(

        matrix,

        interpolation="nearest",

        aspect="auto"

    )

    plt.colorbar(image)

    plt.xticks(

        np.arange(len(matrix.columns)),

        matrix.columns,

        rotation=90,

        fontsize=8

    )

    plt.yticks(

        np.arange(len(matrix.columns)),

        matrix.columns,

        fontsize=8

    )

    plt.title(title)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            RESULTS,

            filename

        ),

        dpi=300

    )

    plt.close()


# ============================================================
# MUTUAL INFORMATION
# ============================================================

def compute_mutual_information(numeric):

    print()

    print("Computing mutual information matrix...")

    columns = list(numeric.columns)

    matrix = np.zeros(

        (len(columns), len(columns))

    )

    for i in range(len(columns)):

        X = numeric[[columns[i]]].fillna(0)

        for j in range(len(columns)):

            y = numeric[columns[j]].fillna(0)

            try:

                value = mutual_info_regression(

                    X,

                    y,

                    random_state=42

                )[0]

            except Exception:

                value = np.nan

            matrix[i, j] = value

    mi = pd.DataFrame(

        matrix,

        columns=columns,

        index=columns

    )

    mi.to_csv(

        os.path.join(

            RESULTS,

            "mutual_information.csv"

        )

    )

    return mi

# ============================================================
# HIERARCHICAL CLUSTERING
# ============================================================

def hierarchical_clustering(pearson_matrix):

    print()

    print("Computing hierarchical clustering...")

    corr = pearson_matrix.fillna(0).values

    distance = 1.0 - np.abs(corr)

    np.fill_diagonal(distance, 0.0)

    condensed = squareform(

        distance,

        checks=False

    )

    linkage_matrix = linkage(

        condensed,

        method="average"

    )

    plt.figure(

        figsize=(14, 8)

    )

    dendrogram(

        linkage_matrix,

        labels=list(pearson_matrix.columns),

        leaf_rotation=90,

        leaf_font_size=8

    )

    plt.title(

        "Observable Hierarchical Clustering"

    )

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            RESULTS,

            "observable_dendrogram.png"

        ),

        dpi=300

    )

    plt.close()

    return linkage_matrix


# ============================================================
# REDUNDANCY ANALYSIS
# ============================================================

def redundancy_analysis(

    pearson,

    spearman,

    threshold=0.95

):

    print()

    print("Detecting redundant observables...")

    observables = list(

        pearson.columns

    )

    report = []

    report.append(

        "REDUNDANCY REPORT"

    )

    report.append("")

    redundant_pairs = []

    for i in range(len(observables)):

        for j in range(i + 1, len(observables)):

            p = pearson.iloc[i, j]

            s = spearman.iloc[i, j]

            if (

                abs(p) >= threshold

                or

                abs(s) >= threshold

            ):

                redundant_pairs.append(

                    (

                        observables[i],

                        observables[j],

                        p,

                        s

                    )

                )

    if len(redundant_pairs) == 0:

        report.append(

            "No redundant variables detected."

        )

    else:

        for a, b, p, s in redundant_pairs:

            report.append(

                f"{a}"

            )

            report.append(

                f"    <-> {b}"

            )

            report.append(

                f"    Pearson : {p:.6f}"

            )

            report.append(

                f"    Spearman: {s:.6f}"

            )

            report.append("")

    with open(

        os.path.join(

            RESULTS,

            "redundancy_report.txt"

        ),

        "w"

    ) as f:

        f.write(

            "\n".join(report)

        )

    return redundant_pairs


# ============================================================
# INDEPENDENT OBSERVABLES
# ============================================================

def independent_observables(

    pearson,

    redundant_pairs,

    threshold=0.95

):

    print()

    print("Selecting independent observables...")

    observables = list(

        pearson.columns

    )

    removed = set()

    rows = []

    for a, b, _, _ in redundant_pairs:

        if b not in removed:

            removed.add(b)

            rows.append({

                "Representative": a,
                "Removed": b

            })

    independent = [

        o

        for o in observables

        if o not in removed

    ]

    independent_df = pd.DataFrame({

        "Observable": independent

    })

    independent_df.to_csv(

        os.path.join(

            RESULTS,

            "independent_observables.csv"

        ),

        index=False

    )

    mapping = pd.DataFrame(rows)

    mapping.to_csv(

        os.path.join(

            RESULTS,

            "observable_reduction_map.csv"

        ),

        index=False

    )

    return independent


# ============================================================
# SUMMARY
# ============================================================

def write_summary(

    numeric,

    pearson,

    spearman,

    mi,

    independent,

    redundant_pairs

):

    print()

    print("Writing summary...")

    abs_pearson = np.abs(

        pearson.values.copy()

    )

    np.fill_diagonal(

        abs_pearson,

        np.nan

    )

    p_index = np.nanargmax(

        abs_pearson

    )

    i, j = np.unravel_index(

        p_index,

        abs_pearson.shape

    )

    pearson_pair = (

        pearson.columns[i],

        pearson.columns[j],

        pearson.iloc[i, j]

    )

    abs_spearman = np.abs(

        spearman.values.copy()

    )

    np.fill_diagonal(

        abs_spearman,

        np.nan

    )

    s_index = np.nanargmax(

        abs_spearman

    )

    i2, j2 = np.unravel_index(

        s_index,

        abs_spearman.shape

    )

    spearman_pair = (

        spearman.columns[i2],

        spearman.columns[j2],

        spearman.iloc[i2, j2]

    )

    mi_values = mi.values.copy()

    np.fill_diagonal(

        mi_values,

        np.nan

    )

    mi_index = np.nanargmax(

        mi_values

    )

    i3, j3 = np.unravel_index(

        mi_index,

        mi_values.shape

    )

    mi_pair = (

        mi.columns[i3],

        mi.columns[j3],

        mi.iloc[i3, j3]

    )

    report = []

    report.append(

        "GER S29-E5.1"

    )

    report.append("")

    report.append(

        f"Regions : {len(numeric)}"

    )

    report.append(

        f"Observables : {len(numeric.columns)}"

    )

    report.append("")

    report.append(

        f"Independent observables : {len(independent)}"

    )

    report.append(

        f"Redundant pairs : {len(redundant_pairs)}"

    )

    report.append("")

    report.append(

        "Highest Pearson correlation"

    )

    report.append(

        f"{pearson_pair[0]} <-> {pearson_pair[1]}"

    )

    report.append(

        f"{pearson_pair[2]:.6f}"

    )

    report.append("")

    report.append(

        "Highest Spearman correlation"

    )

    report.append(

        f"{spearman_pair[0]} <-> {spearman_pair[1]}"

    )

    report.append(

        f"{spearman_pair[2]:.6f}"

    )

    report.append("")

    report.append(

        "Highest Mutual Information"

    )

    report.append(

        f"{mi_pair[0]} <-> {mi_pair[1]}"

    )

    report.append(

        f"{mi_pair[2]:.6f}"

    )

    with open(

        os.path.join(

            RESULTS,

            "summary.txt"

        ),

        "w"

    ) as f:

        f.write(

            "\n".join(report)

        )
# ============================================================
# METRICS SUMMARY
# ============================================================

def save_metrics_summary(
    numeric,
    independent,
    redundant_pairs
):

    metrics = {

        "regions": int(len(numeric)),
        "observables": int(len(numeric.columns)),
        "independent_observables": int(len(independent)),
        "redundant_pairs": int(len(redundant_pairs))

    }

    with open(

        os.path.join(

            RESULTS,

            "metrics_summary.json"

        ),

        "w"

    ) as f:

        json.dump(

            metrics,

            f,

            indent=4

        )


# ============================================================
# MAIN
# ============================================================

def main():

    header()

    validate_database()

    df = build_observable_table()

    numeric = validate_dataframe(df)

    compute_statistics(numeric)

    pearson = compute_pearson_matrix(numeric)

    spearman = compute_spearman_matrix(numeric)

    draw_heatmap(

        pearson,

        "Pearson Correlation Matrix",

        "pearson_heatmap.png"

    )

    draw_heatmap(

        spearman,

        "Spearman Correlation Matrix",

        "spearman_heatmap.png"

    )

    mi = compute_mutual_information(numeric)

    draw_heatmap(

        mi,

        "Mutual Information Matrix",

        "mutual_information_heatmap.png"

    )

    hierarchical_clustering(

        pearson

    )

    redundant_pairs = redundancy_analysis(

        pearson,

        spearman

    )

    independent = independent_observables(

        pearson,

        redundant_pairs

    )

    write_summary(

        numeric,

        pearson,

        spearman,

        mi,

        independent,

        redundant_pairs

    )

    save_metrics_summary(

        numeric,

        independent,

        redundant_pairs

    )

    print()

    line()

    print("Analysis completed successfully.")

    print()

    print("Results saved to:")

    print(RESULTS)

    line()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
