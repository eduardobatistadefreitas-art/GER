# ============================================================
# GER
#
# S27-RA18
#
# Geometry Scan Audit
#
# Interface inspection.
# ============================================================

import inspect

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)

print("=" * 60)
print("GER")
print("S27-RA18")
print("Geometry Scan Audit")
print("=" * 60)
print()

print("Signature")
print("----------------------------------------")
print(inspect.signature(run_geometry_scan))
print()

print("Source")
print("----------------------------------------")
print(inspect.getsource(run_geometry_scan))
