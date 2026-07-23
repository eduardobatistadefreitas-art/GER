# ============================================================
# GER
#
# S27-RA28
#
# Partition Usage Audit
#
# Audits how the first partition experiment
# constructs its universe and key.
# ============================================================

import inspect

from GER_CORE.S27_E1_1_operator_partitions import main

print("=" * 60)
print("GER")
print("S27-RA28")
print("Partition Usage Audit")
print("=" * 60)
print()

print(inspect.getsource(main))
