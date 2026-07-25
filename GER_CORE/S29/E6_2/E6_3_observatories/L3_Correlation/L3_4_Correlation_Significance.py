# ============================================================
# CONFIGURATION
# ============================================================

BASE_RESULTS = Path(

    "/content/drive/MyDrive/GER_RESULTS"

)

L31_FOLDER = (

    BASE_RESULTS /

    "S29_E6.3" /

    "L3_1_Correlation"

)

RESULTS_DIR = (

    BASE_RESULTS /

    "S29_E6.3" /

    "L3_4_Correlation_Significance"

)

RESULTS_DIR.mkdir(

    parents=True,

    exist_ok=True,

)

# ============================================================
# REQUIRED FILES
# ============================================================

REQUIRED_FILES = {

    "pairs":

        L31_FOLDER /

        "correlation_pairs.csv",

}

# ============================================================
# VALIDATION
# ============================================================

def validate_previous_results():

    """
    Verifica se os resultados necessários
    existem.
    """

    missing = []

    for name, path in REQUIRED_FILES.items():

        if not path.exists():

            missing.append(

                str(path)

            )

    if missing:

        raise FileNotFoundError(

            "\n".join(missing)

        )

# ============================================================
# LOAD DATA
# ============================================================

def load_previous_results():

    """
    Carrega os resultados do L3.1.
    """

    validate_previous_results()

    results = {

        "pairs":

        pd.read_csv(

            REQUIRED_FILES["pairs"]

        )

    }

    return results

# ============================================================
# PREPARE TABLE
# ============================================================

def prepare_table(results):

    """
    Organiza a tabela principal
    para os testes de significância.
    """

    table = results["pairs"].copy()

    expected = [

        "variable_1",

        "variable_2",

        "pearson",

        "spearman",

        "kendall",

        "samples",

    ]

    missing = [

        c

        for c in expected

        if c not in table.columns

    ]

    if missing:

        raise ValueError(

            "Missing columns:\n"

            +

            "\n".join(

                missing

            )

        )

    table = table[

        expected

    ].copy()

    table = table.sort_values(

        [

            "variable_1",

            "variable_2",

        ]

    ).reset_index(

        drop=True,

    )

    return table

# ============================================================
# REPORT
# ============================================================

def build_report(results):

    table = prepare_table(

        results

    )

    return {

        "table": table

    }

# ============================================================
# SIGNIFICANCE CLASSIFICATION
# ============================================================

def classify_significance(p):

    """
    Classificação baseada no p-value.
    """

    if p < 0.001:

        return "Highly Significant"

    if p < 0.01:

        return "Very Significant"

    if p < 0.05:

        return "Significant"

    if p < 0.10:

        return "Marginal"

    return "Not Significant"


# ============================================================
# PEARSON
# ============================================================

def pearson_statistics(r, n):

    """
    Estatísticas de Pearson.
    """

    if n <= 3:

        return np.nan, np.nan, np.nan, np.nan

    if abs(r) >= 1.0:

        r = np.sign(r) * 0.999999999

    # --------------------------------------------------------

    df = n - 2

    t = r * np.sqrt(

        df /

        (1.0 - r ** 2)

    )

    p = 2.0 * (

        1.0 -

        stats.t.cdf(

            abs(t),

            df,

        )

    )

    # --------------------------------------------------------
    # Fisher transform
    # --------------------------------------------------------

    z = np.arctanh(r)

    se = 1.0 / np.sqrt(

        n - 3

    )

    z_low = z - 1.96 * se

    z_high = z + 1.96 * se

    ci_low = np.tanh(z_low)

    ci_high = np.tanh(z_high)

    return (

        t,

        p,

        ci_low,

        ci_high,

    )


# ============================================================
# RANK CORRELATIONS
# ============================================================

