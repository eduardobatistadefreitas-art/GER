"""
=========================================================
GER
S29

External Modal Embedding

Primeira implementação experimental do acoplamento
entre sistemas externos e o CORE do GER.

Versão experimental S29-E1.
=========================================================
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "build_external_gamma",
]

EXTERNAL_MODAL_EMBEDDING_VERSION = "1.1"


# =========================================================
# Internal utilities
# =========================================================

def _normalize(signal):

    signal = np.asarray(signal, dtype=float)

    signal = signal - np.mean(signal)

    sigma = np.std(signal)

    if sigma > 0.0:
        signal = signal / sigma

    return signal


# =========================================================
# Public API
# =========================================================

def build_external_gamma(
    signal,
    *,
    method="auto",
    normalize=True,
):
    """
    Constrói uma sequência modal γ compatível
    com o CORE.

    Nesta primeira implementação cada amostra
    temporal é representada por um vetor modal
    unidimensional.

    Returns
    -------
    gamma_sequence
        Lista de vetores γ(t).

    eigenvectors
        Base modal correspondente.
    """

    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1:
        raise ValueError(
            "External signal must be one-dimensional."
        )

    if normalize:
        signal = _normalize(signal)

    gamma_sequence = [
        np.asarray([value], dtype=float)
        for value in signal
    ]

    eigenvectors = np.eye(1)

    return gamma_sequence, eigenvectors
