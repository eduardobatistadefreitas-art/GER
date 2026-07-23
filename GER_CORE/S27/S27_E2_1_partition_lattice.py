# ============================================================
# GER
#
# S27-E2.1
#
# Partition Lattice
#
# Estudo das relações algébricas entre
# as partições fundamentais.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)

from GER.CORE.partition_builder import (
    build_partition,
)

from GER.CORE.partition_algebra import (
    meet,
)


# ============================================================
# Equality
# ============================================================

def same_partition(P, Q):

    return set(P.blocks) == set(Q.blocks)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E2.1")
    print("Partition Lattice")
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

    tests = [

        ("D ∧ C", PD, PC),

        ("D ∧ R", PD, PR),

        ("D ∧ Drift", PD, PDr),

        ("C ∧ R", PC, PR),

        ("C ∧ Drift", PC, PDr),

        ("R ∧ Drift", PR, PDr),

    ]

    print(
        f"{'Meet':<18}"
        f"{'Left':>10}"
        f"{'Right':>10}"
    )

    print("-" * 40)

    for name, A, B in tests:

        M = meet(A, B)

        print(

            f"{name:<18}"

            f"{'YES' if same_partition(M, A) else 'NO':>10}"

            f"{'YES' if same_partition(M, B) else 'NO':>10}"

        )

    print()
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
