%%writefile GER_CORE/S26_B36_1_classifier_audit.py

import numpy as np


# ============================================================
# S26-B36_1
#
# Stationary Scan / Classifier Audit
#
# Entrada:
# observables B35
#
# Saída:
# regime dinâmico
# persistence score
# estatísticas assintóticas
#
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



def compute_persistence(
    Rloc,
    Dspec,
    Hshape,
    Cauto,
    dt
):

    delta_PR = np.abs(
        Hshape * dt
    )


    P = (
        np.abs(Cauto)
        *
        np.exp(
            -(
                dt * Rloc
                +
                Dspec
                +
                delta_PR
            )
        )
    )


    return P



def classify_regime(
    obs,
    dt=1e-4,
    window=None
):


    data = {}

    for key,value in obs.items():

        data[key] = np.asarray(value)



    size = len(
        data["Rloc"]
    )


    if window is None:

        window = size



    # janela terminal

    sl = slice(
        max(0,size-window),
        size
    )


    Rloc = data["Rloc"][sl]
    Dspec = data["Dspec"][sl]
    Hshape = data["Hshape"][sl]
    Cauto = data["Cauto"][sl]


    if "Rmacro" in data:

        Rmacro = data["Rmacro"][sl]

    else:

        Rmacro = np.zeros_like(Rloc)


    if "entropy" in data:

        entropy = data["entropy"][sl]

    else:

        entropy = np.zeros_like(Rloc)



    # diferenças físicas

    delta_PR = np.abs(
        Hshape * dt
    )


    # persistence

    P = compute_persistence(
        Rloc,
        Dspec,
        Hshape,
        Cauto,
        dt
    )


    mean_P = np.mean(P)

    var_P = np.var(P)



    # erro numérico adaptativo

    epsilon = max(
        1e-10,
        np.std(P)
    )



    statistics = {

        "mean_Rloc":
            np.mean(Rloc),

        "mean_Dspec":
            np.mean(Dspec),

        "mean_delta_PR":
            np.mean(delta_PR),

        "var_Rloc":
            np.var(Rloc),

        "var_Dspec":
            np.var(Dspec),

        "slope_Rmacro":
            linear_slope(Rmacro),

        "slope_Cauto":
            linear_slope(Cauto),

        "slope_entropy":
            linear_slope(entropy),

        "mean_P":
            mean_P,

        "var_P":
            var_P

    }



    # ========================================================
    # Classificador
    # ========================================================


    # Persistente:
    #
    # alta memória
    # pouca mudança espectral
    #

    if (

        mean_P > 0.99

        and

        np.mean(delta_PR)
        < 1e-3

    ):

        regime = "PERSISTENTE"



    # Oscilatório:

    elif (

        mean_P > 0.5

        and

        np.var(Cauto)
        > epsilon

    ):

        regime = "OSCILATORIO"



    # Instável:

    elif (

        np.mean(Rloc)
        > 10

        or

        np.var(Rloc)
        > 1

    ):

        regime = "INSTAVEL"



    else:

        regime = "TRANSITORIO"



    return {

        "regime":
            regime,

        "persistence_score":
            mean_P,

        "persistence_variance":
            var_P,

        "statistics":
            statistics,

        "persistence_history":
            P

    }
