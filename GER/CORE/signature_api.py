# ============================================================
# GER
#
# CORE
#
# signature_api.py
#
# Interface pública oficial para produção de
# Assinaturas Geométricas.
#
# Este módulo desacopla os consumidores científicos
# (B37, módulos futuros, auditorias etc.) da
# implementação interna do B35/B36.
# ============================================================

from dataclasses import dataclass
from typing import List


# ============================================================
# Signature
# ============================================================

@dataclass(frozen=True)
class Signature:

    diameter: float

    convergence: float

    recurrence: float

    drift: float


# ============================================================
# API Pública
# ============================================================

def generate_signature(
    *args,
    **kwargs,
) -> Signature:
    """
    Produz uma única Assinatura Geométrica.

    A implementação é fornecida pelo motor do GER.
    """

    raise NotImplementedError(
        "Signature provider not connected."
    )


def generate_signature_dataset(
    n_samples: int,
    *args,
    **kwargs,
) -> List[Signature]:
    """
    Produz um conjunto de Assinaturas Geométricas.

    A implementação é fornecida pelo motor do GER.
    """

    raise NotImplementedError(
        "Signature provider not connected."
    )
  # ============================================================
# Provider Registry
# ============================================================

_signature_provider = None


def register_signature_provider(provider):

    """
    Registra o provider oficial de Assinaturas Geométricas.

    O provider deve implementar:

        generate_signature(...)
        generate_signature_dataset(...)
    """

    global _signature_provider

    _signature_provider = provider


def get_signature_provider():

    return _signature_provider
  # ============================================================
# Provider Protocol
# ============================================================

class SignatureProvider:

    """
    Interface base para qualquer produtor de
    Assinaturas Geométricas.

    Toda implementação deve fornecer os métodos abaixo.
    """

    def generate_signature(
        self,
        *args,
        **kwargs,
    ):

        raise NotImplementedError

    def generate_signature_dataset(
        self,
        n_samples,
        *args,
        **kwargs,
    ):

        raise NotImplementedError


# ============================================================
# Demonstração
# ============================================================

def main():

    print("=" * 60)

    print("GER CORE")

    print("SIGNATURE API")

    print("=" * 60)

    print()

    provider = get_signature_provider()

    if provider is None:

        print("Status")

        print("-" * 60)

        print("No Signature Provider registered.")

        print()

        print("API ready.")

        print("Waiting for engine connection.")

    else:

        print("Status")

        print("-" * 60)

        print("Provider connected:")

        print(type(provider).__name__)

    print()

    print("=" * 60)


# ============================================================

if __name__ == "__main__":

    main()
