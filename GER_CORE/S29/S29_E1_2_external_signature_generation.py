"""
=========================================================
GER
S29-E1.2

External Signature Generation
=========================================================

Primeira validação do pipeline oficial de geração
de Assinaturas Geométricas para sistemas externos.

Pipeline

External System
        ↓
External Modal Embedding
        ↓
Observational Snapshot
        ↓
Persistence Observatory
        ↓
Geometric Signature
        ↓
Structural Certificate

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)

from GER.CORE.signature_api import (
    Signature,
    generate_signature,
    register_signature_provider,
)

from GER.CORE.default_signature_provider import (
    DefaultSignatureProvider,
)

from GER.CORE.ger_structural_certificate import (
    structural_certificate,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S29.ger_external_modal_embedding import (
    build_external_gamma,
)

from GER_CORE.S29.external_systems import (
    simulate_duffing
)


# =========================================================
# Version
# =========================================================

EXPERIMENT_VERSION = "1.0"


# =========================================================
# Result Container
# =========================================================

@dataclass(frozen=True)
class ExternalSignatureResult:
    """
    Resultado completo da geração de uma
    Assinatura Geométrica para um sistema externo.
    """

    system: str

    signature: Signature

    observables: dict

    certificate: dict


# =========================================================
# Initialization
# =========================================================

def initialize_signature_provider():
    """
    Registra o Signature Provider oficial do CORE.

    Pode ser chamado múltiplas vezes sem efeitos
    colaterais relevantes.
    """

    register_signature_provider(
        DefaultSignatureProvider()
    )


# =========================================================
# Internal Pipeline
# =========================================================

def _generate_gamma(
    signal,
):
    """
    Executa o acoplamento modal do sistema externo.
    """

    gamma_sequence, eigenvectors = (
        build_external_gamma(
            signal,
        )
    )

    return gamma_sequence, eigenvectors


def _build_snapshots(
    gamma_sequence,
    eigenvectors,
    time,
):
    """
    Constrói os snapshots observacionais
    utilizados pelo Observatório GER.
    """

    snapshots = []

    for step, gamma in enumerate(gamma_sequence):

        snapshots.append(

            build_observational_snapshot(

                gamma,

                eigenvectors,

                step=step,

                time=time[step],

            )

        )

    return snapshots


def _compute_signature(
    snapshots,
    dt,
):
    """
    Executa o Observatório de Persistência
    seguido da geração da Assinatura Geométrica.
    """

    observables = run_persistence_observatory(
        snapshots,
        dt,
    )

    signature = generate_signature(
        observables,
        dt,
    )

    return signature, observables


def _build_certificate(
    signature,
):
    """
    Constrói o Certificado Estrutural oficial.
    """

    return structural_certificate(
        signature,
    )
  # =========================================================
# Public Pipeline
# =========================================================

def run_external_signature_generation(
    system_name,
    time,
    signal,
    dt,
):
    """
    Executa o pipeline completo de geração de uma
    Assinatura Geométrica para um sistema externo.
    """

    gamma_sequence, eigenvectors = _generate_gamma(
        signal,
    )

    snapshots = _build_snapshots(
        gamma_sequence,
        eigenvectors,
        time,
    )

    signature, observables = _compute_signature(
        snapshots,
        dt,
    )

    certificate = _build_certificate(
        signature,
    )

    return ExternalSignatureResult(

        system=system_name,

        signature=signature,

        observables=observables,

        certificate=certificate,

    )


# =========================================================
# Report
# =========================================================

def report_results(
    result: ExternalSignatureResult,
):
    """
    Exibe um relatório resumido do experimento.
    """

    print("=" * 60)
    print("GER S29-E1.2")
    print("External Signature Generation")
    print(f"Version {EXPERIMENT_VERSION}")
    print("=" * 60)
    print()

    print("System")
    print("------")
    print(result.system)
    print()

    print("Geometric Signature")
    print("-------------------")

    print(
        f"Diameter     : "
        f"{result.signature.diameter:.6f}"
    )

    print(
        f"Convergence : "
        f"{result.signature.convergence:.6f}"
    )

    print(
        f"Recurrence  : "
        f"{result.signature.recurrence:.6f}"
    )

    print(
        f"Drift       : "
        f"{result.signature.drift:.6e}"
    )

    print()

    print("Structural Certificate")
    print("----------------------")

    for deduction in result.certificate["deductions"]:

        print(
            f"{deduction['rule']:<24}"
            f"{deduction['status']}"
        )

    print()

    summary = result.certificate["summary"]

    print("Summary")
    print("-------")

    print(
        f"Passed : {summary['passed']}"
    )

    print(
        f"Failed : {summary['failed']}"
    )

    print()

    print("=" * 60)

    if summary["failed"] == 0:

        print(
            "STATUS : "
            "FIRST EXTERNAL SIGNATURE GENERATED"
        )

    else:

        print(
            "STATUS : "
            "CERTIFICATION FAILED"
        )

    print("=" * 60)


# =========================================================
# Main
# =========================================================

def main():

    DT = 0.01

    initialize_signature_provider()

    time, signal = simulate_duffing(
        dt=DT,
    )

    result = run_external_signature_generation(

        system_name="Duffing",

        time=time,

        signal=signal,

        dt=DT,

    )

    report_results(
        result,
    )


# =========================================================

if __name__ == "__main__":

    main()
