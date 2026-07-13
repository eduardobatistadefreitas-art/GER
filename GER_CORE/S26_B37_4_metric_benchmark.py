# ============================================================
# GER
# S26-B37-4
#
# Metric Benchmark
#
# Objetivo:
#
# Certificar experimentalmente métricas candidatas
# para o espaço das Assinaturas Geométricas.
#
# Este módulo NÃO propõe novas métricas.
#
# Sua função é apenas avaliar métricas existentes
# utilizando a bateria experimental construída
# durante o desenvolvimento do B37.
# ============================================================

import math
import random


# ============================================================
# Configuração
# ============================================================

DEFAULT_SAMPLES = 1000


# ============================================================
# Assinaturas
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
# Métrica Euclidiana
#
# Primeira métrica candidata.
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
# Métricas para Auditoria do Benchmark
# ============================================================

def broken_metric_constant(
    a,
    b,
):

    return 1.0


def broken_metric_signed(
    a,
    b,
):

    return (

        a["diameter"]

        -

        b["diameter"]

    )


def broken_metric_random(
    a,
    b,
):

    return random.random()
  # ============================================================
# Teste T1
#
# Identidade
# ============================================================

def test_identity(
    metric,
    dataset,
):

    passed = True

    for signature in dataset:

        if metric(

            signature,

            signature,

        ) != 0.0:

            passed = False

            break

    return {

        "test": "Identity",

        "status": "PASS" if passed else "FAIL",

    }


# ============================================================
# Teste T2
#
# Simetria
# ============================================================

def test_symmetry(
    metric,
    dataset,
):

    passed = True

    tolerance = 1e-12

    for i in range(len(dataset) - 1):

        a = dataset[i]

        b = dataset[i + 1]

        d1 = metric(a, b)

        d2 = metric(b, a)

        if abs(d1 - d2) > tolerance:

            passed = False

            break

    return {

        "test": "Symmetry",

        "status": "PASS" if passed else "FAIL",

    }


# ============================================================
# Benchmark
# ============================================================

def run_metric_benchmark(

    metric,

    samples=DEFAULT_SAMPLES,

):

    dataset = generate_dataset(samples)

    tests = [

        test_identity,

        test_symmetry,

    ]

    results = []

    passed = 0

    failed = 0

    for test in tests:

        result = test(

            metric,

            dataset,

        )

        results.append(result)

        if result["status"] == "PASS":

            passed += 1

        else:

            failed += 1

    return {

        "results": results,

        "summary": {

            "passed": passed,

            "failed": failed,

        },

          }
  # ============================================================
# Impressão
# ============================================================

def print_report(certificate):

    print("=" * 60)

    print("S26-B37-4")

    print("METRIC BENCHMARK")

    print("=" * 60)

    print()

    print("Tests")

    print("-" * 60)

    for result in certificate["results"]:

        print(

            f"{result['test']:<20}"

            f"{result['status']}"

        )

    print()

    summary = certificate["summary"]

    print("-" * 60)

    print("Summary")

    print("-" * 60)

    print(f"PASS : {summary['passed']}")

    print(f"FAIL : {summary['failed']}")

    print()

    if summary["failed"] == 0:

        print("Metric Certificate : APPROVED")

    else:

        print("Metric Certificate : REJECTED")

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    candidates = [

        ("Euclidean", euclidean_metric),

        ("Broken Constant", broken_metric_constant),

        ("Broken Signed", broken_metric_signed),

        ("Broken Random", broken_metric_random),

    ]

    for name, metric in candidates:

        print()

        print("=" * 60)

        print(name)

        print("=" * 60)

        print()

        certificate = run_metric_benchmark(

            metric,

        )

        print_report(

            certificate,

        )
