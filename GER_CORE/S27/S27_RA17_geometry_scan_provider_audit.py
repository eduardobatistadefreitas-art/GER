# ============================================================
# GER
#
# S27-RA17
#
# Geometry Scan Provider Audit
#
# ============================================================

import inspect

from GER.CORE.providers.geometry_scan_provider import (
    build_signature,
)

print("=" * 60)
print("GER")
print("S27-RA17")
print("Geometry Scan Provider Audit")
print("=" * 60)
print()

print(inspect.signature(build_signature))
print()

print(inspect.getsource(build_signature))
