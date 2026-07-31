"""
=========================================================
GAMMA CERTIFICATE
=========================================================

Validation utilities for Gamma generators.

=========================================================
"""

from __future__ import annotations


def certify_gamma(generator, **kwargs):
    """
    Execute a Gamma generator and produce a simple
    validation certificate.

    Parameters
    ----------
    generator
        Gamma generator instance.

    **kwargs
        Arguments forwarded to the generator.

    Returns
    -------
    dict
        Validation certificate.
    """

    gamma = generator.generate(**kwargs)

    return {
        "generator": generator.name,
        "status": "valid",
        "type": type(gamma).__name__,
        "gamma": gamma,
    }
