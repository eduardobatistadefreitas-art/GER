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
# da implementação interna do motor.
#
# Compatibilidade:
#     Todas as interfaces anteriores permanecem válidas.
#
# Versão:
#     2.0
# ============================================================

from dataclasses import dataclass, asdict


# ============================================================
# Signature
# ============================================================

@dataclass(frozen=True)
class Signature:

    diameter: float

    convergence: float

    recurrence: float

    drift: float

    def to_dict(self):
        """
        Converts the signature into a dictionary.
        """
        return asdict(self)

    def to_tuple(self):
        """
        Converts the signature into an immutable tuple.

        Useful for numerical processing.
        """
        return (
            self.diameter,
            self.convergence,
            self.recurrence,
            self.drift,
        )

    def __iter__(self):
        """
        Backward compatibility.

        Allows legacy code such as

            dict(signature)
        """
        return iter(asdict(self).items())


# ============================================================
# Provider Registry
# ============================================================

_signature_provider = None


def register_signature_provider(provider):
    """
    Registers the official Signature Provider.
    """

    global _signature_provider

    _signature_provider = provider


def get_signature_provider():

    return _signature_provider


def _require_provider():

    provider = get_signature_provider()

    if provider is None:

        raise RuntimeError(
            "No SignatureProvider registered."
        )

    return provider


# ============================================================
# Public API
# ============================================================

def generate_signature(
    *args,
    **kwargs,
):
    """
    Generates a single geometric signature.
    """

    provider = _require_provider()

    return provider.generate_signature(
        *args,
        **kwargs,
    )


def generate_signature_dataset(
    n_samples,
    *args,
    **kwargs,
):
    """
    Generates a collection of signatures.
    """

    provider = _require_provider()

    return provider.generate_signature_dataset(
        n_samples,
        *args,
        **kwargs,
    )


# ============================================================
# New High-Level API
# ============================================================

def load_signatures(
    *args,
    **kwargs,
):
    """
    Loads all available signatures.

    The provider decides where the signatures come from
    (memory, parquet, database, experiments, etc.).
    """

    provider = _require_provider()

    return provider.load_signatures(
        *args,
        **kwargs,
    )


def available_signatures():
    """
    Returns the number of available signatures.
    """

    provider = _require_provider()

    return provider.available_signatures()


def signature_dimension():
    """
    Returns the intrinsic signature dimension.
    """

    provider = _require_provider()

    return provider.signature_dimension()


# ============================================================
# Provider Protocol
# ============================================================

class SignatureProvider:
    """
    Base interface implemented by every official
    Signature Provider.
    """

    # --------------------------------------------------------

    def generate_signature(
        self,
        *args,
        **kwargs,
    ):
        raise NotImplementedError

    # --------------------------------------------------------

    def generate_signature_dataset(
        self,
        n_samples,
        *args,
        **kwargs,
    ):
        raise NotImplementedError

    # --------------------------------------------------------
    # New API
    # --------------------------------------------------------

    def load_signatures(
        self,
        *args,
        **kwargs,
    ):
        """
        Returns every available signature.
        """
        raise NotImplementedError

    def available_signatures(self):
        """
        Returns the number of available signatures.
        """
        raise NotImplementedError

    def signature_dimension(self):
        """
        Returns the intrinsic signature dimension.
        """
        raise NotImplementedError


# ============================================================
# Demonstration
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

        try:

            print(
                f"Available Signatures : "
                f"{provider.available_signatures()}"
            )

        except Exception:
            pass

        try:

            print(
                f"Signature Dimension  : "
                f"{provider.signature_dimension()}"
            )

        except Exception:
            pass

    print()
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
