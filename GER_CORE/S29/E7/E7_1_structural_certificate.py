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

from GER_CORE.OPERATORS.result_manager import ResultManager

from GER_CORE.S29.E7.E7_builder import (
    DynamicRegimeBuilder,
)

from GER_CORE.S29.E7.certificate import (
    generate_certificate,
)


# =============================================================================
# Configuration
# =============================================================================

RESULTS_ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S26")

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


# =============================================================================
# Helpers
# =============================================================================

def latest_json(folder: Path, filename: str) -> Path:

    runs = sorted(
        p for p in folder.iterdir()
        if p.is_dir()
    )

    if not runs:
        raise RuntimeError(
            f"No executions found in {folder}"
        )

    return runs[-1] / filename


# =============================================================================
# Main
# =============================================================================

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

    certificate = generate_certificate(
        regime
    )

    manager = ResultManager(
        experiment="S29_E7_1"
    )

    output = manager.get_output_directory()

    certificate_file = (
        output /
        "dynamic_regime_certificate.json"
    )

    with open(
        certificate_file,
        "w",
        encoding="utf8",
    ) as f:

        json.dump(
            certificate,
            f,
            indent=4,
            ensure_ascii=False,
        )

    report = output / "certificate_report.txt"

    with open(
        report,
        "w",
        encoding="utf8",
    ) as f:

        f.write(
            "GER\n"
        )

        f.write(
            "DynamicRegime Structural Certificate\n\n"
        )

        f.write(
            "Configuration\n"
        )

        f.write(
            "-" * 40 + "\n"
        )

        for k, v in certificate[
            "configuration"
        ].items():

            f.write(
                f"{k:20} {v}\n"
            )

        f.write("\n")

        f.write(
            "Signature\n"
        )

        f.write(
            "-" * 40 + "\n"
        )

        for k, v in certificate[
            "signature"
        ].items():

            f.write(
                f"{k:20} {v}\n"
            )

        f.write("\n")

        f.write(
            "Classification\n"
        )

        f.write(
            "-" * 40 + "\n"
        )

        for k, v in certificate[
            "classification"
        ].items():

            f.write(
                f"{k:20} {v}\n"
            )

        f.write("\n")

        f.write(
            "Integrity\n"
        )

        f.write(
            "-" * 40 + "\n"
        )

        for k, v in certificate[
            "integrity"
        ]["checks"].items():

            status = (
                "PASS"
                if v
                else "FAIL"
            )

            f.write(
                f"{k:30} {status}\n"
            )

        f.write("\n")

        f.write(
            "Certificate Status\n"
        )

        f.write(
            "-" * 40 + "\n"
        )

        if certificate[
            "integrity"
        ]["passed"]:

            f.write("VALID\n")

        else:

            f.write("INVALID\n")

    print()

    print("=" * 80)
    print("RESULT")
    print("=" * 80)

    print()

    print(
        f"Certificate : {certificate_file}"
    )

    print(
        f"Report      : {report}"
    )

    print()

    print(
        "Structural certificate successfully generated."
    )


# =============================================================================

if __name__ == "__main__":
    main()
