# ============================================================
# GER
#
# S27-E3.3
#
# Geometry Scan Audit
#
# Auditoria do pipeline do Geometry Scan.
#
# Objetivo:
# Verificar se a aparente invariância estrutural
# é consequência da física ou de filtragem
# automática de simulações.
# ============================================================

from GER_CORE.S26_B36_geometry_scan import run_geometry_scan


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E3.3")
    print("Geometry Scan Audit")
    print("=" * 60)
    print()

    results = run_geometry_scan()

    print(f"Generated signatures : {len(results)}")
    print()

    missing = 0

    for i, row in enumerate(results):

        ok = "signature" in row

        if not ok:
            missing += 1

        print(
            f"{i:03d} | "
            f"{'OK' if ok else 'MISSING'}"
        )

    print()

    print("=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)

    print(f"Rows returned      : {len(results)}")
    print(f"Missing signatures : {missing}")
    print(f"Valid signatures   : {len(results)-missing}")

    print()

    if missing == 0:

        print("STATUS : PASS")

    else:

        print("STATUS : FAIL")

    print("=" * 60)


if __name__ == "__main__":
    main()
