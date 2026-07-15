# ============================================================
# GER
#
# CORE
#
# providers
#
# geometry_scan_provider.py
#
# Provider oficial de Assinaturas Geométricas
# utilizando o pipeline S26_B36.
# ============================================================

from GER.CORE.signature_api import (
    Signature,
    SignatureProvider,
)

from GER_CORE.S26_B36_geometry_scan import (
    generate_signature,
    generate_signature_dataset,
)


# ============================================================
# Provider
# ============================================================

class B35SignatureProvider(SignatureProvider):
    """
    Provider oficial baseado no pipeline S26_B36.
    """

    def generate_signature(
        self,
        *args,
        **kwargs,
    ):
        return generate_signature(
            *args,
            **kwargs,
        )

    def generate_signature_dataset(
        self,
        *args,
        **kwargs,
    ):
        return generate_signature_dataset(
            *args,
            **kwargs,
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

    return Signature(
        diameter=diameter,
        convergence=convergence,
        recurrence=recurrence,
        drift=drift,
    )


# ============================================================
# Self Audit
# ============================================================

def audit_provider():

    provider = B35SignatureProvider()

    return {

        "implements_generate_signature":
            hasattr(provider, "generate_signature"),

        "implements_generate_signature_dataset":
            hasattr(provider, "generate_signature_dataset"),

        "implements_protocol":
            isinstance(provider, SignatureProvider),

    }


# ============================================================
# Main
# ============================================================

def main():

    report = audit_provider()

    print("=" * 60)
    print("GER CORE")
    print("GEOMETRY SCAN PROVIDER")
    print("=" * 60)
    print()

    for key, value in report.items():

        print(
            f"{key:<40}"
            f"{'PASS' if value else 'FAIL'}"
        )

    print()

    if all(report.values()):
        print("Provider structure approved.")
    else:
        print("Provider structure rejected.")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
