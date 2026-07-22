import numpy as np

from GER_CORE.ger_engine import run_engine


def find_critical_dt(
    beta,
    dts=None,
    n=256,
    sigma=20,
    timesteps=2000,
    snapshot_stride=50,
    potential="A"
):

    if dts is None:
        dts = [
            5e-4,
            2.5e-4,
            1.25e-4,
            6.25e-5,
            3.125e-5,
            1.5625e-5
        ]


    results = []


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


            snapshot = simulation["snapshots"][-1]


            stable = (
                not simulation["diverged"]
                and
                np.isfinite(
                    simulation["final"]["energy"]
                )
            )


            results.append(
                {
                    "beta": beta,
                    "dt": dt,
                    "stable": stable,
                    "energy":
                        simulation["final"]["energy"],
                    "amplitude":
                        snapshot.get(
                            "amplitude",
                            np.nan
                        )
                }
            )


        except Exception:

            results.append(
                {
                    "beta": beta,
                    "dt": dt,
                    "stable": False,
                    "energy": np.nan,
                    "amplitude": np.nan
                }
            )


    stable_dts = [
        r["dt"]
        for r in results
        if r["stable"]
    ]


    critical = None

    if len(stable_dts) > 0:
        critical = max(stable_dts)


    return {
        "beta": beta,
        "critical_dt": critical,
        "scan": results
    }



def run_critical_curve(
    betas=None
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


    curve = []


    for beta in betas:

        result = find_critical_dt(
            beta
        )

        curve.append(
            result
        )


    return curve



def print_critical_curve(curve):

    print("\nCRITICAL DT CURVE\n")

    for item in curve:

        print(
            f"β={item['beta']:>5} | "
            f"dt_crit={item['critical_dt']}"
        )
