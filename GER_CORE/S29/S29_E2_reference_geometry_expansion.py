"""
============================================================
RSG S29-E2
Reference Geometry Expansion Analysis
============================================================

Objective
---------
Quantify how the insertion of a new Geometric Signature
modifies the intrinsic geometry of the Reference Universe.

The Reference Universe is never modified permanently.
The expansion exists only during this experiment.
"""

from __future__ import annotations

import math

from GER.CORE.bootstrap import initialize
from GER.CORE.reference import load_reference

from GER_CORE.S29.S29_E1_1_duffing import run_experiment


# ============================================================
# Utilities
# ============================================================

def vector(signature):
    """
    Converts a Signature object or signature dictionary
    into a numerical vector.
    """

    if isinstance(signature, dict):

        return [

            float(signature["diameter"]),

            float(signature["convergence"]),

            float(signature["recurrence"]),

            float(signature["drift"]),

        ]

    return [

        float(signature.diameter),

        float(signature.convergence),

        float(signature.recurrence),

        float(signature.drift),

    ]


def distance(a, b):
    """
    Euclidean distance.
    """

    return math.sqrt(

        sum(

            (x - y) ** 2

            for x, y in zip(a, b)

        )

    )


# ============================================================
# Geometry
# ============================================================

def pairwise_distances(vectors):
    """
    Computes all pairwise distances.
    """

    values = []

    n = len(vectors)

    for i in range(n):

        for j in range(i + 1, n):

            values.append(

                distance(

                    vectors[i],

                    vectors[j],

                )

            )

    return values


def centroid(vectors):
    """
    Computes the geometric centroid.
    """

    dimension = len(vectors[0])

    center = []

    for i in range(dimension):

        center.append(

            sum(

                v[i]

                for v in vectors

            )

            / len(vectors)

        )

    return center


def radius_statistics(vectors, center=None):
    """
    Computes radius statistics.
    """

    if center is None:

        center = centroid(vectors)

    radii = [

        distance(v, center)

        for v in vectors

    ]

    return {

        "mean_radius":

            sum(radii) / len(radii),

        "max_radius":

            max(radii),

    }


def geometry_statistics(vectors):
    """
    Computes the geometric descriptors
    of the Signature Space.
    """

    center = centroid(vectors)

    pairwise = pairwise_distances(vectors)

    radius = radius_statistics(

        vectors,

        center,

    )

    if pairwise:

        diameter = max(pairwise)

        mean_pair = (

            sum(pairwise)

            / len(pairwise)

        )

    else:

        diameter = 0.0

        mean_pair = 0.0

    return {

        "size":

            len(vectors),

        "centroid":

            center,

        "diameter":

            diameter,

        "mean_pair_distance":

            mean_pair,

        "mean_radius":

            radius["mean_radius"],

        "max_radius":

            radius["max_radius"],

    }

# ============================================================
# Report
# ============================================================

def print_statistics(title, stats):

    print(title)
    print("-" * len(title))

    print(f"Size               : {stats['size']}")
    print(f"Centroid           : {stats['centroid']}")
    print(f"Diameter           : {stats['diameter']:.6f}")
    print(f"Mean Pair Distance : {stats['mean_pair_distance']:.6f}")
    print(f"Mean Radius        : {stats['mean_radius']:.6f}")
    print(f"Maximum Radius     : {stats['max_radius']:.6f}")

    print()


def print_report(before, after):

    print()
    print("=" * 60)
    print("REFERENCE GEOMETRY EXPANSION")
    print("=" * 60)
    print()

    print_statistics(

        "Reference Universe",

        before,

    )

    print_statistics(

        "Expanded Universe",

        after,

    )

    centroid_shift = distance(

        before["centroid"],

        after["centroid"],

    )

    diameter_ratio = (

        after["diameter"]

        /

        before["diameter"]

        if before["diameter"] != 0.0

        else 0.0

    )

    expansion_ratio = (

        after["mean_pair_distance"]

        /

        before["mean_pair_distance"]

        if before["mean_pair_distance"] != 0.0

        else 0.0

    )

    radius_variation = (

        after["mean_radius"]

        -

        before["mean_radius"]

    )

    print("Expansion Metrics")
    print("-----------------")

    print(f"Centroid Shift     : {centroid_shift:.6f}")
    print(f"Diameter Ratio     : {diameter_ratio:.6f}")
    print(f"Expansion Ratio    : {expansion_ratio:.6f}")
    print(f"Radius Variation   : {radius_variation:.6f}")

    print()

    print("=" * 60)
    print("STATUS : GEOMETRY EXPANSION ANALYZED")
    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    initialize()

    print()
    print("=" * 60)
    print("Loading Reference Universe")
    print("=" * 60)

    reference = load_reference(

        "S28_REFERENCE"

    )

    reference_vectors = [

        vector(

            item["signature"]

        )

        for item in reference["reference_universe"]

    ]

    print(

        f"Loaded {len(reference_vectors)} reference signatures."

    )

    print()
    print("=" * 60)
    print("Generating Duffing Signature")
    print("=" * 60)

    result = run_experiment()

    duffing_signature = result["signature"]

    expanded_vectors = list(

        reference_vectors

    )

    expanded_vectors.append(

        vector(

            duffing_signature

        )

    )

    before = geometry_statistics(

        reference_vectors

    )

    after = geometry_statistics(

        expanded_vectors

    )

    print_report(

        before,

        after,

    )


if __name__ == "__main__":

    main()
