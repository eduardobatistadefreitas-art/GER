# ============================================================
# GER
#
# S27-RA29
#
# Family Interface Audit
#
# Audits the implementation of the
# Observational Families.
# ============================================================

import inspect

import GER_CORE.S27_E5_2_lattice_generating_basis as family

print("=" * 60)
print("GER")
print("S27-RA29")
print("Family Interface Audit")
print("=" * 60)
print()

print(dir(family))
print()

for name in dir(family):

    obj = getattr(family, name)

    if inspect.isfunction(obj):

        print("=" * 60)
        print(name)
        print("=" * 60)

        try:
            print(inspect.signature(obj))
        except:
            pass

        print()

        try:
            print(inspect.getsource(obj))
        except Exception:
            pass

        print()
