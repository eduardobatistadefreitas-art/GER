import itertools

from GER_CORE.S26_B36_geometry_scan import (
    generate_signature_dataset,
)

# ============================================================
# GER
# S26-B37
#
# S26-B37-9
#
# Real Signature Geometry
#
# Validação da geometria ordinal utilizando
# Assinaturas Geométricas produzidas pelo próprio GER.
# ============================================================


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
# Distância ordinal
# ============================================================

FIELDS = [

    "diameter",

    "convergence",

    "recurrence",

    "drift",

]


def ordinal_distance(a, b):

    contributions = {}

    total = 0.0

    for field in FIELDS:

        da = a[field]

        db = b[field]

        d = abs(da - db)

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

    return [

        signature_to_dict(s)

        for s in signatures

    ]
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

    print("S26-B37-9")

    print("REAL SIGNATURE GEOMETRY")

    print("=" * 60)

    print()

    print("Generated signatures :",

          report["pairs"] + 1)

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

            "Ordinal geometry appears"

        )

        print(

            "robust for real GER signatures."

        )

    else:

        print("Conclusion:")

        print(

            "Real GER signatures induce"

        )

        print(

            "anisotropic ordinal geometry."

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
