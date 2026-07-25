"""
GER
S29 - E6.3

L3.3 - Rank Correlation Observatory
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd

from scipy.stats import (
    pearsonr,
    spearmanr,
    kendalltau,
)

from GER_CORE.S29.E6_2.E6_3_observatories.L3_Correlation.L3_0_Workspace_Manager import (
    Workspace,
)

# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29_E6.3/L3_3_Rank_Correlation"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATASET_NAME = "signatures"

OBSERVABLES = [

    "diameter",
    "convergence",
    "recurrence",
    "drift",

]

# ============================================================
# LOAD DATA
# ============================================================

def load_signatures(workspace):

    """
    Carrega todas as assinaturas
    do Workspace.
    """

    frames = []

    total_rows = 0

    for chunk in workspace.iter_chunks(DATASET_NAME):

        frames.append(chunk)

        total_rows += len(chunk)

    if not frames:

        raise RuntimeError(

            "No signatures found."

        )

    df = pd.concat(

        frames,

        ignore_index=True,

    )

    df = df[OBSERVABLES].copy()

    return df, total_rows


# ============================================================
# OBSERVABLE PAIRS
# ============================================================

def observable_pairs():

    pairs = []

    n = len(OBSERVABLES)

    for i in range(n):

        for j in range(i + 1, n):

            pairs.append(

                (

                    OBSERVABLES[i],

                    OBSERVABLES[j],

                )

            )

    return pairs


# ============================================================
# EMPTY MATRICES
# ============================================================

def empty_matrix():

    return pd.DataFrame(

        np.eye(

            len(OBSERVABLES)

        ),

        index=OBSERVABLES,

        columns=OBSERVABLES,

        dtype=float,

    )


# ============================================================
# CORRELATION STRENGTH
# ============================================================

def correlation_strength(r):

    value = abs(r)

    if value >= 0.90:

        return "Very Strong"

    if value >= 0.70:

        return "Strong"

    if value >= 0.50:

        return "Moderate"

    if value >= 0.30:

        return "Weak"

    return "Negligible"


# ============================================================
# METHOD CONSISTENCY
# ============================================================

def consistency_classification(

    pearson,
    spearman,
    kendall,

):

    """
    Mede o quanto os três
    coeficientes concordam.
    """

    values = np.array(

        [

            pearson,
            spearman,
            kendall,

        ],

        dtype=float,

    )

    spread = np.max(values) - np.min(values)

    if spread < 0.02:

        return "Excellent"

    if spread < 0.05:

        return "High"

    if spread < 0.10:

        return "Moderate"

    if spread < 0.20:

        return "Low"

    return "Poor"

# ============================================================
# PEARSON MATRIX
# ============================================================

def compute_pearson_matrix(df):

    """
    Matriz completa de Pearson.
    """

    return df[OBSERVABLES].corr(
        method="pearson"
    )


# ============================================================
# SPEARMAN MATRIX
# ============================================================

def compute_spearman_matrix(df):

    """
    Matriz completa de Spearman.
    """

    return df[OBSERVABLES].corr(
        method="spearman"
    )


# ============================================================
# KENDALL MATRIX
# ============================================================

def compute_kendall_matrix(df):

    """
    Matriz completa de Kendall.
    """

    matrix = empty_matrix()

    for x, y in observable_pairs():

        tau, _ = kendalltau(

            df[x],
            df[y],

        )

        matrix.loc[x, y] = tau
        matrix.loc[y, x] = tau

    return matrix


# ============================================================
# AGREEMENT METRICS
# ============================================================

def compute_agreement_metrics(

    pearson,
    spearman,
    kendall,

):

    """
    Métricas de concordância
    entre métodos.
    """

    values = np.array(

        [

            pearson,
            spearman,
            kendall,

        ],

        dtype=float,

    )

    mean_value = np.mean(values)

    std_value = np.std(values)

    max_difference = np.max(values) - np.min(values)

    agreement = max(

        0.0,

        1.0 - max_difference,

    )

    consistency = consistency_classification(

        pearson,
        spearman,
        kendall,

    )

    return {

        "mean": float(mean_value),

        "std_between_methods": float(std_value),

        "max_difference": float(max_difference),

        "agreement_score": float(agreement),

        "consistency": consistency,

    }


# ============================================================
# SUMMARY TABLE
# ============================================================

def build_summary_table(

    pearson_matrix,
    spearman_matrix,
    kendall_matrix,

):

    """
    Comparação completa
    entre os três métodos.
    """

    rows = []

    for x, y in observable_pairs():

        pearson = float(

            pearson_matrix.loc[x, y]

        )

        spearman = float(

            spearman_matrix.loc[x, y]

        )

        kendall = float(

            kendall_matrix.loc[x, y]

        )

        metrics = compute_agreement_metrics(

            pearson,
            spearman,
            kendall,

        )

        rows.append({

            "variable_1": x,

            "variable_2": y,

            "pearson": pearson,

            "spearman": spearman,

            "kendall": kendall,

            "strength": correlation_strength(

                metrics["mean"]

            ),

            "mean_correlation": metrics["mean"],

            "std_between_methods":

                metrics["std_between_methods"],

            "max_difference":

                metrics["max_difference"],

            "agreement_score":

                metrics["agreement_score"],

            "consistency":

                metrics["consistency"],

        })

    table = pd.DataFrame(rows)

    table = table.sort_values(

        by="agreement_score",

        ascending=False,

    ).reset_index(

        drop=True,

    )

    table.insert(

        0,

        "rank",

        np.arange(

            1,

            len(table) + 1,

        ),

    )

    return table


# ============================================================
# BUILD MATRICES
# ============================================================

def build_rank_analysis(df):

    """
    Executa toda a análise
    de correlação por postos.
    """

    pearson_matrix = compute_pearson_matrix(df)

    spearman_matrix = compute_spearman_matrix(df)

    kendall_matrix = compute_kendall_matrix(df)

    summary_table = build_summary_table(

        pearson_matrix,

        spearman_matrix,

        kendall_matrix,

    )

    return {

        "pearson": pearson_matrix,

        "spearman": spearman_matrix,

        "kendall": kendall_matrix,

        "summary": summary_table,

    }

# ============================================================
# CERTIFICATE
# ============================================================

def build_certificate(summary_table):

    """
    Certificado do observatório.
    """

    certificate = {

        "observable_pairs": int(len(summary_table)),

        "excellent": int(
            (summary_table["consistency"] == "Excellent").sum()
        ),

        "high": int(
            (summary_table["consistency"] == "High").sum()
        ),

        "moderate": int(
            (summary_table["consistency"] == "Moderate").sum()
        ),

        "low": int(
            (summary_table["consistency"] == "Low").sum()
        ),

        "poor": int(
            (summary_table["consistency"] == "Poor").sum()
        ),

        "mean_agreement_score": float(

            summary_table["agreement_score"].mean()

        ),

        "minimum_agreement_score": float(

            summary_table["agreement_score"].min()

        ),

        "maximum_agreement_score": float(

            summary_table["agreement_score"].max()

        ),

    }

    return certificate


# ============================================================
# BUILD REPORT
# ============================================================

def build_report(df):

    analysis = build_rank_analysis(df)

    certificate = build_certificate(

        analysis["summary"]

    )

    analysis["certificate"] = certificate

    return analysis


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(report):

    report["pearson"].to_csv(

        RESULTS_DIR /

        "pearson_matrix.csv"

    )

    report["spearman"].to_csv(

        RESULTS_DIR /

        "spearman_matrix.csv"

    )

    report["kendall"].to_csv(

        RESULTS_DIR /

        "kendall_matrix.csv"

    )

    report["summary"].to_csv(

        RESULTS_DIR /

        "rank_correlation_summary.csv",

        index=False,

    )

    report["summary"][

        [

            "variable_1",

            "variable_2",

            "agreement_score",

            "std_between_methods",

            "max_difference",

            "consistency",

        ]

    ].to_csv(

        RESULTS_DIR /

        "rank_consistency.csv",

        index=False,

    )

    with open(

        RESULTS_DIR /

        "rank_correlation_certificate.json",

        "w",

        encoding="utf8",

    ) as f:

        json.dump(

            report["certificate"],

            f,

            indent=4,

            ensure_ascii=False,

        )

    # --------------------------------------------------------

    lines = []

    lines.append("=" * 60)
    lines.append("GER")
    lines.append("S29 - E6.3")
    lines.append("L3.3 - Rank Correlation Observatory")
    lines.append("=" * 60)
    lines.append("")

    c = report["certificate"]

    lines.append(

        f"Observable pairs : {c['observable_pairs']}"

    )

    lines.append("")

    lines.append(

        f"Excellent : {c['excellent']}"

    )

    lines.append(

        f"High      : {c['high']}"

    )

    lines.append(

        f"Moderate  : {c['moderate']}"

    )

    lines.append(

        f"Low       : {c['low']}"

    )

    lines.append(

        f"Poor      : {c['poor']}"

    )

    lines.append("")

    lines.append(

        f"Mean Agreement : "

        f"{c['mean_agreement_score']:.6f}"

    )

    lines.append("")

    lines.append("Ranking")
    lines.append("")

    for _, row in report["summary"].iterrows():

        lines.append(

            f"{int(row['rank']):2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f" | P={row['pearson']:.6f}"

            f" | S={row['spearman']:.6f}"

            f" | K={row['kendall']:.6f}"

            f" | A={row['agreement_score']:.6f}"

            f" | {row['consistency']}"

        )

    with open(

        RESULTS_DIR /

        "rank_correlation_summary.txt",

        "w",

        encoding="utf8",

    ) as f:

        f.write(

            "\n".join(lines)

        )

  # ============================================================
# DASHBOARD
# ============================================================

def print_dashboard(report):

    c = report["certificate"]

    print()
    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.3 - Rank Correlation Observatory")
    print("=" * 60)
    print()

    print("Observable Pairs")
    print(f"   {c['observable_pairs']}")
    print()

    print("Method Consistency")
    print("------------------------------")
    print(f"Excellent : {c['excellent']}")
    print(f"High      : {c['high']}")
    print(f"Moderate  : {c['moderate']}")
    print(f"Low       : {c['low']}")
    print(f"Poor      : {c['poor']}")
    print()

    print(
        f"Mean Agreement Score : "
        f"{c['mean_agreement_score']:.6f}"
    )

    print()

    print("=" * 60)
    print("Pair Ranking")
    print("=" * 60)

    for _, row in report["summary"].iterrows():

        print(

            f"{int(row['rank']):2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f" | P={row['pearson']:.6f}"

            f" | S={row['spearman']:.6f}"

            f" | K={row['kendall']:.6f}"

            f" | Mean={row['mean_correlation']:.6f}"

            f" | Agreement={row['agreement_score']:.6f}"

            f" | {row['consistency']}"

        )

    print()

    print("=" * 60)
    print("Generated Files")
    print("=" * 60)

    files = [

        "pearson_matrix.csv",
        "spearman_matrix.csv",
        "kendall_matrix.csv",
        "rank_correlation_summary.csv",
        "rank_consistency.csv",
        "rank_correlation_certificate.json",
        "rank_correlation_summary.txt",

    ]

    for file in files:

        print(f"   {file}")

    print()

    print("Results")

    print(RESULTS_DIR)

    print()

    print("=" * 60)
    print("Experiment completed.")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.3 - Rank Correlation Observatory")
    print("=" * 60)
    print()

    print("Loading Workspace...")

    workspace = Workspace()

    if not workspace.exists(DATASET_NAME):

        raise RuntimeError(

            f"Dataset '{DATASET_NAME}' not found."

        )

    print("Loading signatures...")

    df, rows = load_signatures(

        workspace

    )

    print(f"Samples loaded : {rows:,}")

    print()

    print("Computing rank correlations...")

    report = build_report(

        df

    )

    print("Saving results...")

    save_results(

        report

    )

    print_dashboard(

        report

    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
