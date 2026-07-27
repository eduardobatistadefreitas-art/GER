"""
GER - Geometria Espectral Relacional
S29 - E7.1

DynamicRegime Structural Certificate

This experiment generates the canonical structural
certificate for a DynamicRegime.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import json

from pathlib import Path

from GER.CORE.ger_storage import (
    ExperimentStorage,
)

from GER_CORE.S29.E7.E7_builder import (
    DynamicRegimeBuilder,
)

from GER_CORE.S29.E7.serializer import (
    dynamic_regime_to_dict,
)

from GER_CORE.S29.E7.certificate import (
    generate_certificate,
)


# ============================================================
# Configuration
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S26"
)

STATIONARY_SCAN = (
    RESULTS_ROOT /
    "S26_B36_stationary_scan"
)

CLASSIFIER = (
    RESULTS_ROOT /
    "S26_B36_classifier"
)

CLASSIFIER_AUDIT = (
    RESULTS_ROOT /
    "S26_B36_1_classifier_audit"
)


# ============================================================
# Helpers
# ============================================================

def latest_json(

    folder: Path,

    filename: str,

) -> Path:

    """
    Return latest execution JSON.
    """

    runs = sorted(

        p

        for p in folder.iterdir()

        if p.is_dir()

    )

    if not runs:

        raise RuntimeError(

            f"No executions found in {folder}"

        )

    return (

        runs[-1]

        /

        filename

    )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.1")
    print("DynamicRegime Structural Certificate")
    print("=" * 80)
    print()

    stationary_scan = latest_json(

        STATIONARY_SCAN,

        "stationary_scan.json",

    )

    classifier = latest_json(

        CLASSIFIER,

        "classifier.json",

    )

    classifier_audit = latest_json(

        CLASSIFIER_AUDIT,

        "classifier_audit.json",

    )

    regime = DynamicRegimeBuilder.build(

        stationary_scan_path=stationary_scan,

        classifier_path=classifier,

        classifier_audit_path=classifier_audit,

    )

    certificate_text = generate_certificate(

        regime

    )

    certificate_json = dynamic_regime_to_dict(

        regime

    )

    storage = ExperimentStorage(

        experiment="S29_E7_1",

        folders=[

            "certificate",

            "json",

        ],

    )

    certificate_txt = storage.file(

        "certificate",

        "dynamic_regime_certificate.txt",

    )

    certificate_json_file = storage.file(

        "json",

        "dynamic_regime_certificate.json",

    )

    with open(

        certificate_txt,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            certificate_text

        )

    with open(

        certificate_json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            certificate_json,

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

        f"Certificate : {certificate_txt}"

    )

    print(

        f"JSON        : {certificate_json_file}"

    )

    print()

    print(

        "DynamicRegime successfully reconstructed."

    )

    print(

        "Structural certificate successfully generated."

    )

    print()

    print("=" * 80)

    print("SUMMARY")

    print("=" * 80)

    print()

    print(

        f"Regime              : "

        f"{regime.classification.regime}"

    )

    print(

        f"Persistence Score   : "

        f"{regime.classification.persistence_score:.6f}"

    )

    print(

        f"Persistence Var.    : "

        f"{regime.classification.persistence_variance:.6e}"

    )

    print()

    print("Signature")

    print("-" * 80)

    print(

        f"Diameter            : "

        f"{regime.signature.diameter}"

    )

    print(

        f"Convergence         : "

        f"{regime.signature.convergence}"

    )

    print(

        f"Recurrence          : "

        f"{regime.signature.recurrence}"

    )

    print(

        f"Drift               : "

        f"{regime.signature.drift}"

    )

    print()

    print("=" * 80)

    print("Finished.")

    print("=" * 80)


# ============================================================

if __name__ == "__main__":

    main()
