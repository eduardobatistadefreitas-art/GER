# ============================================================
# GER
#
# S27-RA18
#
# Geometry Scan Audit
# ============================================================

import inspect

import GER_CORE.S26_B36_geometry_scan as gs

print("=" * 60)
print("GER")
print("S27-RA18")
print("Geometry Scan Audit")
print("=" * 60)
print()

print(dir(gs))
print()

for name in dir(gs):

    obj = getattr(gs, name)

    if inspect.isfunction(obj):

        print("=" * 60)
        print(name)
        print("=" * 60)
        print(inspect.signature(obj))
        print()
