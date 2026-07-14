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

from CORE.partition import Partition


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
