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

    print("Parte 2 concluída.")
    print()


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
