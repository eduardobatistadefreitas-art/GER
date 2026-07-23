# ============================================================
# GER
#
# S27-E1.1
#
# Operator Partition Scan
#
# Primeiro experimento oficial da S27.
#
# Mede as partições induzidas por cada operador
# geométrico utilizando assinaturas produzidas
# pelo motor da S26.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)

from GER.CORE.partition_builder import (
    build_partition,
)

from GER.CORE.partition_metrics import (
    summary,
)


# ============================================================
# Scan
# ============================================================

OPERATORS = [

    "diameter",

    "convergence",

    "recurrence",

    "drift",

]


def main():

    print("=" * 60)
    print("GER")
    print("S27-E1.1")
    print("Operator Partition Scan")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    signatures = [

        row["signature"]

        for row in results

    ]

    print(f"Signatures : {len(signatures)}")
    print()

    print(
        f"{'Operator':<15}"
        f"{'Blocks':>10}"
        f"{'Largest':>10}"
        f"{'Smallest':>12}"
    )

    print("-" * 50)

    for operator in OPERATORS:

        partition = build_partition(

            universe=signatures,

            key=lambda s, op=operator:
                getattr(s, op),

        )

        report = summary(partition)

        print(

            f"{operator:<15}"

            f"{report['blocks']:>10}"

            f"{report['largest']:>10}"

            f"{report['smallest']:>12}"

        )

    print()
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
