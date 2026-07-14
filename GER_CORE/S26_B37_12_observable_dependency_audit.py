import itertools
import numpy as np

from GER_CORE.S26_B36_geometry_scan import (
    generate_signature_dataset,
)

# ============================================================
# GER
# S26-B37
#
# S26-B37-12
#
# observable dependency audit
#
# ============================================================


FIELDS = [

    "diameter",

    "convergence",

    "recurrence",

    "drift",

]


# ============================================================
# Dataset
# ============================================================

def signature_to_vector(signature):

    return {

        "diameter": float(signature.diameter),

        "convergence": float(signature.convergence),

        "recurrence": float(signature.recurrence),

        "drift": float(signature.drift),

    }


def build_dataset():

    signatures = generate_signature_dataset()

    return [

        signature_to_vector(s)

        for s in signatures

    ]


# ============================================================
# Dependência entre dois observáveis
# ============================================================

def analyse_pair(dataset, x_name, y_name):

    x = np.array(

        [

            sample[x_name]

            for sample in dataset

        ],

        dtype=float,

    )

    y = np.array(

        [

            sample[y_name]

            for sample in dataset

        ],

        dtype=float,

    )

    correlation = np.corrcoef(

        x,

        y,

    )[0, 1]

    slope, intercept = np.polyfit(

        x,

        y,

        1,

    )

    prediction = (

        slope * x

        + intercept

    )

    residual = y - prediction

    rmse = np.sqrt(

        np.mean(

            residual ** 2

        )

    )

    r2 = 1.0 - (

        np.sum(

            residual ** 2

        )

        /

        np.sum(

            (y - np.mean(y)) ** 2

        )

    )

    return {

        "x": x_name,

        "y": y_name,

        "correlation": correlation,

        "r2": r2,

        "slope": slope,

        "intercept": intercept,

        "rmse": rmse,

    }
  # ============================================================
# Auditoria completa
# ============================================================

def classify_dependency(result):

    r = abs(result["correlation"])

    if r >= 0.999:

        return "Near deterministic"

    if r >= 0.95:

        return "Very strong"

    if r >= 0.80:

        return "Strong"

    if r >= 0.50:

        return "Moderate"

    if r >= 0.20:

        return "Weak"

    return "Independent"


def run_audit():

    dataset = build_dataset()

    report = []

    for x_name, y_name in itertools.combinations(

        FIELDS,

        2,

    ):

        result = analyse_pair(

            dataset,

            x_name,

            y_name,

        )

        result["classification"] = (

            classify_dependency(

                result

            )

        )

        report.append(

            result

        )

    return {

        "n_signatures": len(dataset),

        "results": report,

    }
  # ============================================================
# Relatório
# ============================================================

def print_report(report):

    print("=" * 60)

    print("S26-B37-12")

    print("observable dependency audit")

    print("=" * 60)

    print()

    print("Generated signatures :",

          report["n_signatures"])

    print()

    for result in report["results"]:

        print("-" * 60)

        print(

            f"{result['x']} × {result['y']}"

        )

        print("-" * 60)

        print(

            f"Pearson     : {result['correlation']:.6f}"

        )

        print(

            f"R²          : {result['r2']:.6f}"

        )

        print(

            f"Slope       : {result['slope']:.6f}"

        )

        print(

            f"Intercept   : {result['intercept']:.6f}"

        )

        print(

            f"RMSE        : {result['rmse']:.6e}"

        )

        print(

            f"Dependency  : {result['classification']}"

        )

        print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    report = run_audit()

    print_report(

        report

    )


# ============================================================

if __name__ == "__main__":

    main()
