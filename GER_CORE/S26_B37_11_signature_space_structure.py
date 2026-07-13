import numpy as np

from GER_CORE.S26_B36_geometry_scan import (
    generate_signature_dataset,
)

# ============================================================
# GER
# S26-B37
#
# S26-B37-11
#
# signature space structure
#
# ============================================================


FIELDS = [

    "diameter",

    "convergence",

    "recurrence",

    "drift",

]


# ============================================================
# Conversão
# ============================================================

def signature_to_vector(signature):

    return [

        signature.diameter,

        signature.convergence,

        signature.recurrence,

        signature.drift,

    ]


# ============================================================
# Dataset
# ============================================================

def build_matrix():

    signatures = generate_signature_dataset()

    matrix = np.array(

        [

            signature_to_vector(s)

            for s in signatures

        ],

        dtype=float,

    )

    return matrix


# ============================================================
# Correlação
# ============================================================

def compute_correlation_matrix(matrix):

    return np.corrcoef(

        matrix,

        rowvar=False,

    )
  # ============================================================
# Estrutura do espaço
# ============================================================

def classify_correlations(correlation):

    strong = []

    moderate = []

    weak = []

    independent = []

    n = len(FIELDS)

    for i in range(n):

        for j in range(i + 1, n):

            value = correlation[i, j]

            pair = (

                FIELDS[i],

                FIELDS[j],

                value,

            )

            magnitude = abs(value)

            if magnitude >= 0.80:

                strong.append(pair)

            elif magnitude >= 0.50:

                moderate.append(pair)

            elif magnitude >= 0.20:

                weak.append(pair)

            else:

                independent.append(pair)

    return {

        "strong": strong,

        "moderate": moderate,

        "weak": weak,

        "independent": independent,

    }


# ============================================================
# Análise completa
# ============================================================

def analyse_structure():

    matrix = build_matrix()

    correlation = compute_correlation_matrix(

        matrix

    )

    classification = classify_correlations(

        correlation

    )

    return {

        "n_signatures": len(matrix),

        "correlation": correlation,

        "classification": classification,

    }
  # ============================================================
# Relatório
# ============================================================

def print_report(report):

    correlation = report["correlation"]

    print("=" * 60)

    print("S26-B37-11")

    print("signature space structure")

    print("=" * 60)

    print()

    print("Generated signatures :",

          report["n_signatures"])

    print()

    print("-" * 60)

    print("Correlation Matrix")

    print("-" * 60)

    print()

    header = " " * 15

    for field in FIELDS:

        header += f"{field[:10]:>12}"

    print(header)

    for i, row_name in enumerate(FIELDS):

        line = f"{row_name:<15}"

        for j in range(len(FIELDS)):

            line += f"{correlation[i, j]:12.3f}"

        print(line)

    print()

    classification = report["classification"]

    for title in [

        "strong",

        "moderate",

        "weak",

        "independent",

    ]:

        print("-" * 60)

        print(title.capitalize())

        print("-" * 60)

        pairs = classification[title]

        if not pairs:

            print("None")

        else:

            for a, b, value in pairs:

                print(

                    f"{a:<12}"

                    f"{b:<12}"

                    f"{value:8.3f}"

                )

        print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    report = analyse_structure()

    print_report(

        report

    )


# ============================================================

if __name__ == "__main__":

    main()
