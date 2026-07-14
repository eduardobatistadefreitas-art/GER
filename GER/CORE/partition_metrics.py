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
