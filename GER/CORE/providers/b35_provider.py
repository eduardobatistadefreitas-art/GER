# ============================================================
# GER
#
# CORE
#
# providers
#
# b35_provider.py
#
# Implementação oficial do SignatureProvider
# utilizando o motor físico do GER.
#
# ============================================================

from GER.CORE.signature_api import (

    Signature,

    SignatureProvider,

)


class B35SignatureProvider(SignatureProvider):

    """
    Provider oficial baseado no motor físico.

    A implementação será conectada ao pipeline
    B35/B36.
    """

    def generate_signature(

        self,

        *args,

        **kwargs,

    ):

        raise NotImplementedError(

            "B35 provider not connected."

        )

    def generate_signature_dataset(

        self,

        n_samples,

        *args,

        **kwargs,

    ):

        raise NotImplementedError(

            "B35 provider not connected."

        )
      # ============================================================
# Utilitário
# ============================================================

def build_signature(
    diameter,
    convergence,
    recurrence,
    drift,
):

    """
    Constrói uma Signature oficial do GER.
    """

    return Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )


# ============================================================
# Demonstração
# ============================================================

def main():

    print("=" * 60)

    print("GER CORE")

    print("B35 SIGNATURE PROVIDER")

    print("=" * 60)

    print()

    provider = B35SignatureProvider()

    print("Provider")

    print("-" * 60)

    print(type(provider).__name__)

    print()

    print("Status")

    print("-" * 60)

    print("Awaiting connection to B35/B36 pipeline.")

    print()

    print("=" * 60)


# ============================================================

if __name__ == "__main__":

    main()
