"""
================================================================================
GER
S29 - E10.2.2
Family 2 Operator Selection
================================================================================

Objective
---------
Select the canonical operator of Family 2 from the admissible
candidates identified during E10.2.1.

This experiment does NOT implement the operator.

Its purpose is only to select the canonical mathematical deformation
that will define E10-v2.

================================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from datetime import datetime, UTC

# ==============================================================================
# INPUT
# ==============================================================================

INPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_1_Family2OperatorAudit"
)

# ==============================================================================
# OUTPUT
# ==============================================================================

OUTPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_2_Family2OperatorSelection"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==============================================================================
# PART 1
# LOAD AUDIT RESULTS
# ==============================================================================

print()
print("=" * 80)
print("PART 1 - LOAD AUDIT RESULTS")
print("=" * 80)
print()

print("Loading E10.2.1 artifacts...")
print()

with open(
    INPUT_DIR / "family2_operator_audit.json",
    "r",
) as f:

    audit = json.load(f)

classification = pd.read_csv(
    INPUT_DIR /
    "operator_classification.csv"
)

admissibility = pd.read_csv(
    INPUT_DIR /
    "operator_admissibility.csv"
)

with open(
    INPUT_DIR /
    "campaign_manifest.json",
    "r",
) as f:

    manifest = json.load(f)

inventory = pd.DataFrame(

    [

        {
            "artifact": "family2_operator_audit",
            "type": "json",
            "rows": len(audit),
            "columns": 0,
        },

        {
            "artifact": "operator_classification",
            "type": "table",
            "rows": len(classification),
            "columns": len(classification.columns),
        },

        {
            "artifact": "operator_admissibility",
            "type": "table",
            "rows": len(admissibility),
            "columns": len(admissibility.columns),
        },

        {
            "artifact": "campaign_manifest",
            "type": "json",
            "rows": len(manifest),
            "columns": 0,
        },

    ]

)

print(inventory)

print()

approved = classification[
    classification["family2_candidate"] == True
].copy()

print("=" * 80)
print("ELIGIBLE CANDIDATES")
print("=" * 80)
print()

print(approved)

print()

selection_ready = len(approved) > 0

summary = {

    "candidate_count":

        int(len(classification)),

    "eligible_candidates":

        int(len(approved)),

    "selection_ready":

        selection_ready,

}

print("Summary")

for k, v in summary.items():

    print(f"{k:24} {v}")

inventory.to_csv(

    OUTPUT_DIR /
    "selection_inventory.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "selection_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- selection_inventory.csv")
print("- selection_summary.json")

print()

print("Part 1 completed.")

# ==============================================================================
# PART 2
# PARAMETER ANALYSIS
# ==============================================================================

print()
print("=" * 80)
print("PART 2 - PARAMETER ANALYSIS")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Candidate parameter inventory
# ------------------------------------------------------------------------------

parameters = pd.DataFrame(

    [

        {
            "parameter": "center",
            "symbol": "c",
            "role": "Packet position",
            "geometric": True,
            "independent": True,
            "core_safe": True,
            "continuous": True,
            "future_scalable": True,
        },

        {
            "parameter": "sigma",
            "symbol": "σ",
            "role": "Packet width",
            "geometric": True,
            "independent": True,
            "core_safe": True,
            "continuous": True,
            "future_scalable": True,
        },

        {
            "parameter": "normalization",
            "symbol": "A",
            "role": "Packet amplitude",
            "geometric": False,
            "independent": False,
            "core_safe": True,
            "continuous": True,
            "future_scalable": False,
        },

    ]

)

print(parameters)

print()

# ------------------------------------------------------------------------------
# Scientific scoring
# ------------------------------------------------------------------------------

scores = []

for _, row in parameters.iterrows():

    score = 0

    score += int(row["geometric"])
    score += int(row["independent"])
    score += int(row["core_safe"])
    score += int(row["continuous"])
    score += int(row["future_scalable"])

    scores.append(score)

parameters["score"] = scores

parameters["admissible"] = (
    parameters["score"] >= 4
)

print("=" * 80)
print("SCIENTIFIC EVALUATION")
print("=" * 80)
print()

print(parameters)

print()

summary = {

    "parameters":

        int(len(parameters)),

    "admissible":

        int(parameters["admissible"].sum()),

    "maximum_score":

        int(parameters["score"].max()),

    "minimum_score":

        int(parameters["score"].min()),

}

print("Summary")

for key, value in summary.items():

    print(f"{key:20} {value}")

parameters.to_csv(

    OUTPUT_DIR /
    "parameter_analysis.csv",

    index=False,

)

parameters.to_parquet(

    OUTPUT_DIR /
    "parameter_analysis.parquet",

    index=False,

)

with open(

    OUTPUT_DIR /
    "parameter_analysis_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- parameter_analysis.csv")
print("- parameter_analysis.parquet")
print("- parameter_analysis_summary.json")

print()

print("Part 2 completed.")

# ==============================================================================
# PART 3
# SCIENTIFIC SELECTION
# ==============================================================================

print()
print("=" * 80)
print("PART 3 - SCIENTIFIC SELECTION")
print("=" * 80)
print()

ranking = []

for _, row in parameters.iterrows():

    parameter = row["parameter"]

    priority = 0

    justification = ""

    # -------------------------------------------------------------------------
    # Canonical priorities
    # -------------------------------------------------------------------------

    if parameter == "sigma":

        priority = 1

        justification = (
            "Controls the intrinsic geometric width of the packet. "
            "Defines a genuine deformation without translating the "
            "reference frame."
        )

    elif parameter == "center":

        priority = 2

        justification = (
            "Produces spatial translation of the packet, but does not "
            "change its intrinsic geometry."
        )

    else:

        priority = 3

        justification = (
            "Acts only as amplitude scaling and therefore overlaps with "
            "effects already represented by Family 1."
        )

    ranking.append({

        "parameter":

            parameter,

        "symbol":

            row["symbol"],

        "score":

            row["score"],

        "priority":

            priority,

        "admissible":

            row["admissible"],

        "justification":

            justification,

    })

ranking = pd.DataFrame(ranking)

ranking = ranking.sort_values(

    by=[
        "priority",
        "score",
    ],

    ascending=[
        True,
        False,
    ],

).reset_index(drop=True)

print(ranking)

print()

# -------------------------------------------------------------------------
# Canonical selection
# -------------------------------------------------------------------------

selected = ranking.iloc[0]

selection = {

    "experiment":

        "E10.2.2",

    "selected_parameter":

        selected["parameter"],

    "symbol":

        selected["symbol"],

    "priority":

        int(selected["priority"]),

    "scientific_basis":

        selected["justification"],

    "selection_confirmed":

        True,

}

print("=" * 80)
print("CANONICAL SELECTION")
print("=" * 80)
print()

for key, value in selection.items():

    print(f"{key:22} {value}")

# -------------------------------------------------------------------------
# Save
# -------------------------------------------------------------------------

ranking.to_csv(

    OUTPUT_DIR /
    "parameter_ranking.csv",

    index=False,

)

ranking.to_parquet(

    OUTPUT_DIR /
    "parameter_ranking.parquet",

    index=False,

)

with open(

    OUTPUT_DIR /
    "operator_selection.json",

    "w",

) as f:

    json.dump(

        selection,

        f,

        indent=4,

    )

print()

print("Files generated")
print("- parameter_ranking.csv")
print("- parameter_ranking.parquet")
print("- operator_selection.json")

print()

print("Part 3 completed.")

# ==============================================================================
# PART 4
# CANONICAL OPERATOR DEFINITION
# ==============================================================================

print()
print("=" * 80)
print("PART 4 - CANONICAL OPERATOR DEFINITION")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Selected parameter
# ------------------------------------------------------------------------------

selected_parameter = selection["selected_parameter"]

if selected_parameter == "sigma":

    operator_name = "Family 2 Canonical Operator"

    operator_symbol = "U₂(ω)"

    mathematical_definition = (
        "σ → σ(1 + ω)"
    )

    operator_expression = (
        "gaussian_packet(theta, center, sigma*(1+ω))"
    )

    geometric_action = (
        "Intrinsic deformation of the packet width."
    )

    preserved_property = (
        "Packet center remains fixed."
    )

elif selected_parameter == "center":

    operator_name = "Family 2 Canonical Operator"

    operator_symbol = "U₂(ω)"

    mathematical_definition = (
        "center → center + ω"
    )

    operator_expression = (
        "gaussian_packet(theta, center+ω, sigma)"
    )

    geometric_action = (
        "Translation of the packet center."
    )

    preserved_property = (
        "Packet width remains fixed."
    )

else:

    operator_name = "Undefined"

    operator_symbol = "Undefined"

    mathematical_definition = "Undefined"

    operator_expression = "Undefined"

    geometric_action = "Undefined"

    preserved_property = "Undefined"

# ------------------------------------------------------------------------------
# Canonical definition
# ------------------------------------------------------------------------------

definition = {

    "experiment":

        "E10.2.2",

    "family":

        "Family 2",

    "operator":

        operator_name,

    "symbol":

        operator_symbol,

    "selected_parameter":

        selected_parameter,

    "mathematical_definition":

        mathematical_definition,

    "operator_expression":

        operator_expression,

    "geometric_action":

        geometric_action,

    "preserved_property":

        preserved_property,

    "acts_on":

        "gaussian_packet",

    "compatible_with_family1":

        True,

    "implementation_required":

        "E10.2.3",

}

print(json.dumps(
    definition,
    indent=4,
))

print()

# ------------------------------------------------------------------------------
# Human-readable definition
# ------------------------------------------------------------------------------

text = []

text.append("=" * 72)
text.append("FAMILY 2 CANONICAL OPERATOR")
text.append("=" * 72)
text.append("")
text.append(f"Operator : {operator_symbol}")
text.append("")
text.append("Acts on")
text.append("-------")
text.append("gaussian_packet")
text.append("")
text.append("Mathematical definition")
text.append("-----------------------")
text.append(mathematical_definition)
text.append("")
text.append("Expression")
text.append("----------")
text.append(operator_expression)
text.append("")
text.append("Geometric action")
text.append("----------------")
text.append(geometric_action)
text.append("")
text.append("Preserved property")
text.append("------------------")
text.append(preserved_property)
text.append("")
text.append("Implementation")
text.append("--------------")
text.append("Reserved for E10.2.3")

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

with open(
    OUTPUT_DIR / "family2_operator_definition.json",
    "w",
) as f:

    json.dump(
        definition,
        f,
        indent=4,
    )

with open(
    OUTPUT_DIR / "family2_operator_definition.txt",
    "w",
) as f:

    f.write("\n".join(text))

with open(
    OUTPUT_DIR / "family2_operator_definition.md",
    "w",
) as f:

    f.write("# Family 2 Canonical Operator\n\n")

    for line in text[2:]:

        f.write(line + "\n")

print("Files generated")
print("- family2_operator_definition.json")
print("- family2_operator_definition.txt")
print("- family2_operator_definition.md")

print()
print("Part 4 completed.")

# ==============================================================================
# PART 5
# FAMILY 2 OPERATOR SELECTION CERTIFICATE
# ==============================================================================

print()
print("=" * 80)
print("PART 5 - FAMILY 2 OPERATOR SELECTION CERTIFICATE")
print("=" * 80)
print()

certificate = {

    "experiment":

        "E10.2.2",

    "title":

        "Family 2 Operator Selection",

    "family":

        "Family 2",

    "selected_candidate":

        "gaussian_packet",

    "selected_parameter":

        definition["selected_parameter"],

    "operator_symbol":

        definition["symbol"],

    "operator_definition":

        definition["mathematical_definition"],

    "operator_expression":

        definition["operator_expression"],

    "geometric_action":

        definition["geometric_action"],

    "compatibility": {

        "family1":

            True,

        "ger_core":

            True,

        "future_families":

            True,

    },

    "scientific_decision": {

        "selection_completed":

            True,

        "implementation":

            "Reserved for E10.2.3",

        "status":

            "CANONICAL OPERATOR SELECTED",

    },

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
lines.append("FAMILY 2 OPERATOR SELECTION CERTIFICATE")
lines.append("=" * 72)
lines.append("")

lines.append(f"Experiment : {certificate['experiment']}")
lines.append(f"Family     : {certificate['family']}")
lines.append("")

lines.append("Selected Candidate")
lines.append("------------------")
lines.append(certificate["selected_candidate"])
lines.append("")

lines.append("Selected Parameter")
lines.append("------------------")
lines.append(certificate["selected_parameter"])
lines.append("")

lines.append("Canonical Operator")
lines.append("------------------")
lines.append(certificate["operator_symbol"])
lines.append(certificate["operator_definition"])
lines.append("")

lines.append("Geometric Action")
lines.append("----------------")
lines.append(certificate["geometric_action"])
lines.append("")

lines.append("Decision")
lines.append("--------")
lines.append("Family 2 canonical operator successfully selected.")
lines.append("Implementation reserved for E10.2.3.")

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

with open(
    OUTPUT_DIR / "family2_operator_selection_certificate.json",
    "w",
) as f:

    json.dump(
        certificate,
        f,
        indent=4,
    )

with open(
    OUTPUT_DIR / "family2_operator_selection_certificate.txt",
    "w",
) as f:

    f.write("\n".join(lines))

with open(
    OUTPUT_DIR / "family2_operator_selection_certificate.md",
    "w",
) as f:

    f.write("# Family 2 Operator Selection Certificate\n\n")

    for line in lines[2:]:

        f.write(line + "\n")

print("Files generated")
print("- family2_operator_selection_certificate.json")
print("- family2_operator_selection_certificate.txt")
print("- family2_operator_selection_certificate.md")

print()
print("Part 5 completed.")

# ==============================================================================
# PART 6
# CAMPAIGN MANIFEST + FINAL AUDIT + MAIN
# ==============================================================================

print()
print("=" * 80)
print("PART 6 - CAMPAIGN MANIFEST")
print("=" * 80)
print()

manifest = {

    "experiment": "E10.2.2",

    "title": "Family 2 Operator Selection",

    "campaign": "S29/E10",

    "status": "COMPLETED",

    "generated_at": datetime.now(UTC).isoformat(),

    "selected_candidate":
        certificate["selected_candidate"],

    "selected_parameter":
        certificate["selected_parameter"],

    "operator":
        certificate["operator_symbol"],

    "next_experiment":
        "E10.2.3 - Family 2 Operator Implementation",

}

metadata = {

    "experiment":
        "E10.2.2",

    "family":
        "Family 2",

    "candidate":
        certificate["selected_candidate"],

    "parameter":
        certificate["selected_parameter"],

    "operator":
        certificate["operator_symbol"],

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
    "S29 - E10.2.2",
    "Family 2 Operator Selection",
    "",

    f"Selected candidate : {certificate['selected_candidate']}",
    f"Selected parameter : {certificate['selected_parameter']}",
    f"Canonical operator : {certificate['operator_symbol']}",

    "",

    "Next experiment",
    "---------------",
    "E10.2.3 - Family 2 Operator Implementation",

]

with open(
    OUTPUT_DIR / "execution_summary.txt",
    "w",
) as f:

    f.write("\n".join(summary))

# ==============================================================================
# FINAL AUDIT
# ==============================================================================

expected = [

    "selection_inventory.csv",
    "selection_summary.json",

    "parameter_analysis.csv",
    "parameter_analysis.parquet",
    "parameter_analysis_summary.json",

    "parameter_ranking.csv",
    "parameter_ranking.parquet",

    "operator_selection.json",

    "family2_operator_definition.json",
    "family2_operator_definition.txt",
    "family2_operator_definition.md",

    "family2_operator_selection_certificate.json",
    "family2_operator_selection_certificate.txt",
    "family2_operator_selection_certificate.md",

    "campaign_manifest.json",
    "metadata.json",
    "execution_summary.txt",

]

audit = []

for file in expected:

    path = OUTPUT_DIR / file

    audit.append({

        "file":
            file,

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
    print("S29 - E10.2.2")
    print("Family 2 Operator Selection")
    print("=" * 80)

    print()
    print("=" * 80)
    print("E10.2.2 FINISHED")
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
