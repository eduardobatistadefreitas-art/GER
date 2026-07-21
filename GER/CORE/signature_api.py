# ============================================================
# GER
#
# CORE
#
# signature_api.py
#
# Official public API for Geometric Signatures.
#
# This module isolates the scientific code from the internal
# implementation of the CORE.
#
# Version
# -------
# 3.0
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable
from .reference_provider import ReferenceProvider


# ============================================================
# Signature
# ============================================================


@dataclass(frozen=True)
class Signature:
    """
    Fundamental Geometric Signature of the RSG framework.
    """

    diameter: float
    convergence: float
    recurrence: float
    drift: float

    # --------------------------------------------------------

    def to_dict(self):
        return asdict(self)

    # --------------------------------------------------------

    def to_tuple(self):
        return (
            self.diameter,
            self.convergence,
            self.recurrence,
            self.drift,
        )

    # --------------------------------------------------------

    def dimension(self):
        return 4

    # --------------------------------------------------------

    def __iter__(self):
        return iter(asdict(self).items())


# ============================================================
# Signature Provider Registry
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


def _require_signature_provider():

    provider = get_signature_provider()

    if provider is None:
        raise RuntimeError(
            "No SignatureProvider registered."
        )

    return provider


# ============================================================
# Reference Provider Registry
# ============================================================

_reference_provider = None


def register_reference_provider(provider):
    """
    Registers the official Reference Provider.
    """
    global _reference_provider
    _reference_provider = provider


def get_reference_provider():
    return _reference_provider


def _require_reference_provider():

    provider = get_reference_provider()

    if provider is None:
        raise RuntimeError(
            "No ReferenceProvider registered."
        )

    return provider


# ============================================================
# Signature Generation API
# ============================================================


def generate_signature(
    *args,
    **kwargs,
):
    """
    Generates one Geometric Signature.
    """

    provider = _require_signature_provider()

    return provider.generate_signature(
        *args,
        **kwargs,
    )


def generate_signature_dataset(
    *args,
    **kwargs,
):
    """
    Generates multiple Geometric Signatures.
    """

    provider = _require_signature_provider()

    return provider.generate_signature_dataset(
        *args,
        **kwargs,
    )


# ============================================================
# Reference API
# ============================================================


def load_signatures(
    *args,
    **kwargs,
):
    """
    Loads a SignatureCollection from the official
    Reference Provider.
    """

    provider = _require_reference_provider()

    return provider.load_signatures(
        *args,
        **kwargs,
    )


def available_signatures():
    """
    Returns the number of available signatures.
    """

    provider = _require_reference_provider()

    return provider.available_signatures()


def signature_names():
    """
    Returns the available signature names.
    """

    provider = _require_reference_provider()

    return provider.signature_names()


def signature_dimension():
    """
    Returns the intrinsic signature dimension.
    """

    provider = _require_reference_provider()

    return provider.signature_dimension()


# ============================================================
# Provider Protocols
# ============================================================


class SignatureProvider:
    """
    Official provider capable of producing
    Geometric Signatures from observational data.
    """

    def generate_signature(
        self,
        *args,
        **kwargs,
    ):
        raise NotImplementedError

    def generate_signature_dataset(
        self,
        *args,
        **kwargs,
    ):
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

    # --------------------------------------------------------
    # Signature Provider
    # --------------------------------------------------------

    signature_provider = get_signature_provider()

    print("Signature Provider")
    print("-" * 60)

    if signature_provider is None:

        print("Status : Not registered")

    else:

        print(
            f"Status : {type(signature_provider).__name__}"
        )

    print()

    # --------------------------------------------------------
    # Reference Provider
    # --------------------------------------------------------

    reference_provider = get_reference_provider()

    print("Reference Provider")
    print("-" * 60)

    if reference_provider is None:

        print("Status : Not registered")

    else:

        print(
            f"Status : {type(reference_provider).__name__}"
        )

        try:

            print(
                "Available Signatures :",
                reference_provider.available_signatures(),
            )

        except Exception:
            pass

        try:

            print(
                "Signature Dimension :",
                reference_provider.signature_dimension(),
            )

        except Exception:
            pass

        try:

            names = reference_provider.signature_names()

            print(
                "Signature Names :",
                ", ".join(names),
            )

        except Exception:
            pass

    print()
    print("=" * 60)
    print("API READY")
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
