# ============================================================
# GER
# S26-B37-0
#
# Signature Separability
#
# Primeiro experimento do B37.
#
# Objetivo:
#
# Investigar se a Assinatura Geométrica possui
# poder discriminativo suficiente para distinguir
# estados diferentes.
#
# Este experimento NÃO utiliza o operador Ψ.
# ============================================================

import random
import math


# ============================================================
# Configuração
# ============================================================

DEFAULT_SAMPLES = 1000

ROUND_DIGITS = 12


# ============================================================
# Geração de Assinaturas
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
# Forma Canônica
# ============================================================

def canonical_signature(signature):

    return (

        round(
            signature["diameter"],
            ROUND_DIGITS,
        ),

        round(
            signature["convergence"],
            ROUND_DIGITS,
        ),

        round(
            signature["recurrence"],
            ROUND_DIGITS,
        ),

        round(
            signature["drift"],
            ROUND_DIGITS,
        ),

    )


# ============================================================
# Distância Euclidiana
# ============================================================

def signature_distance(a, b):

    return math.sqrt(

        (a["diameter"] - b["diameter"]) ** 2 +

        (a["convergence"] - b["convergence"]) ** 2 +

        (a["recurrence"] - b["recurrence"]) ** 2 +

        (a["drift"] - b["drift"]) ** 2

    )
  # ============================================================
# Experimento
# ============================================================

def run_signature_separability(

    samples=DEFAULT_SAMPLES,

):

    signatures = []

    canonical = {}

    collisions = 0

    minimum_distance = None

    nearest_pair = None

    # --------------------------------------------------------
    # Geração
    # --------------------------------------------------------

    for _ in range(samples):

        signature = generate_signature()

        signatures.append(signature)

        key = canonical_signature(signature)

        if key in canonical:

            collisions += 1

        else:

            canonical[key] = signature

    # --------------------------------------------------------
    # Distância mínima
    #
    # Busca O(N²)
    #
    # Para o primeiro experimento priorizamos
    # simplicidade e auditabilidade.
    # --------------------------------------------------------

    for i in range(len(signatures)):

        for j in range(i + 1, len(signatures)):

            distance = signature_distance(

                signatures[i],

                signatures[j],

            )

            if distance == 0:

                continue

            if (

                minimum_distance is None

                or

                distance < minimum_distance

            ):

                minimum_distance = distance

                nearest_pair = (

                    signatures[i],

                    signatures[j],

                )

    return {

        "generated": samples,

        "unique": len(canonical),

        "collisions": collisions,

        "collision_rate": (

            collisions / samples

        ),

        "minimum_distance": minimum_distance,

        "nearest_pair": nearest_pair,

    }
  # ============================================================
# Impressão
# ============================================================

def print_report(results):

    print("=" * 60)

    print("S26-B37-0")

    print("SIGNATURE SEPARABILITY")

    print("=" * 60)

    print()

    print(f"Generated signatures : {results['generated']}")

    print(f"Unique signatures    : {results['unique']}")

    print(f"Collisions           : {results['collisions']}")

    print(f"Collision rate       : {results['collision_rate']:.6f}")

    print()

    if results["minimum_distance"] is not None:

        print(

            f"Minimum distance     : "

            f"{results['minimum_distance']:.12e}"

        )

        print()

        print("Nearest Pair")

        print("-" * 60)

        print(results["nearest_pair"][0])

        print()

        print(results["nearest_pair"][1])

    else:

        print("Minimum distance     : N/A")

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main(

    samples=DEFAULT_SAMPLES,

):

    results = run_signature_separability(

        samples=samples,

    )

    print_report(results)


# ============================================================

if __name__ == "__main__":

    main()
