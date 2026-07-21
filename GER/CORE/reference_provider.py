# ============================================================
# GER
#
# CORE
#
# reference_provider.py
#
# Official interface for Reference Universe providers.
#
# Reference Providers expose collections of Geometric
# Signatures already stored by the framework.
#
# Version
# -------
# 1.0
# ============================================================

from __future__ import annotations

from typing import Any


# ============================================================
# Reference Provider
# ============================================================


class ReferenceProvider:
    """
    Official interface for Reference Universe providers.

    A Reference Provider is responsible for exposing one
    or more collections of Geometric Signatures already
    available to the framework.

    Unlike SignatureProvider, it never computes signatures.
    It only retrieves and describes existing Reference
    Universes.
    """

    # --------------------------------------------------------
    # Loading
    # --------------------------------------------------------

    def load_signatures(
        self,
        *args,
        **kwargs,
    ):
        """
        Loads a SignatureCollection.

        Returns
        -------
        SignatureCollection
        """
        raise NotImplementedError

    # --------------------------------------------------------
    # Information
    # --------------------------------------------------------

    def available_signatures(self):
        """
        Returns the number of available signatures.
        """
        raise NotImplementedError

    def signature_names(self):
        """
        Returns the identifiers of all available signatures.
        """
        raise NotImplementedError

    def signature_dimension(self):
        """
        Returns the intrinsic dimension of the signatures.
        """
        raise NotImplementedError

    # --------------------------------------------------------
    # Reference Universe
    # --------------------------------------------------------

    def reference_name(self):
        """
        Returns the human-readable name of the current
        Reference Universe.
        """
        raise NotImplementedError

    def metadata(self) -> dict[str, Any]:
        """
        Returns optional metadata describing the current
        Reference Universe.

        Examples
        --------
        version
        creation date
        source
        description
        """

        return {}

    # --------------------------------------------------------
    # Convenience
    # --------------------------------------------------------

    def summary(self):

        return {
            "reference": self.reference_name(),
            "signatures": self.available_signatures(),
            "dimension": self.signature_dimension(),
            "metadata": self.metadata(),
        }
      # ============================================================
# Demonstration
# ============================================================


def main():

    print("=" * 60)
    print("GER CORE")
    print("REFERENCE PROVIDER")
    print("=" * 60)
    print()

    provider = ReferenceProvider()

    print("Interface")
    print("-" * 60)

    print("load_signatures()")
    print("available_signatures()")
    print("signature_names()")
    print("signature_dimension()")
    print("reference_name()")
    print("metadata()")
    print("summary()")

    print()
    print("=" * 60)
    print("This module defines the official interface")
    print("for Reference Providers.")
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
