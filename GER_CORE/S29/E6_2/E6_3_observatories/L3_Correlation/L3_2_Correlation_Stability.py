"""
GER
S29 - E6.3

L3.2 - Correlation Stability Observatory
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd

from GER_CORE.S29.E6_2.E6_3_observatories.L3_Correlation.L3_0_Workspace_Manager import (
    Workspace,
)

# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29_E6.3/L3_2_Correlation_Stability"
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

# Número de reamostragens

N_BOOTSTRAP = 1000

# Fração utilizada em cada reamostragem

SAMPLE_FRACTION = 1.0

# Reprodutibilidade

RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)

# ============================================================
# LOAD DATA
# ============================================================

def load_signatures(workspace):

    """
    Carrega todas as assinaturas do Workspace.
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
# BOOTSTRAP SAMPLER
# ============================================================

def bootstrap_sample(df):

    """
    Gera uma reamostragem bootstrap.
    """

    sample_size = int(

        len(df) * SAMPLE_FRACTION

    )

    indices = rng.choice(

        len(df),

        size=sample_size,

        replace=True,

    )

    return df.iloc[indices].reset_index(
        drop=True
    )


# ============================================================
# EMPTY RESULT TABLE
# ============================================================

def initialize_results():

    """
    Estrutura para armazenar
    todas as iterações bootstrap.
    """

    columns = [

        "iteration",

    ]

    for x, y in observable_pairs():

        columns.append(

            f"{x}__{y}"

        )

    return []

# ============================================================
# SINGLE BOOTSTRAP ITERATION
# ============================================================

def run_bootstrap_iteration(
    iteration,
    df,
):

    """
    Executa uma única reamostragem bootstrap.
    """

    sample = bootstrap_sample(df)

    row = {

        "iteration": iteration,

    }

    corr = sample.corr(
        method="pearson"
    )

    for x, y in observable_pairs():

        row[f"{x}__{y}"] = float(

            corr.loc[x, y]

        )

    return row


# ============================================================
# RUN BOOTSTRAP
# ============================================================

def run_bootstrap(df):

    """
    Executa todas as iterações bootstrap.
    """

    results = initialize_results()

    for iteration in range(

        1,

        N_BOOTSTRAP + 1,

    ):

        if (

            iteration == 1

            or iteration % 50 == 0

            or iteration == N_BOOTSTRAP

        ):

            print(

                f"Bootstrap "

                f"{iteration:,}/{N_BOOTSTRAP:,}"

            )

        results.append(

            run_bootstrap_iteration(

                iteration,

                df,

            )

        )

    return pd.DataFrame(results)


# ============================================================
# SUMMARY STATISTICS
# ============================================================

def compute_stability_statistics(

    bootstrap_df,

):

    """
    Estatísticas de estabilidade
    para cada par de observáveis.
    """

    rows = []

    for x, y in observable_pairs():

        column = f"{x}__{y}"

        values = bootstrap_df[column]

        mean = values.mean()

        std = values.std()

        median = values.median()

        minimum = values.min()

        maximum = values.max()

        q025 = values.quantile(0.025)

        q975 = values.quantile(0.975)

        cv = (

            abs(std / mean)

            if abs(mean) > 1e-12

            else np.nan

        )

        rows.append({

            "variable_1": x,

            "variable_2": y,

            "mean": float(mean),

            "median": float(median),

            "std": float(std),

            "cv": float(cv),

            "minimum": float(minimum),

            "maximum": float(maximum),

            "q025": float(q025),

            "q975": float(q975),

        })

    return pd.DataFrame(rows)


# ============================================================
# STABILITY CLASSIFICATION
# ============================================================

def classify_stability(cv):

    """
    Classificação baseada
    no coeficiente de variação.
    """

    if np.isnan(cv):

        return "Undefined"

    cv_percent = cv * 100

    if cv_percent < 1:

        return "Very Stable"

    if cv_percent < 5:

        return "Stable"

    if cv_percent < 10:

        return "Moderately Stable"

    if cv_percent < 20:

        return "Unstable"

    return "Highly Unstable"


# ============================================================
# STABILITY TABLE
# ============================================================

