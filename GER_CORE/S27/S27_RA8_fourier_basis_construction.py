# ============================================================
# GER
#
# S27-RA8
#
# Fourier Basis Construction
#
# Verifies whether a Fourier basis satisfies the
# linear projection architecture used by the GER
# modal framework.
# ============================================================

import numpy as np

print("=" * 60)
print("GER")
print("S27-RA8")
print("Fourier Basis Construction")
print("=" * 60)
print()

N = 16

print("Building Fourier basis...")
print()

# ------------------------------------------------------------
# Fourier matrix
# ------------------------------------------------------------

F = np.fft.fft(np.eye(N)) / np.sqrt(N)

# ------------------------------------------------------------
# Test signal
# ------------------------------------------------------------

gamma = np.random.randn(N)

# ------------------------------------------------------------
# GER-style modal projection
# ------------------------------------------------------------

gamma_hat_projection = F.conj().T @ gamma

# ------------------------------------------------------------
# Standard FFT
# ------------------------------------------------------------

gamma_hat_fft = np.fft.fft(gamma) / np.sqrt(N)

error = np.linalg.norm(
    gamma_hat_projection - gamma_hat_fft
)

print("Projection error")
print("-" * 60)
print(error)
print()

print("Orthogonality")

orthogonality = np.linalg.norm(
    F.conj().T @ F - np.eye(N)
)

print("-" * 60)
print(orthogonality)
print()

print("Energy conservation")

energy_signal = np.sum(np.abs(gamma) ** 2)

energy_modal = np.sum(
    np.abs(gamma_hat_projection) ** 2
)

print("-" * 60)
print("Signal :", energy_signal)
print("Modal  :", energy_modal)
print()

print("=" * 60)

if error < 1e-10:

    print("Projection : PASS")

else:

    print("Projection : FAIL")

if orthogonality < 1e-10:

    print("Orthogonality : PASS")

else:

    print("Orthogonality : FAIL")

if abs(energy_signal - energy_modal) < 1e-10:

    print("Parseval : PASS")

else:

    print("Parseval : FAIL")

print("=" * 60)
