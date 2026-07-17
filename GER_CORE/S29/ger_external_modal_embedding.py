"""
=========================================================
GER CORE (Experimental Interface)

Arquivo : ger_external_modal_embedding.py
=========================================================

External Modal Embedding

Este módulo define a interface de acoplamento entre
sistemas dinâmicos externos e o ecossistema GER.

Sua responsabilidade é converter uma representação
externa do sistema em uma sequência de estados γ
compatíveis com o CORE.

Nenhuma hipótese sobre o sistema físico é feita aqui.

=========================================================
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "build_external_gamma",
]

EXTERNAL_MODAL_EMBEDDING_VERSION = "1.0"


# =========================================================
# Public API
# =========================================================

def build_external_gamma(
    signal,
    *,
    method="fourier",
    normalize=True,
):
    """
    Constrói uma representação modal γ a partir
    de um sinal externo.

    Parameters
    ----------
    signal : array_like
        Série temporal do sistema externo.

    method : str
        Método de projeção modal.

    normalize : bool
        Se True, normaliza γ.

    Returns
    -------
    gamma : ndarray

    eigenvectors : ndarray

    Notes
    -----
    Esta função define apenas a interface pública.

    A implementação matemática da projeção modal
    será introduzida e validada durante os
    experimentos da Série S29.
    """

    raise NotImplementedError(
        "External modal embedding not implemented yet."
    )
