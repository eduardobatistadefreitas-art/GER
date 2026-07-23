# ============================================================
# GER
#
# S27-RA26
#
# Partition Class Audit
# ============================================================

import inspect

from GER.CORE.partition import Partition

print("=" * 60)
print("GER")
print("S27-RA26")
print("Partition Class Audit")
print("=" * 60)
print()

print(inspect.getsource(Partition))
