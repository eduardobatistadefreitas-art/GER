import numpy as np


def run_mixing_scaling(mixing):

    beta = []
    max_entropy = []
    max_width = []
    max_amplitude = []

    for run in mixing:

        if len(run["d_entropy"]) == 0:
            continue

        if np.isnan(np.max(run["d_amplitude"])):
            continue

        beta.append(run["beta"])

        max_entropy.append(
            np.max(run["d_entropy"])
        )

        max_width.append(
            np.max(run["d_width"])
        )

        max_amplitude.append(
            np.max(run["d_amplitude"])
        )

    beta = np.array(beta)

    def fit(x, y):

        lx = np.log(beta)
        ly = np.log(y)

        alpha, logC = np.polyfit(
            lx,
            ly,
            1
        )

        pred = alpha * lx + logC

        ss_res = np.sum(
            (ly - pred) ** 2
        )

        ss_tot = np.sum(
            (ly - np.mean(ly)) ** 2
        )

        r2 = 1 - ss_res / ss_tot

        return {

            "alpha": alpha,

            "C": np.exp(logC),

            "R2": r2

        }

    return {

        "entropy":
            fit(beta, max_entropy),

        "width":
            fit(beta, max_width),

        "amplitude":
            fit(beta, max_amplitude)

    }


def print_mixing_scaling(result):

    print()
    print("MIXING SCALING")
    print()

    for name in [
        "entropy",
        "width",
        "amplitude"
    ]:

        r = result[name]

        print(name.upper())

        print("alpha =", r["alpha"])
        print("C =", r["C"])
        print("R² =", r["R2"])

        print()
