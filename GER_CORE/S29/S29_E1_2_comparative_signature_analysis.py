"""
============================================================
RSG
S29-E1.2
Comparative Signature Analysis
============================================================

Compares the geometric signature produced by the Duffing system
against the official S28 Reference Universe.

Author : GER Project
Series : S29
"""

import math
from pprint import pprint

from GER.CORE.bootstrap import initialize

initialize()

from GER.CORE.reference import load_reference
from GER_CORE.S29.S29_E1_1_duffing import run_experiment


# ---------------------------------------------------------
# Utilities
# ---------------------------------------------------------

def vector(sig):
def vector(sig):

    if isinstance(sig, dict):

    return [

            float(sig["diameter"]),
            float(sig["convergence"]),
            float(sig["recurrence"]),
            float(sig["drift"]),

        ]

    return [

        float(sig.diameter),
        float(sig.convergence),
        float(sig.recurrence),
        float(sig.drift),

    ]

def distance(a, b):

    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("RSG")
    print("S29-E1.2")
    print("Comparative Signature Analysis")
    print("=" * 60)

    # --------------------------------------------------
    # Load official reference
    # --------------------------------------------------

    reference = load_reference("S28_REFERENCE")

    universe = reference["reference_universe"]

    print()
    print("Reference signatures :", len(universe))

    # --------------------------------------------------
    # Generate Duffing signature using the official
    # experiment already validated in S29-E1.1
    # --------------------------------------------------

    print()
    print("Generating Duffing signature...")

    result = run_experiment()

    if "signature" not in result:
        raise RuntimeError(
            "S29-E1.1 did not return a geometric signature."
        )

    duffing_signature = result["signature"]

    print()
    print("Candidate signature")
    pprint(duffing_signature)

    candidate = vector(duffing_signature)

    # --------------------------------------------------
    # Distance ranking
    # --------------------------------------------------

    ranking = []

    for item in universe:

        d = distance(
            candidate,
            vector(item["signature"]),
        )

        ranking.append(
            (
                item["system"],
                d,
            )
        )

    ranking.sort(
        key=lambda x: x[1]
    )

    print()
    print("-" * 60)
    print("Distance ranking")
    print("-" * 60)

    for i, (system, d) in enumerate(ranking, start=1):

        print(
            f"{i:2d}. "
            f"{system:<20}"
            f"{d:.8f}"
        )

    nearest = ranking[0]

    print()
    print("Nearest neighbour :", nearest[0])
    print("Distance          :", f"{nearest[1]:.8f}")

    distances = [d for _, d in ranking]

    mean = sum(distances) / len(distances)

    print()
    print("Statistics")
    print("Minimum :", min(distances))
    print("Mean    :", mean)
    print("Maximum :", max(distances))

    if nearest[1] < mean * 0.50:
        region = "EXISTING REGION"

    elif nearest[1] < mean:
        region = "BOUNDARY"

    else:
        region = "OUTLIER"

    print()
    print("Classification :", region)

    print()
    print("STATUS : COMPARISON COMPLETED")


if __name__ == "__main__":
    main()
