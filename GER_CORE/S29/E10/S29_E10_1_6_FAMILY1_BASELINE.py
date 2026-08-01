"""
=============================================================
E10.1.6
FAMILY 1 BASELINE
=============================================================

Objective
---------
Establish the official quantitative baseline for the
canonical Family 1 operator (E10-v1).

The generated baseline becomes the reference against
which all future operator families (Family 2, Family 3,
...) will be compared.

=============================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd


# ============================================================
# DIRECTORIES
# ============================================================

RESULTS_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/E10"
)

E10_1_4_DIR = RESULTS_DIR / "E10_1_4_Family1Validation"

E10_1_5_DIR = RESULTS_DIR / "E10_1_5_Family1StructuralCertificate"

OUTPUT_DIR = RESULTS_DIR / "E10_1_6_Family1Baseline"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# UTILITIES
# ============================================================

def load_json(path: Path):

    with open(path, "r") as f:
        return json.load(f)


def save_json(data, path: Path):

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4,
        )


def dataframe_inventory(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "nulls": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
    }


# ============================================================
# PART 1
# LOAD BASELINE DATASETS
# ============================================================

print()
print("=" * 80)
print("PART 1 - LOAD BASELINE DATASETS")
print("=" * 80)
print()

print("Loading Family 1 reference datasets...")
print()

datasets = {}

# ------------------------------------------------------------
# JSON
# ------------------------------------------------------------

datasets["family_validation"] = load_json(
    E10_1_4_DIR /
    "family1_validation.json"
)

datasets["family_certificate"] = load_json(
    E10_1_4_DIR /
    "family1_certificate.json"
)

datasets["campaign_certificate"] = load_json(
    E10_1_4_DIR /
    "campaign_certificate.json"
)

datasets["statistical_summary"] = load_json(
    E10_1_4_DIR /
    "statistical_summary.json"
)

datasets["structural_certificate"] = load_json(
    E10_1_5_DIR /
    "family1_structural_certificate.json"
)

print(
    f"family_validation        {len(datasets['family_validation'])} keys"
)

print(
    f"family_certificate       {len(datasets['family_certificate'])} keys"
)

print(
    f"campaign_certificate     {len(datasets['campaign_certificate'])} keys"
)

print(
    f"statistical_summary      {len(datasets['statistical_summary'])} keys"
)

print(
    f"structural_certificate   {len(datasets['structural_certificate'])} keys"
)

# ------------------------------------------------------------
# TABLES
# ------------------------------------------------------------

variation = pd.read_csv(
    E10_1_4_DIR /
    "family1_variation.csv"
)

omega = pd.read_csv(
    E10_1_4_DIR /
    "omega_neutrality.csv"
)

print(
    f"variation                {variation.shape}"
)

print(
    f"omega                    {omega.shape}"
)

datasets["variation"] = variation
datasets["omega"] = omega

# ------------------------------------------------------------
# INVENTORY
# ------------------------------------------------------------

inventory = pd.DataFrame(

    [

        {
            "artifact": "family_validation",
            "type": "json",
            "rows": len(datasets["family_validation"]),
            "columns": 0,
        },

        {
            "artifact": "family_certificate",
            "type": "json",
            "rows": len(datasets["family_certificate"]),
            "columns": 0,
        },

        {
            "artifact": "campaign_certificate",
            "type": "json",
            "rows": len(datasets["campaign_certificate"]),
            "columns": 0,
        },

        {
            "artifact": "statistical_summary",
            "type": "json",
            "rows": len(datasets["statistical_summary"]),
            "columns": 0,
        },

        {
            "artifact": "structural_certificate",
            "type": "json",
            "rows": len(datasets["structural_certificate"]),
            "columns": 0,
        },

        {
            "artifact": "variation",
            "type": "table",
            "rows": len(variation),
            "columns": len(variation.columns),
        },

        {
            "artifact": "omega",
            "type": "table",
            "rows": len(omega),
            "columns": len(omega.columns),
        },

    ]

)

inventory.to_csv(

    OUTPUT_DIR /
    "baseline_inventory.csv",

    index=False,

)

print()
print("=" * 80)
print("BASELINE INVENTORY")
print("=" * 80)
print()

print(inventory)

print()
print("Artifacts loaded :", len(inventory))

print()
print("Part 1 completed.")

# ============================================================
# PART 2
# BASELINE CONSOLIDATION
# ============================================================

print()
print("=" * 80)
print("PART 2 - BASELINE CONSOLIDATION")
print("=" * 80)
print()

baseline = variation.copy()

# ------------------------------------------------------------
# Coeficiente de variação
# ------------------------------------------------------------

baseline["coefficient_variation"] = (

    baseline["amplitude"]

    /

    baseline["maximum"]

)

baseline["coefficient_variation"] = (

    baseline["coefficient_variation"]

    .replace([np.inf, -np.inf], np.nan)

    .fillna(0.0)

)

# ------------------------------------------------------------
# Dynamic Range
# ------------------------------------------------------------

baseline["dynamic_range"] = (

    baseline["maximum"]

    -

    baseline["minimum"]

)

# ------------------------------------------------------------
# Sensibilidade Normalizada
# ------------------------------------------------------------

baseline["normalized_amplitude"] = (

    baseline["amplitude"]

    /

    baseline["amplitude"].max()

)

# ------------------------------------------------------------
# Métricas booleanas
# ------------------------------------------------------------

baseline["gamma_sensitive"] = True

baseline["omega_neutral"] = omega["neutral"].values

baseline["baseline_valid"] = (

    baseline["gamma_sensitive"]

    &

    baseline["omega_neutral"]

    &

    baseline["varying"]

)

# ------------------------------------------------------------
# Estatísticas globais
# ------------------------------------------------------------

summary = {

    "observables":

        int(len(baseline)),

    "mean_amplitude":

        float(

            baseline["amplitude"].mean()

        ),

    "median_amplitude":

        float(

            baseline["amplitude"].median()

        ),

    "std_amplitude":

        float(

            baseline["amplitude"].std()

        ),

    "mean_dynamic_range":

        float(

            baseline["dynamic_range"].mean()

        ),

    "mean_cv":

        float(

            baseline["coefficient_variation"].mean()

        ),

    "gamma_sensitive":

        int(

            baseline["gamma_sensitive"].sum()

        ),

    "omega_neutral":

        int(

            baseline["omega_neutral"].sum()

        ),

    "all_monotonic":

        bool(

            baseline["monotonic"].all()

        ),

    "baseline_ready":

        bool(

            baseline["baseline_valid"].all()

        ),

}

# ------------------------------------------------------------
# Salvando
# ------------------------------------------------------------

baseline.to_csv(

    OUTPUT_DIR /

    "baseline_metrics.csv",

    index=False,

)

baseline.to_parquet(

    OUTPUT_DIR /

    "baseline_metrics.parquet",

    index=False,

)

save_json(

    summary,

    OUTPUT_DIR /

    "baseline_summary.json",

)

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print("Baseline metrics")
print()

print(

    baseline[

        [

            "observable",

            "amplitude",

            "dynamic_range",

            "coefficient_variation",

            "gamma_sensitive",

            "omega_neutral",

            "baseline_valid",

        ]

    ]

)

print()

print("=" * 80)
print("BASELINE SUMMARY")
print("=" * 80)
print()

for key, value in summary.items():

    print(f"{key:24} {value}")

print()

print("Files generated")

print("- baseline_metrics.csv")
print("- baseline_metrics.parquet")
print("- baseline_summary.json")

print()

print("Part 2 completed.")

# ============================================================
# PART 3
# BASELINE SCIENTIFIC CONSOLIDATION
# ============================================================

print()
print("=" * 80)
print("PART 3 - BASELINE SCIENTIFIC CONSOLIDATION")
print("=" * 80)
print()

# ------------------------------------------------------------
# Global indicators
# ------------------------------------------------------------

global_indicators = {

    "mean_amplitude":

        float(
            baseline["amplitude"].mean()
        ),

    "median_amplitude":

        float(
            baseline["amplitude"].median()
        ),

    "std_amplitude":

        float(
            baseline["amplitude"].std()
        ),

    "maximum_amplitude":

        float(
            baseline["amplitude"].max()
        ),

    "minimum_amplitude":

        float(
            baseline["amplitude"].min()
        ),

    "mean_dynamic_range":

        float(
            baseline["dynamic_range"].mean()
        ),

    "mean_cv":

        float(
            baseline["coefficient_variation"].mean()
        ),

    "gamma_sensitive_fraction":

        float(
            baseline["gamma_sensitive"].mean()
        ),

    "omega_neutral_fraction":

        float(
            baseline["omega_neutral"].mean()
        ),

    "monotonic_fraction":

        float(
            baseline["monotonic"].mean()
        ),

    "baseline_valid_fraction":

        float(
            baseline["baseline_valid"].mean()
        ),

}

# ------------------------------------------------------------
# Official reference table
# ------------------------------------------------------------

reference = baseline[[
    "observable",
    "minimum",
    "maximum",
    "amplitude",
    "dynamic_range",
    "coefficient_variation",
    "monotonic",
    "gamma_sensitive",
    "omega_neutral",
    "baseline_valid",
]].copy()

reference.to_csv(

    OUTPUT_DIR /
    "baseline_reference.csv",

    index=False,

)

reference.to_parquet(

    OUTPUT_DIR /
    "baseline_reference.parquet",

    index=False,

)

# ------------------------------------------------------------
# JSON reference
# ------------------------------------------------------------

baseline_reference = {

    "family":

        "Family 1",

    "operator":

        "U(gamma) = (1 + gamma) I",

    "observables":

        int(len(reference)),

    "all_monotonic":

        bool(reference["monotonic"].all()),

    "all_gamma_sensitive":

        bool(reference["gamma_sensitive"].all()),

    "all_omega_neutral":

        bool(reference["omega_neutral"].all()),

    "baseline_valid":

        bool(reference["baseline_valid"].all()),

    "mean_amplitude":

        global_indicators["mean_amplitude"],

    "mean_dynamic_range":

        global_indicators["mean_dynamic_range"],

    "mean_cv":

        global_indicators["mean_cv"],

}

save_json(

    baseline_reference,

    OUTPUT_DIR /
    "baseline_reference.json",

)

save_json(

    global_indicators,

    OUTPUT_DIR /
    "global_indicators.json",

)

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print("Official Baseline Reference")
print()

print(reference)

print()

print("=" * 80)
print("GLOBAL INDICATORS")
print("=" * 80)
print()

for key, value in global_indicators.items():

    print(f"{key:32} {value}")

print()

print("Files generated")

print("- baseline_reference.csv")
print("- baseline_reference.parquet")
print("- baseline_reference.json")
print("- global_indicators.json")

print()

print("Part 3 completed.")

# ============================================================
# PART 4
# BASELINE CERTIFICATE
# ============================================================

print()
print("=" * 80)
print("PART 4 - BASELINE CERTIFICATE")
print("=" * 80)
print()

certificate = {

    "experiment":

        "E10.1.6",

    "title":

        "Family 1 Baseline",

    "family":

        "Family 1",

    "operator":

        "U(gamma) = (1 + gamma) I",

    "status":

        "OFFICIAL BASELINE",

    "reference": {

        "observables":

            baseline_reference["observables"],

        "all_monotonic":

            baseline_reference["all_monotonic"],

        "all_gamma_sensitive":

            baseline_reference["all_gamma_sensitive"],

        "all_omega_neutral":

            baseline_reference["all_omega_neutral"],

        "baseline_valid":

            baseline_reference["baseline_valid"],

    },

    "global_indicators":

        global_indicators,

    "future_use": {

        "comparison_target":

            "Family 2+",

        "mandatory_metrics": [

            "amplitude",

            "dynamic_range",

            "coefficient_variation",

            "gamma_sensitivity",

            "omega_response",

            "monotonicity",

        ],

    },

    "approved":

        bool(summary["baseline_ready"]),

}

# ------------------------------------------------------------
# JSON
# ------------------------------------------------------------

save_json(

    certificate,

    OUTPUT_DIR /
    "baseline_certificate.json",

)

# ------------------------------------------------------------
# TXT
# ------------------------------------------------------------

lines = []

lines.append("=" * 72)
lines.append("FAMILY 1 BASELINE CERTIFICATE")
lines.append("=" * 72)
lines.append("")

lines.append(f"Experiment : {certificate['experiment']}")
lines.append(f"Family     : {certificate['family']}")
lines.append(f"Operator   : {certificate['operator']}")
lines.append(f"Status     : {certificate['status']}")
lines.append("")

lines.append("Reference")
lines.append("---------")

for key, value in certificate["reference"].items():

    lines.append(f"{key:28} {value}")

lines.append("")
lines.append("Global Indicators")
lines.append("-----------------")

for key, value in global_indicators.items():

    lines.append(f"{key:28} {value}")

lines.append("")
lines.append("Mandatory Comparison Metrics")
lines.append("----------------------------")

for metric in certificate["future_use"]["mandatory_metrics"]:

    lines.append(f"- {metric}")

lines.append("")
lines.append("Decision")
lines.append("--------")

lines.append(

    "BASELINE APPROVED"

    if certificate["approved"]

    else

    "BASELINE NOT APPROVED"

)

lines.append("")
lines.append("=" * 72)

with open(

    OUTPUT_DIR /
    "baseline_certificate.txt",

    "w",

) as f:

    f.write("\n".join(lines))

# ------------------------------------------------------------
# Markdown
# ------------------------------------------------------------

md = []

md.append("# Family 1 Baseline")
md.append("")
md.append("## Operator")
md.append("")
md.append(f"`{certificate['operator']}`")
md.append("")
md.append("## Reference")

for key, value in certificate["reference"].items():

    md.append(f"- **{key}**: {value}")

md.append("")
md.append("## Global Indicators")

for key, value in global_indicators.items():

    md.append(f"- **{key}**: {value}")

md.append("")
md.append("## Mandatory Metrics")

for metric in certificate["future_use"]["mandatory_metrics"]:

    md.append(f"- {metric}")

md.append("")
md.append("## Decision")
md.append("")

md.append(

    "**BASELINE APPROVED**"

    if certificate["approved"]

    else

    "**BASELINE NOT APPROVED**"

)

with open(

    OUTPUT_DIR /
    "baseline_certificate.md",

    "w",

) as f:

    f.write("\n".join(md))

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print(json.dumps(

    certificate,

    indent=4,

))

print()

print("Files generated")

print("- baseline_certificate.json")
print("- baseline_certificate.txt")
print("- baseline_certificate.md")

print()

print("Part 4 completed.")

# ============================================================
# PART 5
# CAMPAIGN MANIFEST + FINAL AUDIT
# ============================================================

print()
print("=" * 80)
print("PART 5 - CAMPAIGN MANIFEST")
print("=" * 80)
print()

# ------------------------------------------------------------
# Metadata
# ------------------------------------------------------------

metadata = {

    "experiment":

        "E10.1.6",

    "title":

        "Family 1 Baseline",

    "family":

        "Family 1",

    "operator":

        "U(gamma) = (1 + gamma) I",

    "created_at":

        datetime.utcnow().isoformat(),

    "output_directory":

        str(OUTPUT_DIR),

}

save_json(

    metadata,

    OUTPUT_DIR /
    "metadata.json",

)

# ------------------------------------------------------------
# Campaign Manifest
# ------------------------------------------------------------

generated_files = sorted(

    [

        p.name

        for p in OUTPUT_DIR.iterdir()

        if p.is_file()

    ]

)

manifest = {

    "experiment":

        "E10.1.6",

    "status":

        "COMPLETED",

    "generated_files":

        generated_files,

    "total_files":

        len(generated_files),

}

save_json(

    manifest,

    OUTPUT_DIR /
    "campaign_manifest.json",

)

# ------------------------------------------------------------
# Final Audit
# ------------------------------------------------------------

audit = []

for filename in generated_files:

    path = OUTPUT_DIR / filename

    audit.append({

        "file":

            filename,

        "exists":

            path.exists(),

        "size_bytes":

            path.stat().st_size,

    })

audit = pd.DataFrame(audit)

audit.to_csv(

    OUTPUT_DIR /
    "final_audit.csv",

    index=False,

)

# ------------------------------------------------------------
# Execution Summary
# ------------------------------------------------------------

summary_lines = []

summary_lines.append("=" * 72)
summary_lines.append("E10.1.6 - FAMILY 1 BASELINE")
summary_lines.append("=" * 72)
summary_lines.append("")
summary_lines.append("Campaign completed successfully.")
summary_lines.append("")
summary_lines.append("Family 1 has been frozen as the")
summary_lines.append("official baseline of the E10.")
summary_lines.append("")
summary_lines.append("Future operator families shall")
summary_lines.append("be compared against this")
summary_lines.append("reference baseline.")
summary_lines.append("")
summary_lines.append("Generated files")
summary_lines.append("----------------")

for filename in generated_files:

    summary_lines.append(f"- {filename}")

summary_lines.append("")
summary_lines.append("=" * 72)

with open(

    OUTPUT_DIR /
    "execution_summary.txt",

    "w",

) as f:

    f.write("\n".join(summary_lines))

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print(audit)

print()

print(

    "Campaign complete :",

    audit["exists"].all(),

)

print()

print("Output directory")

print(OUTPUT_DIR)

print()

print("=" * 80)
print("E10.1.6 FINISHED")
print("=" * 80)
print()

print("Experiment completed successfully.")
