# ============================================================
# GER
#
# S27-E2.3
#
# Lattice Consistency Audit
#
# Auditoria da estrutura algébrica das partições.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan

from GER.CORE.partition_builder import build_partition
from GER.CORE.partition_algebra import meet


# ============================================================
# Utilities
# ============================================================

def same_partition(P, Q):

    return set(P.blocks) == set(Q.blocks)


def refines(P, Q):
    """
    P refina Q
    <=> meet(P,Q)=P
    """
    return same_partition(meet(P, Q), P)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E2.3")
    print("Lattice Consistency Audit")
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

    print("Reflexivity")
    print("-" * 40)

    ok = True

    for name in names:

        value = refines(
            partitions[name],
            partitions[name],
        )

        print(f"{name:<10} {'PASS' if value else 'FAIL'}")

        ok &= value

    print()

    print("Antisymmetry")
    print("-" * 40)

    for i, A in enumerate(names):

        for B in names[i+1:]:

            PA = partitions[A]
            PB = partitions[B]

            cond = (
                refines(PA, PB)
                and
                refines(PB, PA)
            )

            if cond:

                equal = same_partition(PA, PB)

                print(

                    f"{A} <-> {B} : "

                    f"{'PASS' if equal else 'FAIL'}"

                )

    print()

    print("Meet Consistency")
    print("-" * 40)

    for A in names:

        for B in names:

            PA = partitions[A]
            PB = partitions[B]

            lhs = refines(PA, PB)

            rhs = same_partition(
                meet(PA, PB),
                PA,
            )

            print(

                f"{A:6s} <= {B:6s}"

                f"{'PASS' if lhs == rhs else 'FAIL'}"

            )

            ok &= (lhs == rhs)

    print()

    print("=" * 60)

    print(
        "LATTICE AUDIT :",
        "PASS" if ok else "FAIL"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
