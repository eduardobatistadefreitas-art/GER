# ============================================================
# PART 1
# LOAD BASELINE DATASETS
# ============================================================

print("\n" + "=" * 80)
print("PART 1 - LOAD BASELINE DATASETS")
print("=" * 80)

print("\nLoading Family 1 reference datasets...\n")

datasets = {}

# ------------------------------------------------------------
# Previous experiments
# ------------------------------------------------------------

datasets["family_validation"] = load_json(
    E10_1_4_DIR / "family1_validation.json"
)

datasets["family_certificate"] = load_json(
    E10_1_4_DIR / "family1_certificate.json"
)

datasets["structural_certificate"] = load_json(
    E10_1_5_DIR /
    "family1_structural_certificate.json"
)

datasets["statistical_summary"] = load_json(
    E10_1_4_DIR /
    "statistical_summary.json"
)

datasets["variation"] = pd.read_csv(
    E10_1_4_DIR /
    "family1_variation.csv"
)

datasets["omega"] = pd.read_csv(
    E10_1_4_DIR /
    "omega_neutrality.csv"
)

datasets["axioms"] = pd.read_csv(
    E10_1_5_DIR /
    "axiom_verification.csv"
)

datasets["experimental"] = pd.read_csv(
    E10_1_5_DIR /
    "experimental_evidence.csv"
)

datasets["limits"] = pd.read_csv(
    E10_1_5_DIR /
    "limits_of_validity.csv"
)

# ------------------------------------------------------------
# Inventory
# ------------------------------------------------------------

inventory = []

for name, obj in datasets.items():

    if isinstance(obj, pd.DataFrame):

        rows, cols = obj.shape

        inventory.append({

            "dataset": name,

            "type": "table",

            "rows": rows,

            "columns": cols,

        })

        print(f"{name:25} {obj.shape}")

    else:

        inventory.append({

            "dataset": name,

            "type": "json",

            "rows": len(obj),

            "columns": 0,

        })

        print(f"{name:25} {len(obj)} keys")

inventory = pd.DataFrame(inventory)

inventory.to_csv(

    OUTPUT_DIR /
    "baseline_inventory.csv",

    index=False,

)

print("\n" + "=" * 80)
print("BASELINE INVENTORY")
print("=" * 80)

print(inventory)

print()

print(

    "Artifacts loaded :",

    len(inventory),

)

print("\nPart 1 completed.")

# ============================================================
# PART 2
# BASELINE CONSOLIDATION
# ============================================================

print("\n" + "=" * 80)
print("PART 2 - BASELINE CONSOLIDATION")
print("=" * 80)

baseline = {}

# ------------------------------------------------------------
# Family identity
# ------------------------------------------------------------

baseline["family"] = "Family 1"

baseline["operator"] = "U(gamma) = (1 + gamma) I"

baseline["omega"] = "Reserved"

# ------------------------------------------------------------
# Experimental status
# ------------------------------------------------------------

baseline["family_validated"] = bool(

    datasets["family_validation"][
        "family1_consistent"
    ]

)

baseline["certificate_approved"] = bool(

    datasets["structural_certificate"][
        "approved"
    ]

)

baseline["axioms_verified"] = int(

    (
        datasets["axioms"]["status"]
        ==
        "PASS"
    ).sum()

)

baseline["axioms_total"] = int(

    len(
        datasets["axioms"]
    )

)

# ------------------------------------------------------------
# Experimental evidence
# ------------------------------------------------------------

baseline["observables"] = int(

    len(
        datasets["experimental"]
    )

)

baseline["gamma_sensitive"] = int(

    (
        datasets["experimental"][
            "gamma_response"
        ]
        ==
        "DETECTED"
    ).sum()

)

baseline["omega_neutral"] = int(

    (
        datasets["experimental"][
            "omega_response"
        ]
        ==
        "NONE"
    ).sum()

)

# ------------------------------------------------------------
# Variation statistics
# ------------------------------------------------------------

variation = datasets["variation"]

baseline["maximum_amplitude"] = float(

    variation.amplitude.max()

)

baseline["minimum_amplitude"] = float(

    variation.amplitude.min()

)

baseline["mean_amplitude"] = float(

    variation.amplitude.mean()

)

baseline["all_monotonic"] = bool(

    variation.monotonic.all()

)

# ------------------------------------------------------------
# Final status
# ------------------------------------------------------------

baseline["baseline_ready"] = (

    baseline["family_validated"]

    and

    baseline["certificate_approved"]

    and

    baseline["all_monotonic"]

)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "baseline_summary.json",

    "w",

) as f:

    json.dump(

        baseline,

        f,

        indent=4,

    )

