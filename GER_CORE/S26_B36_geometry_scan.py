import numpy as np

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

# ============================================================
# GER
# S26-B36
#
# Geometry Scan
#
# Este módulo NÃO classifica regimes.
#
# Seu objetivo é medir propriedades geométricas
# da trajetória produzida pelo observatório B35.
#
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
# Construção da trajetória
# ------------------------------------------------------------

def build_trajectory(observables):

    """
    Constrói a trajetória da dinâmica no espaço
    de observação do B35.

    Cada linha corresponde a um instante.

    Colunas:

        Rloc
        Dspec
        Hshape
        Cauto
        Rmacro
        entropy
    """

    return np.column_stack(

        [

            np.asarray(observables["Rloc"], dtype=float),

            np.asarray(observables["Dspec"], dtype=float),

            np.asarray(observables["Hshape"], dtype=float),

            np.asarray(observables["Cauto"], dtype=float),

            np.asarray(observables["Rmacro"], dtype=float),

            np.asarray(observables["entropy"], dtype=float),

        ]

    )


# ------------------------------------------------------------
# Interface principal
# ------------------------------------------------------------

def run_geometry_scan(

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

                trajectory = build_trajectory(
                    observables
                )

                results.append({

                    "beta": beta,

                    "sigma": sigma,

                    "potential": potential,

                    "trajectory": trajectory,

                    "observables": observables,

                })

    return results
