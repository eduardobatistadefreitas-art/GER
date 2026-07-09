%%writefile GER_CORE/S26_B34_scaling_robustness.py

import numpy as np

from GER_CORE.S26_B31_modal_transfer import run_modal_transfer
from GER_CORE.S26_B32_mixing_rate import run_mixing_rate
from GER_CORE.S26_B33_mixing_scaling import run_mixing_scaling


def run_scaling_robustness(

    dt_values=None,

    betas=None,

    n=256,

    sigma=20,

    timesteps=2000,

    snapshot_stride=50,

    potential="A"

):

    if dt_values is None:

        dt_values = [

            2.5e-4,
            1.25e-4,
            6.25e-5,
            3.125e-5

        ]

    results = []

    for dt in dt_values:

        history = run_modal_transfer(

            betas=betas,

            n=n,

            sigma=sigma,

            dt=dt,

            timesteps=timesteps,

            snapshot_stride=snapshot_stride,

            potential=potential

        )

        mixing = run_mixing_rate(history)

        scaling = run_mixing_scaling(mixing)

        results.append({

            "dt": dt,

            "entropy_alpha":
                scaling["entropy"]["alpha"],

            "width_alpha":
                scaling["width"]["alpha"],

            "amplitude_alpha":
                scaling["amplitude"]["alpha"]

        })

    return results


def print_scaling_robustness(results):

    print()
    print("SCALING ROBUSTNESS")
    print()

    for r in results:

        print(

            f"dt={r['dt']:.2e}"

            f" | αS={r['entropy_alpha']:.4f}"

            f" | αW={r['width_alpha']:.4f}"

            f" | αA={r['amplitude_alpha']:.4f}"

        )