baseline_df = pd.DataFrame(

    [

        {

            "property": k,

            "value": v,

        }

        for k, v in baseline.items()

    ]

)

baseline_df.to_csv(

    OUTPUT_DIR /
    "baseline_summary.csv",

    index=False,

)

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print()

print(json.dumps(

    baseline,

    indent=4,

))

print()

print("Baseline ready :", baseline["baseline_ready"])

print("\nPart 2 completed.")

# ============================================================
# PART 3
# BASELINE METRICS
# ============================================================

print("\n" + "=" * 80)
print("PART 3 - BASELINE METRICS")
print("=" * 80)

variation = datasets["variation"]
experimental = datasets["experimental"]

baseline_metrics = []

# ------------------------------------------------------------
# Observable reference
# ------------------------------------------------------------

for _, row in variation.iterrows():

    observable = row["observable"]

    exp = experimental.loc[
        experimental.observable == observable
    ].iloc[0]

    baseline_metrics.append({

        "observable":

            observable,

        "baseline_amplitude":

            float(row["amplitude"]),

        "baseline_minimum":

            float(row["minimum"]),

        "baseline_maximum":

            float(row["maximum"]),

        "baseline_monotonic":

            bool(row["monotonic"]),

        "gamma_sensitive":

            exp["gamma_response"] == "DETECTED",

        "omega_neutral":

            exp["omega_response"] == "NONE",

    })

baseline_metrics = pd.DataFrame(

    baseline_metrics

)

baseline_metrics.to_csv(

    OUTPUT_DIR /
    "baseline_metrics.csv",

    index=False,

)

# ------------------------------------------------------------
# Reference values
# ------------------------------------------------------------

reference = {

    "operator":

        "Family 1",

    "observables":

        len(baseline_metrics),

    "all_monotonic":

        bool(
            baseline_metrics[
                "baseline_monotonic"
            ].all()
        ),

    "all_gamma_sensitive":

        bool(
            baseline_metrics[
                "gamma_sensitive"
            ].all()
        ),

    "all_omega_neutral":

        bool(
            baseline_metrics[
                "omega_neutral"
            ].all()
        ),

    "mean_amplitude":

        float(
            baseline_metrics[
                "baseline_amplitude"
            ].mean()
        ),

    "max_amplitude":

        float(
            baseline_metrics[
                "baseline_amplitude"
            ].max()
        ),

    "min_amplitude":

        float(
            baseline_metrics[
                "baseline_amplitude"
            ].min()
        ),

}

with open(

    OUTPUT_DIR /
    "baseline_reference.json",

    "w",

) as f:

    json.dump(

        reference,

        f,

        indent=4,

    )

# ------------------------------------------------------------
# Human-readable report
# ------------------------------------------------------------

report = []

report.append("=" * 72)
report.append("BASELINE METRICS")
report.append("=" * 72)
report.append("")

for _, row in baseline_metrics.iterrows():

    report.append(row.observable)

    report.append(
        f"Amplitude : {row.baseline_amplitude:.6f}"
    )

    report.append(
        f"Monotonic : {row.baseline_monotonic}"
    )

    report.append(
        f"Gamma     : {row.gamma_sensitive}"
    )

    report.append(
        f"Omega     : {row.omega_neutral}"
    )

    report.append("")

report.append("-" * 72)
report.append("")

for key, value in reference.items():

    report.append(

        f"{key:24} {value}"

    )

with open(

    OUTPUT_DIR /
    "baseline_metrics.txt",

    "w",

) as f:

    f.write("\n".join(report))

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print()

print(baseline_metrics)

print()

print(json.dumps(

    reference,

    indent=4,

))

print()

print("Part 3 completed.")

# ============================================================
# PART 4
# BASELINE CERTIFICATE
# ============================================================

print("\n" + "=" * 80)
print("PART 4 - BASELINE CERTIFICATE")
print("=" * 80)

reference = load_json(
    OUTPUT_DIR / "baseline_reference.json"
)

summary = load_json(
    OUTPUT_DIR / "baseline_summary.json"
)

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

        "BASELINE",

    "reference": {

        "observables":

            reference["observables"],

        "all_monotonic":

            reference["all_monotonic"],

        "all_gamma_sensitive":

            reference["all_gamma_sensitive"],

        "all_omega_neutral":

            reference["all_omega_neutral"],

        "mean_amplitude":

            reference["mean_amplitude"],

    },

    "comparison_rules": {

        "future_families":

            "Must be compared against this baseline.",

        "required_metrics": [

            "amplitude",

            "gamma sensitivity",

            "omega response",

            "monotonicity",

        ],

    },

    "approved":

        bool(summary["baseline_ready"]),

}

