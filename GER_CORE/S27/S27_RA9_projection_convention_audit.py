# ============================================================
# GER
#
# S27-RA9
#
# Projection Convention Audit
#
# Determines which matrix convention reproduces
# the Fourier transform used by NumPy.
# ============================================================

import numpy as np

print("=" * 60)
print("GER")
print("S27-RA9")
print("Projection Convention Audit")
print("=" * 60)
print()

N = 16

gamma = np.random.randn(N)

F = np.fft.fft(np.eye(N)) / np.sqrt(N)

fft_ref = np.fft.fft(gamma) / np.sqrt(N)
ifft_ref = np.fft.ifft(gamma) * np.sqrt(N)

tests = {

    "F @ gamma":
        F @ gamma,

    "F.T @ gamma":
        F.T @ gamma,

    "F.conj() @ gamma":
        F.conj() @ gamma,

    "F.conj().T @ gamma":
        F.conj().T @ gamma,

}

print(f"{'Projection':<22}{'FFT error':>15}{'IFFT error':>15}")
print("-" * 55)

best = None
best_err = np.inf

for name, proj in tests.items():

    err_fft = np.linalg.norm(
        proj - fft_ref
    )

    err_ifft = np.linalg.norm(
        proj - ifft_ref
    )

    print(
        f"{name:<22}"
        f"{err_fft:15.6e}"
        f"{err_ifft:15.6e}"
    )

    if min(err_fft, err_ifft) < best_err:

        best_err = min(err_fft, err_ifft)
        best = name

print()

print("=" * 60)
print("Best matching convention")
print("=" * 60)

print(best)
print("Error:", best_err)

print("=" * 60)
