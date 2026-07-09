%%writefile GER_CORE/S26_B21_modal_transfer.py

"""
=========================================================
S26-B.2.1
Transferência Modal

Observação temporal da distribuição espectral.

=========================================================
"""

from __future__ import annotations

import numpy as np


from GER_CORE.ger_graph import (
    build_ring_graph,
    gaussian_packet,
    spectral_basis
)


from GER_CORE.ger_engine import run_engine


from GER_CORE.ger_modal import (
    modal_probability
)



def run_modal_transfer(
    n=384,
    beta=1.0,
    sigma=0.10,
    dt=5e-5
):


    result = run_engine(
        n=n,
        timesteps=2000,
        dt=dt,
        beta=beta,
        potential="A",
        sigma=sigma,
        snapshot_stride=50
    )


    _, _, theta = build_ring_graph(n)


    _, eigenvectors = spectral_basis(
        n
    )


    history = []


    for snap in result["snapshots"]:

        probability = modal_probability(
            snap["gamma"],
            eigenvectors
        )


        history.append(
            {
                "step":
                    snap["step"],

                "time":
                    snap["time"],

                "dominant_mode":
                    np.argmax(probability),

                "entropy":
                    snap["spectral_entropy"],

                "participation":
                    snap["participation_ratio"],

                "probability":
                    probability
            }
        )


    return history
