import numpy as np

from GER_CORE.S26_B31_modal_transfer import run_modal_transfer
from GER_CORE.S26_B32_mixing_rate import run_mixing_rate
from GER_CORE.S26_B33_mixing_scaling import run_mixing_scaling


def run_sigma_robustness(

    sigma_values=None,

    betas=None,

    n=256,

    dt=6.25e-5,

    timesteps=2000,

    snapshot_stride=50,

    potential="A"

):

    if sigma_values is None:

        sigma_values = [
            10,
            20,
            40
        ]


    results = []


    for sigma in sigma_values:


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

            "sigma": sigma,

            "entropy_alpha":
                scaling["entropy"]["alpha"],

            "width_alpha":
                scaling["width"]["alpha"],

            "amplitude_alpha":
                scaling["amplitude"]["alpha"]

        })


    return results



def print_sigma_robustness(results):

    print()
    print("SIGMA ROBUSTNESS")
    print()


    for r in results:

        print(

            f"sigma={r['sigma']}"

            f" | αS={r['entropy_alpha']:.4f}"

            f" | αW={r['width_alpha']:.4f}"

            f" | αA={r['amplitude_alpha']:.4f}"

        )
