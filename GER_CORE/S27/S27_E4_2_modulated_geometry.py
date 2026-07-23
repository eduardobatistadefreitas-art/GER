# ============================================================
# GER
#
# S27-E4.2
#
# Modulated Geometry
#
# Analisa quais assinaturas foram fundidas pela
# partição induzida por D*R.
# ============================================================

from collections import defaultdict

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan


# ============================================================

def key(signature):

    return round(
        signature.diameter * signature.recurrence,
        12,
    )


# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.2")
    print("Modulated Geometry")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    groups = defaultdict(list)

    for row in results:

        groups[
            key(row["signature"])
        ].append(row)

    merged = [

        block

        for block in groups.values()

        if len(block) > 1

    ]

    print("Merged classes :", len(merged))
    print()

    for i, block in enumerate(merged, start=1):

        print("-" * 60)

        print(f"Class {i}")
        print(f"Members : {len(block)}")

        print()

        for row in block:

            s = row["signature"]

            print(

                f"id={row['simulation_id']:02d}"

                f"  beta={row['beta']:>6}"

                f"  sigma={row['sigma']:>6}"

                f"  potential={row['potential']:>8}"

            )

            print(

                f"   D={s.diameter:.6f}"

                f"   C={s.convergence:.6f}"

                f"   R={s.recurrence:.6f}"

                f"   Drift={s.drift:.6f}"

            )

        print()

    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
