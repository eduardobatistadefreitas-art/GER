import numpy as np
import csv
import os

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER.CORE.signature_api import Signature


# ============================================================
# GER
# S26-B36
#
# Geometry Scan
#
# Official Geometry Signature Generator
#
# Este módulo NÃO classifica regimes.
#
# Sua única responsabilidade é construir
# Assinaturas Geométricas a partir da trajetória
# produzida pelo Observatório B35.
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

    return np.column_stack(

        [

            np.asarray(
                observables["Rloc"],
                dtype=float,
            ),

            np.asarray(
                observables["Dspec"],
                dtype=float,
            ),

            np.asarray(
                observables["Hshape"],
                dtype=float,
            ),

            np.asarray(
                observables["Cauto"],
                dtype=float,
            ),

            np.asarray(
                observables["Rmacro"],
                dtype=float,
            ),

            np.asarray(
                observables["entropy"],
                dtype=float,
            ),

        ]

    )


# ============================================================
# Operador Geométrico
#
# Diameter
# ============================================================

def compute_diameter(
    trajectory,
):

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


# ------------------------------------------------------------
# Compatibilidade retroativa
# ------------------------------------------------------------

compute_confinement = compute_diameter


# ============================================================
# Operador Geométrico
#
# Convergence
# ============================================================

def compute_convergence(
    trajectory,
    dt,
):

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

    return np.mean(
        speeds
    ) / dt


# ============================================================
# Operador Geométrico
#
# Recurrence
# ============================================================

def compute_recurrence(
    trajectory,
    epsilon=None,
):

    n = len(trajectory)

    if n < 2:
        return 0.0

    if epsilon is None:

        epsilon = (
            0.05 * np.std(trajectory)
        )

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
# Operador Geométrico
#
# Drift
# ============================================================

def compute_drift(
    trajectory,
):

    if len(trajectory) < 2:

        return 0.0, 0.0

    displacement = np.linalg.norm(

        trajectory[-1]
        - trajectory[0]

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

        drift = (
            displacement
            / trajectory_length
        )

    return drift, trajectory_length


# ============================================================
# API Pública
#
# Geração de uma Assinatura
# ============================================================

def generate_signature(
    snapshots,
    dt,
):

    observables = run_persistence_observatory(
        snapshots,
        dt,
    )

    trajectory = build_trajectory(
        observables
    )

    diameter = compute_diameter(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        dt,
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

    return (
        signature,
        trajectory_length,
    )

# ============================================================
# API Pública
#
# Geração de um conjunto de Assinaturas
# ============================================================

def generate_signature_dataset(
    betas=None,
    sigmas=None,
    potentials=None,
    timesteps=2000,
    dt=2.5e-4,
):

    return run_geometry_scan(
        betas=betas,
        sigmas=sigmas,
        potentials=potentials,
        timesteps=timesteps,
        dt=dt,
    )


# ============================================================
# Scan Geométrico
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

    simulation_id = 0

    total = (
        len(betas)
        * len(sigmas)
        * len(potentials)
    )

    print()
    print("=" * 70)
    print("GER — Geometry Scan")
    print("=" * 70)
    print(f"Simulações previstas : {total}")
    print()

    for beta in betas:

        for sigma in sigmas:

            for potential in potentials:

                print(
                    f"[{simulation_id + 1:03d}/{total:03d}] "
                    f"beta={beta} "
                    f"sigma={sigma} "
                    f"potential={potential}"
                )

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
                        f"   ERRO: "
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    )

                    continue

                signature, trajectory_length = (
                    generate_signature(
                        result["snapshots"],
                        result["configuration"]["dt"],
                    )
                )

                results.append(

                    {

                        "simulation_id": simulation_id,

                        "beta": beta,

                        "sigma": sigma,

                        "potential": potential,

                        "dt": result["configuration"]["dt"],

                        "window_size": len(
                            result["snapshots"]
                        ),

                        "diameter": signature.diameter,

                        "convergence": signature.convergence,

                        "recurrence": signature.recurrence,

                        "drift": signature.drift,

                        "trajectory_length": trajectory_length,

                        "signature": signature,

                    }

                )

                simulation_id += 1

    print()
    print("=" * 70)
    print(
        f"Geometry Scan concluído "
        f"({len(results)} assinaturas)"
    )
    print("=" * 70)

    return results

# ============================================================
# Impressão
# ============================================================

def print_table(results):

    if not results:

        print("Nenhum resultado.")
        return

    columns = [

        "simulation_id",

        "beta",

        "sigma",

        "potential",

        "dt",

        "window_size",

        "diameter",

        "convergence",

        "recurrence",

        "drift",

        "trajectory_length",

    ]

    print(",".join(columns))

    for row in results:

        values = []

        for column in columns:

            values.append(str(row[column]))

        print(",".join(values))


# ============================================================
# Exportação CSV
# ============================================================

def save_csv(
    results,
    filename="RESULTS/S26_B36_geometry_scan.csv",
):

    if not results:

        print("Nenhum resultado.")
        return

    directory = os.path.dirname(filename)

    if directory:

        os.makedirs(
            directory,
            exist_ok=True,
        )

    columns = [

        "simulation_id",

        "beta",

        "sigma",

        "potential",

        "dt",

        "window_size",

        "diameter",

        "convergence",

        "recurrence",

        "drift",

        "trajectory_length",

    ]

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

        for row in results:

            writer.writerow(

                {

                    key: row[key]

                    for key in columns

                }

            )

    print()
    print(f"CSV salvo em: {filename}")


# ============================================================
# Resumo Executivo
# ============================================================

def print_summary(results):

    print()
    print("=" * 70)
    print("Resumo")
    print("=" * 70)

    print(
        f"Assinaturas geradas : {len(results)}"
    )

    if results:

        print(
            f"Betas              : "
            f"{sorted(set(r['beta'] for r in results))}"
        )

        print(
            f"Sigmas             : "
            f"{sorted(set(r['sigma'] for r in results))}"
        )

        print(
            f"Potenciais         : "
            f"{sorted(set(r['potential'] for r in results))}"
        )

    print("=" * 70)


# ============================================================
# Execução direta
# ============================================================

def main():

    print("=" * 70)
    print("GER")
    print("S26-B36")
    print("Geometry Scan")
    print("=" * 70)

    results = run_geometry_scan()

    print()

    print_table(results)

    save_csv(results)

    print_summary(results)


# ============================================================

if __name__ == "__main__":

    main()
