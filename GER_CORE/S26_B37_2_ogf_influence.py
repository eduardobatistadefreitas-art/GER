# ============================================================
# GER
# S26-B37-2
#
# OGF Influence Analysis
#
# Objetivo:
#
# Quantificar a contribuição individual de cada
# Operador Geométrico Fundamental para a distância
# entre Assinaturas Geométricas.
#
# Este experimento não altera o espaço das
# assinaturas. Apenas decompõe a distância em
# contribuições individuais.
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
# Distância Decomposta
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

    total = (

        diameter

        +

        convergence

        +

        recurrence

        +

        drift

    )

    return {

        "diameter": diameter,

        "convergence": convergence,

        "recurrence": recurrence,

        "drift": drift,

        "total": total,

    }
  # ============================================================
# Par Mais Próximo
# ============================================================

def nearest_pair(
    dataset,
):

    minimum_distance = None

    nearest = None

    nearest_components = None

    for i in range(len(dataset)):

        for j in range(i + 1, len(dataset)):

            components = distance_components(

                dataset[i],

                dataset[j],

            )

            distance = math.sqrt(

                components["total"]

            )

            if (

                minimum_distance is None

                or

                distance < minimum_distance

            ):

                minimum_distance = distance

                nearest = (

                    i,

                    j,

                )

                nearest_components = components

    return {

        "pair": nearest,

        "distance": minimum_distance,

        "components": nearest_components,

    }


# ============================================================
# Contribuições Relativas
# ============================================================

def relative_contributions(
    components,
):

    total = components["total"]

    if total == 0:

        return {

            "diameter": 0.0,

            "convergence": 0.0,

            "recurrence": 0.0,

            "drift": 0.0,

        }

    return {

        "diameter":

            100.0 * components["diameter"] / total,

        "convergence":

            100.0 * components["convergence"] / total,

        "recurrence":

            100.0 * components["recurrence"] / total,

        "drift":

            100.0 * components["drift"] / total,

    }


# ============================================================
# Experimento
# ============================================================

def run_ogf_influence(
    samples=DEFAULT_SAMPLES,
):

    dataset = generate_dataset(samples)

    nearest = nearest_pair(dataset)

    contributions = relative_contributions(

        nearest["components"]

    )

    return {

        "samples": samples,

        "nearest": nearest,

        "contributions": contributions,

    }
  # ============================================================
# Impressão
# ============================================================

def print_report(results):

    print("=" * 60)

    print("S26-B37-2")

    print("OGF INFLUENCE ANALYSIS")

    print("=" * 60)

    print()

    print(f"Generated signatures : {results['samples']}")

    print()

    nearest = results["nearest"]

    print(f"Nearest pair         : {nearest['pair']}")

    print(f"Distance             : {nearest['distance']:.12e}")

    print()

    print("-" * 60)

    print("Squared Contributions")

    print("-" * 60)

    components = nearest["components"]

    print(f"Diameter     : {components['diameter']:.12e}")

    print(f"Convergence  : {components['convergence']:.12e}")

    print(f"Recurrence   : {components['recurrence']:.12e}")

    print(f"Drift        : {components['drift']:.12e}")

    print()

    print("-" * 60)

    print("Relative Contributions (%)")

    print("-" * 60)

    contributions = results["contributions"]

    print(f"Diameter     : {contributions['diameter']:.2f} %")

    print(f"Convergence  : {contributions['convergence']:.2f} %")

    print(f"Recurrence   : {contributions['recurrence']:.2f} %")

    print(f"Drift        : {contributions['drift']:.2f} %")

    print()

    dominant = max(

        contributions,

        key=contributions.get,

    )

    print("-" * 60)

    print("Dominant OGF")

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

    results = run_ogf_influence(

        samples=samples,

    )

    print_report(results)


# ============================================================

if __name__ == "__main__":

    main()
