# ============================================================
# GER
#
# S27-E4.4
#
# Recurrence Algorithm Audit
#
# Auditoria do algoritmo utilizado para calcular
# a recorrência das assinaturas.
# ============================================================

import inspect

from GER_CORE.S26_B36_geometry_scan import (
    compute_recurrence,
)


def main():

    print("=" * 60)
    print("GER")
    print("S27-E4.4")
    print("Recurrence Algorithm Audit")
    print("=" * 60)
    print()

    print(inspect.getsource(compute_recurrence))

    print()

    print("=" * 60)


if __name__ == "__main__":

    main()
