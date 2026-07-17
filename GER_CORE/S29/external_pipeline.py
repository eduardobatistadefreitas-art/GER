"""
=========================================================
GER
S29

External Pipeline

Connects external systems to relational embeddings.
=========================================================
"""

from __future__ import annotations


class ExternalPipeline:
    """
    Executes an external system through a relational
    embedding, producing a temporal sequence gamma(t).
    """

    def __init__(
        self,
        system,
        embedding,
    ):
        self.system = system
        self.embedding = embedding

    def run(self):
        """
        Generates the complete gamma(t) sequence.
        """

        self.system.reset()
        self.embedding.reset()

        gamma_sequence = []

        while not self.system.finished():

            state = self.system.step()

            gamma = self.embedding.step(state)

            gamma_sequence.append(gamma)

        return gamma_sequence
