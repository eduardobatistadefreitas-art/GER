# ============================================================
# GER
#
# S27-E4.1
#
# New Observable Search
#
# Procura novos operadores observacionais capazes
# de induzir partições diferentes das conhecidas.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan

from GER.CORE.partition_builder import build_partition
from GER.CORE.partition_algebra import meet


# ============================================================

def same_partition(P, Q):

    return set(P.blocks) == set(Q.blocks)


def relation(PA, PB):

    M = meet(PA, PB)

    if same_partition(M, PA) and same_partition(M, PB):
        return "="

    if same_partition(M, PA):
        return "<="

    if same_partition(M, PB):
        return ">="

    return "?"


# ============================================================

def safe_div(a, b):

    if abs(b) < 1e-12:
        return float("inf")

    return a / b


# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.1")
    print("New Observable Search")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    signatures = [

        row["signature"]

        for row in results

    ]

    operators = {

        "D":
            lambda s: s.diameter,

        "C":
            lambda s: s.convergence,

        "R":
            lambda s: s.recurrence,

        "Drift":
            lambda s: s.drift,

        "D/C":
            lambda s: safe_div(
                s.diameter,
                s.convergence,
            ),

        "D*R":
            lambda s:
                s.diameter * s.recurrence,

        "C*R":
            lambda s:
                s.convergence * s.recurrence,

        "D*Drift/C":
            lambda s:
                safe_div(
                    s.diameter * s.drift,
                    s.convergence,
                ),

        "C/(1+R)":
            lambda s:
                safe_div(
                    s.convergence,
                    1 + s.recurrence,
                ),

    }

    partitions = {}

    for name, op in operators.items():

        partitions[name] = build_partition(

            signatures,

            key=op,

        )

    print(
        f"{'Operator':<15}"
        f"{'Blocks':>8}"
    )

    print("-" * 25)

    for name, P in partitions.items():

        print(

            f"{name:<15}"

            f"{len(P.blocks):>8}"

        )

    print()

    print("=" * 60)
    print("Relations")
    print("=" * 60)

    names = list(partitions.keys())

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            A = names[i]
            B = names[j]

            rel = relation(

                partitions[A],

                partitions[B],

            )

            print(

                f"{A:<15}"

                f"{rel:^6}"

                f"{B}"

            )


if __name__ == "__main__":
    main()
