"""
GER
S29 - E6.3

L3.3.1
Correlation Divergence Observatory
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

BASE_RESULTS = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E6.3"
)

RESULTS_DIR = (
    BASE_RESULTS /
    "L3_3_1_Correlation_Divergence"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ============================================================
# PREVIOUS OBSERVATORIES
# ============================================================

L31_FOLDER = (
    BASE_RESULTS /
    "L3_1_Global_Correlation"
)

L32_FOLDER = (
    BASE_RESULTS /
    "L3_2_Correlation_Stability"
)

L33_FOLDER = (
    BASE_RESULTS /
    "L3_3_Rank_Correlation"
)

# ============================================================
# REQUIRED FILES
# ============================================================

REQUIRED_FILES = {

    "L3_1": {

        "pairs":
            "correlation_pairs.csv",

    },

    "L3_2": {

        "stability":
            "correlation_stability.csv",

    },

    "L3_3": {

        "summary":
            "rank_correlation_summary.csv",

    }

}

# ============================================================
# FILE VALIDATION
# ============================================================

def validate_previous_results():

    missing = []

    folders = {

        "L3_1": L31_FOLDER,
        "L3_2": L32_FOLDER,
        "L3_3": L33_FOLDER,

    }

    for experiment, files in REQUIRED_FILES.items():

        folder = folders[experiment]

        for file in files.values():

            path = folder / file

            if not path.exists():

                missing.append(str(path))

    if missing:

        raise RuntimeError(

            "\nMissing required files:\n\n"

            + "\n".join(missing)

        )

# ============================================================
# LOAD RESULTS
# ============================================================

def load_previous_results():

    """
    Carrega automaticamente
    todos os resultados necessários.
    """

    validate_previous_results()

    results = {}

    # ------------------------------------------

    results["L3_1"] = {

        "pairs":

            pd.read_csv(

                L31_FOLDER /

                REQUIRED_FILES["L3_1"]["pairs"]

            )

    }

    # ------------------------------------------

    results["L3_2"] = {

        "stability":

            pd.read_csv(

                L32_FOLDER /

                REQUIRED_FILES["L3_2"]["stability"]

            )

    }

    # ------------------------------------------

    results["L3_3"] = {

        "summary":

            pd.read_csv(

                L33_FOLDER /

                REQUIRED_FILES["L3_3"]["summary"]

            )

    }

    return results

# ============================================================
# BUILD MASTER TABLE
# ============================================================

def build_master_table(results):

    """
    Une os resultados
    dos três observatórios.
    """

    pairs = results["L3_1"]["pairs"]

    stability = results["L3_2"]["stability"]

    rank = results["L3_3"]["summary"]

    master = pairs.merge(

        stability,

        on=[

            "variable_1",

            "variable_2",

        ],

        suffixes=(

            "",

            "_stability",

        ),

    )

    master = master.merge(

        rank,

        on=[

            "variable_1",

            "variable_2",

        ],

        suffixes=(

            "",

            "_rank",

        ),

    )

    return master.reset_index(

        drop=True

  )

# ============================================================
# DIVERGENCE METRICS
# ============================================================

def compute_divergence_metrics(master):

    """
    Calcula todas as métricas de divergência
    entre Pearson, Spearman e Kendall.
    """

    table = master.copy()

    # --------------------------------------------------------

    table["diff_PS"] = np.abs(

        table["pearson"] -

        table["spearman"]

    )

    table["diff_PK"] = np.abs(

        table["pearson"] -

        table["kendall"]

    )

    table["diff_SK"] = np.abs(

        table["spearman"] -

        table["kendall"]

    )

    # --------------------------------------------------------

    table["maximum_divergence"] = table[

        [

            "diff_PS",

            "diff_PK",

            "diff_SK",

        ]

    ].max(axis=1)

    table["mean_divergence"] = table[

        [

            "diff_PS",

            "diff_PK",

            "diff_SK",

        ]

    ].mean(axis=1)

    # --------------------------------------------------------

    table["sign_flip"] = (

        (

            np.sign(table["pearson"])

            !=

            np.sign(table["spearman"])

        )

        |

        (

            np.sign(table["pearson"])

            !=

            np.sign(table["kendall"])

        )

        |

        (

            np.sign(table["spearman"])

            !=

            np.sign(table["kendall"])

        )

    )

    return table


# ============================================================
# DIVERGENCE CLASSIFICATION
# ============================================================

def classify_divergence(value):

    """
    Classificação da divergência.
    """

    if value < 0.05:

        return "Consistent"

    if value < 0.15:

        return "Mild Divergence"

    if value < 0.30:

        return "Moderate Divergence"

    return "Strong Divergence"


# ============================================================
# STRUCTURAL INTERPRETATION
# ============================================================

def structural_interpretation(row):

    """
    Interpretação automática.
    """

    if row["sign_flip"]:

        return "Sign Reversal"

    p = abs(row["pearson"])

    s = abs(row["spearman"])

    if s > p + 0.10:

        return "Monotonic Dominance"

    if p > s + 0.10:

        return "Linear Dominance"

    return "Consistent Behaviour"


# ============================================================
# BUILD DIVERGENCE TABLE
# ============================================================

def build_divergence_table(master):

    """
    Tabela principal do observatório.
    """

    table = compute_divergence_metrics(master)

    table["divergence"] = table[

        "maximum_divergence"

    ].apply(

        classify_divergence

    )

    table["interpretation"] = table.apply(

        structural_interpretation,

        axis=1,

    )

    table = table.sort_values(

        by=[

            "maximum_divergence",

            "agreement_score",

        ],

        ascending=[

            False,

            True,

        ],

    ).reset_index(

        drop=True,

    )

    table.insert(

        0,

        "rank",

        np.arange(

            1,

            len(table)+1

        )

    )

    return table


# ============================================================
# CERTIFICATE
# ============================================================

def build_certificate(table):

    """
    Certificado estrutural.
    """

    return {

        "pairs": int(len(table)),

        "consistent": int(

            (table["divergence"] == "Consistent").sum()

        ),

        "mild": int(

            (table["divergence"] == "Mild Divergence").sum()

        ),

        "moderate": int(

            (table["divergence"] == "Moderate Divergence").sum()

        ),

        "strong": int(

            (table["divergence"] == "Strong Divergence").sum()

        ),

        "sign_flip": int(

            table["sign_flip"].sum()

        ),

        "mean_divergence": float(

            table["maximum_divergence"].mean()

        ),

        "maximum_divergence": float(

            table["maximum_divergence"].max()

        ),

    }


# ============================================================
# BUILD REPORT
# ============================================================

def build_report(results):

    master = build_master_table(results)

    divergence = build_divergence_table(master)

    certificate = build_certificate(

        divergence

    )

    return {

        "master": master,

        "divergence": divergence,

        "certificate": certificate,

    }

# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(report):

    divergence = report["divergence"]
    certificate = report["certificate"]

    # --------------------------------------------------------

    divergence.to_csv(

        RESULTS_DIR /
        "correlation_divergence.csv",

        index=False,

    )

    # --------------------------------------------------------

    divergence.sort_values(

        by="maximum_divergence",

        ascending=False,

    ).to_csv(

        RESULTS_DIR /
        "divergence_ranking.csv",

        index=False,

    )

    # --------------------------------------------------------

    divergence.loc[

        divergence["sign_flip"]

    ].to_csv(

        RESULTS_DIR /
        "sign_flip_analysis.csv",

        index=False,

    )

    # --------------------------------------------------------

    divergence[

        [

            "variable_1",

            "variable_2",

            "pearson",

            "spearman",

            "kendall",

            "diff_PS",

            "diff_PK",

            "diff_SK",

            "maximum_divergence",

            "agreement_score",

            "divergence",

            "interpretation",

        ]

    ].to_csv(

        RESULTS_DIR /
        "method_disagreement.csv",

        index=False,

    )

    # --------------------------------------------------------

    with open(

        RESULTS_DIR /
        "correlation_divergence_certificate.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4,

        )

    # --------------------------------------------------------

    with open(

        RESULTS_DIR /
        "correlation_divergence_summary.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            "GER\n"

            "S29 - E6.3\n"

            "L3.3.1\n"

            "Correlation Divergence Observatory\n\n"

        )

        f.write(

            "============================================================\n"

        )

        f.write(

            "PAIR ANALYSIS\n"

        )

        f.write(

            "============================================================\n\n"

        )

        for _, row in divergence.iterrows():

            f.write(

                f"{row['variable_1']} × {row['variable_2']}\n"

            )

            f.write(

                f"Pearson      : {row['pearson']:.6f}\n"

            )

            f.write(

                f"Spearman     : {row['spearman']:.6f}\n"

            )

            f.write(

                f"Kendall      : {row['kendall']:.6f}\n"

            )

            f.write(

                f"Max Divergence : {row['maximum_divergence']:.6f}\n"

            )

            f.write(

                f"Agreement      : {row['agreement_score']:.6f}\n"

            )

            f.write(

                f"Classification : {row['divergence']}\n"

            )

            f.write(

                f"Interpretation : {row['interpretation']}\n"

            )

            f.write(

                f"Sign Flip      : {row['sign_flip']}\n\n"

            )

# ============================================================
# DASHBOARD
# ============================================================

def print_dashboard(report):

    table = report["divergence"]
    certificate = report["certificate"]

    print()
    print("=" * 60)
    print("GER")
    print("S29 - E6.3")
    print("L3.3.1 - Correlation Divergence Observatory")
    print("=" * 60)

    print()

    print("Observable Pairs")
    print(f"   {len(table)}")

    print()

    print("Divergence Classification")
    print("-" * 30)

    print(

        f"Consistent : "

        f"{certificate['consistent']}"

    )

    print(

        f"Mild       : "

        f"{certificate['mild']}"

    )

    print(

        f"Moderate   : "

        f"{certificate['moderate']}"

    )

    print(

        f"Strong     : "

        f"{certificate['strong']}"

    )

    print()

    print(

        f"Sign Flip Pairs : "

        f"{certificate['sign_flip']}"

    )

    print()

    print(

        f"Mean Divergence : "

        f"{certificate['mean_divergence']:.6f}"

    )

    print()

    print("=" * 60)
    print("Pair Ranking")
    print("=" * 60)

    for _, row in table.iterrows():

        print(

            f"{row['rank']:2d}. "

            f"{row['variable_1']} × "

            f"{row['variable_2']}"

            f" | Max={row['maximum_divergence']:.6f}"

            f" | Agreement={row['agreement_score']:.6f}"

            f" | {row['divergence']}"

            f" | {row['interpretation']}"

        )

    print()

    print("=" * 60)
    print("Generated Files")
    print("=" * 60)

    print("   correlation_divergence.csv")
    print("   divergence_ranking.csv")
    print("   sign_flip_analysis.csv")
    print("   method_disagreement.csv")
    print("   correlation_divergence_certificate.json")
    print("   correlation_divergence_summary.txt")

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
    print("L3.3.1 - Correlation Divergence Observatory")
    print("=" * 60)

    print()

    print("Loading previous observatories...")

    results = load_previous_results()

    print("Building divergence analysis...")

    report = build_report(

        results

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
