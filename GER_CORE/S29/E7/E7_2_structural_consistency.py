"""
GER - Geometria Espectral Relacional
S29 - E7.2

Structural Consistency Analysis

This experiment validates the internal consistency
of the canonical DynamicRegime representation.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import json

from pathlib import Path

from GER.CORE.ger_storage import (
    ExperimentStorage,
)

from GER_CORE.S29.E7.model import (
    Audit,
    Classification,
    Configuration,
    DynamicRegime,
    GeometricSignature,
)

from GER_CORE.S29.E7.consistency import (
    StructuralConsistencyAnalyzer,
)

from GER_CORE.S29.E7.report import (
    generate_consistency_report,
)


# ============================================================
# Configuration
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E7_1/json"
)


# ============================================================
# Helpers
# ============================================================

def latest_certificate() -> Path:

    files = sorted(

        RESULTS_ROOT.glob(
            "*.json"
        )

    )

    if not files:

        raise RuntimeError(

            "No DynamicRegime certificate found."

        )

    return files[-1]


# ============================================================
# Builder
# ============================================================

def load_dynamic_regime(
    path: Path,
) -> DynamicRegime:

    with open(

        path,

        "r",

        encoding="utf-8",

    ) as f:

        data = json.load(f)

    return DynamicRegime(

        configuration=Configuration(
            **data["configuration"]
        ),

        signature=GeometricSignature(
            **data["signature"]
        ),

        classification=Classification(
            **data["classification"]
        ),

        audit=Audit(
            **data["audit"]
        ),

    )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.2")
    print("Structural Consistency Analysis")
    print("=" * 80)
    print()

    certificate = latest_certificate()

    regime = load_dynamic_regime(
        certificate
    )

    result = (

        StructuralConsistencyAnalyzer.analyze(

            regime

        )

    )

    report = generate_consistency_report(
        result
    )

    storage = ExperimentStorage(

        experiment="S29_E7_2",

        folders=[

            "report",

            "json",

        ],

    )

    report_file = storage.file(

        "report",

        "structural_consistency_report.txt",

    )

    with open(

        report_file,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

    summary = {

        "passed": result.passed,

        "checked_fields": result.checked_fields,

        "conflicts": [

            {

                "field": c.field,

                "primary": c.primary_value,

                "secondary": c.secondary_value,

                "description": c.description,

            }

            for c in result.conflicts

        ],

        "warnings": [

            {

                "field": w.field,

                "description": w.description,

            }

            for w in result.warnings

        ],

    }

    summary_file = storage.file(

        "json",

        "structural_consistency.json",

    )

    with open(

        summary_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            summary,

            f,

            indent=4,

            ensure_ascii=False,

        )

    print()

    print("=" * 80)
    print("RESULT")
    print("=" * 80)
    print()

    print(

        f"Report : {report_file}"

    )

    print(

        f"JSON   : {summary_file}"

    )

    print()

    print(

        f"Checked fields : {result.checked_fields}"

    )

    print(

        f"Conflicts      : {len(result.conflicts)}"

    )

    print(

        f"Warnings       : {len(result.warnings)}"

    )

    print()

    if result.passed:

        print(

            "Consistency Status : PASS"

        )

    else:

        print(

            "Consistency Status : FAIL"

        )

    print()

    print("=" * 80)
    print("Finished.")
    print("=" * 80)


# ============================================================

if __name__ == "__main__":

    main()
