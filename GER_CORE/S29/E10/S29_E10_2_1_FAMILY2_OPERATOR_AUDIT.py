"""
================================================================================
GER
S29 - E10.2.1
Family 2 Operator Audit
================================================================================

Objective
---------
Audit every candidate operator already present inside the GER framework
that could originate the second canonical operator (E10-v2).

This experiment DOES NOT select an operator.

Its purpose is only to determine which candidates satisfy the
admissibility principles established during Family 1.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

# ==============================================================================
# OUTPUT
# ==============================================================================

OUTPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S29/E10/E10_2_1_Family2OperatorAudit"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==============================================================================
# CANDIDATE INVENTORY
# ==============================================================================

print()
print("=" * 80)
print("PART 1 - CANDIDATE INVENTORY")
print("=" * 80)
print()

candidates = pd.DataFrame(
    [

        {
            "candidate": "gaussian_packet",
            "module": "ger_graph",
            "category": "initial_state",
            "role": "Initial state generator",
            "called_by": 3,
        },

        {
            "candidate": "build_ring_graph",
            "module": "ger_graph",
            "category": "core_geometry",
            "role": "Graph constructor",
            "called_by": 5,
        },

        {
            "candidate": "spectral_basis",
            "module": "ger_graph",
            "category": "core_geometry",
            "role": "Spectral basis constructor",
            "called_by": 2,
        },

        {
            "candidate": "modal_projection",
            "module": "ger_modal",
            "category": "observatory",
            "role": "Spectral observable",
            "called_by": 1,
        },

        {
            "candidate": "spectral_width",
            "module": "ger_modal",
            "category": "observatory",
            "role": "Spectral observable",
            "called_by": 1,
        },

        {
            "candidate": "spectral_entropy",
            "module": "ger_modal",
            "category": "observatory",
            "role": "Spectral observable",
            "called_by": 1,
        },

        {
            "candidate": "participation_ratio",
            "module": "ger_modal",
            "category": "observatory",
            "role": "Spectral observable",
            "called_by": 1,
        },

    ]
)

print(candidates)

print()

print("=" * 80)
print("CATEGORY SUMMARY")
print("=" * 80)
print()

summary = (

    candidates

    .groupby("category")

    .size()

    .reset_index(name="count")

)

print(summary)

print()

inventory = {

    "experiment": "E10.2.1",

    "title": "Family 2 Operator Audit",

    "total_candidates":

        int(len(candidates)),

    "categories":

        summary.set_index("category")["count"].to_dict(),

}

candidates.to_csv(

    OUTPUT_DIR /
    "candidate_inventory.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "candidate_inventory.json",

    "w",

) as f:

    json.dump(

        inventory,

        f,

        indent=4,

    )

print("Files generated")
print("- candidate_inventory.csv")
print("- candidate_inventory.json")

print()
print("Part 1 completed.")

# ==============================================================================
# PART 2
# ADMISSIBILITY AUDIT
# ==============================================================================

print()
print("=" * 80)
print("PART 2 - ADMISSIBILITY AUDIT")
print("=" * 80)
print()

records = []

for _, row in candidates.iterrows():

    name = row["candidate"]
    category = row["category"]

    # -------------------------------------------------------------------------
    # Critério 1
    # Origem geométrica
    # -------------------------------------------------------------------------

    geometric_origin = category in (
        "initial_state",
        "core_geometry",
    )

    # -------------------------------------------------------------------------
    # Critério 2
    # Atua diretamente sobre o estado inicial
    # -------------------------------------------------------------------------

    acts_on_initial_state = (
        category == "initial_state"
    )

    # -------------------------------------------------------------------------
    # Critério 3
    # É infraestrutura do CORE?
    # -------------------------------------------------------------------------

    core_infrastructure = (
        category == "core_geometry"
    )

    # -------------------------------------------------------------------------
    # Critério 4
    # É apenas observável?
    # -------------------------------------------------------------------------

    observational = (
        category == "observatory"
    )

    # -------------------------------------------------------------------------
    # Critério 5
    # Compatível com o princípio da Família 1
    # -------------------------------------------------------------------------

    compatible_with_core = (
        not observational
    )

    # -------------------------------------------------------------------------
    # Critério 6
    # Potencial para originar operador
    # -------------------------------------------------------------------------

    candidate_operator = (
        acts_on_initial_state
    )

    # -------------------------------------------------------------------------
    # Parecer preliminar
    # -------------------------------------------------------------------------

    if candidate_operator:

        preliminary = "APPROVED"

    elif core_infrastructure:

        preliminary = "RESERVED"

    else:

        preliminary = "REJECTED"

    records.append({

        "candidate":

            name,

        "category":

            category,

        "geometric_origin":

            geometric_origin,

        "acts_on_initial_state":

            acts_on_initial_state,

        "core_infrastructure":

            core_infrastructure,

        "observational":

            observational,

        "compatible_with_core":

            compatible_with_core,

        "candidate_operator":

            candidate_operator,

        "preliminary_decision":

            preliminary,

    })

audit = pd.DataFrame(records)

print(audit)

print()

# -------------------------------------------------------------------------
# Estatísticas
# -------------------------------------------------------------------------

summary = {

    "total_candidates":

        int(len(audit)),

    "approved":

        int(
            (audit["preliminary_decision"] == "APPROVED").sum()
        ),

    "reserved":

        int(
            (audit["preliminary_decision"] == "RESERVED").sum()
        ),

    "rejected":

        int(
            (audit["preliminary_decision"] == "REJECTED").sum()
        ),

}

print("=" * 80)
print("AUDIT SUMMARY")
print("=" * 80)
print()

for key, value in summary.items():

    print(f"{key:24} {value}")

# -------------------------------------------------------------------------
# Salvamento
# -------------------------------------------------------------------------

audit.to_csv(

    OUTPUT_DIR /
    "operator_admissibility.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "operator_admissibility_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print()
print("Files generated")
print("- operator_admissibility.csv")
print("- operator_admissibility_summary.json")

print()
print("Part 2 completed.")

# ==============================================================================
# PART 3
# SCIENTIFIC CLASSIFICATION
# ==============================================================================

print()
print("=" * 80)
print("PART 3 - SCIENTIFIC CLASSIFICATION")
print("=" * 80)
print()

classification = []

for _, row in audit.iterrows():

    candidate = row["candidate"]

    decision = row["preliminary_decision"]

    # -------------------------------------------------------------------------
    # Scientific justification
    # -------------------------------------------------------------------------

    if decision == "APPROVED":

        classification.append({

            "candidate":

                candidate,

            "classification":

                "ADMISSIBLE",

            "family2_candidate":

                True,

            "scientific_role":

                "Initial-state deformation",

            "justification":

                (
                    "Acts directly on the historical initial state "
                    "without modifying the GER CORE."
                ),

            "next_step":

                "Proceed to Family 2 Operator Selection.",

        })

    elif decision == "RESERVED":

        classification.append({

            "candidate":

                candidate,

            "classification":

                "RESERVED",

            "family2_candidate":

                False,

            "scientific_role":

                "CORE infrastructure",

            "justification":

                (
                    "Defines the computational/geometric framework "
                    "rather than an admissible deformation."
                ),

            "next_step":

                "May be reconsidered in future operator families.",

        })

    else:

        classification.append({

            "candidate":

                candidate,

            "classification":

                "REJECTED",

            "family2_candidate":

                False,

            "scientific_role":

                "Observational quantity",

            "justification":

                (
                    "Represents a measured observable rather than "
                    "an operator acting on the initial state."
                ),

            "next_step":

                "Excluded from the canonical operator search.",

        })

classification = pd.DataFrame(classification)

print(classification)

print()

# -------------------------------------------------------------------------
# Final scientific summary
# -------------------------------------------------------------------------

summary = {

    "admissible":

        int(
            (classification["classification"] == "ADMISSIBLE").sum()
        ),

    "reserved":

        int(
            (classification["classification"] == "RESERVED").sum()
        ),

    "rejected":

        int(
            (classification["classification"] == "REJECTED").sum()
        ),

    "family2_candidates":

        classification.loc[
            classification["family2_candidate"],
            "candidate",
        ].tolist(),

}

print("=" * 80)
print("SCIENTIFIC SUMMARY")
print("=" * 80)
print()

for key, value in summary.items():

    print(f"{key:24} {value}")

print()

# -------------------------------------------------------------------------
# Save
# -------------------------------------------------------------------------

classification.to_csv(

    OUTPUT_DIR /
    "operator_classification.csv",

    index=False,

)

with open(

    OUTPUT_DIR /
    "operator_classification_summary.json",

    "w",

) as f:

    json.dump(

        summary,

        f,

        indent=4,

    )

print("Files generated")
print("- operator_classification.csv")
print("- operator_classification_summary.json")

print()
print("Part 3 completed.")

# ==============================================================================
# PART 4
# SCIENTIFIC AUDIT REPORT
# ==============================================================================

print()
print("=" * 80)
print("PART 4 - SCIENTIFIC AUDIT REPORT")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# Approved candidates
# ------------------------------------------------------------------------------

approved = classification[
    classification["classification"] == "ADMISSIBLE"
]

reserved = classification[
    classification["classification"] == "RESERVED"
]

rejected = classification[
    classification["classification"] == "REJECTED"
]

# ------------------------------------------------------------------------------
# Scientific report
# ------------------------------------------------------------------------------

report = {

    "experiment":

        "E10.2.1",

    "title":

        "Family 2 Operator Audit",

    "objective":

        (
            "Audit candidate operators already present inside the "
            "GER framework."
        ),

    "total_candidates":

        int(len(classification)),

    "approved_candidates":

        approved["candidate"].tolist(),

    "reserved_candidates":

        reserved["candidate"].tolist(),

    "rejected_candidates":

        rejected["candidate"].tolist(),

    "family2_selection_ready":

        len(approved) > 0,

    "recommendation":

        (
            "Proceed to E10.2.2 using only the admissible candidates."
        ),

}

# ------------------------------------------------------------------------------
# Human-readable report
# ------------------------------------------------------------------------------

lines = []

lines.append("=" * 72)
lines.append("FAMILY 2 OPERATOR AUDIT")
lines.append("=" * 72)
lines.append("")

lines.append(f"Candidates audited : {len(classification)}")
lines.append(f"Approved           : {len(approved)}")
lines.append(f"Reserved           : {len(reserved)}")
lines.append(f"Rejected           : {len(rejected)}")
lines.append("")

lines.append("Approved Candidates")
lines.append("-------------------")

if len(approved):

    for candidate in approved["candidate"]:

        lines.append(f"- {candidate}")

else:

    lines.append("None")

lines.append("")
lines.append("Reserved Candidates")
lines.append("-------------------")

if len(reserved):

    for candidate in reserved["candidate"]:

        lines.append(f"- {candidate}")

else:

    lines.append("None")

lines.append("")
lines.append("Rejected Candidates")
lines.append("-------------------")

if len(rejected):

    for candidate in rejected["candidate"]:

        lines.append(f"- {candidate}")

else:

    lines.append("None")

lines.append("")
lines.append("Scientific Decision")
lines.append("-------------------")

if report["family2_selection_ready"]:

    lines.append(
        "The audit identified admissible operator candidates."
    )
    lines.append(
        "The canonical operator SHALL be selected during E10.2.2."
    )

else:

    lines.append(
        "No admissible candidate was identified."
    )

# ------------------------------------------------------------------------------
# Save
# ------------------------------------------------------------------------------

with open(
    OUTPUT_DIR / "family2_operator_audit.json",
    "w",
) as f:

    json.dump(
        report,
        f,
        indent=4,
    )

with open(

    OUTPUT_DIR /
    "family2_operator_audit.txt",

    "w",

) as f:

    f.write("\n".join(lines))

with open(

    OUTPUT_DIR /
    "family2_operator_audit.md",

    "w",

) as f:

    f.write("# Family 2 Operator Audit\n\n")

    for line in lines[2:]:

        f.write(line + "\n")

# ------------------------------------------------------------------------------
# Console
# ------------------------------------------------------------------------------

print(json.dumps(

    report,

    indent=4,

))

print()

print("Files generated")

print("- family2_operator_audit.json")
print("- family2_operator_audit.txt")
print("- family2_operator_audit.md")

print()

print("Part 4 completed.")

# ==============================================================================
# PART 5
# CAMPAIGN MANIFEST
# ==============================================================================

print()
print("=" * 80)
print("PART 5 - CAMPAIGN MANIFEST")
print("=" * 80)
print()

manifest = {

    "experiment": "E10.2.1",

    "title": "Family 2 Operator Audit",

    "campaign": "S29/E10",

    "status": "COMPLETED",

    "generated_at": datetime.utcnow().isoformat(),

    "approved_candidates":

        report["approved_candidates"],

    "reserved_candidates":

        report["reserved_candidates"],

    "rejected_candidates":

        report["rejected_candidates"],

    "next_experiment":

        "E10.2.2 - Family 2 Operator Selection",

}

metadata = {

    "experiment": "E10.2.1",

    "family": "Family 2",

    "total_candidates": int(len(classification)),

    "approved": int(len(approved)),

    "reserved": int(len(reserved)),

    "rejected": int(len(rejected)),

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

# --------------------------------------------------------------------------
# Execution summary
# --------------------------------------------------------------------------

summary_lines = [

    "GER",
    "S29 - E10.2.1",
    "Family 2 Operator Audit",
    "",
    f"Candidates audited : {len(classification)}",
    f"Approved           : {len(approved)}",
    f"Reserved           : {len(reserved)}",
    f"Rejected           : {len(rejected)}",
    "",
    "Next step",
    "---------",
    "E10.2.2 - Family 2 Operator Selection",
]

with open(

    OUTPUT_DIR /
    "execution_summary.txt",

    "w",

) as f:

    f.write("\n".join(summary_lines))

# --------------------------------------------------------------------------
# Final audit
# --------------------------------------------------------------------------

expected_files = [

    "candidate_inventory.csv",
    "candidate_inventory.json",

    "operator_admissibility.csv",
    "operator_admissibility_summary.json",

    "operator_classification.csv",
    "operator_classification_summary.json",

    "family2_operator_audit.json",
    "family2_operator_audit.txt",
    "family2_operator_audit.md",

    "campaign_manifest.json",
    "metadata.json",
    "execution_summary.txt",

]

audit = []

for name in expected_files:

    path = OUTPUT_DIR / name

    audit.append({

        "file": name,

        "exists": path.exists(),

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

print("Part 5 completed.")

# ==============================================================================
# MAIN
# ==============================================================================

def main():

    print()
    print("=" * 80)
    print("GER")
    print("S29 - E10.2.1")
    print("Family 2 Operator Audit")
    print("=" * 80)

    # ------------------------------------------------------------------
    # Part 1
    # Candidate inventory
    # ------------------------------------------------------------------

    # (executada automaticamente pelo código da Parte 1)

    # ------------------------------------------------------------------
    # Part 2
    # Admissibility audit
    # ------------------------------------------------------------------

    # (executada automaticamente pelo código da Parte 2)

    # ------------------------------------------------------------------
    # Part 3
    # Scientific classification
    # ------------------------------------------------------------------

    # (executada automaticamente pelo código da Parte 3)

    # ------------------------------------------------------------------
    # Part 4
    # Scientific report
    # ------------------------------------------------------------------

    # (executada automaticamente pelo código da Parte 4)

    # ------------------------------------------------------------------
    # Part 5
    # Campaign manifest
    # ------------------------------------------------------------------

    # (executada automaticamente pelo código da Parte 5)

    print()
    print("=" * 80)
    print("E10.2.1 FINISHED")
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
