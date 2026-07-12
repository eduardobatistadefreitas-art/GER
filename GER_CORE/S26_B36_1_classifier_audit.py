import numpy as np


# ============================================================
# S26-B36.1
# Classificador de Regimes Dinâmicos
#
# Auditoria do Stationary Scan
#
# Entrada:
# observáveis B35
#
# Saída:
# regime matemático
# persistence score
# estatísticas
# ============================================================


def linear_slope(values):

    values = np.asarray(values)

    x = np.arange(len(values))

    if len(values) < 2:
        return 0.0

    return np.polyfit(
        x,
        values,
        1
    )[0]



def compute_persistence(
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



def classify_regime(
    obs,
    dt,
    K=None
):

    if K is None:
        K = len(obs["Rloc"])


    Rloc = np.asarray(
        obs["Rloc"][-K:]
    )

    Dspec = np.asarray(
        obs["Dspec"][-K:]
    )

    Hshape = np.asarray(
        obs["Hshape"][-K:]
    )

    Cauto = np.asarray(
        obs["Cauto"][-K:]
    )

    Rmacro = np.asarray(
        obs["Rmacro"][-K:]
    )


    P = compute_persistence(
        Rloc,
        Dspec,
        Hshape,
        Cauto,
        dt
    )


    mean_P = np.mean(P)

    var_P = np.var(P)


    eps = 1e-6


    mean_Rloc = np.mean(Rloc)
    mean_Dspec = np.mean(Dspec)
    mean_Hshape = np.mean(
        np.abs(Hshape)
    )


    slope_Cauto = linear_slope(
        Cauto
    )

    slope_Rmacro = linear_slope(
        Rmacro
    )


    var_Rloc = np.var(Rloc)
    var_Dspec = np.var(Dspec)


    # ------------------------------------------------
    # Classificação hierárquica
    # ------------------------------------------------


    if (
        mean_P > 0.99
        and
        var_P < 1e-5
    ):

        regime = "PERSISTENTE"


    elif (
        mean_Rloc > eps
        and
        mean_Dspec > eps
        and
        slope_Cauto < -eps
    ):

        regime = "TRANSITORIO"


    elif (
        mean_Rloc > eps
        and
        var_Dspec > eps
    ):

        regime = "OSCILATORIO"


    elif (
        mean_Rloc > 1
        or
        var_Rloc > 1
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
        {

            "mean_Rloc":
                mean_Rloc,

            "mean_Dspec":
                mean_Dspec,

            "mean_Hshape":
                mean_Hshape,

            "var_Rloc":
                var_Rloc,

            "var_Dspec":
                var_Dspec,

            "slope_Rmacro":
                slope_Rmacro,

            "slope_Cauto":
                slope_Cauto,

            "mean_P":
                mean_P,

            "var_P":
                var_P

        },


        "persistence_history":
            P

    }
    
    # ============================================================
# API Pública Oficial do GER
# ============================================================

def run_classifier_audit(*args, **kwargs):
    """
    Interface pública oficial do Classifier Audit.

    Esta função constitui a API estável do framework GER.
    A implementação permanece encapsulada em
    `classify_regime()`, permitindo futuras alterações
    internas sem quebrar compatibilidade.
    """
    return classify_regime(*args, **kwargs)
