# ============================================================
# GER
# S26-B37-8
#
# Ordinal Geometry
#
# Objetivo:
#
# Investigar se a geometria do espaço das Assinaturas
# depende da ordem relativa dos Operadores Geométricos
# Fundamentais, em vez de seus valores absolutos.
#
# Neste experimento cada componente da assinatura é
# substituída por seu rank dentro do conjunto de dados.
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

        "convergence": random.lognormvariate(
            8.0,
            0.5,
        ),

        "recurrence": random.betavariate(
            2.0,
            5.0,
        ),

        "drift": min(

            random.expovariate(
                2.0,
            ),

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
# Conversão para Geometria Ordinal
# ============================================================

def build_rank_dataset(dataset):

    rank_dataset = [

        dict(signature)

        for signature in dataset

    ]

    keys = [

        "diameter",

        "convergence",

        "recurrence",

        "drift",

    ]

    n = len(dataset)

    for key in keys:

        ordering = sorted(

            range(n),

            key=lambda i: dataset[i][key]

        )

        for rank, index in enumerate(ordering):

            rank_dataset[index][key] = rank / (n - 1)

    return rank_dataset
  # ============================================================
# Experimento
# ============================================================

def run_ordinal_geometry(
    samples=DEFAULT_SAMPLES,
):

    dataset = generate_dataset(samples)

    dataset = build_rank_dataset(dataset)

    sums = {

        "diameter": 0.0,

        "convergence": 0.0,

        "recurrence": 0.0,

        "drift": 0.0,

    }

    pairs = 0

    keys = [

        "diameter",

        "convergence",

        "recurrence",

        "drift",

    ]

    n = len(dataset)

    for i in range(n):

        for j in range(i + 1, n):

            components = {}

            total = 0.0

            for key in keys:

                value = (

                    dataset[i][key]

                    -

                    dataset[j][key]

                ) ** 2

                components[key] = value

                total += value

            if total == 0.0:

                continue

            for key in keys:

                sums[key] += (

                    components[key]

                    /

                    total

                )

            pairs += 1

    means = {}

    for key in keys:

        means[key] = (

            sums[key]

            /

            pairs

        )

    return {

        "samples": samples,

        "pairs": pairs,

        "means": means,

    }
  # ============================================================
# Impressão
# ============================================================

def print_report(results):

    print("=" * 60)

    print("S26-B37-8")

    print("ORDINAL GEOMETRY")

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

    spread = (

        max(means.values())

        -

        min(means.values())

    ) * 100.0

    print("-" * 60)

    print("Global Dominant OGF")

    print("-" * 60)

    print(dominant)

    print()

    print(f"Contribution spread : {spread:.2f} %")

    print()

    if spread < 5.0:

        print("Conclusion:")

        print("Ordinal geometry appears")

        print("distribution robust.")

    else:

        print("Conclusion:")

        print("Ordinal geometry still")

        print("depends on the dataset.")

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main(

    samples=DEFAULT_SAMPLES,

):

    results = run_ordinal_geometry(

        samples=samples,

    )

    print_report(

        results,

    )


# ============================================================

if __name__ == "__main__":

    main()
