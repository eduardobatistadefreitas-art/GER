"""
============================================================
GER

L3.1 Correlation Matrix

Analysis

============================================================
"""

from __future__ import annotations

from ...statistics.correlation import (

    clean_dataframe,

    pearson_matrix,

    spearman_matrix,

    kendall_matrix,

    correlation_table,

    correlation_summary,

)


# ============================================================
# Individual Analysis
# ============================================================

def compute_method(df, method):
    """
    Compute a single correlation method.
    """

    method = method.lower()

    if method == "pearson":

        matrix = pearson_matrix(df)

    elif method == "spearman":

        matrix = spearman_matrix(df)

    elif method == "kendall":

        matrix = kendall_matrix(df)

    else:

        raise ValueError(
            f"Unsupported method: {method}"
        )

    table = correlation_table(matrix)

    summary = correlation_summary(matrix)

    return {

        "matrix": matrix,

        "table": table,

        "summary": summary,

    }


# ============================================================
# Complete Analysis
# ============================================================

def run_analysis(df):
    """
    Execute the complete correlation analysis.
    """

    df = clean_dataframe(df)

    results = {

        "variables": list(df.columns),

        "n_variables": len(df.columns),

        "n_samples": len(df),

        "pearson":
            compute_method(
                df,
                "pearson",
            ),

        "spearman":
            compute_method(
                df,
                "spearman",
            ),

        "kendall":
            compute_method(
                df,
                "kendall",
            ),

    }

    return results


# ============================================================
# Validation
# ============================================================

def validate_results(results):
    """
    Validate consistency between correlation methods.
    """

    variables = results["variables"]

    n = len(variables)

    for method in (

        "pearson",

        "spearman",

        "kendall",

    ):

        matrix = results[method]["matrix"]

        if matrix.shape != (n, n):

            raise ValueError(

                f"{method}: invalid matrix dimensions."

            )

        if list(matrix.columns) != variables:

            raise ValueError(

                f"{method}: variable order mismatch."

            )

        if list(matrix.index) != variables:

            raise ValueError(

                f"{method}: index order mismatch."

            )

    return True


# ============================================================
# Global Summary
# ============================================================

def build_summary(results):
    """
    Build experiment summary.
    """

    return {

        "variables":

            results["n_variables"],

        "samples":

            results["n_samples"],

        "methods": [

            "pearson",

            "spearman",

            "kendall",

        ],

        "pearson":

            results["pearson"]["summary"],

        "spearman":

            results["spearman"]["summary"],

        "kendall":

            results["kendall"]["summary"],

    }
