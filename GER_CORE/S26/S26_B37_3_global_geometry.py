# ============================================================
# GER
# S26-B37-3
#
# Global Geometry Analysis
#
# Objetivo:
#
# Caracterizar estatisticamente a geometria global
# do espaço das Assinaturas Geométricas.
#
# O experimento acumula as contribuições dos quatro
# Operadores Geométricos Fundamentais sobre todos
# os pares de assinaturas.
# ============================================================

import random
import math


# ============================================================
# Configuração
# ============================================================

DEFAULT_SAMPLES = 1000


# ============================================================
# Geração das Assinaturas
# ============================================================

def generate_signature():

    return {

        "diameter": random.uniform(
            1.0,
            100.0,
        ),

        "convergence": random.uniform(
            0.0,
            10000.0,
        ),

        "recurrence": random.uniform(
            0.0,
            1.0,
        ),

        "drift": random.uniform(
            0.0,
            1.0,
        ),

    }


def generate_dataset(
    samples=DEFAULT_SAMPLES,
):

    return [

        generate_signature()

        for _ in range(samples)

    ]


# ============================================================
# Componentes da Distância
# ============================================================

def distance_components(
    a,
    b,
):

    diameter = (

        a["diameter"]

        -

        b["diameter"]

    ) ** 2

    convergence = (

        a["convergence"]

        -

        b["convergence"]

    ) ** 2

    recurrence = (

        a["recurrence"]

        -

        b["recurrence"]

    ) ** 2

    drift = (

        a["drift"]

        -

        b["drift"]

    ) ** 2

    return {

        "diameter": diameter,

        "convergence": convergence,

        "recurrence": recurrence,

        "drift": drift,

    }
  # ============================================================
# Experimento
# ============================================================

def run_global_geometry(
    samples=DEFAULT_SAMPLES,
):

    dataset = generate_dataset(samples)

    sums = {

        "diameter": 0.0,

        "convergence": 0.0,

        "recurrence": 0.0,

        "drift": 0.0,

    }

    sums2 = {

        "diameter": 0.0,

        "convergence": 0.0,

        "recurrence": 0.0,

        "drift": 0.0,

    }

    pairs = 0

    for i in range(len(dataset)):

        for j in range(i + 1, len(dataset)):

            components = distance_components(

                dataset[i],

                dataset[j],

            )

            total = (

                components["diameter"]

                +

                components["convergence"]

                +

                components["recurrence"]

                +

                components["drift"]

            )

            if total == 0:

                continue

            for key in components:

                value = (

                    components[key]

                    /

                    total

                )

                sums[key] += value

                sums2[key] += value ** 2

            pairs += 1

    means = {}

    variances = {}

    for key in sums:

        means[key] = sums[key] / pairs

        variances[key] = (

            sums2[key] / pairs

            -

            means[key] ** 2

        )

    return {

        "samples": samples,

        "pairs": pairs,

        "means": means,

        "variances": variances,

    }
  # ============================================================
# Impressão
# ============================================================

def print_report(results):

    print("=" * 60)

    print("S26-B37-3")

    print("GLOBAL GEOMETRY ANALYSIS")

    print("=" * 60)

    print()

    print(f"Generated signatures : {results['samples']}")

    print(f"Pairs analysed       : {results['pairs']}")

    print()

    print("-" * 60)

    print("Mean Relative Contribution")

    print("-" * 60)

    means = results["means"]

    print(f"Diameter     : {100.0 * means['diameter']:.2f} %")

    print(f"Convergence  : {100.0 * means['convergence']:.2f} %")

    print(f"Recurrence   : {100.0 * means['recurrence']:.2f} %")

    print(f"Drift        : {100.0 * means['drift']:.2f} %")

    print()

    dominant = max(

        means,

        key=means.get,

    )

    print("-" * 60)

    print("Global Dominant OGF")

    print("-" * 60)

    print(dominant)

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main(

    samples=DEFAULT_SAMPLES,

):

    results = run_global_geometry(

        samples=samples,

    )

    print_report(results)


# ============================================================

if __name__ == "__main__":

    main()
