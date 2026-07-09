import numpy as np

from GER_CORE.ger_engine import run_engine


def run_transition_scan(
    betas=None,
    n=256,
    sigma=20,
    dt=0.00025,
    timesteps=2000,
    snapshot_stride=50,
    potential="A"
):

    if betas is None:
        betas = [
            1,
            2,
            5,
            10,
            20,
            50,
            100
        ]


    history = []


    for beta in betas:

        simulation = run_engine(
            n=n,
            sigma=sigma,
            dt=dt,
            timesteps=timesteps,
            snapshot_stride=snapshot_stride,
            beta=beta,
            potential=potential
        )


        final = simulation["snapshots"][-1]


        history.append({

            "beta":
                beta,

            "energy":
                simulation["final"]["energy"],

            "energy_error":
                simulation["final"]["energy_error"],

            "amplitude":
                final["amplitude"],

            "dominant_mode":
                final["dominant_mode"],

            "spectral_entropy":
                final["spectral_entropy"],

            "participation_ratio":
                final["participation_ratio"],

            "modal_width":
                final["modal_width"],

            "diverged":
                simulation["diverged"]

        })


    return history



def print_transition_scan(history):

    print("\nTRANSITION SCAN\n")


    for item in history:

        print(
            f"β={item['beta']:>6} | "
            f"E={item['energy']:.5e} | "
            f"A={item['amplitude']:.4f} | "
            f"mode={item['dominant_mode']} | "
            f"PR={item['participation_ratio']:.5f} | "
            f"H={item['spectral_entropy']:.4f}"
        )
