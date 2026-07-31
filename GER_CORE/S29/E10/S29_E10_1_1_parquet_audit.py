"""
===============================================================================
GER
S29 - E10.1.1
PARQUET AUDIT
Parte 1/4
===============================================================================

Auditoria completa dos resultados produzidos pela E10.1.1.

Arquivos analisados

    signature_surface.parquet
    certificate_surface.parquet
    grid.parquet
    metadata.json

Resultados

E10_1_1_PARQUET_AUDIT/

===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/E10/E10_1_1"
)

SIGNATURE_FILE = ROOT / "signature_surface.parquet"
CERTIFICATE_FILE = ROOT / "certificate_surface.parquet"
GRID_FILE = ROOT / "grid.parquet"
METADATA_FILE = ROOT / "metadata.json"

OUTPUT = ROOT / "E10_1_1_PARQUET_AUDIT"

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)

assert OUTPUT.exists()


# =============================================================================
# UTILITÁRIOS
# =============================================================================

def section(title: str):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def save_json(obj, filename):

    with open(
        OUTPUT / filename,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            obj,
            f,
            indent=4,
            ensure_ascii=False,
            default=str,
        )


def save_text(text, filename):

    with open(
        OUTPUT / filename,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(text)


def dataframe_info(df: pd.DataFrame):

    info = {}

    info["rows"] = int(len(df))
    info["columns"] = int(len(df.columns))

    info["column_names"] = list(df.columns)

    info["dtypes"] = {
        c: str(t)
        for c, t in df.dtypes.items()
    }

    info["memory_MB"] = float(
        df.memory_usage(deep=True).sum()
        / 1024**2
    )

    return info


def save_dataframe_info(df, filename):

    info = dataframe_info(df)

    txt = []

    txt.append(f"Rows ............. {info['rows']}")
    txt.append(f"Columns .......... {info['columns']}")
    txt.append(f"Memory (MB) ...... {info['memory_MB']:.3f}")
    txt.append("")
    txt.append("Columns")
    txt.append("-" * 60)

    for c in info["column_names"]:

        txt.append(
            f"{c:<35} {info['dtypes'][c]}"
        )

    txt.append("")
    txt.append("HEAD")
    txt.append("-" * 60)
    txt.append(df.head().to_string())

    txt.append("")
    txt.append("TAIL")
    txt.append("-" * 60)
    txt.append(df.tail().to_string())

    save_text(
        "\n".join(txt),
        filename,
    )

    return info


def numeric_columns(df):

    return list(
        df.select_dtypes(
            include=np.number
        ).columns
    )


# =============================================================================
# CARREGAMENTO
# =============================================================================

section("Loading files")

signature = pd.read_parquet(SIGNATURE_FILE)
certificate = pd.read_parquet(CERTIFICATE_FILE)
grid = pd.read_parquet(GRID_FILE)

with open(
    METADATA_FILE,
    "r",
    encoding="utf-8",
) as f:

    metadata = json.load(f)

print("Signature :", signature.shape)
print("Certificate :", certificate.shape)
print("Grid :", grid.shape)

save_json(
    metadata,
    "metadata.json",
)

signature_info = save_dataframe_info(
    signature,
    "signature_info.txt",
)

certificate_info = save_dataframe_info(
    certificate,
    "certificate_info.txt",
)

grid_info = save_dataframe_info(
    grid,
    "grid_info.txt",
)

print()
print("Parte 1 concluída.")

# =============================================================================
# ESTATÍSTICAS
# =============================================================================

section("Statistical analysis")


def statistics_table(df):

    nums = numeric_columns(df)

    if len(nums) == 0:
        return pd.DataFrame()

    rows = []

    for col in nums:

        s = df[col]

        rows.append({

            "column": col,

            "count": int(s.count()),
            "nulls": int(s.isna().sum()),

            "min": float(s.min()),
            "max": float(s.max()),
            "range": float(s.max() - s.min()),

            "mean": float(s.mean()),
            "median": float(s.median()),
            "std": float(s.std()),

            "q25": float(s.quantile(0.25)),
            "q75": float(s.quantile(0.75)),

            "variance": float(s.var()),
            "unique": int(s.nunique()),

        })

    return pd.DataFrame(rows)


signature_stats = statistics_table(signature)
certificate_stats = statistics_table(certificate)

signature_stats.to_csv(
    OUTPUT / "signature_statistics.csv",
    index=False,
)

certificate_stats.to_csv(
    OUTPUT / "certificate_statistics.csv",
    index=False,
)

print(signature_stats)



# =============================================================================
# NULOS
# =============================================================================

section("Null values")


def null_table(df):

    rows = []

    for c in df.columns:

        rows.append({

            "column": c,
            "nulls": int(df[c].isna().sum()),
            "percent":

                100.0
                * df[c].isna().sum()
                / len(df)

        })

    return pd.DataFrame(rows)


signature_nulls = null_table(signature)
certificate_nulls = null_table(certificate)

signature_nulls.to_csv(
    OUTPUT / "signature_nulls.csv",
    index=False,
)

certificate_nulls.to_csv(
    OUTPUT / "certificate_nulls.csv",
    index=False,
)



# =============================================================================
# VALORES ÚNICOS
# =============================================================================

section("Unique values")


def unique_table(df):

    rows = []

    for c in df.columns:

        rows.append({

            "column": c,
            "unique": int(df[c].nunique())

        })

    return pd.DataFrame(rows)


signature_unique = unique_table(signature)
certificate_unique = unique_table(certificate)

signature_unique.to_csv(
    OUTPUT / "signature_unique_values.csv",
    index=False,
)

certificate_unique.to_csv(
    OUTPUT / "certificate_unique_values.csv",
    index=False,
)



# =============================================================================
# DUPLICATAS
# =============================================================================

section("Duplicate rows")

duplicate_signature = int(signature.duplicated().sum())
duplicate_certificate = int(certificate.duplicated().sum())
duplicate_grid = int(grid.duplicated().sum())

print("Signature :", duplicate_signature)
print("Certificate :", duplicate_certificate)
print("Grid :", duplicate_grid)



# =============================================================================
# INFINITOS
# =============================================================================

section("Infinite values")


def infinite_table(df):

    rows = []

    nums = numeric_columns(df)

    for c in nums:

        inf = np.isinf(df[c]).sum()

        rows.append({

            "column": c,
            "infinite": int(inf)

        })

    return pd.DataFrame(rows)


signature_inf = infinite_table(signature)
certificate_inf = infinite_table(certificate)

signature_inf.to_csv(
    OUTPUT / "signature_infinite.csv",
    index=False,
)

certificate_inf.to_csv(
    OUTPUT / "certificate_infinite.csv",
    index=False,
)



# =============================================================================
# COBERTURA DA MALHA
# =============================================================================

section("Grid coverage")

expected = (
    metadata["grid_size"]
    * metadata["grid_size"]
)

processed = len(grid)

coverage = (
    processed
    / expected
)

grid_summary = {

    "expected_points": int(expected),
    "processed_points": int(processed),
    "coverage": float(coverage),

    "unique_gamma":

        int(grid["gamma"].nunique()),

    "unique_omega":

        int(grid["omega"].nunique()),

}

save_json(
    grid_summary,
    "grid_summary.json",
)

print(grid_summary)



# =============================================================================
# INTEGRIDADE γ × ω
# =============================================================================

section("Grid integrity")

pairs = grid[
    ["gamma", "omega"]
].drop_duplicates()

pairs.to_csv(
    OUTPUT / "grid_pairs.csv",
    index=False,
)

print(
    "Unique pairs:",
    len(pairs),
)

print()
print("Parte 2 concluída.")

# =============================================================================
# DEPENDÊNCIA EM γ
# =============================================================================

section("Gamma dependence")


def grouped_statistics(df, group_col):

    nums = [
        c for c in numeric_columns(df)
        if c != group_col
    ]

    if len(nums) == 0:
        return {}

    results = {}

    for col in nums:

        stats = (
            df
            .groupby(group_col)[col]
            .agg([
                "mean",
                "std",
                "min",
                "max",
                "median",
            ])
            .reset_index()
        )

        results[col] = stats

    return results


gamma_tables = grouped_statistics(
    signature,
    "gamma",
)

for name, table in gamma_tables.items():

    table.to_csv(
        OUTPUT / f"gamma_{name}.csv",
        index=False,
    )

print("Gamma tables:", len(gamma_tables))


# =============================================================================
# DEPENDÊNCIA EM ω
# =============================================================================

section("Omega dependence")

omega_tables = grouped_statistics(
    signature,
    "omega",
)

for name, table in omega_tables.items():

    table.to_csv(
        OUTPUT / f"omega_{name}.csv",
        index=False,
    )

print("Omega tables:", len(omega_tables))


# =============================================================================
# SUPERFÍCIES γ × ω
# =============================================================================

section("Surface extraction")

reserved = {
    "i",
    "j",
    "gamma",
    "omega",
}

surface_columns = [

    c

    for c in numeric_columns(signature)

    if c not in reserved

]

for column in surface_columns:

    try:

        surface = signature.pivot_table(

            index="gamma",

            columns="omega",

            values=column,

        )

        surface.to_csv(

            OUTPUT / f"{column}_surface.csv"

        )

        print("Surface:", column)

    except Exception:

        pass


# =============================================================================
# MATRIZ DE CORRELAÇÃO
# =============================================================================

section("Correlation matrix")

corr_columns = [

    c

    for c in numeric_columns(signature)

    if signature[c].nunique() > 1

]

if len(corr_columns) > 1:

    correlation = signature[corr_columns].corr()

    correlation.to_csv(

        OUTPUT / "correlation_matrix.csv"

    )

    print(correlation)


# =============================================================================
# VARIAÇÃO DAS COMPONENTES
# =============================================================================

section("Component variation")

rows = []

for col in surface_columns:

    s = signature[col]

    rows.append({

        "observable": col,

        "minimum": float(s.min()),

        "maximum": float(s.max()),

        "range": float(s.max() - s.min()),

        "std": float(s.std()),

        "variance": float(s.var()),

        "unique": int(s.nunique()),

    })

variation = pd.DataFrame(rows)

variation.to_csv(

    OUTPUT / "component_variation.csv",

    index=False,

)

print(variation)


# =============================================================================
# CERTIFICADOS
# =============================================================================

section("Certificate audit")

certificate_summary = []

for column in certificate.columns:

    certificate_summary.append({

        "column": column,

        "unique": int(

            certificate[column].nunique()

        ),

        "nulls": int(

            certificate[column].isna().sum()

        )

    })

certificate_summary = pd.DataFrame(

    certificate_summary

)

certificate_summary.to_csv(

    OUTPUT / "certificate_summary.csv",

    index=False,

)


# =============================================================================
# CERTIFICADOS DISTINTOS
# =============================================================================

section("Distinct certificates")

certificate_unique = (

    certificate[
        [
            "signature",
            "relations",
            "deductions",
            "consistency",
            "summary",
        ]
    ]

    .drop_duplicates()

    .reset_index(drop=True)

)

certificate_unique.to_csv(

    OUTPUT / "distinct_certificates.csv",

    index=False,

)

print(

    "Distinct certificates:",

    len(certificate_unique)

)


# =============================================================================
# CONSISTÊNCIA DOS CERTIFICADOS
# =============================================================================

section("Certificate consistency")

consistency = {}

for col in certificate.columns:

    consistency[col] = {

        "unique":

            int(certificate[col].nunique()),

        "constant":

            bool(certificate[col].nunique() == 1),

    }

save_json(

    consistency,

    "certificate_consistency.json",

)

print()

print("Parte 3 concluída.")

# =============================================================================
# RELATÓRIO FINAL
# =============================================================================

section("Building final report")

report = []

report.append("=" * 80)
report.append("GER")
report.append("S29 - E10.1.1")
report.append("PARQUET AUDIT REPORT")
report.append("=" * 80)
report.append("")

# =============================================================================
# METADATA
# =============================================================================

report.append("EXPERIMENT")
report.append("-" * 80)

for k, v in metadata.items():
    report.append(f"{k:<20} : {v}")

report.append("")

# =============================================================================
# DATASETS
# =============================================================================

report.append("DATASETS")
report.append("-" * 80)

report.append(
    f"Signature rows      : {len(signature)}"
)

report.append(
    f"Certificate rows    : {len(certificate)}"
)

report.append(
    f"Grid rows           : {len(grid)}"
)

report.append("")

# =============================================================================
# GRID
# =============================================================================

report.append("GRID")
report.append("-" * 80)

for k, v in grid_summary.items():
    report.append(f"{k:<20} : {v}")

report.append("")

# =============================================================================
# COMPONENT VARIATION
# =============================================================================

report.append("SIGNATURE VARIATION")
report.append("-" * 80)

for _, row in variation.iterrows():

    report.append(
        f"{row.observable:<25}"
        f" range={row['range']:.8f}"
        f" std={row['std']:.8f}"
        f" unique={int(row['unique'])}"
    )

report.append("")

# =============================================================================
# CONSTANT COMPONENTS
# =============================================================================

constant = variation[
    variation["unique"] == 1
]

if len(constant):

    report.append("CONSTANT COMPONENTS")
    report.append("-" * 80)

    for c in constant["observable"]:

        report.append(f"- {c}")

    report.append("")

# =============================================================================
# CORRELATION
# =============================================================================

if "correlation" in locals():

    report.append("CORRELATION MATRIX")
    report.append("-" * 80)

    report.append(correlation.round(5).to_string())

    report.append("")

# =============================================================================
# CERTIFICATES
# =============================================================================

report.append("CERTIFICATES")
report.append("-" * 80)

report.append(
    f"Distinct certificates : {len(certificate_unique)}"
)

report.append("")

for _, row in certificate_summary.iterrows():

    report.append(

        f"{row.column:<30}"

        f" unique={row.unique}"

        f" nulls={row.nulls}"

    )

report.append("")

# =============================================================================
# AUTOMATIC DIAGNOSIS
# =============================================================================

diagnosis = []

if coverage == 1.0:

    diagnosis.append(
        "Grid coverage is complete."
    )

else:

    diagnosis.append(
        "Grid coverage is incomplete."
    )

if duplicate_signature == 0:

    diagnosis.append(
        "No duplicated signature rows."
    )

if duplicate_certificate == 0:

    diagnosis.append(
        "No duplicated certificate rows."
    )

if len(constant):

    diagnosis.append(
    f"{len(constant)} signature components are constant."
)

for comp in constant["observable"]:

    diagnosis.append(
        f"  - {comp}"
    )

else:

    diagnosis.append(
        "All signature components vary."
    )

if len(certificate_unique) == 1:

    diagnosis.append(
        "Single structural certificate over the whole surface."
    )

else:

    diagnosis.append(
        f"{len(certificate_unique)} distinct structural certificates detected."
    )

report.append("AUTOMATIC DIAGNOSIS")
report.append("-" * 80)

for line in diagnosis:

    report.append(f"- {line}")

report.append("")

# =============================================================================
# SAVE REPORT
# =============================================================================

save_text(

    "\n".join(report),

    "audit_report.txt",

)

audit = {

    "metadata": metadata,

    "grid": grid_summary,

    "variation":

        variation.to_dict(
            orient="records"
        ),

    "diagnosis":

        diagnosis,

    "distinct_certificates":

        int(len(certificate_unique)),

}

save_json(

    audit,

    "audit.json",

)

# =============================================================================
# CONSOLE SUMMARY
# =============================================================================

section("AUDIT SUMMARY")

print()

print("Audit directory")
print(OUTPUT)

print()

print("Files generated")

for file in sorted(OUTPUT.iterdir()):

    print(" -", file.name)

print()

print("Automatic diagnosis")

for item in diagnosis:

    print(" •", item)

print()

print("=" * 80)
print("PARQUET AUDIT FINISHED")
print("=" * 80)

# =============================================================================
# FIGURES
# =============================================================================

import matplotlib.pyplot as plt

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURES = OUTPUT / "FIGURES"

FIGURES.mkdir(
    parents=True,
    exist_ok=True,
)

assert FIGURES.exists()

section("Generating figures")


# =============================================================================
# SURFACES
# =============================================================================

reserved = {
    "i",
    "j",
    "gamma",
    "omega",
}

surface_columns = [
    c
    for c in numeric_columns(signature)
    if c not in reserved
]

for column in surface_columns:

    try:

        surface = signature.pivot_table(
            index="gamma",
            columns="omega",
            values=column,
        )

        plt.figure(figsize=(7,6))

        plt.imshow(
            surface.values,
            origin="lower",
            aspect="auto",
        )

        plt.colorbar(label=column)

        plt.xticks(
            range(len(surface.columns)),
            np.round(surface.columns.values,2),
            rotation=90,
        )

        plt.yticks(
            range(len(surface.index)),
            np.round(surface.index.values,2),
        )

        plt.xlabel("omega")
        plt.ylabel("gamma")
        plt.title(column)

        plt.tight_layout()

        plt.savefig(
            FIGURES / f"{column}_surface.png",
            dpi=300,
        )

        plt.close()

    except Exception:

        pass


# =============================================================================
# GAMMA PROFILES
# =============================================================================

for column in surface_columns:

    try:

        stats = (
            signature
            .groupby("gamma")[column]
            .agg(["mean","std"])
        )

        plt.figure(figsize=(7,4))

        plt.plot(
            stats.index,
            stats["mean"],
        )

        plt.fill_between(
            stats.index,
            stats["mean"]-stats["std"],
            stats["mean"]+stats["std"],
            alpha=0.25,
        )

        plt.xlabel("gamma")
        plt.ylabel(column)

        plt.tight_layout()

        plt.savefig(
            FIGURES / f"{column}_gamma_profile.png",
            dpi=300,
        )

        plt.close()

    except Exception:

        pass


# =============================================================================
# OMEGA PROFILES
# =============================================================================

for column in surface_columns:

    try:

        stats = (
            signature
            .groupby("omega")[column]
            .agg(["mean","std"])
        )

        plt.figure(figsize=(7,4))

        plt.plot(
            stats.index,
            stats["mean"],
        )

        plt.fill_between(
            stats.index,
            stats["mean"]-stats["std"],
            stats["mean"]+stats["std"],
            alpha=0.25,
        )

        plt.xlabel("omega")
        plt.ylabel(column)

        plt.tight_layout()

        plt.savefig(
            FIGURES / f"{column}_omega_profile.png",
            dpi=300,
        )

        plt.close()

    except Exception:

        pass


# =============================================================================
# HISTOGRAMS
# =============================================================================

for column in surface_columns:

    plt.figure(figsize=(6,4))

    signature[column].hist(
        bins=40,
    )

    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{column}_histogram.png",
        dpi=300,
    )

    plt.close()


# =============================================================================
# VARIANCE
# =============================================================================

if len(variation):

    plt.figure(figsize=(8,4))

    plt.bar(
        variation["observable"],
        variation["variance"],
    )

    plt.xticks(rotation=45)

    plt.ylabel("Variance")

    plt.tight_layout()

    plt.savefig(
        FIGURES / "component_variance.png",
        dpi=300,
    )

    plt.close()


# =============================================================================
# CORRELATION
# =============================================================================

if "correlation" in locals():

    plt.figure(figsize=(8,7))

    plt.imshow(
        correlation.values,
        origin="lower",
    )

    plt.colorbar()

    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=90,
    )

    plt.yticks(
        range(len(correlation.index)),
        correlation.index,
    )

    plt.tight_layout()

    plt.savefig(
        FIGURES / "correlation_heatmap.png",
        dpi=300,
    )

    plt.close()


# =============================================================================
# CERTIFICATES
# =============================================================================

if len(certificate_summary):

    plt.figure(figsize=(8,4))

    plt.bar(
        certificate_summary["column"],
        certificate_summary["unique"],
    )

    plt.xticks(rotation=90)

    plt.ylabel("Unique values")

    plt.tight_layout()

    plt.savefig(
        FIGURES / "certificate_distribution.png",
        dpi=300,
    )

    plt.close()


# =============================================================================
# MISSING VALUES
# =============================================================================

nulls = signature.isna().sum()

plt.figure(figsize=(8,4))

plt.bar(
    nulls.index,
    nulls.values,
)

plt.xticks(rotation=90)

plt.ylabel("Missing")

plt.tight_layout()

plt.savefig(
    FIGURES / "missing_values.png",
    dpi=300,
)

plt.close()


# =============================================================================
# DASHBOARD
# =============================================================================

fig = plt.figure(figsize=(12,8))

plt.axis("off")

txt = []

txt.append("GER")
txt.append("S29 - E10.1.1")
txt.append("")
txt.append(f"Grid: {grid_summary['processed_points']} points")
txt.append(f"Coverage: {100*grid_summary['coverage']:.2f}%")
txt.append("")
txt.append("Automatic diagnosis")
txt.append("---------------------")

for item in diagnosis:
    txt.append("• " + item)

plt.text(
    0.02,
    0.98,
    "\n".join(txt),
    va="top",
    family="monospace",
    fontsize=11,
)

plt.tight_layout()

plt.savefig(
    FIGURES / "audit_dashboard.png",
    dpi=300,
)

plt.close()

print()
print("="*80)
print("FIGURES GENERATED")
print("="*80)
print(FIGURES)