def rank_statistics(table):

    """
    p-values aproximados
    para Spearman e Kendall.
    """

    table = table.copy()

    spearman_p = []

    kendall_p = []

    for _, row in table.iterrows():

        n = int(

            row["samples"]

        )

        rho = row["spearman"]

        tau = row["kendall"]

        # ----------------------------------------------------

        if n > 2:

            t = rho * np.sqrt(

                (n - 2)

                /

                (1 - rho ** 2)

            )

            p = 2 * (

                1 -

                stats.t.cdf(

                    abs(t),

                    n - 2,

                )

            )

        else:

            p = np.nan

        spearman_p.append(p)

        # ----------------------------------------------------

        if n > 1:

            z = (

                3 *

                tau *

                np.sqrt(

                    n * (n - 1)

                )

            ) / np.sqrt(

                2 *

                (2 * n + 5)

            )

            p = 2 * (

                1 -

                stats.norm.cdf(

                    abs(z)

                )

            )

        else:

            p = np.nan

        kendall_p.append(

            p

        )

    table["pearson_t"] = np.nan
    table["pearson_p"] = np.nan
    table["pearson_ci_low"] = np.nan
    table["pearson_ci_high"] = np.nan

    for idx, row in table.iterrows():

        (

            t,

            p,

            low,

            high,

        ) = pearson_statistics(

            row["pearson"],

            int(

                row["samples"]

            )

        )

        table.loc[

            idx,

            "pearson_t"

        ] = t

        table.loc[

            idx,

            "pearson_p"

        ] = p

        table.loc[

            idx,

            "pearson_ci_low"

        ] = low

        table.loc[

            idx,

            "pearson_ci_high"

        ] = high

    table["spearman_p"] = spearman_p

    table["kendall_p"] = kendall_p

    return table


# ============================================================
# MULTIPLE TESTING
# ============================================================

def multiple_testing(table):

    """
    Bonferroni e FDR.
    """

    table = table.copy()

    m = len(table)

    # --------------------------------------------------------

    table["bonferroni_p"] = np.minimum(

        table["pearson_p"] * m,

        1.0,

    )

    # --------------------------------------------------------

    order = np.argsort(

        table["pearson_p"]

    )

    ranked = table.iloc[

        order

    ].copy()

    ranked["fdr_p"] = (

        ranked["pearson_p"]

        *

        m

        /

        np.arange(

            1,

            m + 1,

        )

    )

    ranked["fdr_p"] = np.minimum(

        ranked["fdr_p"],

        1.0,

    )

    table.loc[

        ranked.index,

        "fdr_p"

    ] = ranked["fdr_p"]

    return table


# ============================================================
# AGREEMENT
# ============================================================

def agreement_score(row):

    """
    Quantos métodos
    concordam na significância.
    """

    count = 0

    if row["pearson_p"] < 0.05:

        count += 1

    if row["spearman_p"] < 0.05:

        count += 1

    if row["kendall_p"] < 0.05:

        count += 1

    return count


# ============================================================
# BUILD SIGNIFICANCE TABLE
# ============================================================

def build_significance_table(table):

    """
    Tabela principal.
    """

    table = rank_statistics(

        table

    )

    table = multiple_testing(

        table

    )

    table["agreement"] = table.apply(

        agreement_score,

        axis=1,

    )

    table["classification"] = table[

        "pearson_p"

    ].apply(

        classify_significance

    )

    table = table.sort_values(

        by=[

            "agreement",

            "pearson_p",

            "pearson",

        ],

        ascending=[

            False,

            True,

            False,

        ],

    ).reset_index(

        drop=True,

    )

    if "rank" in table.columns:

        table = table.drop(

            columns=["rank"]

        )

    table["rank"] = np.arange(

        1,

        len(table) + 1

    )

    cols = [

        "rank"

    ] + [

        c

        for c in table.columns

        if c != "rank"

    ]

    table = table[

        cols

    ]

    return table


# ============================================================
# CERTIFICATE
# ============================================================

def build_certificate(table):

    """
    Certificado estrutural.
    """

    return {

        "pairs":

            int(

                len(table)

            ),

        "highly_significant":

            int(

                (table["classification"]

                 == "Highly Significant").sum()

            ),

        "very_significant":

            int(

                (table["classification"]

                 == "Very Significant").sum()

            ),

        "significant":

            int(

                (table["classification"]

                 == "Significant").sum()

            ),

        "marginal":

            int(

                (table["classification"]

                 == "Marginal").sum()

            ),

        "not_significant":

            int(

                (table["classification"]

                 == "Not Significant").sum()

            ),

        "agreement_3":

            int(

                (table["agreement"] == 3).sum()

            ),

        "agreement_2":

            int(

                (table["agreement"] == 2).sum()

            ),

        "agreement_1":

            int(

                (table["agreement"] == 1).sum()

            ),

        "agreement_0":

            int(

                (table["agreement"] == 0).sum()

            ),

    }


# ============================================================
# REPORT
# ============================================================

def build_report(results):

    table = prepare_table(

        results

    )

    table = build_significance_table(

        table

    )

    certificate = build_certificate(

        table

    )

    return {

        "table": table,

        "certificate": certificate,

      }

# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(report):

    table = report["table"]
    certificate = report["certificate"]

    # --------------------------------------------------------

    table.to_csv(

        RESULTS_DIR /

        "correlation_significance.csv",

        index=False,

    )

    # --------------------------------------------------------

    table[

        [

            "rank",

            "variable_1",

            "variable_2",

            "pearson",

            "pearson_t",

            "pearson_p",

            "pearson_ci_low",

            "pearson_ci_high",

            "classification",

        ]

    ].to_csv(

        RESULTS_DIR /

        "pearson_significance.csv",

        index=False,

    )

    # --------------------------------------------------------

    table[

        [

            "rank",

            "variable_1",

            "variable_2",

            "spearman",

            "spearman_p",

        ]

    ].to_csv(

        RESULTS_DIR /

        "spearman_significance.csv",

        index=False,

    )

    # --------------------------------------------------------

    table[

        [

            "rank",

            "variable_1",

            "variable_2",

            "kendall",

            "kendall_p",

        ]

    ].to_csv(

        RESULTS_DIR /

        "kendall_significance.csv",

        index=False,

    )

    # --------------------------------------------------------

    table[

        [

            "rank",

            "variable_1",

            "variable_2",

            "pearson_p",

            "bonferroni_p",

            "fdr_p",

        ]

    ].to_csv(

        RESULTS_DIR /

        "multiple_testing.csv",

        index=False,

    )

    # --------------------------------------------------------

    with open(

        RESULTS_DIR /

        "significance_certificate.json",

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

        "correlation_significance_summary.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            "GER\n"

            "S29 - E6.3\n"

            "L3.4\n"

            "Correlation Significance Observatory\n\n"

        )

        f.write(

            "=" * 60 +

            "\n"

        )

        f.write(

            "PAIR ANALYSIS\n"

        )

        f.write(

            "=" * 60 +

            "\n\n"

        )

        for _, row in table.iterrows():

            f.write(

                f"{row['variable_1']} × {row['variable_2']}\n"

            )

            f.write(

                f"Pearson = {row['pearson']:.6f}\n"

            )

            f.write(

                f"t = {row['pearson_t']:.6f}\n"

            )

            f.write(

                f"p = {row['pearson_p']:.8e}\n"

            )

            f.write(

                f"95% CI = "

                f"[{row['pearson_ci_low']:.6f}, "

                f"{row['pearson_ci_high']:.6f}]\n"

            )

            f.write(

                f"Spearman p = "

                f"{row['spearman_p']:.8e}\n"

            )

            f.write(

                f"Kendall p = "

                f"{row['kendall_p']:.8e}\n"

            )

            f.write(

                f"Bonferroni = "

                f"{row['bonferroni_p']:.8e}\n"

            )

            f.write(

                f"FDR = "

                f"{row['fdr_p']:.8e}\n"

            )

            f.write(

                f"Agreement = "

                f"{row['agreement']}/3\n"

            )

            f.write(

                f"Classification = "

                f"{row['classification']}\n\n"

            )


# ============================================================
# DASHBOARD
# ============================================================

def print_dashboard(report):

    table = report["table"]

    certificate = report["certificate"]

    print()

    print("=" * 60)

    print("GER")

    print("S29 - E6.3")

    print("L3.4 - Correlation Significance Observatory")

    print("=" * 60)

    print()

    print("Observable Pairs")

    print(f"   {len(table)}")

    print()

    print("Classification")

    print("-" * 30)

    print(

        "Highly Significant :",

        certificate["highly_significant"]

    )

    print(

        "Very Significant   :",

        certificate["very_significant"]

    )

    print(

        "Significant        :",

        certificate["significant"]

    )

    print(

        "Marginal           :",

        certificate["marginal"]

    )

    print(

        "Not Significant    :",

        certificate["not_significant"]

    )

    print()

    print("Agreement")

    print("-" * 30)

    print(

        "3/3 :",

        certificate["agreement_3"]

    )

    print(

        "2/3 :",

        certificate["agreement_2"]

    )

    print(

        "1/3 :",

        certificate["agreement_1"]

    )

    print(

        "0/3 :",

        certificate["agreement_0"]

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

            f" | p={row['pearson_p']:.3e}"

            f" | Agreement={row['agreement']}/3"

            f" | {row['classification']}"

        )

    print()

    print("=" * 60)

    print("Generated Files")

    print("=" * 60)

    print("   correlation_significance.csv")

    print("   pearson_significance.csv")

    print("   spearman_significance.csv")

    print("   kendall_significance.csv")

    print("   multiple_testing.csv")

    print("   significance_certificate.json")

    print("   correlation_significance_summary.txt")

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

    print("L3.4 - Correlation Significance Observatory")

    print("=" * 60)

    print()

    print("Loading previous observatories...")

    results = load_previous_results()

    print("Running significance tests...")

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
