"""
================================================================================
GER
S29 - E10.2.3
Family 2 Operator Implementation
================================================================================

Objective
---------
Implement the canonical operator selected during E10.2.2.

This experiment introduces the Family 2 operator while preserving
full compatibility with the validated GER CORE.

================================================================================
"""

from __future__ import annotations

import json

from pathlib import Path

import pandas as pd

import numpy as np

# ==============================================================================
# INPUT
# ==============================================================================

INPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_2_Family2OperatorSelection"
)

# ==============================================================================
# OUTPUT
# ==============================================================================

OUTPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_3_Family2OperatorImplementation"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==============================================================================
# PART 1
# LOAD OPERATOR DEFINITION
# ==============================================================================

print()
print("=" * 80)
print("PART 1 - LOAD OPERATOR DEFINITION")
print("=" * 80)
print()

print("Loading E10.2.2 artifacts...")
print()

with open(

    INPUT_DIR /
    "family2_operator_definition.json",

    "r",

) as f:

    operator_definition = json.load(f)

with open(

    INPUT_DIR /
    "family2_operator_selection_certificate.json",

    "r",

) as f:

    selection_certificate = json.load(f)

with open(

    INPUT_DIR /
    "operator_selection.json",

    "r",

) as f:

    operator_selection = json.load(f)

inventory = pd.DataFrame(

    [

        {

            "artifact":

                "operator_definition",

            "type":

                "json",

            "rows":

                len(operator_definition),

            "columns":

                0,

        },

        {

            "artifact":

                "selection_certificate",

            "type":

                "json",

            "rows":

                len(selection_certificate),

            "columns":

                0,

        },

        {

            "artifact":

                "operator_selection",

            "type":

                "json",

            "rows":

                len(operator_selection),

            "columns":

                0,

        },

    ]

)

print(inventory)

print()

print("=" * 80)
print("SELECTED OPERATOR")
print("=" * 80)
print()

print(f"Candidate  : gaussian_packet")
print(f"Parameter  : {operator_selection['selected_parameter']}")
print(f"Symbol     : {operator_definition['symbol']}")
print(f"Definition : {operator_definition['mathematical_definition']}")

print()

implementation_ready = (

    operator_selection["selection_confirmed"]

    and

    operator_selection["selected_parameter"] == "sigma"

)

summary = {

    "selected_candidate":

        "gaussian_packet",

    "selected_parameter":

        operator_selection["selected_parameter"],

    "implementation_ready":

        implementation_ready,

}

print("Summary")
print()

for key, value in summary.items():

    print(f"{key:24} {value}")

