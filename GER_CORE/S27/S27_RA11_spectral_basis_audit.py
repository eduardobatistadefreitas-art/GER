# ============================================================
# GER
#
# S27-RA11
#
# Spectral Basis Audit
#
# Final architectural audit before generalizing
# the modal interface.
# ============================================================

import inspect

from GER.CORE.ger_graph import spectral_basis

print("=" * 60)
print("GER")
print("S27-RA11")
print("Spectral Basis Audit")
print("=" * 60)
print()

print(inspect.getsource(spectral_basis))
