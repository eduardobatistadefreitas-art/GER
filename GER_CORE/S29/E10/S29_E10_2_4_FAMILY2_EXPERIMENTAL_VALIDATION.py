"""
================================================================================
GER
S29 - E10.2.4
Family 2 Experimental Validation
================================================================================

Objective
---------
Experimentally validate the canonical Family 2 operator by comparing its
geometric behaviour against the official Family 1 baseline.

================================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from GER.CORE.ger_graph import gaussian_packet_family2
# ==============================================================================
# INPUT
# ==============================================================================

BASELINE_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_1_6_Family1Baseline"
)

IMPLEMENTATION_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_3_Family2OperatorImplementation"
)

# ==============================================================================
# OUTPUT
# ==============================================================================

OUTPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_4_Family2ExperimentalValidation"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==============================================================================
# PART 1
# LOAD REFERENCE DATA
# ==============================================================================

print()
print("=" * 80)
print("PART 1 - LOAD REFERENCE DATA")
print("=" * 80)
print()

print("Loading Family 1 baseline...")
print()

with open(
    BASELINE_DIR /
    "baseline_certificate.json",
    "r",
) as f:

    baseline_certificate = json.load(f)

baseline_reference = pd.read_csv(
    BASELINE_DIR /
    "baseline_reference.csv"
)

with open(
    BASELINE_DIR /
    "global_indicators.json",
    "r",
) as f:

    baseline_indicators = json.load(f)

print("Loading Family 2 implementation...")
print()

with open(
    IMPLEMENTATION_DIR /
    "implementation_certificate.json",
    "r",
) as f:

    implementation_certificate = json.load(f)

with open(
    IMPLEMENTATION_DIR /
    "compatibility_report.json",
    "r",
) as f:

    compatibility = json.load(f)

implementation_report = pd.read_csv(
    IMPLEMENTATION_DIR /
    "implementation_report.csv"
)

# ==============================================================================
# INVENTORY
# ==============================================================================

inventory = pd.DataFrame(

    [

        {
            "artifact": "baseline_certificate",
            "type": "json",
            "rows": len(baseline_certificate),
            "columns": 0,
        },

        {
            "artifact": "baseline_reference",
            "type": "table",
            "rows": len(baseline_reference),
            "columns": len(baseline_reference.columns),
        },

        {
            "artifact": "global_indicators",
            "type": "json",
            "rows": len(baseline_indicators),
            "columns": 0,
        },

        {
            "artifact": "implementation_certificate",
            "type": "json",
            "rows": len(implementation_certificate),
            "columns": 0,
        },

        {
            "artifact": "compatibility_report",
            "type": "json",
            "rows": len(compatibility),
            "columns": 0,
        },

        {
            "artifact": "implementation_report",
            "type": "table",
            "rows": len(implementation_report),
            "columns": len(implementation_report.columns),
        },

    ]

)

print(inventory)

print()

# ==============================================================================
# VALIDATION STATUS
# ==============================================================================

ready = (

    compatibility["implementation_valid"]

    and

    implementation_certificate["validation"]["implementation_valid"]

)

summary = {

    "family1_baseline":

        True,

    "family2_implemented":

        implementation_certificate["implementation_status"] == "IMPLEMENTED",

    "implementation_valid":

        compatibility["implementation_valid"],

    "experimental_validation_ready":

        ready,

}

print("=" * 80)
print("VALIDATION STATUS")
print("=" * 80)
print()

for key, value in summary.items():

    print(f"{key:30} {value}")

inventory.to_csv(

    OUTPUT_DIR /
    "validation_inventory.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "validation_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- validation_inventory.csv")
print("- validation_summary.json")

print()

print("Part 1 completed.")

# ==============================================================================
# PART 2
# FAMILY 2 EXPERIMENTAL CAMPAIGN
# ==============================================================================

print()
print("=" * 80)
print("PART 2 - FAMILY 2 EXPERIMENTAL CAMPAIGN")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Experimental grid
# ------------------------------------------------------------------------------

gamma_values = np.linspace(

    0.0,

    1.0,

    21,

)

omega_values = np.array([

    0.00,
    0.05,
    0.10,
    0.15,
    0.20,

])

theta = np.linspace(

    0.0,

    2.0 * np.pi,

    512,

)

records = []

print("Running experimental campaign...")
print()

for gamma in gamma_values:

    for omega in omega_values:

        signal = gaussian_packet(
            theta,
            sigma=0.10,
            omega=float(omega),
        )

        # ----------------------------------------------------------
        # Experimental observables
        # ----------------------------------------------------------

        diameter = float(

            np.sum(signal > 0.5)

        )

        convergence = float(

            np.sum(signal)

        )

        recurrence = float(

            np.mean(

                signal > np.mean(signal)

            )

        )

        drift = float(

            np.max(signal)

        )

        records.append({

            "gamma":

                float(gamma),

            "omega":

                float(omega),

            "diameter":

                diameter,

            "convergence":

                convergence,

            "recurrence":

                recurrence,

            "drift":

                drift,

        })

family2_surface = pd.DataFrame(records)

print(family2_surface.head())

print()

print("=" * 80)
print("EXPERIMENT SUMMARY")
print("=" * 80)
print()

summary = {

    "gamma_samples":

        len(gamma_values),

    "omega_samples":

        len(omega_values),

    "grid_size":

        len(family2_surface),

    "observables":

        4,

}

for key, value in summary.items():

    print(f"{key:24} {value}")

# ------------------------------------------------------------------------------
# Aggregate statistics
# ------------------------------------------------------------------------------

statistics = family2_surface[

    [

        "diameter",

        "convergence",

        "recurrence",

        "drift",

    ]

].describe()

print()
print(statistics)

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

family2_surface.to_csv(

    OUTPUT_DIR /
    "family2_response_surface.csv",

    index=False,

)

family2_surface.to_parquet(

    OUTPUT_DIR /
    "family2_response_surface.parquet",

    index=False,

)

statistics.to_csv(

    OUTPUT_DIR /
    "family2_statistics.csv",

)

with open(

    OUTPUT_DIR /
    "family2_campaign_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- family2_response_surface.csv")
print("- family2_response_surface.parquet")
print("- family2_statistics.csv")
print("- family2_campaign_summary.json")

print()

print("Part 2 completed.")

# ==============================================================================
# PART 3
# FAMILY 2 vs FAMILY 1
# ==============================================================================

print()
print("=" * 80)
print("PART 3 - FAMILY 2 vs FAMILY 1")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Baseline reference
# ------------------------------------------------------------------------------

baseline = {}

for _, row in baseline_reference.iterrows():

    baseline[row["observable"]] = {

        "minimum": row["minimum"],
        "maximum": row["maximum"],
        "amplitude": row["amplitude"],

    }

comparison = []

for observable in [

    "diameter",
    "convergence",
    "recurrence",
    "drift",

]:

    values = family2_surface[observable]

    minimum = float(values.min())

    maximum = float(values.max())

    amplitude = maximum - minimum

    reference = baseline[observable]

    delta = amplitude - reference["amplitude"]

    relative_gain = (

        delta /

        reference["amplitude"]

        if reference["amplitude"] > 0

        else np.nan

    )

    omega_sensitivity = float(

        family2_surface
        .groupby("omega")[observable]
        .mean()
        .std()

    )

    gamma_sensitivity = float(

        family2_surface
        .groupby("gamma")[observable]
        .mean()
        .std()

    )

    comparison.append({

        "observable":

            observable,

        "family1_amplitude":

            reference["amplitude"],

        "family2_amplitude":

            amplitude,

        "delta":

            delta,

        "relative_gain":

            relative_gain,

        "omega_sensitivity":

            omega_sensitivity,

        "gamma_sensitivity":

            gamma_sensitivity,

        "different_from_family1":

            abs(delta) > 1e-12,

    })

comparison = pd.DataFrame(comparison)

print(comparison)

print()

# ------------------------------------------------------------------------------
# Global comparison
# ------------------------------------------------------------------------------

summary = {

    "observables":

        len(comparison),

    "modified":

        int(

            comparison[
                "different_from_family1"
            ].sum()

        ),

    "mean_relative_gain":

        float(

            comparison[
                "relative_gain"
            ].mean()

        ),

    "mean_omega_sensitivity":

        float(

            comparison[
                "omega_sensitivity"
            ].mean()

        ),

    "mean_gamma_sensitivity":

        float(

            comparison[
                "gamma_sensitivity"
            ].mean()

        ),

}

print("=" * 80)
print("COMPARISON SUMMARY")
print("=" * 80)
print()

for key, value in summary.items():

    print(f"{key:28} {value}")

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

comparison.to_csv(

    OUTPUT_DIR /
    "family2_vs_family1.csv",

    index=False,

)

comparison.to_parquet(

    OUTPUT_DIR /
    "family2_vs_family1.parquet",

    index=False,

)

with open(

    OUTPUT_DIR /
    "family2_comparison_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- family2_vs_family1.csv")
print("- family2_vs_family1.parquet")
print("- family2_comparison_summary.json")

print()

print("Part 3 completed.")

# ==============================================================================
# PART 4
# FAMILY 2 VALIDATION
# ==============================================================================

print()
print("=" * 80)
print("PART 4 - FAMILY 2 VALIDATION")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Validation criteria
# ------------------------------------------------------------------------------

omega_effect = bool(

    comparison["omega_sensitivity"].max() > 0

)

family_distinction = bool(

    comparison["different_from_family1"].any()

)

stable_operator = bool(

    compatibility["implementation_valid"]

)

validation = {

    "experiment":

        "E10.2.4",

    "family":

        "Family 2",

    "operator":

        operator_definition["symbol"],

    "omega_effect_detected":

        omega_effect,

    "family_distinct_from_family1":

        family_distinction,

    "implementation_stable":

        stable_operator,

    "observables_modified":

        int(

            comparison[
                "different_from_family1"
            ].sum()

        ),

    "validated":

        bool(

            omega_effect
            and
            family_distinction
            and
            stable_operator

        ),

}

print(json.dumps(

    validation,

    indent=4,

))

print()

# ------------------------------------------------------------------------------
# Validation certificate
# ------------------------------------------------------------------------------

certificate = {

    "experiment":

        "E10.2.4",

    "title":

        "Family 2 Experimental Validation",

    "family":

        "Family 2",

    "operator":

        operator_definition["symbol"],

    "validation": validation,

    "scientific_conclusion":

        (
            "The Family 2 operator produces measurable geometric "
            "deformations while preserving compatibility with the "
            "validated GER CORE."
        )

        if validation["validated"]

        else

        (
            "Experimental evidence is currently insufficient "
            "to validate Family 2."
        ),

    "next_step":

        "E10.2.5 - Family 2 Structural Characterization",

}

print("=" * 80)
print("VALIDATION DECISION")
print("=" * 80)
print()

print(

    "Family 2 validated :",

    certificate["validation"]["validated"]

)

print()

# ------------------------------------------------------------------------------
# Human-readable certificate
# ------------------------------------------------------------------------------

lines = []

lines.append("=" * 72)
lines.append("FAMILY 2 EXPERIMENTAL VALIDATION")
lines.append("=" * 72)
lines.append("")

lines.append(f"Operator : {operator_definition['symbol']}")
lines.append("")

lines.append("Validation Criteria")
lines.append("-------------------")

lines.append(
    f"Omega effect detected        : {validation['omega_effect_detected']}"
)

lines.append(
    f"Distinct from Family 1       : {validation['family_distinct_from_family1']}"
)

lines.append(
    f"Implementation stable        : {validation['implementation_stable']}"
)

lines.append(
    f"Modified observables         : {validation['observables_modified']}"
)

lines.append("")

lines.append("Scientific Conclusion")
lines.append("---------------------")

lines.append(
    certificate["scientific_conclusion"]
)

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "family2_validation.json",

    "w",

) as f:

    json.dump(

        validation,

        f,

        indent=4,

    )

with open(

    OUTPUT_DIR /
    "validation_certificate.json",

    "w",

) as f:

    json.dump(

        certificate,

        f,

        indent=4,

    )

with open(

    OUTPUT_DIR /
    "family2_validation.txt",

    "w",

) as f:

    f.write("\n".join(lines))

with open(

    OUTPUT_DIR /
    "family2_validation.md",

    "w",

) as f:

    f.write("# Family 2 Experimental Validation\n\n")

    for line in lines[2:]:

        f.write(line + "\n")

print("Files generated")
print("- family2_validation.json")
print("- validation_certificate.json")
print("- family2_validation.txt")
print("- family2_validation.md")

print()
print("Part 4 completed.")

# ==============================================================================
# PART 5
# SCIENTIFIC REPORT
# ==============================================================================

print()
print("=" * 80)
print("PART 5 - SCIENTIFIC REPORT")
print("=" * 80)
print()

report = {

    "experiment":

        "E10.2.4",

    "title":

        "Family 2 Experimental Validation",

    "family":

        "Family 2",

    "operator":

        operator_definition["symbol"],

    "validation":

        validation,

    "comparison_summary":

        summary,

    "implementation":

        implementation,

    "scientific_conclusion":

        certificate["scientific_conclusion"],

    "next_experiment":

        "E10.2.5 - Family 2 Structural Characterization",

}

print(

    json.dumps(

        report,

        indent=4,

    )

)

print()

# ------------------------------------------------------------------------------
# Human-readable report
# ------------------------------------------------------------------------------

lines = []

lines.append("=" * 72)
lines.append("FAMILY 2 EXPERIMENTAL VALIDATION REPORT")
lines.append("=" * 72)
lines.append("")

lines.append(f"Experiment : {report['experiment']}")
lines.append(f"Family     : {report['family']}")
lines.append(f"Operator   : {report['operator']}")
lines.append("")

lines.append("Validation")
lines.append("----------")

lines.append(
    f"Validated                : {validation['validated']}"
)

lines.append(
    f"Implementation stable    : {validation['implementation_stable']}"
)

lines.append(
    f"Omega effect             : {validation['omega_effect_detected']}"
)

lines.append(
    f"Distinct from Family 1   : {validation['family_distinct_from_family1']}"
)

lines.append(
    f"Modified observables     : {validation['observables_modified']}"
)

lines.append("")

lines.append("Comparison Summary")
lines.append("------------------")

lines.append(
    f"Mean relative gain       : {summary['mean_relative_gain']:.6f}"
)

lines.append(
    f"Mean omega sensitivity   : {summary['mean_omega_sensitivity']:.6f}"
)

lines.append(
    f"Mean gamma sensitivity   : {summary['mean_gamma_sensitivity']:.6f}"
)

lines.append("")

lines.append("Scientific Conclusion")
lines.append("---------------------")

lines.append(
    report["scientific_conclusion"]
)

lines.append("")

lines.append("Next Experiment")
lines.append("---------------")

lines.append(
    report["next_experiment"]
)

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "family2_validation_report.json",

    "w",

) as f:

    json.dump(

        report,

        f,

        indent=4,

    )

with open(

    OUTPUT_DIR /
    "family2_validation_report.txt",

    "w",

) as f:

    f.write("\n".join(lines))

with open(

    OUTPUT_DIR /
    "family2_validation_report.md",

    "w",

) as f:

    f.write("# Family 2 Experimental Validation Report\n\n")

    for line in lines[2:]:

        f.write(line + "\n")

print("Files generated")
print("- family2_validation_report.json")
print("- family2_validation_report.txt")
print("- family2_validation_report.md")

print()

print("Part 5 completed.")

# ==============================================================================
# PART 6
# CAMPAIGN MANIFEST + FINAL AUDIT + MAIN
# ==============================================================================

from datetime import datetime, UTC

print()
print("=" * 80)
print("PART 6 - CAMPAIGN MANIFEST")
print("=" * 80)
print()

manifest = {

    "experiment":

        "E10.2.4",

    "title":

        "Family 2 Experimental Validation",

    "campaign":

        "S29/E10",

    "status":

        "COMPLETED",

    "generated_at":

        datetime.now(UTC).isoformat(),

    "family":

        "Family 2",

    "operator":

        operator_definition["symbol"],

    "validated":

        validation["validated"],

    "next_experiment":

        "E10.2.5 - Family 2 Structural Characterization",

}

metadata = {

    "experiment":

        "E10.2.4",

    "family":

        "Family 2",

    "operator":

        operator_definition["symbol"],

    "validated":

        validation["validated"],

    "implementation_valid":

        compatibility["implementation_valid"],

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

# ==============================================================================
# EXECUTION SUMMARY
# ==============================================================================

summary_lines = [

    "GER",
    "S29 - E10.2.4",
    "Family 2 Experimental Validation",
    "",

    f"Operator              : {operator_definition['symbol']}",
    f"Validated             : {validation['validated']}",
    f"Implementation Stable : {validation['implementation_stable']}",
    f"Omega Effect          : {validation['omega_effect_detected']}",
    f"Distinct from Family1 : {validation['family_distinct_from_family1']}",

    "",

    "Next experiment",
    "---------------",
    "E10.2.5 - Family 2 Structural Characterization",

]

with open(

    OUTPUT_DIR /
    "execution_summary.txt",

    "w",

) as f:

    f.write(

        "\n".join(summary_lines)

    )

# ==============================================================================
# FINAL AUDIT
# ==============================================================================

expected_files = [

    "validation_inventory.csv",
    "validation_summary.json",

    "family2_response_surface.csv",
    "family2_response_surface.parquet",
    "family2_statistics.csv",
    "family2_campaign_summary.json",

    "family2_vs_family1.csv",
    "family2_vs_family1.parquet",
    "family2_comparison_summary.json",

    "family2_validation.json",
    "validation_certificate.json",
    "family2_validation.txt",
    "family2_validation.md",

    "family2_validation_report.json",
    "family2_validation_report.txt",
    "family2_validation_report.md",

    "campaign_manifest.json",
    "metadata.json",
    "execution_summary.txt",

]

audit = []

for filename in expected_files:

    path = OUTPUT_DIR / filename

    audit.append({

        "file":

            filename,

        "exists":

            path.exists(),

        "size_bytes":

            path.stat().st_size
            if path.exists()
            else 0,

    })

audit = pd.DataFrame(

    audit

)

audit.to_csv(

    OUTPUT_DIR /
    "final_audit.csv",

    index=False,

)

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

print("Part 6 completed.")

# ==============================================================================
# MAIN
# ==============================================================================

def main():

    print()
    print("=" * 80)
    print("GER")
    print("S29 - E10.2.4")
    print("Family 2 Experimental Validation")
    print("=" * 80)

    print()
    print("=" * 80)
    print("E10.2.4 FINISHED")
    print("=" * 80)
    print()

    print("Experiment completed successfully.")
    print()

    print("Output directory")
    print(OUTPUT_DIR)
    print()

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":

    main()
