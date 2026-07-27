"""
GER - Geometria Espectral Relacional
S29 - E7.4.2

Identity Symmetry

Experimental validation of the symmetry property
of the canonical identity operator.

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
# COMPARISON
# ============================================================

def compare_pair(
    left: DynamicRegime,
    right: DynamicRegime,
    left_name: str,
    right_name: str,
):

    comparison = IdentityAnalyzer.compare(

        left,

        right,

        left=left_name,

        right=right_name,

    )

    return {

        "left": left_name,

        "right": right_name,

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

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.4.2")
    print("Identity Symmetry")
    print("=" * 80)
    print()

    original = load_dynamic_regime(
        CERTIFICATE
    )

    configuration = perturb_configuration(
        original
    )

    signature = perturb_signature(
        original
    )

    classification = perturb_classification(
        original
    )

    audit = perturb_audit(
        original
    )

    experiments = [

        (
            "Configuration",
            original,
            configuration,
        ),

        (
            "Signature",
            original,
            signature,
        ),

        (
            "Classification",
            original,
            classification,
        ),

        (
            "Audit",
            original,
            audit,
        ),

    ]

    results = []

    print("Running symmetry experiments...")
    print()

    for name, left, right in experiments:

        forward = compare_pair(

            left,

            right,

            "Original",

            name,

        )

        reverse = compare_pair(

            right,

            left,

            name,

            "Original",

        )

        symmetric = (

            forward["configuration_match"]
            ==
            reverse["configuration_match"]

            and

            forward["signature_match"]
            ==
            reverse["signature_match"]

            and

            forward["classification_match"]
            ==
            reverse["classification_match"]

            and

            forward["audit_match"]
            ==
            reverse["audit_match"]

            and

            forward["canonical_identity"]
            ==
            reverse["canonical_identity"]

        )

        result = {

            "pair": name,

            "forward_identity":
                forward["canonical_identity"],

            "reverse_identity":
                reverse["canonical_identity"],

            "configuration_match":
                forward["configuration_match"],

            "signature_match":
                forward["signature_match"],

            "classification_match":
                forward["classification_match"],

            "audit_match":
                forward["audit_match"],

            "symmetric":
                symmetric,

        }

        results.append(
            result
        )

        print(f"[{name}]")

        print(
            f"  Forward Identity : "
            f"{result['forward_identity']}"
        )

        print(
            f"  Reverse Identity : "
            f"{result['reverse_identity']}"
        )

        print(
            f"  Symmetric        : "
            f"{result['symmetric']}"
        )

        print()

    operator_symmetry = all(

        item["symmetric"]

        for item in results

    )

    storage = ExperimentStorage(

        experiment="S29_E7_4_2",

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
    report_lines.append("IDENTITY SYMMETRY REPORT")
    report_lines.append("=" * 60)
    report_lines.append("")

    report_lines.append(
        f"Certificate : {CERTIFICATE.name}"
    )

    report_lines.append("")

    report_lines.append(

        "{:<18} {:<8} {:<8} {:<10}".format(

            "Pair",

            "Forward",

            "Reverse",

            "Symmetric",

        )

    )

    report_lines.append("-" * 60)

    for result in results:

        report_lines.append(

            "{:<18} {:<8} {:<8} {:<10}".format(

                result["pair"],

                str(
                    result["forward_identity"]
                ),

                str(
                    result["reverse_identity"]
                ),

                str(
                    result["symmetric"]
                ),

            )

        )

    report_lines.append("")
    report_lines.append(
        f"Operator Symmetry : {operator_symmetry}"
    )

    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(report_lines)

    report_file = storage.file(

        "report",

        "identity_symmetry_report.txt",

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

        "identity_symmetry.json",

    )

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "operator_symmetry":
                    operator_symmetry,

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

            "{:<18} {}".format(

                result["pair"],

                "PASS"

                if result["symmetric"]

                else "FAIL",

            )

        )

    print()

    print(
        f"Operator Symmetry : "
        f"{'APPROVED' if operator_symmetry else 'REJECTED'}"
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
