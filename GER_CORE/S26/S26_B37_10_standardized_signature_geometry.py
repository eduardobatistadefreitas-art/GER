import itertools
import numpy as np

from GER_CORE.S26_B36_geometry_scan import (
    generate_signature_dataset,
)

# ============================================================
# GER
# S26-B37
#
# S26-B37-10
#
# standardized signature geometry
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

def signature_to_dict(signature):

    return {

        "diameter": signature.diameter,

        "convergence": signature.convergence,

        "recurrence": signature.recurrence,

        "drift": signature.drift,

    }


# ============================================================
# Padronização
# ============================================================

def standardize_dataset(dataset):

    statistics = {}

    for field in FIELDS:

        values = np.array(

            [

                sample[field]

                for sample in dataset

            ],

            dtype=float,

        )

        mean = np.mean(values)

        std = np.std(values)

        if std < 1e-15:

            std = 1.0

        statistics[field] = (

            mean,

            std,

        )

    standardized = []

    for sample in dataset:

        transformed = {}

        for field in FIELDS:

            mean, std = statistics[field]

            transformed[field] = (

                sample[field] - mean

            ) / std

        standardized.append(

            transformed

        )

    return standardized


# ============================================================
# Distância ordinal
# ============================================================

def ordinal_distance(a, b):

    contributions = {}

    total = 0.0

    for field in FIELDS:

        d = abs(

            a[field]

            - b[field]

        )

        contributions[field] = d

        total += d

    if total > 0:

        for field in FIELDS:

            contributions[field] /= total

    return contributions


# ============================================================
# Dataset
# ============================================================

def build_dataset():

    signatures = generate_signature_dataset()

    dataset = [

        signature_to_dict(s)

        for s in signatures

    ]

    return standardize_dataset(dataset)
  # ============================================================
# Geometria Global
# ============================================================

def analyse_geometry(dataset):

    totals = {

        field: 0.0

        for field in FIELDS

    }

    n_pairs = 0

    for a, b in itertools.combinations(

        dataset,

        2,

    ):

        contributions = ordinal_distance(

            a,

            b,

        )

        for field in FIELDS:

            totals[field] += contributions[field]

        n_pairs += 1

    if n_pairs == 0:

        raise RuntimeError(

            "Not enough signatures."

        )

    means = {

        field:

            totals[field] / n_pairs

        for field in FIELDS

    }

    dominant = max(

        means,

        key=means.get,

    )

    spread = (

        max(means.values())

        -

        min(means.values())

    )

    return {

        "n_signatures": len(dataset),

        "pairs": n_pairs,

        "means": means,

        "dominant": dominant,

        "spread": spread,

    }
  # ============================================================
# Relatório
# ============================================================

def print_report(report):

    print("=" * 60)

    print("S26-B37-10")

    print("standardized signature geometry")

    print("=" * 60)

    print()

    print("Generated signatures :",

          report["n_signatures"])

    print("Pairs analysed       :",

          report["pairs"])

    print()

    print("-" * 60)

    print("Mean Relative Contribution")

    print("-" * 60)

    for field in FIELDS:

        print(

            f"{field.capitalize():<14}"

            f"{100.0 * report['means'][field]:6.2f} %"

        )

    print()

    print("Global Dominant OGF")

    print("-" * 60)

    print(report["dominant"])

    print()

    spread = 100.0 * report["spread"]

    print(

        f"Contribution spread : {spread:.2f} %"

    )

    print()

    if spread < 1.0:

        print("Conclusion:")

        print(

            "Standardization removes"

        )

        print(

            "the observed anisotropy."

        )

    else:

        print("Conclusion:")

        print(

            "Anisotropy persists after"

        )

        print(

            "standardization."

        )

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    dataset = build_dataset()

    report = analyse_geometry(

        dataset

    )

    print_report(

        report

    )


# ============================================================

if __name__ == "__main__":

    main()
