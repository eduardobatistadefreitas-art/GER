# ============================================================
# GER
# S26-B37-7
#
# Distribution Robustness
#
# Objetivo:
#
# Investigar se a métrica euclidiana normalizada
# permanece geometricamente equilibrada quando as
# Assinaturas Geométricas deixam de ser geradas por
# distribuições uniformes.
#
# Este experimento reutiliza exatamente o protocolo
# do S26-B37-6, alterando apenas o mecanismo de
# geração das assinaturas.
# ============================================================

import random
import math


# ============================================================
# Configuração
# ============================================================

DEFAULT_SAMPLES = 1000


# ============================================================
# Assinaturas Não Uniformes
# ============================================================

def generate_signature():

    return {

        # Uniforme

        "diameter": random.uniform(
            1.0,
            100.0,
        ),

        # Log-normal

        "convergence": random.lognormvariate(
            8.0,
            0.5,
        ),

        # Beta

        "recurrence": random.betavariate(
            2.0,
            5.0,
        ),

        # Exponencial truncada

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
# Faixas
# ============================================================

def compute_ranges(dataset):

    ranges = {}

    for key in [

        "diameter",

        "convergence",

        "recurrence",

        "drift",

    ]:

        values = [

            s[key]

            for s in dataset

        ]

        ranges[key] = (

            min(values),

            max(values),

        )

    return ranges
  # ============================================================
# Experimento
# ============================================================

def run_distribution_robustness(
    samples=DEFAULT_SAMPLES,
):

    dataset = generate_dataset(samples)

    ranges = compute_ranges(dataset)

    sums = {

        "diameter": 0.0,

        "convergence": 0.0,

        "recurrence": 0.0,

        "drift": 0.0,

    }

    pairs = 0

    for i in range(len(dataset)):

        for j in range(i + 1, len(dataset)):

            normalized = {}

            total = 0.0

            for key in [

                "diameter",

                "convergence",

                "recurrence",

                "drift",

            ]:

                minimum, maximum = ranges[key]

                scale = maximum - minimum

                if scale == 0:

                    value = 0.0

                else:

                    delta = (

                        dataset[i][key]

                        -

                        dataset[j][key]

                    ) / scale

                    value = delta ** 2

                normalized[key] = value

                total += value

            if total == 0:

                continue

            for key in normalized:

                sums[key] += (

                    normalized[key]

                    /

                    total

                )

            pairs += 1

    means = {}

    for key in sums:

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

    print("S26-B37-7")

    print("DISTRIBUTION ROBUSTNESS")

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

        print("Normalized metric appears robust under")
        print("distribution changes.")

    else:

        print("Conclusion:")

        print("Distribution significantly affects")
        print("the induced geometry.")

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main(

    samples=DEFAULT_SAMPLES,

):

    results = run_distribution_robustness(

        samples=samples,

    )

    print_report(

        results,

    )


# ============================================================

if __name__ == "__main__":

    main()
