# ============================================================
# GER
#
# S27-E3.2
#
# Partition Numerical Stability
#
# Testa a estabilidade estrutural das partições
# sob regimes numericamente instáveis.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan

from GER.CORE.partition_builder import build_partition
from GER.CORE.partition_algebra import meet


# ============================================================
# Utilities
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
# Test configurations
# ============================================================

CONFIGURATIONS = [

    ("Stable", 0.00025),

    ("Moderate", 0.00050),

    ("Aggressive", 0.00100),

    ("Extreme", 0.00200),

]


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E3.2")
    print("Partition Numerical Stability")
    print("=" * 60)
    print()

    reference = None

    invariant = True

    for label, dt in CONFIGURATIONS:

        print(f"Configuration : {label}")
        print(f"dt            : {dt}")

        results = run_geometry_scan(
            dt=dt,
        )

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

        current = (

            relation(PD, PC),

            relation(PD, PR),

            relation(PD, PDr),

            relation(PC, PR),

            relation(PC, PDr),

            relation(PR, PDr),

        )

        print(current)
        print()

        if reference is None:

            reference = current

        elif current != reference:

            invariant = False

    print("=" * 60)

    print(
        "Partition lattice invariant :",
        "YES" if invariant else "NO"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
