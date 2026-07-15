# ============================================================
# GER
#
# S27-RA20
#
# Certificate Input Audit
# ============================================================

import inspect

from GER_CORE.S26_B36_stationary_scan import (
    create_certificate,
)

print("=" * 60)
print("GER")
print("S27-RA20")
print("Certificate Input Audit")
print("=" * 60)
print()

print(inspect.getsource(create_certificate))
