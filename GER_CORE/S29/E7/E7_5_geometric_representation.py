"""
GER - Geometria Espectral Relacional

S29 - E7.5

Geometric Representation

Scientific question
-------------------

How should a DynamicRegime be represented geometrically?

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import json

from pathlib import Path

from GER.CORE.storage import ExperimentStorage

from GER_CORE.S29.E7.E7_builder import (
    DynamicRegimeBuilder,
)

from GER_CORE.S29.E7.representation_analyzer import (
    RepresentationAnalyzer,
)


# ============================================================
# INPUT FILES
# ============================================================

STATIONARY_SCAN = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S26_B36_1/json/stationary_scan.json"
)

CLASSIFIER = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S26_B36_1/json/classifier.json"
)

CLASSIFIER_AUDIT = Path(
    "/content/drive/MyDrive/GER_RESULTS/"
    "S26_B36_1/json/classifier_audit.json"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.5")
    print("Geometric Representation")
    print("=" * 80)
    print()

    print("Building DynamicRegime...")
    print()

    regime = DynamicRegimeBuilder.build(

        stationary_scan_path=STATIONARY_SCAN,

        classifier_path=CLASSIFIER,

        classifier_audit_path=CLASSIFIER_AUDIT,

    )

    print("[OK] DynamicRegime created.")
    print()

    print("Running representation analysis...")
    print()

    analysis = RepresentationAnalyzer.analyze(
        regime
    )

    storage = ExperimentStorage(

        experiment="S29_E7_5",

        folders=[

            "json",

            "report",

        ],

    )

    # ========================================================
    # REPORT
    # ========================================================

    report_lines = []

    report_lines.append("=" * 60)
    report_lines.append("GER")
    report_lines.append("GEOMETRIC REPRESENTATION")
    report_lines.append("=" * 60)
    report_lines.append("")

    report_lines.append(
        "{:<15} {:<12} {:<12}".format(
            "Hypothesis",
            "Supported",
            "Confidence",
        )
    )

    report_lines.append("-" * 60)

    for evidence in analysis.evidences:

        report_lines.append(

            "{:<15} {:<12} {:<12.3f}".format(

                evidence.hypothesis.value,

                str(evidence.supported),

                evidence.confidence,

            )

        )

    report_lines.append("")
    report_lines.append(
        f"Recommended : {analysis.recommended.value}"
    )

    report_lines.append(
        f"Completed   : {analysis.completed}"
    )

    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(
        report_lines
    )

    report_file = storage.file(

        "report",

        "geometric_representation_report.txt",

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

        "geometric_representation.json",

    )

    json_data = {

        "recommended":
            analysis.recommended.value,

        "completed":
            analysis.completed,

        "hypotheses": [

            {

                "representation":
                    evidence.hypothesis.value,

                "supported":
                    evidence.supported,

                "confidence":
                    evidence.confidence,

                "reason":
                    evidence.reason,

            }

            for evidence in analysis.evidences

        ],

    }

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            json_data,

            f,

            indent=4,

            ensure_ascii=False,

        )

      # ========================================================
    # SUMMARY
    # ========================================================

    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    for evidence in analysis.evidences:

        print(f"[{evidence.hypothesis.value}]")
        print(
            f"  Supported : {evidence.supported}"
        )
        print(
            f"  Confidence: {evidence.confidence:.3f}"
        )
        print(
            f"  Reason    : {evidence.reason}"
        )
        print()

    print("=" * 80)
    print("FINAL DECISION")
    print("=" * 80)
    print()

    print(
        f"Recommended Representation : "
        f"{analysis.recommended.value}"
    )

    print(
        f"Analysis Completed         : "
        f"{analysis.completed}"
    )

    print()

    print("=" * 80)
    print("OUTPUT")
    print("=" * 80)

    print(
        f"Report : {report_file}"
    )

    print(
        f"JSON   : {json_file}"
    )

    print()

    print("=" * 80)
    print("Finished.")
    print("=" * 80)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
