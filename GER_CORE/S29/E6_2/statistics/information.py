"""
============================================================
GER
Information Theory Utilities
============================================================

Reusable information-theoretic functions for the
Relational Signature Geometry framework.

The module is intentionally independent of observatories.

Functions
---------
compression_ratio()
compression_gain()
compression_efficiency()
ideal_storage_bits()
uniform_storage_bits()
"""

from __future__ import annotations 

import numpy as np


# ============================================================
# COMPRESSION RATIO
# ============================================================

def compression_ratio(
    total_occurrences: int,
    unique_signatures: int,
) -> float:
    """
    Fraction of unique signatures with respect to the
    total number of observations.
    """

    if total_occurrences <= 0:
        return 0.0

    return float(
        unique_signatures / total_occurrences
    )


# ============================================================
# COMPRESSION GAIN
# ============================================================

def compression_gain(
    total_occurrences: int,
    unique_signatures: int,
) -> float:
    """
    Theoretical storage reduction obtained by storing
    only unique signatures.
    """

    return float(
        1.0
        - compression_ratio(
            total_occurrences,
            unique_signatures,
        )
    )


# ============================================================
# COMPRESSION EFFICIENCY
# ============================================================

def compression_efficiency(
    entropy: float,
    richness: int,
    entropy_base: str = "e",
) -> float:
    """
    Relative entropy with respect to the maximum
    possible entropy.

    Returns
    -------
    Value in [0,1].
    """

    if richness <= 1:
        return 0.0

    if entropy_base == "e":

        maximum_entropy = np.log(richness)

    elif entropy_base in ("bits", "2"):

        maximum_entropy = np.log2(richness)

    elif entropy_base == "10":

        maximum_entropy = np.log10(richness)

    else:

        raise ValueError(
            f"Unsupported entropy base: {entropy_base}"
        )

    if maximum_entropy == 0:

        return 0.0

    efficiency = (
        entropy
        / maximum_entropy
    )

    return float(

        np.clip(

            efficiency,

            0.0,

            1.0,

        )

    )


# ============================================================
# IDEAL STORAGE
# ============================================================

def ideal_storage_bits(
    entropy_bits: float,
    total_occurrences: int,
) -> float:
    """
    Shannon lower bound for optimal coding.

    Parameters
    ----------
    entropy_bits
        Shannon entropy in bits.

    total_occurrences
        Number of observations.
    """

    return float(
        entropy_bits
        * total_occurrences
    )


# ============================================================
# UNIFORM STORAGE
# ============================================================

def uniform_storage_bits(
    richness: int,
    total_occurrences: int,
) -> float:
    """
    Storage requirement assuming all signatures are
    equiprobable.
    """

    if richness <= 1:

        return 0.0

    return float(
        np.log2(richness)
        * total_occurrences
    )


# ============================================================
# STORAGE SAVING
# ============================================================

def storage_saving(
    entropy_bits: float,
    richness: int,
) -> float:
    """
    Relative saving of an optimal Shannon code with
    respect to a fixed-length code.

    Returns
    -------
    Value in [0,1].
    """

    if richness <= 1:

        return 0.0

    fixed_bits = np.log2(richness)

    if fixed_bits == 0:

        return 0.0

    return float(
        1.0
        - entropy_bits / fixed_bits
    )

# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "compression_ratio",
    "compression_gain",
    "compression_efficiency",
    "ideal_storage_bits",
    "uniform_storage_bits",
    "storage_saving",
]
