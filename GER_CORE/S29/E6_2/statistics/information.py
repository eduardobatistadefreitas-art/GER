"""
============================================================
GER
Information Theory Utilities
============================================================

Reusable information-theoretic functions for the
Relational Signature Geometry framework.

This module is intentionally independent from
specific observatories.

Existing public functions remain fully compatible.

Functions
---------
compression_ratio(...)
compression_gain(...)
compression_efficiency(...)
ideal_storage_bits(...)
uniform_storage_bits(...)
storage_saving(...)

Additional utilities
--------------------
clean_distribution(...)
probability_distribution(...)
normalize_distribution(...)
shannon_entropy(...)
normalized_entropy(...)
effective_number_of_states(...)
============================================================
"""

from __future__ import annotations

import numpy as np


# ============================================================
# Version
# ============================================================

INFORMATION_VERSION = "2.0"


# ============================================================
# Constants
# ============================================================

EPSILON = 1e-12


# ============================================================
# Public API
# ============================================================

__all__ = [

    "compression_ratio",

    "compression_gain",

    "compression_efficiency",

    "ideal_storage_bits",

    "uniform_storage_bits",

    "storage_saving",

    "clean_distribution",

    "normalize_distribution",

    "probability_distribution",

    "shannon_entropy",

    "normalized_entropy",

    "effective_number_of_states",

]


# ============================================================
# Utilities
# ============================================================

def clean_distribution(values):
    """
    Convert an iterable into a valid probability vector.
    """

    values = np.asarray(
        values,
        dtype=float,
    )

    values = values[
        np.isfinite(values)
    ]

    values = values[
        values >= 0
    ]

    return values


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_distribution(values):
    """
    Normalize a non-negative vector into a probability
    distribution.
    """

    values = clean_distribution(values)

    total = values.sum()

    if total <= 0:

        return np.array([], dtype=float)

    return values / total


# ============================================================
# PROBABILITY DISTRIBUTION
# ============================================================

def probability_distribution(values):
    """
    Estimate the empirical probability distribution.
    """

    values = np.asarray(values)

    _, counts = np.unique(
        values,
        return_counts=True,
    )

    return normalize_distribution(counts)


# ============================================================
# SHANNON ENTROPY
# ============================================================

def shannon_entropy(

    probabilities,

    base="e",

):
    """
    Shannon entropy.
    """

    p = normalize_distribution(
        probabilities
    )

    if len(p) == 0:

        return 0.0

    p = p[
        p > 0
    ]

    if base == "e":

        log = np.log

    elif base in ("2", "bits"):

        log = np.log2

    elif base == "10":

        log = np.log10

    else:

        raise ValueError(
            f"Unsupported entropy base: {base}"
        )

    return float(

        -np.sum(

            p * log(p)

        )

    )


# ============================================================
# NORMALIZED ENTROPY
# ============================================================

def normalized_entropy(

    probabilities,

    base="e",

):
    """
    Entropy normalized by its theoretical maximum.
    """

    p = normalize_distribution(
        probabilities
    )

    richness = len(p)

    if richness <= 1:

        return 0.0

    entropy = shannon_entropy(

        p,

        base,

    )

    if base == "e":

        maximum = np.log(richness)

    elif base in ("2", "bits"):

        maximum = np.log2(richness)

    else:

        maximum = np.log10(richness)

    if maximum <= 0:

        return 0.0

    return float(

        np.clip(

            entropy / maximum,

            0.0,

            1.0,

        )

    )


# ============================================================
# EFFECTIVE NUMBER OF STATES
# ============================================================

def effective_number_of_states(

    probabilities,

):
    """
    Hill number of order one.

    Effective number of equally probable states.
    """

    entropy = shannon_entropy(

        probabilities,

        base="e",

    )

    return float(

        np.exp(entropy)

    )


# ============================================================
# COMPRESSION RATIO
# ============================================================

def compression_ratio(

    total_occurrences,

    unique_signatures,

):
    """
    Fraction of unique signatures with respect to
    the total number of observations.
    """

    if total_occurrences <= 0:

        return 0.0

    return float(

        unique_signatures

        / total_occurrences

    )


# ============================================================
# COMPRESSION GAIN
# ============================================================

def compression_gain(

    total_occurrences,

    unique_signatures,

):
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

    entropy,

    richness,

    entropy_base="e",

):
    """
    Relative entropy with respect to the maximum
    theoretical entropy.
    """

    if richness <= 1:

        return 0.0

    if entropy_base == "e":

        maximum = np.log(richness)

    elif entropy_base in ("bits", "2"):

        maximum = np.log2(richness)

    elif entropy_base == "10":

        maximum = np.log10(richness)

    else:

        raise ValueError(

            f"Unsupported entropy base: {entropy_base}"

        )

    if maximum == 0:

        return 0.0

    return float(

        np.clip(

            entropy / maximum,

            0.0,

            1.0,

        )

    )

# ============================================================
# IDEAL STORAGE
# ============================================================