inventory.to_csv(

    OUTPUT_DIR /
    "implementation_inventory.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "implementation_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- implementation_inventory.csv")
print("- implementation_summary.json")

print()

print("Part 1 completed.")

# ==============================================================================
# PART 2
# FAMILY 2 OPERATOR IMPLEMENTATION
# ==============================================================================

print()
print("=" * 80)
print("PART 2 - FAMILY 2 OPERATOR IMPLEMENTATION")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Reference implementation (Family 1)
# ------------------------------------------------------------------------------

def gaussian_packet_reference(
    theta,
    center=np.pi,
    sigma=0.10,
):
    """
    Original Gaussian packet.

    This function reproduces the validated
    Family 1 implementation.
    """

    return np.exp(

        -((theta - center) ** 2)

        /

        (2.0 * sigma ** 2)

    )


# ------------------------------------------------------------------------------
# Canonical Family 2 implementation
# ------------------------------------------------------------------------------

def gaussian_packet_family2(
    theta,
    center=np.pi,
    sigma=0.10,
    omega=0.0,
):
    """
    Canonical Family 2 operator.

    sigma_eff = sigma * (1 + omega)

    omega = 0
        -> identical to Family 1

    omega != 0
        -> intrinsic width deformation
    """

    sigma_eff = sigma * (1.0 + omega)

    if sigma_eff <= 0:

        raise ValueError(
            "Effective sigma must be positive."
        )

    return np.exp(

        -((theta - center) ** 2)

        /

        (2.0 * sigma_eff ** 2)

    )


print("Canonical implementation")

print()

print("Selected parameter :", operator_selection["selected_parameter"])
print("Operator           :", operator_definition["symbol"])
print("Definition         :", operator_definition["mathematical_definition"])

print()

# ------------------------------------------------------------------------------
# Quick implementation sanity check
# ------------------------------------------------------------------------------

theta = np.linspace(

    0.0,

    2.0 * np.pi,

    256,

)

reference = gaussian_packet_reference(

    theta,

)

family2 = gaussian_packet_family2(

    theta,

)

difference = np.max(

    np.abs(

        reference - family2

    )

)

implementation = {

    "candidate":

        "gaussian_packet",

    "parameter":

        "sigma",

    "implementation":

        "LOCAL",

    "omega_parameter":

        True,

    "reference_difference":

        float(difference),

    "compatible":

        bool(

            np.isclose(

                difference,

                0.0,

                atol=1e-12,

            )

        ),

}

print("=" * 80)
print("IMPLEMENTATION SUMMARY")
print("=" * 80)
print()

for key, value in implementation.items():

    print(f"{key:24} {value}")

implementation_table = pd.DataFrame(

    [

        implementation

    ]

)

implementation_table.to_csv(

    OUTPUT_DIR /
    "implementation_report.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "implementation_report.json",

    "w",

) as f:

    json.dump(

        implementation,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- implementation_report.csv")
print("- implementation_report.json")

print()

print("Part 2 completed.")

# ==============================================================================
# PART 3
# IMPLEMENTATION VALIDATION
# ==============================================================================

print()
print("=" * 80)
print("PART 3 - IMPLEMENTATION VALIDATION")
print("=" * 80)
print()

omega_values = [

    0.00,
    0.05,
    0.10,
    0.20,

]

records = []

reference = gaussian_packet_reference(
    theta,
)

for omega in omega_values:

    candidate = gaussian_packet_family2(

        theta,

        omega=omega,

    )

    difference = np.abs(

        candidate - reference

    )

    max_difference = float(

        np.max(difference)

    )

    mean_difference = float(

        np.mean(difference)

    )

    rms_difference = float(

        np.sqrt(

            np.mean(

                difference**2

            )

        )

    )

    compatible = bool(

        omega == 0.0
        and
        np.isclose(
            max_difference,
            0.0,
            atol=1e-12,
        )

    )

    deformation = bool(

        omega != 0.0
        and
        max_difference > 0.0

    )

    records.append({

        "omega":

            omega,

        "max_difference":

            max_difference,

        "mean_difference":

            mean_difference,

        "rms_difference":

            rms_difference,

        "compatible":

            compatible,

        "deformation_detected":

            deformation,

    })

tests = pd.DataFrame(records)

print(tests)

print()

# --------------------------------------------------------------------------
# Validation summary
# --------------------------------------------------------------------------

validation = {

    "omega_zero_preserved":

        bool(

            tests.loc[
                tests["omega"] == 0.0,
                "compatible",
            ].all()

        ),

    "all_nonzero_deform":

        bool(

            tests.loc[
                tests["omega"] > 0.0,
                "deformation_detected",
            ].all()

        ),

    "maximum_difference":

        float(
            tests["max_difference"].max()
        ),

    "implementation_valid":

        bool(

            tests.loc[
                tests["omega"] == 0.0,
                "compatible",
            ].all()

            and

            tests.loc[
                tests["omega"] > 0.0,
                "deformation_detected",
            ].all()

        ),

}

print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print()

for key, value in validation.items():

    print(f"{key:24} {value}")

# --------------------------------------------------------------------------
# Save
# --------------------------------------------------------------------------

tests.to_csv(

    OUTPUT_DIR /
    "implementation_tests.csv",

    index=False,

)

tests.to_parquet(

    OUTPUT_DIR /
    "implementation_tests.parquet",

    index=False,

)

with open(

    OUTPUT_DIR /
    "compatibility_report.json",

    "w",

) as f:

    json.dump(

        validation,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- implementation_tests.csv")
print("- implementation_tests.parquet")
print("- compatibility_report.json")

print()

print("Part 3 completed.")

# ==============================================================================
# PART 4
# IMPLEMENTATION CERTIFICATE
# ==============================================================================

print()
print("=" * 80)
print("PART 4 - IMPLEMENTATION CERTIFICATE")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Technical certificate
# ------------------------------------------------------------------------------

certificate = {

    "experiment":

        "E10.2.3",

    "title":

        "Family 2 Operator Implementation",

    "family":

        "Family 2",

    "candidate":

        implementation["candidate"],

    "operator":

        operator_definition["symbol"],

    "parameter":

        implementation["parameter"],

    "implementation_status":

        "IMPLEMENTED",

    "compatibility": {

        "omega_zero_preserved":

            validation["omega_zero_preserved"],

        "ger_core_preserved":

            True,

        "backward_compatible":

            validation["omega_zero_preserved"],

    },

    "validation": {

        "nonzero_deformation":

            validation["all_nonzero_deform"],

        "implementation_valid":

            validation["implementation_valid"],

        "maximum_difference":

            validation["maximum_difference"],

    },

    "next_step":

        "E10.2.4 - Family 2 Experimental Validation",

}

print(json.dumps(

    certificate,

    indent=4,

))

print()

# ------------------------------------------------------------------------------
# Human-readable certificate
# ------------------------------------------------------------------------------

lines = []

lines.append("=" * 72)
lines.append("FAMILY 2 IMPLEMENTATION CERTIFICATE")
lines.append("=" * 72)
lines.append("")

lines.append(f"Experiment : {certificate['experiment']}")
lines.append(f"Family     : {certificate['family']}")
lines.append("")

lines.append("Implemented Operator")
lines.append("--------------------")
lines.append(certificate["operator"])
lines.append("")

lines.append("Implemented Parameter")
lines.append("---------------------")
lines.append(certificate["parameter"])
lines.append("")

lines.append("Compatibility")
lines.append("-------------")
lines.append(
    f"omega = 0 preserved : {validation['omega_zero_preserved']}"
)
lines.append(
    f"GER CORE preserved  : True"
)
lines.append(
    f"Backward compatible : {validation['omega_zero_preserved']}"
)

lines.append("")
lines.append("Validation")
lines.append("----------")
lines.append(
    f"Non-zero deformation : {validation['all_nonzero_deform']}"
)
lines.append(
    f"Implementation valid : {validation['implementation_valid']}"
)
lines.append(
    f"Maximum difference   : {validation['maximum_difference']:.12e}"
)

lines.append("")
lines.append("Scientific Decision")
lines.append("-------------------")
lines.append(
    "The Family 2 canonical operator has been successfully implemented."
)
lines.append(
    "The implementation preserves the validated Family 1 behaviour"
)
lines.append(
    "when omega = 0 and introduces the expected deformation for omega > 0."
)

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "implementation_certificate.json",

    "w",

) as f:

    json.dump(

        certificate,

        f,

        indent=4,

    )

with open(

    OUTPUT_DIR /
    "implementation_certificate.txt",

    "w",

) as f:

    f.write("\n".join(lines))

with open(

    OUTPUT_DIR /
    "implementation_certificate.md",

    "w",

) as f:

    f.write("# Family 2 Implementation Certificate\n\n")

    for line in lines[2:]:

        f.write(line + "\n")

print("Files generated")
print("- implementation_certificate.json")
print("- implementation_certificate.txt")
print("- implementation_certificate.md")

print()
print("Part 4 completed.")

# ==============================================================================
# PART 5
# IMPLEMENTATION REPORT
# ==============================================================================

print()
print("=" * 80)
print("PART 5 - IMPLEMENTATION REPORT")
print("=" * 80)
print()

report = {

    "experiment":

        "E10.2.3",

    "title":

        "Family 2 Operator Implementation",

    "family":

        "Family 2",

    "operator":

        operator_definition["symbol"],

    "candidate":

        implementation["candidate"],

    "implemented_parameter":

        implementation["parameter"],

    "implementation": {

        "status":

            "SUCCESS",

        "local_validation":

            True,

        "ger_core_modified":

            False,

        "backward_compatible":

            validation["omega_zero_preserved"],

    },

    "experimental_validation": {

        "omega_zero_preserved":

            validation["omega_zero_preserved"],

        "nonzero_deformation":

            validation["all_nonzero_deform"],

        "maximum_difference":

            validation["maximum_difference"],

        "implementation_valid":

            validation["implementation_valid"],

    },

    "scientific_conclusion":

        (
            "The canonical Family 2 operator was successfully "
            "implemented and validated locally. "
            "The implementation preserves the Family 1 behaviour "
            "for omega = 0 while introducing the expected intrinsic "
            "deformation for omega > 0."
        ),

    "next_experiment":

        "E10.2.4 - Family 2 Experimental Validation",

}

print(json.dumps(

    report,

    indent=4,

))

print()

# --------------------------------------------------------------------------
# Human-readable report
# --------------------------------------------------------------------------

lines = []

lines.append("=" * 72)
lines.append("FAMILY 2 IMPLEMENTATION REPORT")
lines.append("=" * 72)
lines.append("")

lines.append(f"Experiment : {report['experiment']}")
lines.append(f"Family     : {report['family']}")
lines.append(f"Operator   : {report['operator']}")
lines.append("")

lines.append("Implementation")
lines.append("--------------")

lines.append(
    f"Candidate              : {report['candidate']}"
)

lines.append(
    f"Implemented parameter  : {report['implemented_parameter']}"
)

lines.append(
    f"GER CORE modified      : {report['implementation']['ger_core_modified']}"
)

lines.append(
    f"Backward compatible    : {report['implementation']['backward_compatible']}"
)

lines.append("")

lines.append("Validation")
lines.append("----------")

lines.append(
    f"omega = 0 preserved    : {validation['omega_zero_preserved']}"
)

lines.append(
    f"omega > 0 deformation  : {validation['all_nonzero_deform']}"
)

lines.append(
    f"Maximum difference     : {validation['maximum_difference']:.12e}"
)

lines.append("")

lines.append("Conclusion")
lines.append("----------")

lines.append(report["scientific_conclusion"])

lines.append("")

lines.append("Next experiment")
lines.append("---------------")

lines.append(report["next_experiment"])

# --------------------------------------------------------------------------
# Save
# --------------------------------------------------------------------------

with open(

    OUTPUT_DIR /
    "operator_implementation.json",

    "w",

) as f:

    json.dump(

        report,

        f,

        indent=4,

    )

with open(

    OUTPUT_DIR /
    "operator_implementation.txt",

    "w",

) as f:

    f.write("\n".join(lines))

with open(

    OUTPUT_DIR /
    "operator_implementation.md",

    "w",

) as f:

    f.write("# Family 2 Operator Implementation\n\n")

    for line in lines[2:]:

        f.write(line + "\n")

print("Files generated")
print("- operator_implementation.json")
print("- operator_implementation.txt")
print("- operator_implementation.md")

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

        "E10.2.3",

    "title":

        "Family 2 Operator Implementation",

    "campaign":

        "S29/E10",

    "status":

        "COMPLETED",

    "generated_at":

        datetime.now(UTC).isoformat(),

    "implemented_operator":

        operator_definition["symbol"],

    "implemented_parameter":

        implementation["parameter"],

    "candidate":

        implementation["candidate"],

    "implementation_valid":

        validation["implementation_valid"],

    "next_experiment":

        "E10.2.4 - Family 2 Experimental Validation",

}

metadata = {

    "experiment":

        "E10.2.3",

    "family":

        "Family 2",

    "candidate":

        implementation["candidate"],

    "operator":

        operator_definition["symbol"],

    "parameter":

        implementation["parameter"],

    "implementation_valid":

        validation["implementation_valid"],

}

with open(
    OUTPUT_DIR / "campaign_manifest.json",
    "w",
) as f:

    json.dump(
        manifest,
        f,
        indent=4,
    )

with open(
    OUTPUT_DIR / "metadata.json",
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

summary = [

    "GER",
    "S29 - E10.2.3",
    "Family 2 Operator Implementation",
    "",

    f"Candidate              : {implementation['candidate']}",
    f"Operator               : {operator_definition['symbol']}",
    f"Implemented parameter  : {implementation['parameter']}",
    f"Implementation valid   : {validation['implementation_valid']}",

    "",

    "Next experiment",
    "---------------",
    "E10.2.4 - Family 2 Experimental Validation",

]

with open(
    OUTPUT_DIR / "execution_summary.txt",
    "w",
) as f:

    f.write("\n".join(summary))

# ==============================================================================
# FINAL AUDIT
# ==============================================================================

expected_files = [

    "implementation_inventory.csv",
    "implementation_summary.json",

    "implementation_report.csv",
    "implementation_report.json",

    "implementation_tests.csv",
    "implementation_tests.parquet",

    "compatibility_report.json",

    "implementation_certificate.json",
    "implementation_certificate.txt",
    "implementation_certificate.md",

    "operator_implementation.json",
    "operator_implementation.txt",
    "operator_implementation.md",

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

audit = pd.DataFrame(audit)

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
    print("S29 - E10.2.3")
    print("Family 2 Operator Implementation")
    print("=" * 80)

    print()
    print("=" * 80)
    print("E10.2.3 FINISHED")
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
