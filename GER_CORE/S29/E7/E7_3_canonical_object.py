"""
GER - Geometria Espectral Relacional
S29 - E7.3

Canonical Object Analysis

Determines the canonical structure of a
DynamicRegime object.

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

from GER_CORE.S29.E7.canonical import (
    CanonicalObjectAnalyzer,
)

from GER_CORE.S29.E7.report_canonical import (
    generate_canonical_report,
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
        RESULTS_ROOT.glob("*.json")
    )

    if not files:
        raise RuntimeError(
            "No DynamicRegime certificate found."
        )

    return files[-1]


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
    print("S29-E7.3")
    print("Canonical Object Analysis")
    print("=" * 80)
    print()

    certificate = latest_certificate()

    regime = load_dynamic_regime(
        certificate
    )

    analysis = (

        CanonicalObjectAnalyzer.analyze(
            regime
        )

    )

    report = generate_canonical_report(
        analysis
    )

    storage = ExperimentStorage(

        experiment="S29_E7_3",

        folders=[
            "report",
            "json",
        ],

    )

    report_file = storage.file(

        "report",
        "canonical_object_report.txt",

    )

    with open(

        report_file,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

    summary = {

        "core_components": analysis.core_components,

        "derived_components": analysis.derived_components,

        "metadata_components": analysis.metadata_components,

        "unknown_components": analysis.unknown_components,

        "components": [

            {

                "name": c.name,

                "category": c.category,

                "required": c.required,

                "reason": c.reason,

            }

            for c in analysis.components

        ],

    }

    summary_file = storage.file(

        "json",

        "canonical_object_analysis.json",

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
        f"Core Components      : {analysis.core_components}"
    )

    print(
        f"Derived Components  : {analysis.derived_components}"
    )

    print(
        f"Metadata Components : {analysis.metadata_components}"
    )

    print(
        f"Unknown Components  : {analysis.unknown_components}"
    )

    print()

    print("=" * 80)
    print("Finished.")
    print("=" * 80)


# ============================================================

if __name__ == "__main__":

    main()
