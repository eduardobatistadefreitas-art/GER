"""
GER - Geometria Espectral Relacional
S29 - E7.4.4

Identity Transitivity

Experimental validation of the transitivity property
of the canonical identity operator.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import copy
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
# COMPARISON
# ============================================================

def identity(
    left: DynamicRegime,
    right: DynamicRegime,
) -> bool:

    comparison = IdentityAnalyzer.compare(
        left,
        right,
        left="A",
        right="B",
    )

    return comparison.canonical_identity


# ============================================================
# TRANSITIVITY
# ============================================================

def evaluate_transitivity(
    name: str,
    prototype: DynamicRegime,
):

    A = copy.deepcopy(prototype)
    B = copy.deepcopy(prototype)
    C = copy.deepcopy(prototype)

    ab = identity(A, B)
    bc = identity(B, C)
    ac = identity(A, C)

    transitive = (ab and bc) <= ac

    return {

        "object": name,

        "AB": ab,

        "BC": bc,

        "AC": ac,

        "transitive": transitive,

    }

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.4.4")
    print("Identity Transitivity")
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
        "Running transitivity experiments..."
    )

    print()

    results = []

    for name, obj in objects:

        result = evaluate_transitivity(

            name,

            obj,

        )

        results.append(
            result
        )

        print(f"[{name}]")

        print(
            f"  I(A,B) : {result['AB']}"
        )

        print(
            f"  I(B,C) : {result['BC']}"
        )

        print(
            f"  I(A,C) : {result['AC']}"
        )

        print(
            f"  Transitive : "
            f"{result['transitive']}"
        )

        print()

    operator_transitivity = all(

        result["transitive"]

        for result in results

    )

    storage = ExperimentStorage(

        experiment="S29_E7_4_4",

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
    report_lines.append("IDENTITY TRANSITIVITY REPORT")
    report_lines.append("=" * 60)
    report_lines.append("")

    report_lines.append(
        f"Certificate : {CERTIFICATE.name}"
    )

    report_lines.append("")

    report_lines.append(

        "{:<18} {:<8} {:<8} {:<8} {:<12}".format(

            "Object",

            "I(A,B)",

            "I(B,C)",

            "I(A,C)",

            "Transitive",

        )

    )

    report_lines.append("-" * 60)

    for result in results:

        report_lines.append(

            "{:<18} {:<8} {:<8} {:<8} {:<12}".format(

                result["object"],

                str(result["AB"]),

                str(result["BC"]),

                str(result["AC"]),

                str(result["transitive"]),

            )

        )

    report_lines.append("")
    report_lines.append(
        f"Operator Transitivity : {operator_transitivity}"
    )
    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(report_lines)

    report_file = storage.file(

        "report",

        "identity_transitivity_report.txt",

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

        "identity_transitivity.json",

    )

    with open(

        json_file,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "operator_transitivity":
                    operator_transitivity,

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

                if result["transitive"]

                else "FAIL",

            )

        )

    print()

    print(

        f"Operator Transitivity : "

        f"{'APPROVED' if operator_transitivity else 'REJECTED'}"

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
