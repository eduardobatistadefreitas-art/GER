%%writefile GER_CORE/S26_B36_stationary_scan.py

import numpy as np

# ============================================================
# S26-B36
# Stationary Scan
#
# API definitiva
#
# Esta rotina recebe os observáveis produzidos pela B35 e
# produz:
#
#   • estatísticas
#   • persistence score
#   • classificação
#
# Toda a série B36 deve utilizar SOMENTE esta API.
# ============================================================


# ------------------------------------------------------------
# Inclinação linear
# ------------------------------------------------------------

def linear_slope(values):

    values = np.asarray(values, dtype=float)

    if len(values) < 2:
        return 0.0

    x = np.arange(len(values))

    return np.polyfit(x, values, 1)[0]


# ------------------------------------------------------------
# Persistence Score
# ------------------------------------------------------------

def persistence_score(

    Rloc,
    Dspec,
    delta_PR,
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

                np.abs(delta_PR)

            )

        )

    )


# ------------------------------------------------------------
# Estatísticas
# ------------------------------------------------------------

def compute_statistics(

    observables,
    dt,
    K=None

):

    if K is None:

        K = len(observables["Rloc"])

    data = {}

    for key in observables:

        data[key] = np.asarray(
            observables[key]
        )[-K:]


    delta_PR = np.abs(
        data["Hshape"]
    ) * dt


    P = persistence_score(

        data["Rloc"],

        data["Dspec"],

        delta_PR,

        data["Cauto"],

        dt

    )


    statistics = {

        "mean_Rloc":
            np.mean(data["Rloc"]),

        "mean_Dspec":
            np.mean(data["Dspec"]),

        "mean_delta_PR":
            np.mean(delta_PR),

        "var_Rloc":
            np.var(data["Rloc"]),

        "var_Dspec":
            np.var(data["Dspec"]),

        "slope_Rmacro":
            linear_slope(data["Rmacro"]),

        "slope_Cauto":
            linear_slope(data["Cauto"]),

        "slope_entropy":
            linear_slope(data["entropy"]),

        "mean_P":
            np.mean(P),

        "var_P":
            np.var(P)

    }

    return statistics, P


# ------------------------------------------------------------
# Classificador
# ------------------------------------------------------------

def classify_regime(

    statistics,

    epsilon=1e-8

):

    if (

        statistics["mean_Dspec"] < epsilon

        and

        statistics["mean_delta_PR"] < epsilon

        and

        statistics["mean_P"] > 0.99

    ):

        return "PERSISTENTE"


    if (

        statistics["mean_delta_PR"] > epsilon

        and

        statistics["slope_Cauto"] < -epsilon

    ):

        return "TRANSITORIO"


    if (

        statistics["var_Dspec"] > epsilon

    ):

        return "OSCILATORIO"


    if (

        statistics["var_Rloc"] > 1.0

    ):

        return "INSTAVEL"


    return "TRANSITORIO"


# ------------------------------------------------------------
# API Pública
# ------------------------------------------------------------

def run_stationary_scan(

    observables,

    dt,

    K=None,

    epsilon=1e-8

):

    statistics, P = compute_statistics(

        observables,

        dt,

        K

    )

    regime = classify_regime(

        statistics,

        epsilon

    )

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
