"""
========================================================================
GER S29-E2.1

Pipeline Determinism Audit

========================================================================

Objetivo

Auditar o pipeline oficial de geração de Assinaturas Geométricas
em busca de possíveis fontes explícitas de não determinismo.

Este experimento NÃO executa simulações.

========================================================================
"""

import inspect
import re

from GER.CORE import ger_observational_snapshot
from GER.CORE import default_signature_provider
from GER.CORE import ger_structural_certificate

from GER_CORE import S26_B35_persistence_metrics
from GER_CORE.S29 import ger_external_modal_embedding
from GER_CORE.S29 import external_systems


# ============================================================
# Configuration
# ============================================================

EXPERIMENT_VERSION = "1.0"

KEYWORDS = [

    "np.random",
    "random.",
    "random(",
    "seed",
    "shuffle",
    "permutation",
    "datetime",
    "time.time",
    "uuid",

]


# ============================================================
# Audit
# ============================================================

MODULES = [

    (
        "External Simulator",
        external_systems,
    ),

    (
        "External Modal Embedding",
        ger_external_modal_embedding,
    ),

    (
        "Observational Snapshot",
        ger_observational_snapshot,
    ),

    (
        "Persistence Observatory",
        S26_B35_persistence_metrics,
    ),

    (
        "Signature Provider",
        default_signature_provider,
    ),

    (
        "Structural Certificate",
        ger_structural_certificate,
    ),

]


def audit_module(module):

    source = inspect.getsource(module)

    findings = []

    for keyword in KEYWORDS:

        if re.search(re.escape(keyword), source):

            findings.append(keyword)

    return findings


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 72)
    print("GER S29-E2.1")
    print("Pipeline Determinism Audit")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 72)
    print()

    total_findings = 0

    for name, module in MODULES:

        findings = audit_module(module)

        if findings:

            total_findings += len(findings)

            print(f"{name:<32} NON-DETERMINISTIC?")
            print("   Possible sources:")

            for item in findings:
                print(f"      - {item}")

        else:

            print(f"{name:<32} DETERMINISTIC")

    print()
    print("-" * 72)
    print(f"Possible Random Sources : {total_findings}")

    if total_findings == 0:

        print("Pipeline Status : FULLY DETERMINISTIC")

    else:

        print("Pipeline Status : REVIEW REQUIRED")

    print("=" * 72)


# ============================================================

if __name__ == "__main__":

    main()
