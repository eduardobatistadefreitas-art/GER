# ============================================================
# GER
#
# S27-E3.4
#
# Parameter Expansion
#
# Expande o espaço de parâmetros do Geometry Scan
# para testar a robustez estrutural das partições.
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

EXPERIMENTS = [

    {
        "name": "Default",
        "betas": None,
        "sigmas": None,
        "potentials": None,
    },

    {
        "name": "Expanded Beta",
        "betas": [-2, -1, -0.5, 0, 0.5, 1, 2],
        "sigmas": None,
        "potentials": None,
    },

    {
        "name": "Expanded Sigma",
        "betas": None,
        "sigmas": [0.05, 0.10, 0.20, 0.50, 1.00],
        "potentials": None,
    },

]


# ============================================================

def build_relations(results):

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

    return (

        relation(PD, PC),

        relation(PD, PR),

        relation(PD, PDr),

        relation(PC, PR),

        relation(PC, PDr),

        relation(PR, PDr),

    )


# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E3.4")
    print("Parameter Expansion")
    print("=" * 60)
    print()

    reference = None

    invariant = True

    for exp in EXPERIMENTS:

        print(exp["name"])
        print("-" * 40)

        results = run_geometry_scan(

            betas=exp["betas"],

            sigmas=exp["sigmas"],

            potentials=exp["potentials"],

        )

        print("Signatures :", len(results))

        current = build_relations(results)

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


if __name__ == "__main__":

    main()
