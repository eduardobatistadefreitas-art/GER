# ============================================================
# GER
#
# S27-E1.2
#
# Recurrence Degeneracy Analysis
#
# Analisa as classes de equivalência induzidas
# pelo operador Recurrence.
# ============================================================

from collections import defaultdict

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E1.2")
    print("Recurrence Degeneracy Analysis")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    signatures = [

        row["signature"]

        for row in results

    ]

    groups = defaultdict(list)

    for signature in signatures:

        groups[signature.recurrence].append(signature)

    print(f"Total signatures : {len(signatures)}")
    print(f"Recurrence classes : {len(groups)}")
    print()

    for recurrence in sorted(groups):

        block = groups[recurrence]

        diameters = [s.diameter for s in block]
        convergences = [s.convergence for s in block]
        drifts = [s.drift for s in block]

        print("-" * 60)
        print(f"Recurrence : {recurrence}")
        print(f"Block size : {len(block)}")
        print()

        print(
            f"Diameter     : "
            f"{min(diameters):.6f}"
            f" -> "
            f"{max(diameters):.6f}"
        )

        print(
            f"Convergence : "
            f"{min(convergences):.6f}"
            f" -> "
            f"{max(convergences):.6f}"
        )

        print(
            f"Drift       : "
            f"{min(drifts):.6f}"
            f" -> "
            f"{max(drifts):.6f}"
        )

        print()

    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
