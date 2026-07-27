"""
GER - Geometria Espectral Relacional
S29 - E7.4.1

Identity Perturbation

Evaluates the robustness of the canonical identity under
controlled perturbations of a DynamicRegime.

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


# ============================================================
# INPUT
# ============================================================

CERTIFICATE = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29_E7_1/json/dynamic_regime_certificate.json"
)


# ============================================================
# LOADER
# ============================================================

def load_dynamic_regime(
    certificate: Path,
) -> DynamicRegime:

    with open(
        certificate,
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
        )
        if data.get("audit") is not None
        else None,

    )


# ============================================================
# PERTURBATIONS
# ============================================================

def perturb_configuration(
    regime: DynamicRegime,
) -> DynamicRegime:

    return DynamicRegime(

        configuration=Configuration(

            beta=regime.configuration.beta + 1,

            sigma=regime.configuration.sigma,

            potential=regime.configuration.potential,

            timesteps=regime.configuration.timesteps,

            dt=regime.configuration.dt,

        ),

        signature=regime.signature,

        classification=regime.classification,

        audit=regime.audit,

    )


def perturb_signature(
    regime: DynamicRegime,
) -> DynamicRegime:

    return DynamicRegime(

        configuration=regime.configuration,

        signature=GeometricSignature(

            diameter=regime.signature.diameter + 1e-6,

            convergence=regime.signature.convergence,

            recurrence=regime.signature.recurrence,

            drift=regime.signature.drift,

        ),

        classification=regime.classification,

        audit=regime.audit,

    )


def perturb_classification(
    regime: DynamicRegime,
) -> DynamicRegime:

    return DynamicRegime(

        configuration=regime.configuration,

        signature=regime.signature,

        classification=Classification(

            regime="TEST_CLASSIFICATION",

            persistence_score=(
                regime.classification.persistence_score
            ),

            persistence_variance=(
                regime.classification.persistence_variance
            ),

        ),

        audit=regime.audit,

    )


def perturb_audit(
    regime: DynamicRegime,
) -> DynamicRegime:

    if regime.audit is None:

        return regime

    new_data = dict(regime.audit.data)

    new_data["regime"] = "TEST_AUDIT"

    return DynamicRegime(

        configuration=regime.configuration,

        signature=regime.signature,

        classification=regime.classification,

        audit=Audit(

            data=new_data,

        ),

    )

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.4.1")
    print("Identity Perturbation")
    print("=" * 80)
    print()

    original = load_dynamic_regime(
        CERTIFICATE
    )

    experiments = [

        (
            "Configuration",
            perturb_configuration(original),
        ),

        (
            "Signature",
            perturb_signature(original),
        ),

        (
            "Classification",
            perturb_classification(original),
        ),

        (
            "Audit",
            perturb_audit(original),
        ),

    ]

    results = []

    print("Running perturbation experiments...")
    print()

    for name, perturbed in experiments:

        comparison = IdentityAnalyzer.compare(

            original,

            perturbed,

            left="Original",

            right=name,

        )

        result = {

            "perturbation": name,

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

        results.append(result)

        print(f"[{name}]")

        print(
            f"  Configuration : "
            f"{result['configuration_match']}"
        )

        print(
            f"  Signature     : "
            f"{result['signature_match']}"
        )

        print(
            f"  Classification: "
            f"{result['classification_match']}"
        )

        print(
            f"  Audit         : "
            f"{result['audit_match']}"
        )

        print(
            f"  Canonical Identity : "
            f"{result['canonical_identity']}"
        )

        print()

    storage = ExperimentStorage(

        experiment="S29_E7_4_1",

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
    report_lines.append("IDENTITY PERTURBATION REPORT")
    report_lines.append("=" * 60)
    report_lines.append("")

    report_lines.append(
        f"Certificate : {CERTIFICATE.name}"
    )

    report_lines.append("")

    report_lines.append(
        "{:<20} {:<6} {:<6} {:<6} {:<6} {:<8}".format(
            "Perturbation",
            "Cfg",
            "Sig",
            "Cls",
            "Aud",
            "Identity",
        )
    )

    report_lines.append("-" * 60)

    for result in results:

        report_lines.append(

            "{:<20} {:<6} {:<6} {:<6} {:<6} {:<8}".format(

                result["perturbation"],

                str(result["configuration_match"]),

                str(result["signature_match"]),

                str(result["classification_match"]),

                str(result["audit_match"]),

                str(result["canonical_identity"]),

            )

        )

    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(report_lines)

    report_file = storage.file(

        "report",

        "identity_perturbation_report.txt",

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

        "identity_perturbation.json",

    )

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            results,

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

                result["perturbation"],

                result["canonical_identity"],

            )

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
