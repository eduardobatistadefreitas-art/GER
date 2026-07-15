# ============================================================
# GER
#
# S27-RA1
#
# Observatory Input Audit
#
# Audits the minimum input required by the
# GER Persistence Observatory.
# ============================================================

import inspect

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


print("=" * 60)
print("GER")
print("S27-RA1")
print("Observatory Input Audit")
print("=" * 60)
print()

print(inspect.getsource(run_persistence_observatory))
