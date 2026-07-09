%%writefile GER_CORE/S26_B24_2_stability_map.py

import numpy as np

from GER_CORE.ger_engine import run_engine


def run_stability_map(
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
            1,
            2,
            5,
            10,
            20,
            30,
            50
        ]


    if dts is None:
        dts = [
            2.5e-4,
            1.25e-4,
            6.25e-5,
            3.125e-5
        ]


    stability = []


    for beta in betas:

        for dt in dts:

            try:

                simulation = run_engine(
                    n=n,
                    sigma=sigma,
                    dt=dt,
                    timesteps=timesteps,
                    beta=beta,
                    snapshot_stride=snapshot_stride,
                    potential=potential
                )


                snapshots = simulation["snapshots"]

                if len(snapshots) == 0:
                    raise RuntimeError(
                        "Sem snapshots"
                    )


                final_snapshot = snapshots[-1]


                result = {

                    "beta":
                        beta,

                    "dt":
                        dt,

                    "energy":
                        simulation["final"]["energy"],

                    "energy_error":
                        simulation["final"]["energy_error"],

                    "amplitude":
                        final_snapshot.get(
                            "amplitude",
                            np.nan
                        ),

                    "participation_ratio":
                        final_snapshot.get(
                            "participation_ratio",
                            np.nan
                        ),

                    "dominant_mode":
                        final_snapshot.get(
                            "dominant_mode",
                            np.nan
                        ),

                    "stable":
                        not simulation["diverged"]
                    and
                        np.isfinite(
                            simulation["final"]["energy"]
                        )

                }


            except Exception as e:

                result = {

                    "beta":
                        beta,

                    "dt":
                        dt,

                    "energy":
                        np.nan,

                    "energy_error":
                        np.nan,

                    "amplitude":
                        np.nan,

                    "participation_ratio":
                        np.nan,

                    "dominant_mode":
                        np.nan,

                    "stable":
                        False,

                    "error":
                        str(e)
                }


            stability.append(result)


    return stability



def print_stability_map(stability):

    print("\nSTABILITY MAP\n")

    for item in stability:

        status = "YES" if item["stable"] else "NO"

        print(
            f"β={item['beta']:>5} | "
            f"dt={item['dt']:.2e} | "
            f"stable={status:<3} | "
            f"E={item['energy']:.5e} | "
            f"A={item['amplitude']:.5f}"
        )
