# ============================================================
# GER
# S26-B37-1
#
# Metric Sensitivity
#
# Objetivo:
#
# Investigar se a geometria do espaço das
# Assinaturas Geométricas depende da métrica
# utilizada.
#
# Este experimento compara diferentes métricas
# utilizando exatamente o mesmo conjunto de
# assinaturas.
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


# ============================================================
# Geração do conjunto experimental
# ============================================================

def generate_dataset(
    samples=DEFAULT_SAMPLES,
):

    return [

        generate_signature()

        for _ in range(samples)

    ]


# ============================================================
# Métrica Euclidiana
# ============================================================

def euclidean_distance(a, b):

    return math.sqrt(

        (a["diameter"] - b["diameter"]) ** 2 +

        (a["convergence"] - b["convergence"]) ** 2 +

        (a["recurrence"] - b["recurrence"]) ** 2 +

        (a["drift"] - b["drift"]) ** 2

    )
  # ============================================================
# Estatísticas do conjunto
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
# Métrica Euclidiana Normalizada
# ============================================================

def normalized_distance(

    a,

    b,

    ranges,

):

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

            continue

        da = (

            a[key] - b[key]

        ) / scale

        total += da ** 2

    return math.sqrt(total)


# ============================================================
# Busca do par mais próximo
# ============================================================

def nearest_pair(

    dataset,

    distance_function,

    *args,

):

    minimum_distance = None

    pair = None

    comparisons = 0

    for i in range(len(dataset)):

        for j in range(i + 1, len(dataset)):

            d = distance_function(

                dataset[i],

                dataset[j],

                *args,

            )

            comparisons += 1

            if (

                minimum_distance is None

                or

                d < minimum_distance

            ):

                minimum_distance = d

                pair = (

    i,

    j,

)

    return {

        "distance": minimum_distance,

        "pair": pair,

        "comparisons": comparisons,
      
      "dataset": dataset,

    }


# ============================================================
# Experimento
# ============================================================

def run_metric_sensitivity(

    samples=DEFAULT_SAMPLES,

):

    dataset = generate_dataset(samples)

    ranges = compute_ranges(dataset)

    euclidean = nearest_pair(

        dataset,

        euclidean_distance,

    )

    normalized = nearest_pair(

        dataset,

        normalized_distance,

        ranges,

    )

    return {

        "samples": samples,

        "ranges": ranges,

        "euclidean": euclidean,

        "normalized": normalized,

    }
    # ============================================================
# Auditoria Estatística
# ============================================================

def run_metric_sensitivity_audit(
    repetitions=30,
    samples=DEFAULT_SAMPLES,
):

    identical = 0
    different = 0

    for _ in range(repetitions):

        results = run_metric_sensitivity(
            samples=samples,
        )

        if (
            results["euclidean"]["pair"]
            ==
            results["normalized"]["pair"]
        ):

            identical += 1

        else:

            different += 1

    return {

        "repetitions": repetitions,

        "samples": samples,

        "identical": identical,

        "different": different,

    }
  # ============================================================
# Impressão
# ============================================================

def print_report(results):

    print("=" * 60)

    print("S26-B37-1")

    print("METRIC SENSITIVITY")

    print("=" * 60)

    print()

    print(f"Generated signatures : {results['samples']}")

    print()

    euclidean = results["euclidean"]

    normalized = results["normalized"]

    print("Euclidean Metric")

    print("-" * 60)

    print(f"Minimum distance : {euclidean['distance']:.12e}")

    print(f"Nearest pair     : {euclidean['pair']}")

    print()

    print("Normalized Metric")

    print("-" * 60)

    print(f"Minimum distance : {normalized['distance']:.12e}")

    print(f"Nearest pair     : {normalized['pair']}")

    print()

    identical = (

        euclidean["pair"]

        ==

        normalized["pair"]

    )

    print("-" * 60)

    print("Nearest pair identical?")

    print()

    print(

        "YES"

        if identical

        else

        "NO"

    )

    print()

    if identical:

        print(

            "Conclusion:")

        print(

            "The nearest-neighbor structure "

            "is preserved under normalization."

        )

    else:

        print(

            "Conclusion:")

        print(

            "The nearest-neighbor structure "

            "changes with the adopted metric."

        )

    print()

    print("=" * 60)
# ============================================================
# Impressão da Auditoria
# ============================================================

def print_audit(audit):

    print()

    print("=" * 60)

    print("METRIC SENSITIVITY AUDIT")

    print("=" * 60)

    print()

    print(f"Repetitions : {audit['repetitions']}")

    print(f"Samples     : {audit['samples']}")

    print()

    print(f"YES : {audit['identical']}")

    print(f"NO  : {audit['different']}")

    print()

    robustness = (

        audit["different"]

        /

        audit["repetitions"]

    )

    print(

        f"Robustness : {robustness:.3f}"

    )

    print()

    if robustness >= 0.95:

        print(

            "Conclusion: "

            "Metric sensitivity is robust."

        )

    else:

        print(

            "Conclusion: "

            "Metric sensitivity is inconclusive."

        )

    print()

    print("=" * 60)

# ============================================================
# Main
# ============================================================

def main(

    samples=DEFAULT_SAMPLES,

    repetitions=30,

):

    results = run_metric_sensitivity(

        samples=samples,

    )

    print_report(results)

    audit = run_metric_sensitivity_audit(

        repetitions=repetitions,

        samples=samples,

    )

    print_audit(audit)


# ============================================================

if __name__ == "__main__":

    main()
