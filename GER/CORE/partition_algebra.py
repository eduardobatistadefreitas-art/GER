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

from .partition import Partition


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
