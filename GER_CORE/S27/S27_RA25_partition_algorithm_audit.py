# ============================================================
# GER
#
# S27-RA25
#
# Partition Algorithm Audit
#
# Audits the implementation of the partition
# operators used by the GER framework.
# ============================================================

import inspect

from GER_CORE.S27_E2_1_partition_lattice import (

    build_partition,

    meet,

    same_partition,

)

print("=" * 60)
print("GER")
print("S27-RA25")
print("Partition Algorithm Audit")
print("=" * 60)
print()

for func in (

    build_partition,

    meet,

    same_partition,

):

    print("=" * 60)
    print(func.__name__)
    print("=" * 60)
    print()

    print(inspect.getsource(func))
    print()
