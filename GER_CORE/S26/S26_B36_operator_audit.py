"""
============================================================
GER - Geometria Espectral Relacional

S26_B36_operator_audit.py

Operator Audit
Versão: 1.0

Objetivo
--------
Auditar os Operadores Geométricos Fundamentais produzidos
pelo Geometry Scan.

Este módulo NÃO realiza classificação.

Ele apenas verifica consistência matemática e estrutural
dos operadores.

Entrada
--------
RESULTS/S26_B36_geometry_scan.csv

Saídas
------
Relatório textual
RESULTS/S26_B36_operator_audit.csv

============================================================
"""

import os

import numpy as np
import pandas as pd


# ==========================================================
# Configuração
# ==========================================================

INPUT_CSV = "RESULTS/S26_B36_geometry_scan.csv"

OUTPUT_CSV = "RESULTS/S26_B36_operator_audit.csv"


REQUIRED_COLUMNS = [

    "simulation_id",

    "beta",
    "sigma",
    "potential",

    "dt",
    "window_size",

    "diameter",
    "convergence",
    "recurrence",
    "drift",
    "trajectory_length",
]


# ==========================================================
# Utilidades
# ==========================================================

def status(flag):
    return "PASS" if flag else "FAIL"


def print_header():

    print()
    print("=" * 60)
    print("S26-B36 OPERATOR AUDIT")
    print("=" * 60)
    print()


# ==========================================================
# Leitura do CSV
# ==========================================================

def load_geometry_scan(csv_path=INPUT_CSV):

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Arquivo não encontrado:\n{csv_path}"
        )

    df = pd.read_csv(csv_path)

    return df


# ==========================================================
# Validação estrutural
# ==========================================================

def validate_structure(df):

    report = {}

    report["row_count"] = len(df)

    report["column_count"] = len(df.columns)

    report["missing_columns"] = [
        c for c in REQUIRED_COLUMNS
        if c not in df.columns
    ]

    report["has_all_columns"] = (
        len(report["missing_columns"]) == 0
    )

    return report


# ==========================================================
# Impressão da validação estrutural
# ==========================================================

def print_structure_report(report):

    print("--------------------------------------------")
    print("Estrutura")
    print("--------------------------------------------")

    print(f"Linhas   : {report['row_count']}")
    print(f"Colunas  : {report['column_count']}")
    print()

    print(
        "Colunas obrigatórias :",
        status(report["has_all_columns"])
    )

    if not report["has_all_columns"]:

        print()
        print("Colunas ausentes:")

        for col in report["missing_columns"]:
            print("  -", col)

    print()


# ==========================================================
# Main
# ==========================================================

def main():

    print_header()

    df = load_geometry_scan()

    structure = validate_structure(df)

    print_structure_report(structure)

    integrity = audit_integrity(df)

    print_integrity(integrity)

    stats = compute_statistics(df)

    print_statistics(stats)

    pearson, spearman = compute_correlations(df)

    print_correlations(pearson, spearman)

    mono = monotonicity_beta(df)

    print_monotonicity(mono)

    sigma = sigma_dependence(df)

    print_sigma(sigma)

    deg = detect_degenerate(stats)

    print_degenerate(deg)

    red = detect_redundancy(pearson)

    print_redundancy(red)

    audit_df = build_audit_dataframe(
        stats,
        integrity,
        deg,
        red
    )

    save_audit_csv(audit_df)

    executive_summary(
        integrity,
        deg,
        red
    )

    scientific_conclusion()


if __name__ == "__main__":
    main()

# ==========================================================
# Auditoria de integridade
# ==========================================================

def audit_integrity(df):

    report = {}

    report["has_nan"] = df.isna().any().any()

    report["has_inf"] = np.isinf(
        df.select_dtypes(include=[np.number])
    ).any().any()

    report["negative_diameter"] = (df["diameter"] < 0).any()

    report["negative_convergence"] = (df["convergence"] < 0).any()

    report["negative_recurrence"] = (df["recurrence"] < 0).any()

    report["negative_drift"] = (df["drift"] < 0).any()

    report["negative_length"] = (
        df["trajectory_length"] < 0
    ).any()

    report["dt_constant"] = (
        df["dt"].nunique() == 1
    )

    report["window_constant"] = (
        df["window_size"].nunique() == 1
    )

    return report


