import numpy as np


def analyze_beta_dependence(history):
    """
    Analisa a resposta dinâmica em função de beta.

    Entrada:
        history:
            lista produzida por run_beta_dependence()

    Saída:
        dicionário com métricas de sensibilidade.
    """

    if len(history) < 2:
        raise ValueError(
            "Histórico insuficiente para análise."
        )


    beta = np.array(
        [
            item["beta"]
            for item in history
        ],
        dtype=float
    )


    energy = np.array(
        [
            item["energy"]
            for item in history
        ],
        dtype=float
    )


    amplitude = np.array(
        [
            item["amplitude"]
            for item in history
        ],
        dtype=float
    )


    modes = [
        item["dominant_mode"]
        for item in history
    ]


    pr = np.array(
        [
            item["participation_ratio"]
            for item in history
        ],
        dtype=float
    )


    dE_dbeta = np.gradient(
        energy,
        beta
    )


    amplitude_gain = (
        amplitude[-1] - amplitude[0]
    ) / amplitude[0]


    mode_stable = (
        len(set(modes)) == 1
    )


    result = {

        "beta_range":
            (
                beta[0],
                beta[-1]
            ),


        "energy_gradient":
            dE_dbeta,


        "energy_monotonic_decrease":
            bool(
                np.all(
                    np.diff(energy) < 0
                )
            ),


        "amplitude_gain":
            amplitude_gain,


        "mode_stable":
            mode_stable,


        "dominant_modes":
            modes,


        "pr_variation":
            (
                pr[-1] - pr[0]
            ),


        "mean_pr":
            np.mean(pr)

    }


    return result



def print_beta_analysis(result):

    print("\nBETA ANALYSIS\n")


    print(
        "Beta range:",
        result["beta_range"]
    )


    print(
        "Energy monotonic decrease:",
        result["energy_monotonic_decrease"]
    )


    print(
        "Amplitude gain:",
        f"{100*result['amplitude_gain']:.3f}%"
    )


    print(
        "Dominant mode stable:",
        result["mode_stable"]
    )


    print(
        "Modes:",
        result["dominant_modes"]
    )


    print(
        "PR variation:",
        result["pr_variation"]
    )


    print(
        "Mean PR:",
        result["mean_pr"]
    )