def build_stability_table(

    bootstrap_df,

):

    """
    Tabela resumida
    da estabilidade.
    """

    table = compute_stability_statistics(

        bootstrap_df

    )

    table["stability"] = table["cv"].apply(

        classify_stability

    )

    table = table.sort_values(

        by="cv",

        ascending=True,

    ).reset_index(

        drop=True

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
# CERTIFICATE
# ============================================================

def build_certificate(

    bootstrap_df,
    stability_table,

):

    """
    Certificado estatístico
    do observatório.
    """

    certificate = {

        "bootstrap_iterations": int(

            len(bootstrap_df)

        ),

        "observable_pairs": int(

            len(stability_table)

        ),

        "very_stable": int(

            (stability_table["stability"] == "Very Stable").sum()

        ),

        "stable": int(

            (stability_table["stability"] == "Stable").sum()

        ),

        "moderately_stable": int(

            (stability_table["stability"] == "Moderately Stable").sum()

        ),

        "unstable": int(

            (stability_table["stability"] == "Unstable").sum()

        ),

        "highly_unstable": int(

            (stability_table["stability"] == "Highly Unstable").sum()

        ),

    }

    return certificate


# ============================================================
# ENRICH STABILITY TABLE
# ============================================================

def enrich_stability_table(

    stability_table,

):

    """
    Acrescenta métricas
    complementares.
    """

    table = stability_table.copy()

    table["range"] = (

        table["maximum"]

        - table["minimum"]

    )

    table["ci_width"] = (

        table["q975"]

        - table["q025"]

    )

    table["standard_error"] = (

        table["std"]

        / np.sqrt(

            N_BOOTSTRAP

        )

    )

    return table


# ============================================================
# BUILD REPORT
# ============================================================

def build_report(

    bootstrap_df,

):

    stability_table = build_stability_table(

        bootstrap_df

    )

    stability_table = enrich_stability_table(

        stability_table

    )

    certificate = build_certificate(

        bootstrap_df,

        stability_table,

    )

    return {

        "bootstrap": bootstrap_df,

        "stability": stability_table,

        "certificate": certificate,

    }


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(

    report,

):

    report["bootstrap"].to_csv(

        RESULTS_DIR /

        "correlation_bootstrap.csv",

        index=False,

    )

    report["stability"].to_csv(

        RESULTS_DIR /

        "correlation_stability.csv",

        index=False,

    )

    report["stability"][

        [

            "variable_1",

            "variable_2",

            "std",

            "standard_error",

            "range",

            "ci_width",

            "cv",

        ]

    ].to_csv(

        RESULTS_DIR /

        "correlation_variability.csv",

        index=False,

    )

    report["stability"][

        [

            "variable_1",

            "variable_2",

            "q025",

            "q975",

            "ci_width",

        ]

    ].to_csv(

        RESULTS_DIR /

        "correlation_bootstrap_ci.csv",

        index=False,

    )

    with open(

        RESULTS_DIR /

        "correlation_stability_certificate.json",

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

    lines.append("L3.2 - Correlation Stability Observatory")

    lines.append("=" * 60)

    lines.append("")

    c = report["certificate"]

    lines.append(

        f"Bootstrap iterations : {c['bootstrap_iterations']}"

    )

    lines.append(

        f"Observable pairs      : {c['observable_pairs']}"

    )

    lines.append("")

    lines.append(

        f"Very Stable        : {c['very_stable']}"

    )

    lines.append(

        f"Stable             : {c['stable']}"

    )

    lines.append(

        f"Moderately Stable  : {c['moderately_stable']}"

    )

    lines.append(

        f"Unstable           : {c['unstable']}"

    )

    lines.append(

        f"Highly Unstable    : {c['highly_unstable']}"

    )

    lines.append("")

    lines.append("Ranking")

    lines.append("")

    for _, row in report["stability"].iterrows():

        lines.append(

            f"{int(row['rank']):2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f"  mean={row['mean']:.6f}"

            f"  std={row['std']:.6e}"

            f"  range={row['range']:.6e}"

            f"  ci={row['ci_width']:.6e}"

            f"  [{row['stability']}]"

        )

    with open(

        RESULTS_DIR /

        "correlation_stability_summary.txt",

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
    print("L3.2 - Correlation Stability Observatory")
    print("=" * 60)
    print()

    print(f"Bootstrap Iterations : {c['bootstrap_iterations']:,}")
    print(f"Observable Pairs     : {c['observable_pairs']}")
    print()

    print("Stability Summary")
    print("------------------------------")
    print(f"Very Stable        : {c['very_stable']}")
    print(f"Stable             : {c['stable']}")
    print(f"Moderately Stable  : {c['moderately_stable']}")
    print(f"Unstable           : {c['unstable']}")
    print(f"Highly Unstable    : {c['highly_unstable']}")
    print()

    print("=" * 60)
    print("Correlation Stability Ranking")
    print("=" * 60)

    for _, row in report["stability"].iterrows():

        print(

            f"{int(row['rank']):2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f" | mean={row['mean']:.6f}"

            f" | std={row['std']:.3e}"

            f" | range={row['range']:.3e}"

            f" | CI={row['ci_width']:.3e}"

            f" | {row['stability']}"

        )

    print()

    print("=" * 60)
    print("Generated Files")
    print("=" * 60)

    files = [

        "correlation_bootstrap.csv",
        "correlation_stability.csv",
        "correlation_variability.csv",
        "correlation_bootstrap_ci.csv",
        "correlation_stability_certificate.json",
        "correlation_stability_summary.txt",

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
    print("L3.2 - Correlation Stability Observatory")
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

    print("Running bootstrap...")
    print()

    bootstrap_df = run_bootstrap(df)

    print()
    print("Computing stability statistics...")

    report = build_report(

        bootstrap_df

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
