# ============================================================
# GER
#
# S27-RA23
#
# Partition Interface Audit
# ============================================================

import inspect

import GER_CORE.S27_E2_1_partition_lattice as lattice

print("=" * 60)
print("GER")
print("S27-RA23")
print("Partition Interface")
print("=" * 60)
print()

print(dir(lattice))
print()

for name in dir(lattice):

    obj = getattr(lattice, name)

    if inspect.isfunction(obj):

        print("=" * 60)
        print(name)
        print("=" * 60)

        try:
            print(inspect.signature(obj))
        except:
            pass

        print()
