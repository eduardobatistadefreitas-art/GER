%%writefile GER_CORE/S26_B36_stationary_scan.py

import numpy as np


# ============================================================
# S26-B36
# Stationary Scan
#
# Classificação de regimes dinâmicos
#
# Entrada:
# observables B35
#
# Saída:
# regime matemático
# persistence score
# estatísticas assintóticas
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



def persistence_score(
    Rloc,
    Dspec,
    Hshape,
    Cauto,
    dt
):

    return (
        abs(Cauto)
        *
        np.exp(
            -(
                dt*Rloc
                +
                Dspec
                +
                dt*abs(Hshape)
            )
        )
    )



def compute_statistics(
    obs,
    K=10
):

    data = {}

    for key in obs:

        data[key] = np.asarray(
            obs[key]
        )


    window = {}

    for key in data:

        window[key] = data[key][-K:]



    stats = {

        "mean_Rloc":
            np.mean(
                window["Rloc"]
            ),

        "mean_Dspec":
            np.mean(
                window["Dspec"]
            ),

        "mean_Hshape":
            np.mean(
                np.abs(
                    window["Hshape"]
                )
            ),

        "var_Rloc":
            np.var(
                window["Rloc"]
            ),

        "var_Dspec":
            np.var(
                window["Dspec"]
            ),

        "slope_Rmacro":
            linear_slope(
                window["Rmacro"]
            ),

        "slope_Cauto":
            linear_slope(
                window["Cauto"]
            ),

        "slope_entropy":
            linear_slope(
                window["entropy"]
            )

    }


    P = []

    for i in range(len(window["Rloc"])):

        P.append(

            persistence_score(
                window["Rloc"][i],
                window["Dspec"][i],
                window["Hshape"][i],
                window["Cauto"][i],
                1.0
            )

        )


    stats["persistence"] = np.asarray(P)

    stats["mean_P"] = np.mean(P)

    stats["var_P"] = np.var(P)


    return stats



def classify_regime(
    stats,
    epsilon=1e-3
):


    # ----------------------------
    # Persistente
    # ----------------------------

    if (

        stats["mean_Rloc"] <= epsilon

        and

        stats["mean_Dspec"] <= epsilon

        and

        stats["mean_Hshape"] <= epsilon

        and

        abs(stats["slope_Rmacro"])
        <= epsilon

    ):

        return "PERSISTENTE"



    # ----------------------------
    # Instável
    # ----------------------------

    if (

        stats["mean_Rloc"] > 1.0

        or

        stats["var_Rloc"]
        >
        1/epsilon

    ):

        return "INSTAVEL"



    # ----------------------------
    # Transitório
    # ----------------------------

    if (

        abs(
            stats["slope_entropy"]
        )
        >
        epsilon

        or

        stats["mean_Dspec"]
        >
        epsilon

    ):

        return "TRANSITORIO"



    # ----------------------------
    # Oscilatório
    # ----------------------------

    if (

        stats["var_Dspec"]
        >
        epsilon

    ):

        return "OSCILATORIO"



    return "TRANSITORIO"



def run_stationary_scan(
    observables,
    K=10,
    epsilon=1e-3
):


    stats = compute_statistics(
        observables,
        K
    )


    regime = classify_regime(
        stats,
        epsilon
    )


    return {

        "regime": regime,

        "persistence_score":
            stats["mean_P"],

        "persistence_variance":
            stats["var_P"],

        "statistics":
            stats

    }
