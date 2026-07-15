# ============================================================
# GER
#
# S27-RA2
#
# Snapshot Generation Audit
#
# Audits how the GER engine constructs the
# spectral snapshot consumed by the Persistence
# Observatory.
# ============================================================

import inspect

from GER.CORE import ger_modal

print("=" * 60)
print("GER")
print("S27-RA2")
print("Snapshot Generation Audit")
print("=" * 60)
print()

TARGETS = [
    "compute_probability_distribution",
    "compute_participation_ratio",
    "compute_modal_center",
    "compute_modal_energy",
]

for name in TARGETS:

    if hasattr(ger_modal, name):

        print("=" * 60)
        print(name)
        print("=" * 60)
        print()

        print(
            inspect.getsource(
                getattr(ger_modal, name)
            )
        )

        print()
