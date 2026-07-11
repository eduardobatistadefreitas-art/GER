%%writefile GER_CORE/S26_B36_stationary_scan.py

import numpy as np


# ============================================================
# S26-B36
# Stationary Scan
#
# Classificação algorítmica de regimes
# baseada no observatório B35
# ============================================================


def linear_slope(values):

    values = np.asarray(values)

    if len(values) < 2:
        return 0.0

    x = np.arange(len(values))

    coef = np.polyfit(
        x,
        values,
        1
    )

    return coef[0]



def mean_abs(x):

    return np.mean(
        np.abs(
            np.asarray(x)
        )
    )



def compute_persistence_score(
    Rloc,
    Dspec,
    Hshape,
    Cauto,
    dt
):

    return (
        np.abs(Cauto)
        *
        np.exp(
            -(
                dt * Rloc
                +
                Dspec
                +
                dt * np.abs(Hshape)
            )
        )
    )



def stationary_scan(
    observables,
    dt,
    K=None,
    epsilon=1e-8
):

    if K is None:
        K = len(
            observables["Rloc"]
        )


    data = {}

    for key in observables:

        data[key] = np.asarray(
            observables[key]
        )[-K:]


    # -------------------------
    # Estatísticas
    # -------------------------

    statistics = {

        "mean_Rloc":
            np.mean(data["Rloc"]),

        "mean_Dspec":
            np.mean(data["Dspec"]),

        "mean_Hshape":
            mean_abs(data["Hshape"]),

        "var_Rloc":
            np.var(data["Rloc"]),

        "var_Dspec":
            np.var(data["Dspec"]),

        "slope_Rmacro":
            linear_slope(
                data["Rmacro"]
            ),

        "slope_Cauto":
            linear_slope(
                data["Cauto"]
            ),

        "slope_entropy":
            linear_slope(
                data["entropy"]
            )

    }


    # -------------------------
    # Persistence score
    # -------------------------

    P = []

    for i in range(len(data["Rloc"])):

        P.append(

            compute_persistence_score(
                data["Rloc"][i],
                data["Dspec"][i],
                data["Hshape"][i],
                data["Cauto"][i],
                dt
            )

        )


    P = np.asarray(P)


    statistics["mean_P"] = np.mean(P)
    statistics["var_P"] = np.var(P)



    # -------------------------
    # Classificação
    # -------------------------

    if (

        statistics["mean_Rloc"] < epsilon
        and
        statistics["mean_Dspec"] < epsilon
        and
        statistics["mean_Hshape"] < epsilon

    ):

        regime = "PERSISTENTE"



    elif (

        statistics["mean_Hshape"] > epsilon
        and
        statistics["slope_Cauto"] < -epsilon

    ):

        regime = "TRANSITORIO"



    elif (

        statistics["mean_Rloc"] > epsilon
        and
        statistics["var_Dspec"] > epsilon

    ):

        regime = "OSCILATORIO"



    elif (

        statistics["var_Rloc"] > 1/epsilon

    ):

        regime = "INSTAVEL"



    else:

        regime = "TRANSITORIO"



    return {

        "regime": regime,

        "persistence_score":
            statistics["mean_P"],

        "persistence_variance":
            statistics["var_P"],

        "statistics":
            statistics,

        "persistence_history":
            P

    }
