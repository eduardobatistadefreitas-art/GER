# ============================================================
# GER
#
# S27-RA24
#
# Reference Universe Interface
#
# Audit of the Geometry Scan output used as the
# reference universe for external validation.
# ============================================================

import inspect

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)

print("=" * 60)
print("GER")
print("S27-RA24")
print("Reference Universe Interface")
print("=" * 60)
print()

print("run_geometry_scan signature")
print("-" * 60)
print(inspect.signature(run_geometry_scan))

print()

print("Generating reference universe...")

results = run_geometry_scan()

print()

print("Number of signatures :", len(results))

print()

print("First entry")
print("-" * 60)

for key, value in results[0].items():

    print(f"{key:<20}{value}")
