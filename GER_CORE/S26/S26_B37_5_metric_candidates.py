# ============================================================
# GER
# S26-B37-5
#
# Metric Candidates
#
# Objetivo:
#
# Implementar métricas candidatas para o espaço das
# Assinaturas Geométricas.
#
# A avaliação das métricas é realizada exclusivamente
# pelo módulo S26_B37_4_metric_benchmark.
# ============================================================

import math


# ============================================================
# Euclidiana
#
# Métrica de referência.
# ============================================================

def euclidean_metric(
    a,
    b,
):

    return math.sqrt(

        (a["diameter"] - b["diameter"]) ** 2 +

        (a["convergence"] - b["convergence"]) ** 2 +

        (a["recurrence"] - b["recurrence"]) ** 2 +

        (a["drift"] - b["drift"]) ** 2

    )


# ============================================================
# Euclidiana Normalizada
#
# Primeira candidata estrutural.
# ============================================================

def normalized_metric(
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

        delta = (

            a[key]

            -

            b[key]

        ) / scale

        total += delta ** 2

    return math.sqrt(total)
  # ============================================================
# Configuração das Métricas
# ============================================================

class MetricFactory:

    @staticmethod
    def normalized(ranges):

        def metric(a, b):

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

                delta = (

                    a[key]

                    -

                    b[key]

                ) / scale

                total += delta ** 2

            return math.sqrt(total)

        return metric


# ============================================================
# Utilitário
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
# Registro das Métricas
# ============================================================

AVAILABLE_METRICS = {

    "euclidean": euclidean_metric,

}


def build_metrics(dataset):

    ranges = compute_ranges(dataset)

    metrics = dict(AVAILABLE_METRICS)

    metrics["normalized"] = MetricFactory.normalized(

        ranges

    )

    return metrics


# ============================================================
# Demonstração
# ============================================================

def main():

    print("=" * 60)

    print("S26-B37-5")

    print("METRIC CANDIDATES")

    print("=" * 60)

    print()

    dataset = [

        {

            "diameter": 10.0,

            "convergence": 5000.0,

            "recurrence": 0.30,

            "drift": 0.70,

        },

        {

            "diameter": 12.0,

            "convergence": 5200.0,

            "recurrence": 0.35,

            "drift": 0.65,

        },

    ]

    metrics = build_metrics(dataset)

    a = dataset[0]

    b = dataset[1]

    print("Registered Metrics")

    print("-" * 60)

    for name in metrics:

        print(name)

    print()

    print("Example Distances")

    print("-" * 60)

    for name, metric in metrics.items():

        value = metric(a, b)

        print(f"{name:<15} {value:.12f}")

    print()

    print("=" * 60)


# ============================================================

if __name__ == "__main__":

    main()
