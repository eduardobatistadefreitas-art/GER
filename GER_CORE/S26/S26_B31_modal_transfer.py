import numpy as np

from GER_CORE.ger_engine import run_engine


def run_modal_transfer(
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
            5,
            10,
            30
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

        snapshots = simulation["snapshots"]

        transfer = []

        for s in snapshots:

            transfer.append({

                "step":
                    s.get("step"),

                "time":
                    s.get("time"),

                "energy":
                    s.get("energy"),

                "energy_error":
                    s.get("energy_error"),

                "amplitude":
                    s.get("amplitude"),

                "dominant_mode":
                    s.get("dominant_mode"),

                "modal_center":
                    s.get("modal_center"),

                "modal_width":
                    s.get("modal_width"),

                "spectral_entropy":
                    s.get("spectral_entropy"),

                "participation_ratio":
                    s.get("participation_ratio"),

                "spectral_bands":
                    s.get("spectral_bands")

            })

        history.append({

            "beta":
                beta,

            "diverged":
                simulation["diverged"],

            "snapshots":
                transfer

        })

    return history


def print_modal_transfer(history):

    print()
    print("MODAL TRANSFER")
    print()

    for run in history:

        beta = run["beta"]

        data = run["snapshots"]

        first = data[0]
        last = data[-1]

        print(f"β={beta}")

        print(
            f"Snapshots : {len(data)}"
        )

        print(
            f"Mode : {first['dominant_mode']} -> {last['dominant_mode']}"
        )

        print(
            f"Entropy : "
            f"{first['spectral_entropy']:.6f}"
            f" -> "
            f"{last['spectral_entropy']:.6f}"
        )

        print(
            f"Width : "
            f"{first['modal_width']:.6f}"
            f" -> "
            f"{last['modal_width']:.6f}"
        )

        print(
            f"Amplitude : "
            f"{first['amplitude']:.6f}"
            f" -> "
            f"{last['amplitude']:.6f}"
        )

        print(
            f"PR : "
            f"{first['participation_ratio']:.6f}"
            f" -> "
            f"{last['participation_ratio']:.6f}"
        )

        print()
