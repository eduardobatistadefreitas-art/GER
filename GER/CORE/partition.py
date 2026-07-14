"""
============================================================
GER

Partition

S27 Core

Representação matemática de uma partição de um conjunto.

Uma partição é composta por:

- Universo
- Blocos disjuntos
- União dos blocos = Universo

Esta classe NÃO constrói partições.
Ela apenas representa uma partição válida.

============================================================
"""


class Partition:
    """
    Representação imutável de uma partição.

    Parameters
    ----------
    universe : iterable
        Conjunto universo.

    blocks : iterable of iterables
        Blocos da partição.
    """

    def __init__(self, universe, blocks):

        self._universe = frozenset(universe)

        self._blocks = tuple(
            frozenset(block)
            for block in blocks
        )

        self._validate()

    # ---------------------------------------------------------
    # Validação
    # ---------------------------------------------------------

    def _validate(self):

        # nenhum bloco vazio
        for block in self._blocks:

            if len(block) == 0:
                raise ValueError(
                    "Partition contains an empty block."
                )

        # blocos disjuntos
        seen = set()

        for block in self._blocks:

            overlap = seen.intersection(block)

            if overlap:
                raise ValueError(
                    "Partition blocks are not disjoint."
                )

            seen.update(block)

        # cobertura total
        if seen != self._universe:

            raise ValueError(
                "Blocks do not cover the universe."
            )

    # ---------------------------------------------------------
    # Acesso
    # ---------------------------------------------------------

    @property
    def universe(self):

        return self._universe

    @property
    def blocks(self):

        return self._blocks

    # ---------------------------------------------------------
    # Informações básicas
    # ---------------------------------------------------------

    def number_of_blocks(self):

        return len(self._blocks)

    def cardinalities(self):

        return [
            len(block)
            for block in self._blocks
        ]

    def contains(self, element):

        return element in self._universe

    def block_of(self, element):

        for block in self._blocks:

            if element in block:
                return block

        raise KeyError(
            "Element not found in partition."
        )

    # ---------------------------------------------------------
    # Métodos especiais
    # ---------------------------------------------------------

    def __len__(self):

        return len(self._blocks)

    def __iter__(self):

        return iter(self._blocks)

    def __repr__(self):

        return (
            "Partition("
            f"universe={len(self._universe)}, "
            f"blocks={len(self._blocks)})"
    )
