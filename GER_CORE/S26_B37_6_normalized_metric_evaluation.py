# ============================================================
# GER
# S26-B37-6
#
# Normalized Metric Evaluation
#
# Objetivo:
#
# Avaliar experimentalmente a geometria global
# induzida pela distância euclidiana normalizada.
#
# A infraestrutura é idêntica ao S26-B37-3.
# A única diferença é a métrica utilizada.
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
# Faixas de Normalização
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

            signature[key]

            for signature in dataset

        ]

        ranges[key] = (

            min(values),

            max(values),

        )

    return ranges
  # ============================================================
# Experimento
# ============================================================

def run_normalized_geometry(
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

                    value = (

                        (

                            dataset[i][key]

                            -

                            dataset[j][key]

                        )

                        /

                        scale

                    ) ** 2

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

    print("S26-B37-6")

    print("NORMALIZED METRIC EVALUATION")

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

    results = run_normalized_geometry(

        samples=samples,

    )

    print_report(

        results,

    )


# ============================================================

if __name__ == "__main__":

    main()
