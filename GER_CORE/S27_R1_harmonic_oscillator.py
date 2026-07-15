# ============================================================
# GER
#
# S27-R1
#
# External Snapshot Construction
#
# First Reality Validation experiment.
#
# Goal:
# Construct a GER-compatible spectral snapshot
# from a Fourier representation of a harmonic
# oscillator.
# ============================================================

import numpy as np

from GER.CORE.ger_modal import (
    modal_probability,
    participation_ratio,
    spectral_center,
    spectral_entropy,
)

# ------------------------------------------------------------

def harmonic_signal(
    omega=1.0,
    amplitude=1.0,
    samples=2048,
    dt=1e-3,
):

    t = np.arange(samples) * dt

    x = amplitude * np.cos(
        omega * t
    )

    return t, x

# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("GER")
    print("S27-R1")
    print("External Snapshot Construction")
    print("=" * 60)
    print()

    _, signal = harmonic_signal()

    coeff = np.fft.rfft(signal)

    probability = modal_probability(coeff)

    pr = participation_ratio(probability)

    center = spectral_center(probability)

    entropy = spectral_entropy(probability)

    snapshot = {

        "gamma": coeff,

        "probability": probability,

        "participation_ratio": pr,

        "modal_center": center,

        "spectral_entropy": entropy,

    }

    print("Snapshot fields")
    print("-" * 60)

    for key in snapshot:

        value = snapshot[key]

        if np.isscalar(value):

            print(f"{key:<24}{value}")

        else:

            print(
                f"{key:<24}"
                f"shape={np.shape(value)}"
            )

    print()

    print("Consistency")

    print("-" * 60)

    print(
        "Probability sum :",
        np.sum(probability),
    )

    print(
        "Participation Ratio :",
        pr,
    )

    print(
        "Modal Center :",
        center,
    )

    print(
        "Spectral Entropy :",
        entropy,
    )

    print()

    print("=" * 60)
    print("STATUS : SNAPSHOT CONSTRUCTED")
    print("=" * 60)


if __name__ == "__main__":

    main()
