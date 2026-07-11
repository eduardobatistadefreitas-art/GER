import numpy as np


def run_mixing_rate(history):

    results = []

    for run in history:

        beta = run["beta"]
        snapshots = run["snapshots"]

        time = []
        d_entropy = []
        d_width = []
        d_pr = []
        d_amplitude = []

        for i in range(1, len(snapshots)):

            s0 = snapshots[i - 1]
            s1 = snapshots[i]

            dt = s1["time"] - s0["time"]

            if dt <= 0:
                continue

            if (
                np.isnan(s0["spectral_entropy"])
                or np.isnan(s1["spectral_entropy"])
            ):
                break

            time.append(s1["time"])

            d_entropy.append(
                (s1["spectral_entropy"] -
                 s0["spectral_entropy"]) / dt
            )

            d_width.append(
                (s1["modal_width"] -
                 s0["modal_width"]) / dt
            )

            d_pr.append(
                (s1["participation_ratio"] -
                 s0["participation_ratio"]) / dt
            )

            d_amplitude.append(
                (s1["amplitude"] -
                 s0["amplitude"]) / dt
            )

        results.append({

            "beta": beta,

            "time": np.array(time),

            "d_entropy": np.array(d_entropy),

            "d_width": np.array(d_width),

            "d_pr": np.array(d_pr),

            "d_amplitude": np.array(d_amplitude)

        })

    return results


def print_mixing_rate(results):

    print()
    print("MIXING RATE")
    print()

    for r in results:

        print(f"β={r['beta']}")

        if len(r["d_entropy"]) == 0:

            print("Sem dados.")
            print()
            continue

        print(
            f"max dS/dt = {np.max(r['d_entropy']):.6f}"
        )

        print(
            f"mean dS/dt = {np.mean(r['d_entropy']):.6f}"
        )

        print(
            f"max dWidth/dt = {np.max(r['d_width']):.6f}"
        )

        print(
            f"max dPR/dt = {np.max(r['d_pr']):.6f}"
        )

        print(
            f"max dA/dt = {np.max(r['d_amplitude']):.6f}"
        )

        print()
