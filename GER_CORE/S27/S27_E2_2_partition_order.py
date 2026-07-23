# ============================================================
# GER
#
# S27-E2.2
#
# Partition Order
#
# Reconstrói automaticamente a ordem parcial
# entre as partições fundamentais.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan

from GER.CORE.partition_builder import build_partition
from GER.CORE.partition_algebra import meet


# ============================================================
# Utilitário
# ============================================================

def same_partition(P, Q):

    return set(P.blocks) == set(Q.blocks)


def refines(P, Q):
    """
    P refina Q  <=>  P ∧ Q = P
    """

    return same_partition(meet(P, Q), P)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E2.2")
    print("Partition Order")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    signatures = [
        row["signature"]
        for row in results
    ]

    partitions = {

        "D": build_partition(
            signatures,
            key=lambda s: s.diameter,
        ),

        "C": build_partition(
            signatures,
            key=lambda s: s.convergence,
        ),

        "R": build_partition(
            signatures,
            key=lambda s: s.recurrence,
        ),

        "Drift": build_partition(
            signatures,
            key=lambda s: s.drift,
        ),

    }

    names = list(partitions.keys())

    print("Refinement relations")
    print("-" * 60)

    for A in names:

        for B in names:

            if A == B:
                continue

            PA = partitions[A]
            PB = partitions[B]

            if same_partition(PA, PB):

                print(f"{A:6s} = {B}")

            elif refines(PA, PB):

                print(f"{A:6s} ⪯ {B}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
