%%writefile GER_CORE/S26_B36_2_classifier_robustness.py

import numpy as np


# ============================================================
# GER
# S26-B36-2
#
# Classifier Robustness
#
# Auditoria de estabilidade da classificação.
#
# Não altera o classificador.
# Apenas testa sensibilidade:
#
# - epsilon
# - janela K
# - passo temporal dt
#
# ============================================================


from GER_CORE.S26_B36_stationary_scan import (
    run_stationary_scan
)



# ------------------------------------------------------------
# Uma execução de teste
# ------------------------------------------------------------

def run_single_test(
    observables,
    dt,
    K,
    epsilon
):

    result = run_stationary_scan(
        observables,
        dt=dt,
        K=K,
        epsilon=epsilon
    )

    return {

        "regime":
            result["regime"],

        "persistence":
            result["persistence_score"],

        "variance":
            result["persistence_variance"]

    }



# ------------------------------------------------------------
# Robustez em epsilon
# ------------------------------------------------------------

def epsilon_robustness(
    observables,
    dt,
    K
):

    epsilons = [

        1e-2,
        1e-3,
        1e-4,
        1e-5,
        1e-6,
        1e-8

    ]

    results = []


    for eps in epsilons:

        test = run_single_test(
            observables,
            dt,
            K,
            eps
        )

        test["epsilon"] = eps

        results.append(test)


    return results



# ------------------------------------------------------------
# Robustez em janela temporal
# ------------------------------------------------------------

def window_robustness(
    observables,
    dt,
    epsilon
):

    total = len(
        observables["Rloc"]
    )


    windows = [

        total,

        max(2, total//2),

        max(2, total//3)

    ]


    results = []


    for K in windows:

        test = run_single_test(
            observables,
            dt,
            K,
            epsilon
        )

        test["K"] = K

        results.append(test)


    return results



# ------------------------------------------------------------
# Robustez principal
# ------------------------------------------------------------

def run_classifier_robustness(
    observables,
    dt,
    K=None,
    epsilon=1e-8
):


    if K is None:

        K = len(
            observables["Rloc"]
        )


    base = run_single_test(
        observables,
        dt,
        K,
        epsilon
    )


    eps_scan = epsilon_robustness(
        observables,
        dt,
        K
    )


    window_scan = window_robustness(
        observables,
        dt,
        epsilon
    )


    regimes = [

        x["regime"]

        for x in eps_scan

    ] + [

        x["regime"]

        for x in window_scan

    ]


    persistence = np.array([

        x["persistence"]

        for x in eps_scan

    ] + [

        x["persistence"]

        for x in window_scan

    ])


    return {

        "base": base,

        "epsilon_scan":
            eps_scan,

        "window_scan":
            window_scan,


        "regime_changes":
            len(set(regimes)),


        "persistence_mean":
            np.mean(
                persistence
            ),


        "persistence_std":
            np.std(
                persistence
            )

    }



# ------------------------------------------------------------
# Impressão
# ------------------------------------------------------------

def print_classifier_report(
    report
):

    print(
        "\n===== S26-B36-2 CLASSIFIER ROBUSTNESS ====="
    )


    print(
        "\nBase:"
    )

    print(
        report["base"]
    )


    print(
        "\nEpsilon scan:"
    )

    for r in report["epsilon_scan"]:

        print(
            "eps=",
            r["epsilon"],
            "|",
            r["regime"],
            "| P=",
            r["persistence"]
        )


    print(
        "\nWindow scan:"
    )

    for r in report["window_scan"]:

        print(
            "K=",
            r["K"],
            "|",
            r["regime"],
            "| P=",
            r["persistence"]
        )


    print(
        "\nMudanças de regime:",
        report["regime_changes"]
    )


    print(
        "Persistência média:",
        report["persistence_mean"]
    )


    print(
        "Persistência desvio:",
        report["persistence_std"]
    )
