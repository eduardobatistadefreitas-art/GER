"""
=========================================================
GER
S29

Identity Embedding

Reference embedding used to validate the external
embedding architecture.

gamma = state
=========================================================
"""

from __future__ import annotations

import numpy as np

from GER_CORE.S29.external_embedding_protocol import (
    ExternalEmbedding,
)


class IdentityEmbedding(ExternalEmbedding):
    """
    Identity embedding.

    Performs no transformation.

    The external state itself becomes the relational
    state accepted by the RSG CORE.
    """

    def reset(self):
        """
        Nothing to reset.
        """
        pass

    def step(self, state):
        """
        Identity transformation.
        """

        return np.asarray(state, dtype=float)

    def finished(self):
        """
        Stateless embedding.
        """
        return False
