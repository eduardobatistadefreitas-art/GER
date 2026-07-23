# ============================================================
# GER
#
# S27-E1.3
#
# Partition Refinement
#
# Estuda o refinamento das partições induzidas
# pelos operadores fundamentais.
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

from GER.CORE.partition_algebra import (
    meet,
)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E1.3")
    print("Partition Refinement")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    signatures = [
        row["signature"]
        for row in results
    ]

    PD = build_partition(
        signatures,
        key=lambda s: s.diameter,
    )

    PC = build_partition(
        signatures,
        key=lambda s: s.convergence,
    )

    PR = build_partition(
        signatures,
        key=lambda s: s.recurrence,
    )

    PDr = build_partition(
        signatures,
        key=lambda s: s.drift,
    )

    partitions = [

        ("D", PD),

        ("D ∧ C",
            meet(PD, PC)
        ),

        ("D ∧ C ∧ R",
            meet(
                meet(PD, PC),
                PR,
            )
        ),

        ("D ∧ C ∧ R ∧ Drift",
            meet(
                meet(
                    meet(PD, PC),
                    PR,
                ),
                PDr,
            )
        ),

    ]

    print(
        f"{'Partition':<20}"
        f"{'Blocks':>10}"
        f"{'Largest':>10}"
        f"{'Smallest':>12}"
    )

    print("-" * 55)

    for name, partition in partitions:

        report = summary(partition)

        print(
            f"{name:<20}"
            f"{report['blocks']:>10}"
            f"{report['largest']:>10}"
            f"{report['smallest']:>12}"
        )

    print()
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
