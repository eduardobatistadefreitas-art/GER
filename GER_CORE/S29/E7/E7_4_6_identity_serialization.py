"""
GER - Geometria Espectral Relacional
S29 - E7.4.6

Identity Serialization

Experimental validation of serialization invariance
of the canonical identity operator.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import json

from dataclasses import asdict
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

    new_data = dict(
        regime.audit.data
    )

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
# SERIALIZATION
# ============================================================

def serialize_roundtrip(
    regime: DynamicRegime,
) -> DynamicRegime:

    json_text = json.dumps(

        asdict(regime),

        ensure_ascii=False,

        indent=4,

    )

    data = json.loads(
        json_text
    )

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
# SERIALIZATION TEST
# ============================================================

def evaluate_serialization(
    name: str,
    regime: DynamicRegime,
):

    restored = serialize_roundtrip(
        regime
    )

    comparison = IdentityAnalyzer.compare(

        regime,

        restored,

        left=name,

        right=f"{name}_RESTORED",

    )

    return {

        "object": name,

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

        "serialization_ok":

            comparison.configuration_match

            and

            comparison.signature_match

            and

            comparison.classification_match

            and

            comparison.audit_match

            and

            comparison.canonical_identity,

  }

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.4.6")
    print("Identity Serialization")
    print("=" * 80)
    print()

    original = load_dynamic_regime(
        CERTIFICATE
    )

    objects = [

        (
            "Original",
            original,
        ),

        (
            "Configuration",
            perturb_configuration(
                original
            ),
        ),

        (
            "Signature",
            perturb_signature(
                original
            ),
        ),

        (
            "Classification",
            perturb_classification(
                original
            ),
        ),

        (
            "Audit",
            perturb_audit(
                original
            ),
        ),

    ]

    print(
        "Running serialization experiments..."
    )

    print()

    results = []

    for name, obj in objects:

        result = evaluate_serialization(

            name,

            obj,

        )

        results.append(
            result
        )

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
            f"  Identity      : "
            f"{result['canonical_identity']}"
        )

        print(
            f"  Serialization : "
            f"{result['serialization_ok']}"
        )

        print()

    operator_serialization = all(

        result["serialization_ok"]

        for result in results

    )

    storage = ExperimentStorage(

        experiment="S29_E7_4_6",

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
    report_lines.append("IDENTITY SERIALIZATION REPORT")
    report_lines.append("=" * 60)
    report_lines.append("")

    report_lines.append(
        f"Certificate : {CERTIFICATE.name}"
    )

    report_lines.append("")

    report_lines.append(

        "{:<18} {:<15}".format(

            "Object",

            "Serialization",

        )

    )

    report_lines.append("-" * 60)

    for result in results:

        report_lines.append(

            "{:<18} {:<15}".format(

                result["object"],

                str(
                    result["serialization_ok"]
                ),

            )

        )

    report_lines.append("")
    report_lines.append(
        f"Operator Serialization : {operator_serialization}"
    )

    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(
        report_lines
    )

    report_file = storage.file(

        "report",

        "identity_serialization_report.txt",

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

        "identity_serialization.json",

    )

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "operator_serialization":
                    operator_serialization,

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

                result["object"],

                "PASS"

                if result["serialization_ok"]

                else "FAIL",

            )

        )

    print()

    print(

        f"Operator Serialization : "

        f"{'APPROVED' if operator_serialization else 'REJECTED'}"

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
