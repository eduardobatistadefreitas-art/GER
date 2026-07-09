%%writefile GER_CORE/S26_B34_2_spatial_robustness.py

import numpy as np

from GER_CORE.S26_B31_modal_transfer import run_modal_transfer
from GER_CORE.S26_B32_mixing_rate import run_mixing_rate
from GER_CORE.S26_B33_mixing_scaling import run_mixing_scaling


def run_spatial_robustness(

    n_values=None,

    betas=None,

    dt=6.25e-5,

    sigma=20,

    timesteps=2000,

    snapshot_stride=50,

    potential="A"

):

    if n_values is None:

        n_values = [
            128,
            256,
            512
        ]


    results = []


    for n in n_values:


        history = run_modal_transfer(

            betas=betas,

            n=n,

            sigma=sigma,

            dt=dt,

            timesteps=timesteps,

            snapshot_stride=snapshot_stride,

            potential=potential

        )


        mixing = run_mixing_rate(
            history
        )


        scaling = run_mixing_scaling(
            mixing
        )


        results.append({

            "n": n,

            "entropy_alpha":
                scaling["entropy"]["alpha"],

            "width_alpha":
                scaling["width"]["alpha"],

            "amplitude_alpha":
                scaling["amplitude"]["alpha"]

        })


    return results



def print_spatial_robustness(results):

    print()
    print("SPATIAL ROBUSTNESS")
    print()


    for r in results:

        print(

            f"n={r['n']}"

            f" | αS={r['entropy_alpha']:.4f}"

            f" | αW={r['width_alpha']:.4f}"

            f" | αA={r['amplitude_alpha']:.4f}"

        )
