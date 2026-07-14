"""
============================================================
GER

S27-E1

Partition Observatory

Primeiro observatório experimental da Série S27.

Objetivo:

Validar computacionalmente a construção de partições
induzidas pelos Operadores Geométricos Fundamentais
utilizando exclusivamente o motor consolidado da S26.

============================================================
"""

from GER.CORE.partition_builder import build_partition

from GER.CORE.partition_metrics import summary

from GER.CORE.signature_api import (
    generate_signature,
)


# ============================================================
# Partition
# ============================================================

def build_signature_partition(
    trajectories,
    key,
):
    """
    Constrói uma partição utilizando um único operador
    observacional.

    Parameters
    ----------
    trajectories

        Coleção de trajetórias.

    key

        Nome do atributo da assinatura.

    Returns
    -------
    Partition
    """

    return build_partition(

        universe=trajectories,

        key=lambda trajectory:
            getattr(
                generate_signature(trajectory),
                key,
            ),

    )


# ============================================================
# Report
# ============================================================

def report_partition(
    partition,
):

    report = summary(partition)

    print("=" * 60)
    print("S27-E1")
    print("Partition Observatory")
    print("=" * 60)
    print()

    print("Blocks       :", report["blocks"])
    print("Largest      :", report["largest"])
    print("Smallest     :", report["smallest"])
    print()

    print("Distribution")

    for size, count in sorted(
        report["distribution"].items()
    ):

        print(

            f"{size:4d} -> {count:4d}"

        )

    print()

    print("=" * 60)
