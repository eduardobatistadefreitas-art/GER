"""
GER - Geometria Espectral Relacional
S29 - E7.4.7

Canonical Identity Audit

Final audit of the canonical identity operator.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import json

from pathlib import Path

from GER.CORE.ger_storage import (
    ExperimentStorage,
)


# ============================================================
# INPUT
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS"
)

EXPERIMENTS = {

    "Perturbation":
        RESULTS_ROOT
        / "S29_E7_4_1"
        / "json"
        / "identity_perturbation.json",

    "Symmetry":
        RESULTS_ROOT
        / "S29_E7_4_2"
        / "json"
        / "identity_symmetry.json",

    "Reflexivity":
        RESULTS_ROOT
        / "S29_E7_4_3"
        / "json"
        / "identity_reflexivity.json",

    "Transitivity":
        RESULTS_ROOT
        / "S29_E7_4_4"
        / "json"
        / "identity_transitivity.json",

    "Determinism":
        RESULTS_ROOT
        / "S29_E7_4_5"
        / "json"
        / "identity_determinism.json",

    "Serialization":
        RESULTS_ROOT
        / "S29_E7_4_6"
        / "json"
        / "identity_serialization.json",

}


# ============================================================
# JSON LOADER
# ============================================================

def load_json(
    filename: Path,
):

    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


# ============================================================
# AUDIT
# ============================================================

def audit_property(
    name: str,
    filename: Path,
):

    data = load_json(
        filename
    )

    key = next(

        k

        for k in data.keys()

        if k.startswith("operator_")

    )

    approved = bool(
        data[key]
    )

    return {

        "property": name,

        "approved": approved,

        "file": str(
            filename
        ),

    }

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.4.7")
    print("Canonical Identity Audit")
    print("=" * 80)
    print()

    print("Running canonical audit...")
    print()

    results = []

    for name, filename in EXPERIMENTS.items():

        result = audit_property(

            name,

            filename,

        )

        results.append(
            result
        )

        print(f"[{name}]")

        print(
            f"  Approved : "
            f"{result['approved']}"
        )

        print(
            f"  File     : "
            f"{filename.name}"
        )

        print()

    canonical_operator = all(

        result["approved"]

        for result in results

    )

    promotion_ready = canonical_operator

    storage = ExperimentStorage(

        experiment="S29_E7_4_7",

        folders=[

            "report",

            "json",

        ],

    )

    # ========================================================
    # REPORT
    # ========================================================

    report_lines = []

    report_lines.append("=" * 60)
    report_lines.append("GER")
    report_lines.append("CANONICAL IDENTITY AUDIT")
    report_lines.append("=" * 60)
    report_lines.append("")

    report_lines.append(

        "{:<20} {:<10}".format(

            "Property",

            "Approved",

        )

    )

    report_lines.append("-" * 60)

    for result in results:

        report_lines.append(

            "{:<20} {:<10}".format(

                result["property"],

                str(result["approved"]),

            )

        )

    report_lines.append("")
    report_lines.append(
        f"Canonical Operator : {canonical_operator}"
    )

    report_lines.append(
        f"Promotion Ready    : {promotion_ready}"
    )

    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(report_lines)

    report_file = storage.file(

        "report",

        "canonical_identity_audit_report.txt",

    )

    with open(

        report_file,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

    # ========================================================
    # JSON
    # ========================================================

    json_file = storage.file(

        "json",

        "canonical_identity_audit.json",

    )

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "canonical_operator":
                    canonical_operator,

                "promotion_ready":
                    promotion_ready,

                "results":
                    results,

            },

            f,

            indent=4,

            ensure_ascii=False,

        )

    # ========================================================
    # SUMMARY
    # ========================================================

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    for result in results:

        print(

            "{:<20} {}".format(

                result["property"],

                "PASS"

                if result["approved"]

                else "FAIL",

            )

        )

    print()

    print(

        f"Canonical Operator : "

        f"{'APPROVED' if canonical_operator else 'REJECTED'}"

    )

    print(

        f"Promotion to GER/CORE : "

        f"{'READY' if promotion_ready else 'NOT READY'}"

    )

    print()

    print(f"Report : {report_file}")
    print(f"JSON   : {json_file}")

    print()

    print("=" * 80)
    print("Finished.")
    print("=" * 80)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
