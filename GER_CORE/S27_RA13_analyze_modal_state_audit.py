# ============================================================
# GER
#
# S27-RA13
#
# Analyze Modal State Audit
#
# Audits how the GER computes modal observables
# from modal coefficients.
# ============================================================

import inspect

from GER.CORE.ger_modal import (
    analyze_modal_state,
    modal_energy,
    modal_probability,
    participation_ratio,
    spectral_center,
    spectral_entropy,
)

print("=" * 60)
print("GER")
print("S27-RA13")
print("Analyze Modal State Audit")
print("=" * 60)
print()

functions = [

    analyze_modal_state,
    modal_energy,
    modal_probability,
    participation_ratio,
    spectral_center,
    spectral_entropy,

]

for func in functions:

    print("=" * 60)
    print(func.__name__)
    print("=" * 60)
    print(inspect.getsource(func))
    print()
