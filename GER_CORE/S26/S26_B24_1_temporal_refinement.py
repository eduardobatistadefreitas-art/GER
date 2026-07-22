import numpy as np

from GER_CORE.ger_engine import run_engine


def run_temporal_refinement(
    betas=None,
    dts=None,
    n=256,
    sigma=20,
    timesteps=2000,
    snapshot_stride=50,
    potential="A"
):

    if betas is None:
        betas = [
            10,
            20
        ]

    if dts is None:
        dts = [
            2.5e-4,
            1.25e-4,
            6.25e-5,
            3.125e-5
        ]


    history = []


    for beta in betas:

        for dt in dts:

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

                "dt":
                    dt,

                "energy":
                    simulation["final"]["energy"],

                "energy_error":
                    simulation["final"]["energy_error"],

                "amplitude":
                    final.get(
                        "amplitude",
                        np.nan
                    ),

                "spectral_entropy":
                    final.get(
                        "spectral_entropy",
                        np.nan
                    ),

                "participation_ratio":
                    final.get(
                        "participation_ratio",
                        np.nan
                    ),

                "diverged":
                    simulation["diverged"]

            })


    return history



def print_temporal_refinement(history):

    print("\nTEMPORAL REFINEMENT\n")

    for item in history:

        print(
            f"β={item['beta']:>3} | "
            f"dt={item['dt']:.2e} | "
            f"E={item['energy']:.5e} | "
            f"A={item['amplitude']} | "
            f"PR={item['participation_ratio']} | "
            f"div={item['diverged']}"
        )
