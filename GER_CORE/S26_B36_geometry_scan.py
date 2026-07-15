import numpy as np
import csv
import os

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)
from GER.CORE.signature_api import Signature

# ============================================================
# GER
# S26-B36
#
# Geometry Scan
#
# Este módulo NÃO classifica regimes.
#
# Ele mede propriedades geométricas da trajetória
# produzida pelo observatório B35.
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


# ============================================================
# Construção da trajetória
# ============================================================

def build_trajectory(observables):

    return np.column_stack([

        np.asarray(observables["Rloc"], dtype=float),

        np.asarray(observables["Dspec"], dtype=float),

        np.asarray(observables["Hshape"], dtype=float),

        np.asarray(observables["Cauto"], dtype=float),

        np.asarray(observables["Rmacro"], dtype=float),

        np.asarray(observables["entropy"], dtype=float),

    ])


# ============================================================
# Operador 1
# Confinamento
# ============================================================

def compute_confinement(trajectory):

    n = len(trajectory)

    if n < 2:
        return 0.0

    diameter = 0.0

    for i in range(n):

        for j in range(i + 1, n):

            d = np.linalg.norm(
                trajectory[i] - trajectory[j]
            )

            if d > diameter:
                diameter = d

    return diameter


# ============================================================
# Operador 2
# Convergência
# ============================================================

def compute_convergence(trajectory, dt):

    if len(trajectory) < 2:
        return 0.0

    steps = np.diff(
        trajectory,
        axis=0,
    )

    speeds = np.linalg.norm(
        steps,
        axis=1,
    )

    return np.mean(speeds) / dt


# ============================================================
# Operador 3
# Recorrência
# ============================================================

def compute_recurrence(
    trajectory,
    epsilon=None,
):

    n = len(trajectory)

    if n < 2:
        return 0.0

    if epsilon is None:

        epsilon = 0.05 * np.std(trajectory)

    count = 0
    total = 0

    for i in range(n):

        for j in range(i + 1, n):

            total += 1

            d = np.linalg.norm(
                trajectory[i] - trajectory[j]
            )

            if d < epsilon:

                count += 1

    if total == 0:
        return 0.0

    return count / total


# ============================================================
# Operador 4
# Deriva
# ============================================================

def compute_drift(trajectory):

    if len(trajectory) < 2:

        return 0.0, 0.0

    displacement = np.linalg.norm(

        trajectory[-1] - trajectory[0]

    )

    steps = np.diff(
        trajectory,
        axis=0,
    )

    trajectory_length = np.sum(

        np.linalg.norm(
            steps,
            axis=1,
        )

    )

    if trajectory_length == 0:

        drift = 0.0

    else:

        drift = displacement / trajectory_length

    return drift, trajectory_length

# ============================================================
# Scan geométrico
# ============================================================

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

                except Exception as exc:

                    print(
                        f"[GeometryScan] "
                        f"beta={beta} "
                        f"sigma={sigma} "
                        f"potential={potential} "
                        f"{type(exc).__name__}: {exc}"
                    )

                    continue

                observables = run_persistence_observatory(
                    result["snapshots"],
                    result["configuration"]["dt"],
                )
                )

                trajectory = build_trajectory(
                    observables
                )

                diameter = compute_confinement(
                    trajectory
                )

                convergence = compute_convergence(
                    trajectory,
                    result["configuration"]["dt"],
                )

                recurrence = compute_recurrence(
                    trajectory
                )

                drift, trajectory_length = compute_drift(
                    trajectory
                )
                signature = Signature(

    diameter=diameter,

    convergence=convergence,

    recurrence=recurrence,

    drift=drift,

                )

                results.append({

    "simulation_id": len(results),

    "beta": beta,

    "sigma": sigma,

    "potential": potential,

    "dt": result["configuration"]["dt"],

    "window_size": len(trajectory),

    "diameter": diameter,

    "convergence": convergence,

    "recurrence": recurrence,

    "drift": drift,

    "trajectory_length": trajectory_length,

                    "signature": signature,

})

    return results

# ============================================================
# API pública
# ============================================================

def generate_signature_dataset(
    *args,
    **kwargs,
):

    results = run_geometry_scan(
        *args,
        **kwargs,
    )

    return [

        row["signature"]

        for row in results

    ]


def generate_signature(
    *args,
    **kwargs,
):

    signatures = generate_signature_dataset(
        *args,
        **kwargs,
    )

    if not signatures:

        raise RuntimeError(
            "No signatures generated."
        )

    return signatures[0]
# ============================================================
# Impressão
# ============================================================

def print_table(results):

    if not results:

        print("Nenhum resultado.")
        return

    columns = list(results[0].keys())

    print(",".join(columns))

    for row in results:

        print(

            ",".join(

                str(row[c])

                for c in columns

            )

        )


# ============================================================
# CSV
# ============================================================

def save_csv(
    results,
    filename="RESULTS/S26_B36_geometry_scan.csv",
):

    if not results:

        print("Nenhum resultado.")
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


# ============================================================
# Execução direta
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("GER — S26-B36 Geometry Scan")
    print("=" * 70)

    table = run_geometry_scan()

    print_table(table)

    save_csv(table)

    print()

    print(f"Simulações executadas: {len(table)}")

    print("=" * 70)
