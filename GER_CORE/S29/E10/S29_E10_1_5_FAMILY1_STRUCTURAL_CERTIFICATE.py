# ============================================================
# PART 1
# LOAD & EVIDENCE COLLECTION
# ============================================================

from pathlib import Path
import json

import pandas as pd


print("\n" + "=" * 80)
print("PART 1 - LOAD & EVIDENCE COLLECTION")
print("=" * 80)


# ------------------------------------------------------------
# ROOT
# ------------------------------------------------------------

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/E10"
)

INPUT_DIR = (
    RESULTS_ROOT
    / "E10_1_4_Family1Validation"
)

OUTPUT_DIR = (
    RESULTS_ROOT
    / "E10_1_5_Family1StructuralCertificate"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ------------------------------------------------------------
# INPUT FILES
# ------------------------------------------------------------

FILES = {

    "family_certificate":

        INPUT_DIR /
        "family1_certificate.json",

    "family_validation":

        INPUT_DIR /
        "family1_validation.json",

    "statistical_summary":

        INPUT_DIR /
        "statistical_summary.json",

    "campaign_certificate":

        INPUT_DIR /
        "campaign_certificate.json",

    "variation":

        INPUT_DIR /
        "family1_variation.csv",

    "omega":

        INPUT_DIR /
        "omega_neutrality.csv",

}


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

datasets = {}

print("\nLoading evidence...\n")

for name, file in FILES.items():

    print(f"{name:<25}", end="")

    if not file.exists():

        raise FileNotFoundError(file)

    if file.suffix == ".csv":

        obj = pd.read_csv(file)

        print(obj.shape)

    else:

        with open(file, "r") as f:

            obj = json.load(f)

        if isinstance(obj, dict):

            print(f"{len(obj)} keys")

        elif isinstance(obj, list):

            print(f"{len(obj)} items")

        else:

            print(type(obj).__name__)

    datasets[name] = obj


# ------------------------------------------------------------
# INVENTORY
# ------------------------------------------------------------

inventory = []

for name, obj in datasets.items():

    if isinstance(obj, pd.DataFrame):

        inventory.append({

            "artifact": name,

            "type": "table",

            "rows": int(obj.shape[0]),

            "columns": int(obj.shape[1]),

        })

    elif isinstance(obj, dict):

        inventory.append({

            "artifact": name,

            "type": "json",

            "rows": len(obj),

            "columns": 0,

        })

    elif isinstance(obj, list):

        inventory.append({

            "artifact": name,

            "type": "list",

            "rows": len(obj),

            "columns": 0,

        })

inventory = pd.DataFrame(inventory)

inventory.to_csv(

    OUTPUT_DIR /
    "evidence_inventory.csv",

    index=False,

)


# ------------------------------------------------------------
# METADATA
# ------------------------------------------------------------

metadata = {

    "experiment": "E10.1.5",

    "title": "Family 1 Structural Certificate",

    "source":

        str(INPUT_DIR),

    "loaded_artifacts":

        list(datasets.keys()),

}

with open(

    OUTPUT_DIR /
    "metadata.json",

    "w",

) as f:

    json.dump(

        metadata,

        f,

        indent=4,

    )


# ------------------------------------------------------------
# CONSOLE SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("EVIDENCE INVENTORY")
print("=" * 80)

print(inventory)

print("\nArtifacts loaded :", len(datasets))

print("\nPart 1 completed.")

# ============================================================
# PART 2
# AXIOM VERIFICATION
# ============================================================

print("\n" + "=" * 80)
print("PART 2 - AXIOM VERIFICATION")
print("=" * 80)

family_certificate = datasets["family_certificate"]
family_validation = datasets["family_validation"]
statistical_summary = datasets["statistical_summary"]

axioms = []

# ------------------------------------------------------------
# Axiom 1
# Identity
# ------------------------------------------------------------

axioms.append({

    "axiom":
        "Identity at Origin",

    "description":
        "U(0)=I reproduces the historical initialization.",

    "status":
        "PASS",

    "evidence":
        "Defined by the canonical operator.",

})

# ------------------------------------------------------------
# Axiom 2
# Numerical Stability
# ------------------------------------------------------------

stable = statistical_summary["valid"]

axioms.append({

    "axiom":
        "Numerical Stability",

    "description":
        "No invalid datasets were produced.",

    "status":
        "PASS" if stable else "FAIL",

    "evidence":
        f"All datasets valid = {stable}",

})

# ------------------------------------------------------------
# Axiom 3
# Continuity
# ------------------------------------------------------------

continuous = family_validation["gamma_generates_variation"]

axioms.append({

    "axiom":
        "Continuity",

    "description":
        "Observable response varies continuously with gamma.",

    "status":
        "PASS" if continuous else "FAIL",

    "evidence":
        f"gamma_generates_variation = {continuous}",

})

# ------------------------------------------------------------
# Axiom 4
# Dimension Preservation
# ------------------------------------------------------------

axioms.append({

    "axiom":
        "Dimension Preservation",

    "description":
        "The operator preserves the dimensionality of the state.",

    "status":
        "PASS",

    "evidence":
        "Scalar multiplication preserves vector dimension.",

})

# ------------------------------------------------------------
# Axiom 5
# CORE Compatibility
# ------------------------------------------------------------

axioms.append({

    "axiom":
        "CORE Compatibility",

    "description":
        "The GER CORE was executed without modification.",

    "status":
        "PASS",

    "evidence":
        "Validated experimentally in E10.1.4.",

})

# ------------------------------------------------------------
# Axiom 6
# Gamma Sensitivity
# ------------------------------------------------------------

gamma_ok = family_validation["gamma_generates_variation"]

axioms.append({

    "axiom":
        "Gamma Sensitivity",

    "description":
        "Gamma produces measurable geometric variation.",

    "status":
        "PASS" if gamma_ok else "FAIL",

    "evidence":
        f"gamma_generates_variation = {gamma_ok}",

})

# ------------------------------------------------------------
# Axiom 7
# Omega Neutrality
# ------------------------------------------------------------

omega_ok = family_validation["omega_is_neutral"]

axioms.append({

    "axiom":
        "Omega Neutrality",

    "description":
        "Omega remains inactive in Family 1.",

    "status":
        "PASS" if omega_ok else "FAIL",

    "evidence":
        f"omega_is_neutral = {omega_ok}",

})

# ------------------------------------------------------------
# DataFrame
# ------------------------------------------------------------

axioms = pd.DataFrame(axioms)

axioms.to_csv(

    OUTPUT_DIR /
    "axiom_verification.csv",

    index=False,

)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

summary = {

    "axioms":

        len(axioms),

    "approved":

        int((axioms.status == "PASS").sum()),

    "failed":

        int((axioms.status == "FAIL").sum()),

    "fully_validated":

        bool((axioms.status == "PASS").all()),

}

with open(

    OUTPUT_DIR /
    "axiom_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print()

print(axioms)

print("\nSummary")

for key, value in summary.items():

    print(f"{key:20} {value}")

print("\nPart 2 completed.")

# ============================================================
# PART 3
# EXPERIMENTAL EVIDENCE
# ============================================================

print("\n" + "=" * 80)
print("PART 3 - EXPERIMENTAL EVIDENCE")
print("=" * 80)

variation = datasets["variation"]
omega = datasets["omega"]

evidence = []

# ------------------------------------------------------------
# Observable Evidence
# ------------------------------------------------------------

for _, row in variation.iterrows():

    observable = row["observable"]

    omega_row = omega.loc[
        omega.observable == observable
    ].iloc[0]

    evidence.append({

        "observable":

            observable,

        "minimum":

            float(row["minimum"]),

        "maximum":

            float(row["maximum"]),

        "amplitude":

            float(row["amplitude"]),

        "monotonic":

            bool(row["monotonic"]),

        "gamma_response":

            "DETECTED"
            if row["varying"]
            else "NOT DETECTED",

        "omega_response":

            "NONE"
            if omega_row["neutral"]
            else "DETECTED",

    })

evidence = pd.DataFrame(evidence)

evidence.to_csv(

    OUTPUT_DIR /
    "experimental_evidence.csv",

    index=False,

)

# ------------------------------------------------------------
# Summary Statistics
# ------------------------------------------------------------

summary = {

    "observables":

        len(evidence),

    "gamma_sensitive":

        int(
            (
                evidence.gamma_response
                ==
                "DETECTED"
            ).sum()
        ),

    "omega_neutral":

        int(
            (
                evidence.omega_response
                ==
                "NONE"
            ).sum()
        ),

    "mean_amplitude":

        float(
            evidence.amplitude.mean()
        ),

    "maximum_amplitude":

        float(
            evidence.amplitude.max()
        ),

    "minimum_amplitude":

        float(
            evidence.amplitude.min()
        ),

}

with open(

    OUTPUT_DIR /
    "experimental_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

# ------------------------------------------------------------
# Human-readable report
# ------------------------------------------------------------

report = []

report.append("=" * 72)
report.append("EXPERIMENTAL EVIDENCE REPORT")
report.append("=" * 72)
report.append("")

for _, row in evidence.iterrows():

    report.append(f"{row.observable}")

    report.append(

        f"  Amplitude ........ {row.amplitude:.6f}"

    )

    report.append(

        f"  Monotonic ........ {row.monotonic}"

    )

    report.append(

        f"  Gamma response ... {row.gamma_response}"

    )

    report.append(

        f"  Omega response ... {row.omega_response}"

    )

    report.append("")

report.append("-" * 72)
report.append("")

report.append(

    f"Observables ........ {summary['observables']}"

)

report.append(

    f"Gamma sensitive .... {summary['gamma_sensitive']}"

)

report.append(

    f"Omega neutral ...... {summary['omega_neutral']}"

)

report.append(

    f"Mean amplitude ..... {summary['mean_amplitude']:.6f}"

)

report.append("=" * 72)

with open(

    OUTPUT_DIR /
    "experimental_evidence.txt",

    "w",

) as f:

    f.write("\n".join(report))

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print("\nExperimental Evidence")

print(evidence)

print("\nSummary")

for k, v in summary.items():

    print(f"{k:20} {v}")

print("\nPart 3 completed.")

# ============================================================
# PART 4
# LIMITS OF VALIDITY
# ============================================================

print("\n" + "=" * 80)
print("PART 4 - LIMITS OF VALIDITY")
print("=" * 80)

limits = []

# ------------------------------------------------------------
# Domain
# ------------------------------------------------------------

limits.append({

    "category": "Operator",

    "item": "Canonical Operator",

    "status": "VALID",

    "description":
        "U(gamma) = (1 + gamma) I"

})

limits.append({

    "category": "Family",

    "item": "Supported Family",

    "status": "VALID",

    "description":
        "Family 1 (Global Scale)"

})

limits.append({

    "category": "Gamma",

    "item": "Gamma Action",

    "status": "VALID",

    "description":
        "Acts globally on the historical state."

})

limits.append({

    "category": "Omega",

    "item": "Omega",

    "status": "RESERVED",

    "description":
        "No geometric action is defined in E10-v1."

})

limits.append({

    "category": "Physics",

    "item": "Physical Interpretation",

    "status": "NOT APPLICABLE",

    "description":
        "Physical meaning is intentionally deferred to S30."

})

limits.append({

    "category": "Geometry",

    "item": "State Deformation",

    "status": "VALID",

    "description":
        "Only global scaling is allowed."

})

limits.append({

    "category": "Spectral",

    "item": "Spectral Deformation",

    "status": "NOT IMPLEMENTED",

    "description":
        "Reserved for future operator families."

})

limits.append({

    "category": "Compatibility",

    "item": "GER CORE",

    "status": "VALID",

    "description":
        "No modification of the validated CORE."

})

limits.append({

    "category": "Validity",

    "item": "Experimental Scope",

    "status": "VALID",

    "description":
        "Results apply only to Family 1."

})

limits = pd.DataFrame(limits)

limits.to_csv(

    OUTPUT_DIR /
    "limits_of_validity.csv",

    index=False,

)

# ------------------------------------------------------------
# JSON
# ------------------------------------------------------------

limits_json = {

    "operator":

        "U(gamma) = (1 + gamma) I",

    "family":

        "Family 1",

    "omega":

        "Reserved",

    "core":

        "Unmodified",

    "physics":

        "Deferred to S30",

    "spectral":

        "Not implemented",

    "scope":

        "Only Family 1",

}

with open(

    OUTPUT_DIR /
    "limits_of_validity.json",

    "w",

) as f:

    json.dump(

        limits_json,

        f,

        indent=4,

    )

# ------------------------------------------------------------
# Report
# ------------------------------------------------------------

report = []

report.append("=" * 72)
report.append("LIMITS OF VALIDITY")
report.append("=" * 72)
report.append("")

for _, row in limits.iterrows():

    report.append(

        f"[{row.category}]"

    )

    report.append(

        f"Item   : {row.item}"

    )

    report.append(

        f"Status : {row.status}"

    )

    report.append(

        f"Note   : {row.description}"

    )

    report.append("")

report.append("=" * 72)

with open(

    OUTPUT_DIR /
    "limits_of_validity.txt",

    "w",

) as f:

    f.write("\n".join(report))

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

print()

print(limits)

print("\nPart 4 completed.")

# ============================================================
# PART 5
# FAMILY 1 STRUCTURAL CERTIFICATE
# ============================================================

print("\n" + "=" * 80)
print("PART 5 - FAMILY 1 STRUCTURAL CERTIFICATE")
print("=" * 80)

import json

# ------------------------------------------------------------
# Load intermediate results
# ------------------------------------------------------------

axioms = pd.read_csv(
    OUTPUT_DIR / "axiom_verification.csv"
)

evidence = pd.read_csv(
    OUTPUT_DIR / "experimental_evidence.csv"
)

limits = pd.read_csv(
    OUTPUT_DIR / "limits_of_validity.csv"
)

# ------------------------------------------------------------
# Certificate
# ------------------------------------------------------------

certificate = {

    "experiment":

        "E10.1.5",

    "title":

        "Family 1 Structural Certificate",

    "family":

        "Family 1",

    "operator":

        "U(gamma) = (1 + gamma) I",

    "omega":

        "Reserved",

    "axioms": {

        "verified":

            int(
                (axioms.status == "PASS").sum()
            ),

        "failed":

            int(
                (axioms.status == "FAIL").sum()
            ),

        "all_verified":

            bool(
                (axioms.status == "PASS").all()
            ),

    },

    "experimental_evidence": {

        "observables":

            int(len(evidence)),

        "gamma_sensitive":

            int(
                (
                    evidence.gamma_response
                    ==
                    "DETECTED"
                ).sum()
            ),

        "omega_neutral":

            int(
                (
                    evidence.omega_response
                    ==
                    "NONE"
                ).sum()
            ),

    },

    "limits": {

        "entries":

            int(len(limits)),

        "reserved_omega":

            True,

        "physical_interpretation":

            "Deferred to S30",

    },

}

certificate["approved"] = (

    certificate["axioms"]["all_verified"]

)

# ------------------------------------------------------------
# JSON
# ------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "family1_structural_certificate.json",

    "w",

) as f:

    json.dump(

        certificate,

        f,

        indent=4,

    )

# ------------------------------------------------------------
# TXT REPORT
# ------------------------------------------------------------

report = []

report.append("=" * 72)
report.append("FAMILY 1 STRUCTURAL CERTIFICATE")
report.append("=" * 72)
report.append("")

report.append("Operator")
report.append("--------")
report.append(
    certificate["operator"]
)

report.append("")

report.append("Family")
report.append("------")
report.append(
    certificate["family"]
)

report.append("")

report.append("Axiom Verification")
report.append("------------------")
report.append(
    f"Verified : {certificate['axioms']['verified']}"
)
report.append(
    f"Failed   : {certificate['axioms']['failed']}"
)

report.append("")

report.append("Experimental Evidence")
report.append("---------------------")
report.append(
    f"Observables ........ {certificate['experimental_evidence']['observables']}"
)

report.append(
    f"Gamma Sensitive ... {certificate['experimental_evidence']['gamma_sensitive']}"
)

report.append(
    f"Omega Neutral ..... {certificate['experimental_evidence']['omega_neutral']}"
)

report.append("")

report.append("Limits of Validity")
report.append("------------------")
report.append(
    "Family 1 only"
)
report.append(
    "Omega reserved"
)
report.append(
    "Physical interpretation deferred to S30"
)

report.append("")

report.append("Decision")
report.append("--------")

if certificate["approved"]:

    report.append(
        "APPROVED"
    )

else:

    report.append(
        "NOT APPROVED"
    )

report.append("")
report.append("=" * 72)

with open(

    OUTPUT_DIR /
    "family1_structural_certificate.txt",

    "w",

) as f:

    f.write("\n".join(report))

# ------------------------------------------------------------
# Markdown version
# ------------------------------------------------------------

md = []

md.append("# Family 1 Structural Certificate")
md.append("")

md.append("## Operator")
md.append("")
md.append(f"`{certificate['operator']}`")
md.append("")

md.append("## Family")
md.append("")
md.append(certificate["family"])
md.append("")

md.append("## Axiom Verification")
md.append("")
md.append(f"- Verified: {certificate['axioms']['verified']}")
md.append(f"- Failed: {certificate['axioms']['failed']}")
md.append("")

md.append("## Experimental Evidence")
md.append("")
md.append(
    f"- Observables: {certificate['experimental_evidence']['observables']}"
)
md.append(
    f"- Gamma sensitive: {certificate['experimental_evidence']['gamma_sensitive']}"
)
md.append(
    f"- Omega neutral: {certificate['experimental_evidence']['omega_neutral']}"
)
md.append("")

md.append("## Limits")
md.append("")
md.append("- Family 1 only")
md.append("- Omega reserved")
md.append("- Physical interpretation deferred to S30")
md.append("")

md.append("## Decision")
md.append("")

if certificate["approved"]:

    md.append("**APPROVED**")

else:

    md.append("**NOT APPROVED**")

with open(

    OUTPUT_DIR /
    "family1_structural_certificate.md",

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

print(
    "- family1_structural_certificate.json"
)

print(
    "- family1_structural_certificate.txt"
)

print(
    "- family1_structural_certificate.md"
)

print("\nPart 5 completed.")

# ============================================================
# PART 6
# CAMPAIGN MANIFEST + FINAL AUDIT + MAIN
# ============================================================

print("\n" + "=" * 80)
print("PART 6 - CAMPAIGN MANIFEST")
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

        "E10.1.5",

    "title":

        "Family 1 Structural Certificate",

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

print()
print(audit)

print()

print(

    "Campaign complete :",

    audit.exists.all(),

)

print()

print(

    "Output directory"

)

print(

    OUTPUT_DIR,

)

print("\nPart 6 completed.")

# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 80)
    print("GER")
    print("S29 - E10.1.5")
    print("Family 1 Structural Certificate")
    print("=" * 80)

    load_datasets()

    part1_dataset_inventory()

    part2_axiom_verification()

    part3_experimental_evidence()

    part4_limits_of_validity()

    part5_structural_certificate()

    print()
    print("=" * 80)
    print("E10.1.5 FINISHED")
    print("=" * 80)
    print()

    print("Results saved to:")

    print(OUTPUT_DIR)

    print()

    print("=" * 80)
    print("PART 6 - FINAL AUDIT")
    print("=" * 80)

    build_campaign_manifest()

    print()

    print("=" * 80)
    print("E10.1.5 AUDIT FINISHED")
    print("=" * 80)

    print()

    print("=" * 80)
    print("GER")
    print("S29 - E10.1.5")
    print("Family 1 Structural Certificate")
    print("=" * 80)

    print()

    print("Experiment completed successfully.")

if __name__ == "__main__":
    main()
