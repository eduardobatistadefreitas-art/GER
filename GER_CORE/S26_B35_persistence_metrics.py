%%writefile GER_CORE/S26_B35_persistence_metrics.py

import numpy as np


# ============================================================
# S26-B35
# Persistence Metrics
# Observatório de estados persistentes
# ============================================================


def temporal_residual(gamma_t, gamma_next, dt):
    """
    Mede a variação temporal normalizada do campo.

    R_gamma -> 0 indica baixa evolução instantânea.
    """

    numerator = np.linalg.norm(
        gamma_next - gamma_t
    )

    denominator = (
        dt *
        np.linalg.norm(gamma_t)
        + 1e-15
    )

    return numerator / denominator



def finite_difference(values, dt):
    """
    Derivada temporal discreta.
    """

    values = np.asarray(values)

    return np.gradient(
        values,
        dt
    )



def persistence_derivatives(
    entropy,
    width,
    amplitude,
    participation,
    dt
):
    """
    Calcula taxas de variação das métricas espectrais.
    """

    return {

        "d_entropy_dt":
            finite_difference(
                entropy,
                dt
            ),

        "d_width_dt":
            finite_difference(
                width,
                dt
            ),

        "d_amplitude_dt":
            finite_difference(
                amplitude,
                dt
            ),

        "d_PR_dt":
            finite_difference(
                participation,
                dt
            )
    }



def autocorrelation(
    gamma_history,
    lag
):
    """
    Autocorrelação temporal do campo.

    Valores próximos de 1:
    forte persistência.

    Oscilações:
    possível regime periódico.
    """

    gamma_history = np.asarray(
        gamma_history
    )

    if lag >= len(gamma_history):
        return np.nan


    x = gamma_history[:-lag]
    y = gamma_history[lag:]


    numerator = np.mean(
        x * y
    )

    denominator = (
        np.mean(x*x)
        + 1e-15
    )

    return numerator / denominator



def stationary_score(
    residual,
    d_entropy,
    d_width,
    tolerance=1e-3
):
    """
    Classificador neutro.

    Não identifica fenômenos.
    Apenas organiza regimes.
    """

    residual_small = (
        np.mean(np.abs(residual))
        < tolerance
    )

    entropy_small = (
        np.mean(np.abs(d_entropy))
        < tolerance
    )

    width_small = (
        np.mean(np.abs(d_width))
        < tolerance
    )


    if (
        residual_small
        and entropy_small
        and width_small
    ):

        return "PERSISTENT_CANDIDATE"


    elif (
        entropy_small
        and width_small
    ):

        return "STATISTICAL_STABILITY"


    elif not np.isnan(
        np.mean(residual)
    ):

        return "TRANSIENT"


    else:

        return "UNSTABLE"



def summarize_persistence(
    residual,
    derivatives
):
    """
    Resumo automático da auditoria.
    """

    return {

        "mean_R_gamma":
            np.mean(
                residual
            ),

        "max_R_gamma":
            np.max(
                residual
            ),

        "mean_dS":
            np.mean(
                np.abs(
                    derivatives[
                        "d_entropy_dt"
                    ]
                )
            ),

        "mean_dW":
            np.mean(
                np.abs(
                    derivatives[
                        "d_width_dt"
                    ]
                )
            ),

        "mean_dA":
            np.mean(
                np.abs(
                    derivatives[
                        "d_amplitude_dt"
                    ]
                )
            ),

        "mean_dPR":
            np.mean(
                np.abs(
                    derivatives[
                        "d_PR_dt"
                    ]
                )
            )

    }



def print_persistence_report(
    summary,
    classification
):

    print("\n")
    print("="*50)
    print("PERSISTENCE AUDIT")
    print("="*50)

    for key, value in summary.items():

        print(
            f"{key}: {value:.6e}"
        )


    print("\nCLASSIFICATION:")
    print(
        classification
    )

    print("="*50)
