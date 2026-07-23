# ============================================================
# GER
#
# S27-E4.3
#
# Zero Recurrence Regime
#
# Investiga a estrutura dos estados com
# recorrência exatamente nula.
# ============================================================

from collections import defaultdict

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan


# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.3")
    print("Zero Recurrence Regime")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    zero = []

    for row in results:

        if row["signature"].recurrence == 0.0:

            zero.append(row)

    print("Total signatures :", len(results))
    print("Zero recurrence  :", len(zero))
    print()

    print("=" * 60)
    print("Distribution")
    print("=" * 60)

    by_beta = defaultdict(int)
    by_sigma = defaultdict(int)
    by_potential = defaultdict(int)

    for row in zero:

        by_beta[row["beta"]] += 1
        by_sigma[row["sigma"]] += 1
        by_potential[row["potential"]] += 1

    print()

    print("Beta")
    print("-" * 40)

    for beta in sorted(by_beta):

        print(
            f"{beta:>8} : {by_beta[beta]}"
        )

    print()

    print("Sigma")
    print("-" * 40)

    for sigma in sorted(by_sigma):

        print(
            f"{sigma:>8} : {by_sigma[sigma]}"
        )

    print()

    print("Potential")
    print("-" * 40)

    for pot in sorted(by_potential):

        print(
            f"{pot:>8} : {by_potential[pot]}"
        )

    print()

    print("=" * 60)
    print("Members")
    print("=" * 60)

    for row in zero:

        s = row["signature"]

        print(

            f"id={row['simulation_id']:02d}"

            f"  beta={row['beta']:>5}"

            f"  sigma={row['sigma']:>5}"

            f"  potential={row['potential']}"

        )

        print(

            f"   D={s.diameter:.6f}"

            f"   C={s.convergence:.6f}"

            f"   Drift={s.drift:.6f}"

        )

        print()

    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
