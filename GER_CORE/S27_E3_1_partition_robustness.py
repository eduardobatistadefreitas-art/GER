# ============================================================
# GER
#
# S27-E3.1
#
# Partition Robustness
#
# Testa se a estrutura das partições permanece
# invariante para diferentes datasets.
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
# Experiment
# ============================================================

TIMESTEPS = [

    500,

    1000,

    2000,

    4000,

]


def build_partitions(timesteps):

    results = run_geometry_scan(
        timesteps=timesteps,
    )

    signatures = [

        row["signature"]

        for row in results

    ]

    return {

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


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E3.1")
    print("Partition Robustness")
    print("=" * 60)
    print()

    reference = None

    invariant = True

    for timesteps in TIMESTEPS:

        partitions = build_partitions(
            timesteps
        )

        current = (

            relation(partitions["D"], partitions["C"]),

            relation(partitions["D"], partitions["R"]),

            relation(partitions["D"], partitions["Drift"]),

            relation(partitions["C"], partitions["R"]),

            relation(partitions["C"], partitions["Drift"]),

            relation(partitions["R"], partitions["Drift"]),

        )

        print(f"Timesteps : {timesteps}")
        print(current)
        print()

        if reference is None:

            reference = current

        elif current != reference:

            invariant = False

    print("=" * 60)

    print(
        "Partition lattice invariant :",
        "YES" if invariant else "NO",
    )

    print("=" * 60)


# ============================================================

if __name__ == "__main__":

    main()
