%%writefile GER_CORE/S26_B36_stationary_scan.py

import numpy as np


# ============================================================
# S26-B36
# Stationary Scan
# ============================================================


def linear_slope(values):

    values = np.asarray(values)

    if len(values) < 2:
        return 0.0

    x = np.arange(len(values))

    return np.polyfit(
        x,
        values,
        1
    )[0]


def persistence_score(
    Rloc,
    Dspec,
    delta_PR,
    Cauto
):

    return (
        np.abs(Cauto)
        *
        np.exp(
            -(
                Rloc
                +
                Dspec
                +
                np.abs(delta_PR)
            )
        )
    )


def compute_statistics(
    observables,
    K=None
):

    if K is None:
        K = len(observables["Rloc"])

    stats = {}

    data = {}

    for key in observables:

        data[key] = np.asarray(
            observables[key]
        )[-K:]

    stats["mean_Rloc"] = np.mean(data["Rloc"])
    stats["mean_Dspec"] = np.mean(data["Dspec"])

    stats["mean_delta_PR"] = np.mean(
        np.abs(data["Hshape"])
    )

    stats["var_Rloc"] = np.var(data["Rloc"])
    stats["var_Dspec"] = np.var(data["Dspec"])

    stats["slope_Rmacro"] = linear_slope(
        data["Rmacro"]
    )

    stats["slope_Cauto"] = linear_slope(
        data["Cauto"]
    )

    stats["slope_entropy"] = linear_slope(
        data["entropy"]
    )

    P = []

    for i in range(len(data["Rloc"])):

        P.append(

            persistence_score(

                data["Rloc"][i],

                data["Dspec"][i],

                data["Hshape"][i],

                data["Cauto"][i]

            )

        )

    P = np.asarray(P)

    stats["mean_P"] = np.mean(P)
    stats["var_P"] = np.var(P)

    return stats, P


def classify_regime(

    stats,

    epsilon=1e-8

):

    if (

        stats["mean_Dspec"] < epsilon
        and
        stats["mean_delta_PR"] < 1e-3
        and
        stats["var_P"] < 1e-6

    ):

        return "PERSISTENTE"

    if (

        stats["mean_delta_PR"] > 1e-3
        and
        stats["slope_Cauto"] < -epsilon

    ):

        return "TRANSITORIO"

    if (

        stats["var_Dspec"] > epsilon

    ):

        return "OSCILATORIO"

    if (

        stats["var_Rloc"] > 1/epsilon

    ):

        return "INSTAVEL"

    return "TRANSITORIO"


def run_stationary_scan(

    observables,

    K=None,

    epsilon=1e-8

):

    stats, P = compute_statistics(

        observables,

        K

    )

    regime = classify_regime(

        stats,

        epsilon

    )

    return {

        "regime": regime,

        "persistence_score": stats["mean_P"],

        "persistence_variance": stats["var_P"],

        "statistics": stats,

        "persistence_history": P

    }