# ==========================================================
# Estatísticas dos operadores
# ==========================================================

OPERATORS = [

    "diameter",

    "convergence",

    "recurrence",

    "drift",

    "trajectory_length",
]


def compute_statistics(df):

    rows = []

    for op in OPERATORS:

        values = df[op].values

        mean = np.mean(values)

        std = np.std(values)

        if abs(mean) > 1e-15:
            cv = std / abs(mean)
        else:
            cv = np.nan

        rows.append({

            "operator": op,

            "min": np.min(values),

            "max": np.max(values),

            "mean": mean,

            "std": std,

            "cv": cv

        })

    return pd.DataFrame(rows)


# ==========================================================
# Impressão da integridade
# ==========================================================

def print_integrity(report):

    print("--------------------------------------------")
    print("Integridade")
    print("--------------------------------------------")

    print("NaN..................", status(not report["has_nan"]))

    print("Inf..................", status(not report["has_inf"]))

    print(
        "Diameter >= 0........",
        status(not report["negative_diameter"])
    )

    print(
        "Convergence >= 0.....",
        status(not report["negative_convergence"])
    )

    print(
        "Recurrence >= 0......",
        status(not report["negative_recurrence"])
    )

    print(
        "Drift >= 0...........",
        status(not report["negative_drift"])
    )

    print(
        "Trajectory >= 0......",
        status(not report["negative_length"])
    )

    print(
        "dt constante.........",
        status(report["dt_constant"])
    )

    print(
        "window constante.....",
        status(report["window_constant"])
    )

    print()


# ==========================================================
# Impressão das estatísticas
# ==========================================================

def print_statistics(stats):

    print("--------------------------------------------")
    print("Estatísticas")
    print("--------------------------------------------")

    print(stats.round(6))

    print()

# ==========================================================
# Correlações
# ==========================================================

def compute_correlations(df):

    data = df[OPERATORS]

    pearson = data.corr(method="pearson")

    spearman = data.corr(method="spearman")

    return pearson, spearman


# ==========================================================
# Monotonicidade em beta
# ==========================================================

def monotonicity_beta(df):

    report = {}

    for op in OPERATORS:

        report[op] = {}

        for pot in sorted(df["potential"].unique()):

            subset = (
                df[df["potential"] == pot]
                .sort_values("beta")
            )

            y = subset[op].values

            diff = np.diff(y)

            increasing = np.all(diff >= -1e-12)

            decreasing = np.all(diff <= 1e-12)

            if increasing:
                trend = "UP"

            elif decreasing:
                trend = "DOWN"

            else:
                trend = "NON_MONOTONIC"

            report[op][pot] = trend

    return report


# ==========================================================
# Dependência de sigma
# ==========================================================

def sigma_dependence(df):

    report = {}

    for op in OPERATORS:

        report[op] = {}

        for pot in sorted(df["potential"].unique()):

            subset = (
                df[df["potential"] == pot]
                .sort_values("sigma")
            )

            values = subset.groupby("sigma")[op].mean()

            amplitude = values.max() - values.min()

            report[op][pot] = amplitude

    return report


# ==========================================================
# Degenerescência
# ==========================================================

def detect_degenerate(stats, tol=1e-12):

    degenerate = []

    for _, row in stats.iterrows():

        if row["std"] < tol:

            degenerate.append(row["operator"])

    return degenerate


# ==========================================================
# Redundância
# ==========================================================

def detect_redundancy(pearson, threshold=0.98):

    redundant = []

    cols = pearson.columns

    for i in range(len(cols)):

        for j in range(i + 1, len(cols)):

            rho = pearson.iloc[i, j]

            if abs(rho) >= threshold:

                redundant.append(
                    (cols[i], cols[j], rho)
                )

    return redundant


# ==========================================================
# Impressão das correlações
# ==========================================================

def print_correlations(pearson, spearman):

    print("--------------------------------------------")
    print("Pearson")
    print("--------------------------------------------")

    print(pearson.round(3))

    print()

    print("--------------------------------------------")
    print("Spearman")
    print("--------------------------------------------")

    print(spearman.round(3))

    print()


# ==========================================================
# Impressão da monotonicidade
# ==========================================================

