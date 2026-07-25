"""
GER_CORE/S29/E6_2/E6_3_observatories/L3_Correlation/L3_1_Global_Correlation.py

============================================================
GER
S29 - E6.3

L3.1 - Global Correlation Observatory
============================================================

Pergunta científica

Quais relações lineares existem entre todos
os observáveis do espaço de assinaturas?

Este observatório calcula:

• Matriz de correlação de Pearson
• p-values
• Intervalos de confiança
• Ranking das correlações
• Certificado estatístico

Toda leitura de dados é realizada através do
Workspace Manager.

"""

from __future__ import annotations

import json

from pathlib import Path

import numpy as np
import pandas as pd

from scipy.stats import pearsonr
from scipy.stats import t

from GER_CORE.S29.E6_2.E6_3_observatories.L3_Correlation.L3_0_Workspace_Manager import (
    Workspace,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

RESULTS_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E6.3/L3_1_Global_Correlation"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATASET_NAME = "signatures"

CONFIDENCE_LEVEL = 0.95


# ============================================================
# OBSERVÁVEIS
# ============================================================

OBSERVABLES = [

    "diameter",
    "convergence",
    "recurrence",
    "drift",

]


# ============================================================
# CORRELAÇÃO
# ============================================================

def correlation_strength(r):

    r = abs(r)

    if r < 0.20:
        return "Negligible"

    if r < 0.40:
        return "Weak"

    if r < 0.60:
        return "Moderate"

    if r < 0.80:
        return "Strong"

    return "Very Strong"


# ============================================================
# FISHER CONFIDENCE INTERVAL
# ============================================================

def fisher_confidence_interval(
    r,
    n,
    confidence=0.95
):

    if n < 4:

        return np.nan, np.nan

    if abs(r) >= 1.0:

        return r, r

    z = np.arctanh(r)

    se = 1 / np.sqrt(n - 3)

    alpha = 1.0 - confidence

    zcrit = abs(

        t.ppf(
            alpha / 2,
            df=n - 3
        )

    )

    low = np.tanh(z - zcrit * se)

    high = np.tanh(z + zcrit * se)

    return low, high


# ============================================================
# STREAMING LOADER
# ============================================================

def load_signatures(workspace):

    frames = []

    total_rows = 0

    for chunk in workspace.iter_chunks(DATASET_NAME):

        frames.append(chunk)

        total_rows += len(chunk)

    df = pd.concat(

        frames,

        ignore_index=True

    )

    return df, total_rows


# ============================================================
# PAIR GENERATOR
# ============================================================

def observable_pairs():

    pairs = []

    for i in range(len(OBSERVABLES)):

        for j in range(i + 1, len(OBSERVABLES)):

            pairs.append(

                (

                    OBSERVABLES[i],

                    OBSERVABLES[j],

                )

            )

    return pairs

# ============================================================
# PEARSON MATRIX
# ============================================================

def compute_correlation_matrix(df):

    """
    Matriz de correlação de Pearson.
    """

    return df[OBSERVABLES].corr(
        method="pearson"
    )


# ============================================================
# P-VALUE MATRIX
# ============================================================

def compute_pvalue_matrix(df):

    """
    Matriz de p-values.
    """

    matrix = pd.DataFrame(

        np.nan,

        index=OBSERVABLES,

        columns=OBSERVABLES,

    )

    for a in OBSERVABLES:

        matrix.loc[a, a] = 0.0

    for x, y in observable_pairs():

        r, p = pearsonr(

            df[x],

            df[y],

        )

        matrix.loc[x, y] = p
        matrix.loc[y, x] = p

    return matrix


# ============================================================
# CONFIDENCE MATRIX
# ============================================================

def compute_confidence_table(df):

    """
    Intervalos de confiança para cada par.
    """

    rows = []

    n = len(df)

    for x, y in observable_pairs():

        r, p = pearsonr(

            df[x],

            df[y],

        )

        low, high = fisher_confidence_interval(

            r,

            n,

            CONFIDENCE_LEVEL,

        )

        rows.append({

            "variable_1": x,

            "variable_2": y,

            "correlation": float(r),

            "p_value": float(p),

            "confidence": CONFIDENCE_LEVEL,

            "lower": float(low),

            "upper": float(high),

        })

    return pd.DataFrame(rows)


# ============================================================
# PAIR RANKING
# ============================================================

def compute_pair_table(df):

    """
    Ranking absoluto das correlações.
    """

    rows = []

    n = len(df)

    for x, y in observable_pairs():

        r, p = pearsonr(

            df[x],

            df[y],

        )

        low, high = fisher_confidence_interval(

            r,

            n,

            CONFIDENCE_LEVEL,

        )

        rows.append({

            "variable_1": x,

            "variable_2": y,

            "correlation": float(r),

            "abs_correlation": float(abs(r)),

            "strength": correlation_strength(r),

            "p_value": float(p),

            "ci_lower": float(low),

            "ci_upper": float(high),

        })

    table = pd.DataFrame(rows)

    table = table.sort_values(

        by="abs_correlation",

        ascending=False,

    ).reset_index(

        drop=True

    )

    table.insert(

        0,

        "rank",

        np.arange(

            1,

            len(table) + 1

        )

    )

    return table


# ============================================================
# CERTIFICATE
# ============================================================

def build_certificate(

    df,

    pair_table,

):

    """
    Certificado estatístico.
    """

    certificate = {

        "method": "Pearson",

        "confidence_level": CONFIDENCE_LEVEL,

        "samples": int(len(df)),

        "variables": len(OBSERVABLES),

        "pairs": len(pair_table),

        "very_strong": int(

            (pair_table["strength"] == "Very Strong").sum()

        ),

        "strong": int(

            (pair_table["strength"] == "Strong").sum()

        ),

        "moderate": int(

            (pair_table["strength"] == "Moderate").sum()

        ),

        "weak": int(

            (pair_table["strength"] == "Weak").sum()

        ),

        "negligible": int(

            (pair_table["strength"] == "Negligible").sum()

        ),

    }

    return certificate

# ============================================================
# REPORT
# ============================================================

def build_report(

    workspace,
    df,

):

    correlation_matrix = compute_correlation_matrix(df)

    pvalue_matrix = compute_pvalue_matrix(df)

    confidence_table = compute_confidence_table(df)

    pair_table = compute_pair_table(df)

    certificate = build_certificate(

        df,

        pair_table,

    )

    return {

        "workspace": workspace,

        "correlation_matrix": correlation_matrix,

        "pvalue_matrix": pvalue_matrix,

        "confidence_table": confidence_table,

        "pair_table": pair_table,

        "certificate": certificate,

    }


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(report):

    # --------------------------------------------------------
    # MATRIZ DE CORRELAÇÃO
    # --------------------------------------------------------

    report["correlation_matrix"].to_csv(

        RESULTS_DIR / "correlation_matrix.csv"

    )

    # --------------------------------------------------------
    # MATRIZ DE P-VALUES
    # --------------------------------------------------------

    report["pvalue_matrix"].to_csv(

        RESULTS_DIR / "correlation_pvalues.csv"

    )

    # --------------------------------------------------------
    # INTERVALOS DE CONFIANÇA
    # --------------------------------------------------------

    report["confidence_table"].to_csv(

        RESULTS_DIR / "correlation_confidence.csv",

        index=False,

    )

    # --------------------------------------------------------
    # RANKING DOS PARES
    # --------------------------------------------------------

    report["pair_table"].to_csv(

        RESULTS_DIR / "correlation_pairs.csv",

        index=False,

    )

    # --------------------------------------------------------
    # CERTIFICADO
    # --------------------------------------------------------

    with open(

        RESULTS_DIR / "correlation_certificate.json",

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
    # SUMMARY
    # --------------------------------------------------------

    lines = []

    lines.append("=" * 60)
    lines.append("GER")
    lines.append("S29 - E6.3")
    lines.append("L3.1 - Global Correlation Observatory")
    lines.append("=" * 60)
    lines.append("")

    lines.append(

        f"Samples : {report['certificate']['samples']}"

    )

    lines.append(

        f"Variables : {report['certificate']['variables']}"

    )

    lines.append(

        f"Pairs : {report['certificate']['pairs']}"

    )

    lines.append("")

    lines.append("Correlation Strength")

    lines.append(

        f"Very Strong : {report['certificate']['very_strong']}"

    )

    lines.append(

        f"Strong      : {report['certificate']['strong']}"

    )

    lines.append(

        f"Moderate    : {report['certificate']['moderate']}"

    )

    lines.append(

        f"Weak        : {report['certificate']['weak']}"

    )

    lines.append(

        f"Negligible  : {report['certificate']['negligible']}"

    )

    lines.append("")

    lines.append("Ranking")

    for _, row in report["pair_table"].iterrows():

        lines.append(

            f"{int(row['rank']):2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f"  r={row['correlation']:.6f}"

            f"  p={row['p_value']:.3e}"

            f"  [{row['strength']}]"

        )

    with open(

        RESULTS_DIR / "correlation_summary.txt",

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

    certificate = report["certificate"]

    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.1 - Global Correlation Observatory")
    print("=" * 60)
    print()

    print("Dataset")
    print(f"   {DATASET_NAME}")
    print()

    print("Samples")
    print(f"   {certificate['samples']:,}")
    print()

    print("Variables")
    print(f"   {certificate['variables']}")
    print()

    print("Pairs")
    print(f"   {certificate['pairs']}")
    print()

    print("Correlation Strength")

    print(f"   Very Strong : {certificate['very_strong']}")
    print(f"   Strong      : {certificate['strong']}")
    print(f"   Moderate    : {certificate['moderate']}")
    print(f"   Weak        : {certificate['weak']}")
    print(f"   Negligible  : {certificate['negligible']}")
    print()

    print("=" * 60)
    print("Correlation Ranking")
    print("=" * 60)

    ranking = report["pair_table"]

    for _, row in ranking.iterrows():

        print(

            f"{int(row['rank']):2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f"   r={row['correlation']:.6f}"

            f"   p={row['p_value']:.3e}"

            f"   {row['strength']}"

        )

    print()

    print("=" * 60)
    print("Generated")
    print("=" * 60)

    generated = [

        "correlation_matrix.csv",
        "correlation_pvalues.csv",
        "correlation_confidence.csv",
        "correlation_pairs.csv",
        "correlation_certificate.json",
        "correlation_summary.txt",

    ]

    for file in generated:

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
    print("L3.1 - Global Correlation Observatory")
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

    print("Computing correlations...")

    report = build_report(

        workspace,

        df,

    )

    print("Saving results...")

    save_results(

        report

    )

    print_dashboard(

        report

    )


if __name__ == "__main__":

    main()
