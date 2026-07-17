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
    method="auto",
    normalize=True,
):
    """
    Constrói uma representação modal γ a partir
    de um sinal externo.

    Parameters
    ----------
    signal : array_like
        Série temporal do sistema externo.

    method : str, default="auto"
        Método de projeção modal.

        O valor "auto" permite que o CORE utilize
        o método padrão validado experimentalmente,
        preservando a estabilidade da API caso esse
        método evolua durante a Série S29.

    normalize : bool, default=True
        Se True, normaliza γ.

    Returns
    -------
    gamma : ndarray
        Sequência de estados modais.

    eigenvectors : ndarray
        Base modal correspondente.

    Notes
    -----
    Esta função define apenas a interface pública.

    A implementação matemática da projeção modal
    será introduzida e validada durante os
    experimentos da Série S29.
    """

    raise NotImplementedError(
        "No external modal embedding has been validated yet. "
        "The implementation will be introduced during the "
        "S29 experimental series."
    )
