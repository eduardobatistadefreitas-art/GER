# ============================================================
# GER
#
# S27-RA12
#
# Snapshot Dependency Audit
#
# Determines which snapshot fields are actually
# consumed by the GER framework.
# ============================================================

import inspect

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER.CORE.ger_snapshot import (
    build_snapshot,
)

print("=" * 60)
print("GER")
print("S27-RA12")
print("Snapshot Dependency Audit")
print("=" * 60)
print()

print("build_snapshot()")
print("-" * 60)
print(inspect.getsource(build_snapshot))

print()

print("run_persistence_observatory()")
print("-" * 60)
print(inspect.getsource(run_persistence_observatory))