# ------------------------------------------------------------
# Save JSON
# ------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "baseline_certificate.json",

    "w",

) as f:

    json.dump(

        certificate,

        f,

        indent=4,

    )

# ------------------------------------------------------------
# TXT
# ------------------------------------------------------------

report = []

report.append("=" * 72)
report.append("FAMILY 1 BASELINE CERTIFICATE")
report.append("=" * 72)
report.append("")

report.append(f"Experiment : {certificate['experiment']}")
report.append(f"Family     : {certificate['family']}")
report.append(f"Operator   : {certificate['operator']}")
report.append("")

report.append("Reference Properties")
report.append("--------------------")

for key, value in certificate["reference"].items():

    report.append(f"{key:24} {value}")

report.append("")
report.append("Comparison Rules")
report.append("----------------")

for metric in certificate["comparison_rules"]["required_metrics"]:

    report.append(f"- {metric}")

report.append("")
report.append("Decision")
report.append("--------")

report.append(

    "BASELINE APPROVED"

    if certificate["approved"]

    else

    "BASELINE NOT APPROVED"

)

report.append("")
report.append("=" * 72)

with open(

    OUTPUT_DIR /
    "baseline_certificate.txt",

    "w",

) as f:

    f.write("\n".join(report))

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

md.append("## Baseline Properties")
md.append("")

for key, value in certificate["reference"].items():

    md.append(f"- **{key}**: {value}")

md.append("")
md.append("## Comparison Rules")
md.append("")

for metric in certificate["comparison_rules"]["required_metrics"]:

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

print()

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

print("\n" + "=" * 80)
print("PART 5 - CAMPAIGN MANIFEST")
print("=" * 80)

from datetime import datetime

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

    "title":

        "Family 1 Baseline",

    "created_at":

        datetime.utcnow().isoformat(),

    "output_directory":

        str(OUTPUT_DIR),

    "generated_files":

        generated_files,

    "status":

        "COMPLETED",

}

with open(

    OUTPUT_DIR /
    "campaign_manifest.json",

    "w",

) as f:

    json.dump(

        manifest,

        f,

        indent=4,

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

summary = []

summary.append("=" * 72)
summary.append("E10.1.6 - FAMILY 1 BASELINE")
summary.append("=" * 72)
summary.append("")

summary.append("Campaign status")
summary.append("----------------")
summary.append("Completed successfully")
summary.append("")

summary.append("Baseline")
summary.append("--------")
summary.append("Family 1 frozen as official baseline.")
summary.append("")

summary.append("Future comparisons")
summary.append("------------------")
summary.append("- Family 2")
summary.append("- Family 3")
summary.append("- Family 4")
summary.append("- Higher-order operators")
summary.append("")

summary.append("Generated files")
summary.append("----------------")

for file in generated_files:

    summary.append(f"- {file}")

summary.append("")
summary.append("=" * 72)

with open(

    OUTPUT_DIR /
    "execution_summary.txt",

    "w",

) as f:

    f.write("\n".join(summary))

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print()

print(audit)

print()

print(

    "Campaign complete :",

    audit.exists.all(),

)

print()

print("Generated files")

for file in generated_files:

    print(" -", file)

print()

print("Output directory")

print(OUTPUT_DIR)

print()

print("Part 5 completed.")

# ============================================================
# PART 6
# MAIN
# ============================================================

def main():

    print()
    print("=" * 80)
    print("GER")
    print("S29 - E10.1.6")
    print("Family 1 Baseline")
    print("=" * 80)

    load_baseline_datasets()

    part1_load_baseline()

    part2_baseline_consolidation()

    part3_baseline_metrics()

    part4_baseline_certificate()

    print()
    print("=" * 80)
    print("E10.1.6 FINISHED")
    print("=" * 80)
    print()

    print("Results saved to:")

    print(OUTPUT_DIR)

    print()

    print("=" * 80)
    print("PART 5 - FINAL AUDIT")
    print("=" * 80)

    build_campaign_manifest()

    print()

    print("=" * 80)
    print("E10.1.6 AUDIT FINISHED")
    print("=" * 80)

    print()

    print("=" * 80)
    print("GER")
    print("S29 - E10.1.6")
    print("Family 1 Baseline")
    print("=" * 80)

    print()

    print("Experiment completed successfully.")


if __name__ == "__main__":
    main()
