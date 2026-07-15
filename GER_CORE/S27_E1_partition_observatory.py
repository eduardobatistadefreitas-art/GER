"""
============================================================
GER

S27-E1

Partition Observatory
Partition Observatory

Primeiro observatório experimental da Série S27.

Objetivo

Verificar se um Operador Geométrico Fundamental
induz corretamente uma partição computacional
sobre o conjunto de trajetórias produzidas
pelo motor do GER.

Nesta primeira versão apenas o operador D
é utilizado.

============================================================
"""

from GER.CORE.partition_builder import build_partition

from GER.CORE.partition_metrics import summary

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)

# ============================================================
# Provider Registration
# ============================================================

register_signature_provider(
    B35SignatureProvider()
)

# ============================================================
# Partition
# ============================================================

def build_observable_partition(
    key,
):
    """
    Constrói uma partição utilizando um único operador
    observacional do GER.
    """

    results = run_geometry_scan()

    signatures = [
        row["signature"]
        for row in results
    ]

    return build_partition(

        universe=signatures,

        key=lambda signature:
            getattr(
                signature,
                key,
            ),

    )


# ============================================================
# Report
# ============================================================

def report_partition(
    partition,
    operator,
):

    report = summary(partition)

    print("Operator :", operator)
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

# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    signatures = [

        {"diameter": 1.0, "volume": 5.0, "recurrence": 0.20},
        {"diameter": 1.0, "volume": 6.0, "recurrence": 0.30},
        {"diameter": 2.0, "volume": 4.0, "recurrence": 0.20},
        {"diameter": 2.0, "volume": 4.0, "recurrence": 0.40},
        {"diameter": 3.0, "volume": 2.0, "recurrence": 0.50},

    ]

    partition = build_observable_partition(
    "diameter",
)

    report_partition(
        partition,
        operator="D",
    )