def print_monotonicity(report):

    print("--------------------------------------------")
    print("Monotonicidade em beta")
    print("--------------------------------------------")

    for op in OPERATORS:

        print()

        print(op)

        for pot in sorted(report[op].keys()):

            print(f"  Potencial {pot}: {report[op][pot]}")

    print()


# ==========================================================
# Impressão da dependência de sigma
# ==========================================================

def print_sigma(report):

    print("--------------------------------------------")
    print("Dependência de sigma")
    print("--------------------------------------------")

    for op in OPERATORS:

        print()

        print(op)

        for pot in sorted(report[op].keys()):

            amp = report[op][pot]

            print(f"  Potencial {pot}: amplitude = {amp:.6f}")

    print()


# ==========================================================
# Impressão da degenerescência
# ==========================================================

def print_degenerate(degenerate):

    print("--------------------------------------------")
    print("Degenerescência")
    print("--------------------------------------------")

    if len(degenerate) == 0:

        print("Nenhum operador degenerado.")

    else:

        for op in degenerate:

            print(op)

    print()


# ==========================================================
# Impressão da redundância
# ==========================================================

def print_redundancy(redundant):

    print("--------------------------------------------")
    print("Redundância")
    print("--------------------------------------------")

    if len(redundant) == 0:

        print("Nenhum par altamente correlacionado.")

    else:

        for a, b, rho in redundant:

            print(
                f"{a:20s} <-> {b:20s} : {rho:.3f}"
            )

    print()

# ==========================================================
# Geração do DataFrame de Auditoria
# ==========================================================

def build_audit_dataframe(stats,
                          integrity,
                          degenerate,
                          redundant):

    rows = []

    for _, row in stats.iterrows():

        op = row["operator"]

        rows.append({

            "operator": op,

            "min": row["min"],
            "max": row["max"],
            "mean": row["mean"],
            "std": row["std"],
            "cv": row["cv"],

            "degenerate": op in degenerate

        })

    audit_df = pd.DataFrame(rows)

    audit_df.attrs["integrity"] = integrity
    audit_df.attrs["redundant_pairs"] = len(redundant)

    return audit_df


# ==========================================================
# Salvar CSV
# ==========================================================

def save_audit_csv(df,
                   filename=OUTPUT_CSV):

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )

    df.to_csv(
        filename,
        index=False
    )

    print()
    print("CSV salvo em:")
    print(filename)
    print()


# ==========================================================
# Resumo Executivo
# ==========================================================

def executive_summary(integrity,
                      degenerate,
                      redundant):

    print("=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)
    print()

    overall = "PASS"

    if integrity["has_nan"]:
        overall = "FAIL"

    if integrity["has_inf"]:
        overall = "FAIL"

    if len(degenerate) > 0:
        overall = "WARNING"

    if len(redundant) > 0:
        overall = "WARNING"

    print(f"Overall Status : {overall}")
    print()

    print("Integridade.............",
          status(
              not integrity["has_nan"]
              and
              not integrity["has_inf"]
          ))

    print("Degenerescência.........",
          "PASS" if len(degenerate)==0 else "WARNING")

    print("Redundância............",
          "PASS" if len(redundant)==0 else "WARNING")

    print()

    print("Observação:")

    print(
        "Este módulo audita os Operadores "
        "Geométricos Fundamentais."
    )

    print(
        "Nenhuma classificação dinâmica é "
        "realizada."
    )

    print(
        "Nenhum threshold científico é "
        "introduzido por esta auditoria."
    )

    print()


# ==========================================================
# Conclusão Científica
# ==========================================================

def scientific_conclusion():

    print("=" * 60)
    print("CONCLUSÃO")
    print("=" * 60)
    print()

    print(
        "O Operator Audit verifica apenas a "
        "consistência matemática dos "
        "Operadores Geométricos Fundamentais."
    )

    print()

    print(
        "Ele não produz diagnóstico "
        "geométrico."
    )

    print(
        "Ele não produz classificação."
    )

    print(
        "Ele não calibra parâmetros."
    )

    print()

    print(
        "Sua função é garantir que os "
        "operadores produzidos pelo "
        "Geometry Scan permaneçam "
        "consistentes com a especificação "
        "GER-S26-B36-OGF."
    )

    print()

    print("=" * 60)
