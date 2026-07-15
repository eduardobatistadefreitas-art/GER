# ============================================================
# GER
#
# S27-RA14
#
# Stationary Scan Interface
#
# ============================================================

import inspect

from GER_CORE.S26_B36_stationary_scan import (
    stationary_scan,
)

print("=" * 60)
print("GER")
print("S27-RA14")
print("Stationary Scan Interface")
print("=" * 60)
print()

print(inspect.getsource(stationary_scan))
