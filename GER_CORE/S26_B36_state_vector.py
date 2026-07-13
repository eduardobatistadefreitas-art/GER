import numpy as np

from GER.CORE.ger_engine import run_engine
from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


# ============================================================
# GER
# S26-B36
#
# State Vector Characterization
#
# Este módulo NÃO classifica regimes.
#
# Seu objetivo é caracterizar o espaço de estados
# produzido pelo motor atual do GER.
#
# A saída serve de base para a reconstrução científica
# do Stationary Scan.
# ============================================================


DEFAULT_BETAS = [
    0.1,
    0.2,
    0.5,
    1.0,
    2.0,
    5.0,
    10.0,
]


DEFAULT_SIGMAS = [
    0.05,
    0.10,
    0.20,
    0.50,
]


DEFAULT_POTENTIALS = [
    "A",
    "C",
]


# ------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------

def slope(values):

    values = np.asarray(values, dtype=float)

    if len(values) < 2:
        return 0.0

    x = np.arange(len(values))

    return np.polyfit(x, values, 1)[0]


def compute_persistence(observables, dt):

    Rloc = np.asarray(observables["Rloc"], dtype=float)
    Dspec = np.asarray(observables["Dspec"], dtype=float)
    Hshape = np.asarray(observables["Hshape"], dtype=float)
    Cauto = np.asarray(observables["Cauto"], dtype=float)

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


def compute_state_vector(observables, dt):

    state = {}

    names = [

        "Rloc",
        "Dspec",
        "Hshape",
        "Cauto",
        "Rmacro",
        "entropy",

    ]

    for name in names:

        values = np.asarray(
            observables[name],
            dtype=float,
        )

        state[f"mean_{name}"] = np.mean(values)

        state[f"var_{name}"] = np.var(values)

        state[f"slope_{name}"] = slope(values)

    P = compute_persistence(
        observables,
        dt,
    )

    state["mean_P"] = np.mean(P)

    state["var_P"] = np.var(P)

    return state
  # ------------------------------------------------------------
# Scan completo do espaço de estados
# ------------------------------------------------------------

def run_state_vector_scan(
    betas=None,
    sigmas=None,
    potentials=None,
    timesteps=2000,
    dt=2.5e-4,
):

    if betas is None:
        betas = DEFAULT_BETAS

    if sigmas is None:
        sigmas = DEFAULT_SIGMAS

    if potentials is None:
        potentials = DEFAULT_POTENTIALS

    results = []

    for beta in betas:

        for sigma in sigmas:

            for potential in potentials:

                try:

                    result = run_engine(
                        beta=beta,
                        sigma=sigma,
                        potential=potential,
                        timesteps=timesteps,
                        dt=dt,
                    )

                except Exception:

                    continue

                observables = run_persistence_observatory(
                    result["snapshots"],
                    result["configuration"]["dt"],
                )

                state = compute_state_vector(
                    observables,
                    result["configuration"]["dt"],
                )

                row = {
                    "beta": beta,
                    "sigma": sigma,
                    "potential": potential,
                }

                row.update(state)

                results.append(row)

    return results


# ------------------------------------------------------------
# Impressão em formato CSV
# ------------------------------------------------------------

def print_table(results):
    
import csv
import os


def save_csv(results, filename="RESULTS/S26_B36_state_vector.csv"):

    if not results:
        print("Nenhum resultado para salvar.")
        return

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True,
    )

    columns = list(results[0].keys())

    with open(
        filename,
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=columns,
        )

        writer.writeheader()

        writer.writerows(results)

    print(f"\nCSV salvo em: {filename}")
    if not results:
        print("Nenhum resultado.")
        return

    columns = list(results[0].keys())

    print(",".join(columns))

    for row in results:

        print(",".join(str(row[c]) for c in columns))


# ------------------------------------------------------------
# Execução direta
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("GER - S26-B36 STATE VECTOR")
    print("=" * 60)

    table = run_state_vector_scan()

print_table(table)

save_csv(table)

print("=" * 60)
print(f"Simulações executadas: {len(table)}")
print("=" * 60)
