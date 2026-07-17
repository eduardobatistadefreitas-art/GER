"""
=========================================================
GER CORE

default_signature_provider.py

=========================================================

Default Signature Provider

Official implementation of the SignatureProvider
interface.

This provider converts observational data into an
official Geometric Signature using the CORE
implementation.

It performs no validation, certification or auditing.

Its only responsibility is to produce a Signature.
"""

from __future__ import annotations

from GER.CORE.signature_api import (
    SignatureProvider,
)

from GER.CORE.ger_geometric_signature import (
    compute_geometric_signature,
)

__all__ = [
    "DefaultSignatureProvider",
]

DEFAULT_SIGNATURE_PROVIDER_VERSION = "1.0"


class DefaultSignatureProvider(SignatureProvider):
    """
    Default implementation of the official
    SignatureProvider.
    """

    def generate_signature(
        self,
        observables,
        dt,
        *args,
        **kwargs,
    ):
        """
        Generates one Geometric Signature.

        Parameters
        ----------
        observables
            Observational data produced by the
            Persistence Observatory.

        dt : float
            Sampling interval.

        Returns
        -------
        Signature
        """

        return compute_geometric_signature(
            observables,
            dt,
        )

    def generate_signature_dataset(
        self,
        dataset,
        dt,
        *args,
        **kwargs,
    ):
        """
        Generates a collection of Geometric
        Signatures.

        Parameters
        ----------
        dataset
            Iterable containing observational
            datasets.

        dt : float

        Returns
        -------
        list[Signature]
        """

        return [

            self.generate_signature(
                observables,
                dt,
            )

            for observables in dataset

        ]
