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
      """
============================================================
GER

Partition Builder

S27 Core

Constrói uma partição a partir de uma aplicação.

A teoria da S27 demonstra que toda aplicação

    f : X -> Y

induz naturalmente uma partição sobre X.

Este módulo implementa exatamente essa construção.

============================================================
"""

from collections import defaultdict

from GER.CORE.partition import Partition


# ------------------------------------------------------------
# Builder
# ------------------------------------------------------------

def build_partition(
    universe,
    key,
):
    """
    Constrói a partição induzida por uma aplicação.

    Parameters
    ----------
    universe : iterable

        Conjunto de elementos.

    key : callable

        Aplicação

            key(element)

        que retorna o valor observacional utilizado
        para definir as classes.

    Returns
    -------
    Partition
    """

    groups = defaultdict(list)

    for element in universe:

        value = key(element)

        groups[value].append(element)

    blocks = list(groups.values())

    return Partition(
        universe=universe,
        blocks=blocks,
    )
"""
============================================================
GER

Partition Algebra

S27 Core

Operações matemáticas entre partições.

Nesta primeira versão implementamos apenas:

    meet(P, Q)

A operação meet produz o refinamento comum entre duas
partições.

============================================================
"""

from collections import defaultdict

from GER.CORE.partition import Partition


# ------------------------------------------------------------
# Meet
# ------------------------------------------------------------

def meet(P, Q):
    """
    Retorna o meet (refinamento comum) entre duas partições.

    Parameters
    ----------
    P : Partition

    Q : Partition

    Returns
    -------
    Partition
    """

    if P.universe != Q.universe:

        raise ValueError(
            "Partitions must have the same universe."
        )

    groups = defaultdict(list)

    for element in P.universe:

        key = (

            P.block_of(element),

            Q.block_of(element),

        )

        groups[key].append(element)

    return Partition(

        universe=P.universe,

        blocks=groups.values(),

    )

"""
============================================================
GER

Partition Metrics

S27 Core

Métricas quantitativas sobre partições.

Nenhuma função modifica a partição.

Todas retornam apenas medidas.

============================================================
"""

from collections import Counter


# ------------------------------------------------------------
# Número de blocos
# ------------------------------------------------------------

def number_of_blocks(partition):

    return partition.number_of_blocks()


# ------------------------------------------------------------
# Cardinalidades
# ------------------------------------------------------------

def cardinalities(partition):

    return partition.cardinalities()


# ------------------------------------------------------------
# Maior bloco
# ------------------------------------------------------------

def largest_block(partition):

    return max(

        partition.cardinalities()

    )


# ------------------------------------------------------------
# Menor bloco
# ------------------------------------------------------------

def smallest_block(partition):

    return min(

        partition.cardinalities()

    )


# ------------------------------------------------------------
# Distribuição
# ------------------------------------------------------------

def cardinality_distribution(partition):

    return dict(

        Counter(

            partition.cardinalities()

        )

    )


# ------------------------------------------------------------
# Resumo
# ------------------------------------------------------------

def summary(partition):

    return {

        "blocks":
            number_of_blocks(partition),

        "largest":
            largest_block(partition),

        "smallest":
            smallest_block(partition),

        "distribution":
            cardinality_distribution(partition),

}