def ideal_storage_bits(

    entropy_bits,

    total_occurrences,

):
    """
    Shannon lower bound for optimal coding.
    """

    return float(

        entropy_bits

        * total_occurrences

    )


# ============================================================
# UNIFORM STORAGE
# ============================================================

def uniform_storage_bits(

    richness,

    total_occurrences,

):
    """
    Fixed-length coding requirement.
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

    entropy_bits,

    richness,

):
    """
    Relative storage saving with respect to
    a fixed-length code.
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
# CROSS ENTROPY
# ============================================================

def cross_entropy(

    p,

    q,

    base="e",

):
    """
    Cross entropy H(P,Q).
    """

    p = normalize_distribution(p)

    q = normalize_distribution(q)

    if len(p) != len(q):

        raise ValueError(

            "Distributions must have identical size."

        )

    q = np.clip(

        q,

        EPSILON,

        None,

    )

    if base == "e":

        log = np.log

    elif base in ("2", "bits"):

        log = np.log2

    elif base == "10":

        log = np.log10

    else:

        raise ValueError(

            f"Unsupported base: {base}"

        )

    return float(

        -np.sum(

            p * log(q)

        )

    )


# ============================================================
# KL DIVERGENCE
# ============================================================

def kl_divergence(

    p,

    q,

    base="e",

):
    """
    Kullback-Leibler divergence.
    """

    p = normalize_distribution(p)

    q = normalize_distribution(q)

    if len(p) != len(q):

        raise ValueError(

            "Distributions must have identical size."

        )

    p = np.clip(

        p,

        EPSILON,

        None,

    )

    q = np.clip(

        q,

        EPSILON,

        None,

    )

    if base == "e":

        log = np.log

    elif base in ("2", "bits"):

        log = np.log2

    elif base == "10":

        log = np.log10

    else:

        raise ValueError(

            f"Unsupported base: {base}"

        )

    return float(

        np.sum(

            p * log(

                p / q

            )

        )

    )


# ============================================================
# JENSEN-SHANNON DIVERGENCE
# ============================================================

def jensen_shannon_divergence(

    p,

    q,

    base="e",

):
    """
    Jensen-Shannon divergence.
    """

    p = normalize_distribution(p)

    q = normalize_distribution(q)

    m = 0.5 * (p + q)

    return float(

        0.5 *

        (

            kl_divergence(

                p,

                m,

                base,

            )

            +

            kl_divergence(

                q,

                m,

                base,

            )

        )

    )


# ============================================================
# TOTAL VARIATION DISTANCE
# ============================================================

def total_variation_distance(

    p,

    q,

):
    """
    Total variation distance.
    """

    p = normalize_distribution(p)

    q = normalize_distribution(q)

    return float(

        0.5 *

        np.sum(

            np.abs(

                p - q

            )

        )

    )


# ============================================================
# INFORMATION GAIN
# ============================================================

def information_gain(

    prior_entropy,

    posterior_entropy,

):
    """
    Entropy reduction.
    """

    return float(

        prior_entropy

        - posterior_entropy

    )


# ============================================================
# REDUNDANCY
# ============================================================

def redundancy(

    entropy,

    richness,

    base="e",

):
    """
    Information redundancy.
    """

    return float(

        1.0

        - compression_efficiency(

            entropy,

            richness,

            base,

        )

    )


# ============================================================
# CODING EFFICIENCY
# ============================================================

def coding_efficiency(

    entropy_bits,

    richness,

):
    """
    Coding efficiency.
    """

    return compression_efficiency(

        entropy_bits,

        richness,

        entropy_base="bits",

    )


# ============================================================
# ENTROPY DEFICIT
# ============================================================

def entropy_deficit(

    entropy,

    richness,

    base="e",

):
    """
    Missing entropy relative to the theoretical maximum.
    """

    if richness <= 1:

        return 0.0

    if base == "e":

        maximum = np.log(richness)

    elif base in ("2", "bits"):

        maximum = np.log2(richness)

    else:

        maximum = np.log10(richness)

    return float(

        maximum - entropy

    )


# ============================================================
# SELF TEST
# ============================================================

def main():

    counts = np.array(

        [50, 30, 15, 5]

    )

    p = normalize_distribution(

        counts

    )

    q = normalize_distribution(

        [45, 35, 10, 10]

    )

    print("=" * 60)

    print("GER")

    print("Information Theory")

    print("=" * 60)

    print()

    print(

        "Entropy:",

        shannon_entropy(

            p,

            base="bits",

        ),

    )

    print(

        "Normalized:",

        normalized_entropy(

            p,

            base="bits",

        ),

    )

    print(

        "Effective states:",

        effective_number_of_states(

            p,

        ),

    )

    print(

        "KL:",

        kl_divergence(

            p,

            q,

            base="bits",

        ),

    )

    print(

        "JS:",

        jensen_shannon_divergence(

            p,

            q,

            base="bits",

        ),

    )

    print(

        "TVD:",

        total_variation_distance(

            p,

            q,

        ),

    )


if __name__ == "__main__":

    main()
