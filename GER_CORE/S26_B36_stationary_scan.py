%%writefile GER_CORE/S26_B36_stationary_scan.py

import numpy as np

from GER_CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_metrics import (
    temporal_residual,
    persistence_derivatives,
    autocorrelation,
    summarize_persistence
)


# ============================================================
# S26-B36
# Stationary Scan
# Busca inicial de regimes persistentes
# ============================================================


def run_stationary_scan(
    betas,
    steps=2000,
    dt=1e-4
):
    """
    Executa varredura de persistência
    em regimes conhecidos de beta.
    """

    results = {}


    for beta in betas:

        print("\n")
        print("="*50)
        print(f"BETA = {beta}")
        print("="*50)


        output = run_engine(
            beta=beta,
            steps=steps,
            dt=dt,
            return_history=True
        )


        gamma_history = np.asarray(
            output["gamma_history"]
        )


        entropy = np.asarray(
            output["entropy"]
        )

        width = np.asarray(
            output["width"]
        )

        amplitude = np.asarray(
            output["amplitude"]
        )

        PR = np.asarray(
            output["PR"]
        )


        residual = []


        for i in range(
            len(gamma_history)-1
        ):

            residual.append(
                temporal_residual(
                    gamma_history[i],
                    gamma_history[i+1],
                    dt
                )
            )


        residual = np.asarray(
            residual
        )


        derivatives = persistence_derivatives(
            entropy,
            width,
            amplitude,
            PR,
            dt
        )


        summary = summarize_persistence(
            residual,
            derivatives
        )


        auto = autocorrelation(
            gamma_history,
            lag=100
        )


        summary["autocorrelation"] = auto


        results[beta] = summary


        print(
            f"mean R_gamma = "
            f"{summary['mean_R_gamma']:.6e}"
        )

        print(
            f"mean |dS/dt| = "
            f"{summary['mean_dS']:.6e}"
        )

        print(
            f"mean |dW/dt| = "
            f"{summary['mean_dW']:.6e}"
        )

        print(
            f"R_auto(100) = "
            f"{auto:.6e}"
        )


    return results



def print_stationary_scan(
    results
):

    print("\n")
    print("="*60)
    print("PERSISTENCE SCAN")
    print("="*60)


    for beta, data in results.items():

        print("\n")
        print(
            f"β={beta}"
        )

        for key,value in data.items():

            print(
                f"{key}: {value:.6e}"
            )
