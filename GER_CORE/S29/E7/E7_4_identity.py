"""
GER - Geometria Espectral Relacional
S29 - E7.4

Relational Identity

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

from GER_CORE.S29.E7.identity import (
    IdentityAnalyzer,
)

from GER_CORE.S29.E7.identity_report import (
    generate_identity_report,
)


# ============================================================
# INPUT CERTIFICATES
# ============================================================

LEFT_CERTIFICATE = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E7_1/json/dynamic_regime_certificate.json"
)

RIGHT_CERTIFICATE = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E7_1/json/dynamic_regime_certificate.json"
)


# ============================================================
# Loader
# ============================================================

def load_dynamic_regime(path: Path) -> DynamicRegime:

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
    print("S29-E7.4")
    print("Relational Identity")
    print("=" * 80)
    print()

    left = load_dynamic_regime(
        LEFT_CERTIFICATE
    )

    right = load_dynamic_regime(
        RIGHT_CERTIFICATE
    )

    comparison = IdentityAnalyzer.compare(

        left,

        right,

        LEFT_CERTIFICATE.stem,

        RIGHT_CERTIFICATE.stem,

    )

    report = generate_identity_report(
        comparison
    )

    storage = ExperimentStorage(

        experiment="S29_E7_4",

        folders=[
            "report",
            "json",
        ],

    )

    report_file = storage.file(

        "report",

        "identity_report.txt",

    )

    with open(

        report_file,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

    summary = {

        "left": comparison.left,

        "right": comparison.right,

        "configuration_match":
            comparison.configuration_match,

        "signature_match":
            comparison.signature_match,

        "classification_match":
            comparison.classification_match,

        "audit_match":
            comparison.audit_match,

        "canonical_identity":
            comparison.canonical_identity,

    }

    json_file = storage.file(

        "json",

        "identity_result.json",

    )

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            summary,

            f,

            indent=4,

            ensure_ascii=False,

        )

    print("=" * 80)
    print("RESULT")
    print("=" * 80)
    print()

    print(f"Left  : {comparison.left}")
    print(f"Right : {comparison.right}")
    print()

    print(
        f"Configuration : {comparison.configuration_match}"
    )

    print(
        f"Signature     : {comparison.signature_match}"
    )

    print(
        f"Classification: {comparison.classification_match}"
    )

    print(
        f"Audit         : {comparison.audit_match}"
    )

    print()

    print(
        f"Canonical Identity : {comparison.canonical_identity}"
    )

    print()

    print(f"Report : {report_file}")
    print(f"JSON   : {json_file}")

    print()

    print("=" * 80)
    print("Finished.")
    print("=" * 80)


if __name__ == "__main__":

    main()
