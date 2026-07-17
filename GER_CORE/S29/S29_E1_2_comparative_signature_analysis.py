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

# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

from GER.CORE.reference import load_reference

# ---------------------------------------------------------------------
# Small runtime introspection helpers
# ---------------------------------------------------------------------


def find_signature(obj):
    """
    Searches recursively for the first dictionary containing the
    four official geometric observables.
    """

    required = {
        "diameter",
        "convergence",
        "recurrence",
        "drift",
    }

    if isinstance(obj, dict):

        if required.issubset(obj.keys()):
            return obj

        for value in obj.values():
            result = find_signature(value)
            if result is not None:
                return result

    elif isinstance(obj, (list, tuple)):
        for value in obj:
            result = find_signature(value)
            if result is not None:
                return result

    return None


def load_duffing_signature():
    """
    Tries to obtain the Duffing signature from the official
    public pipeline.

    If future versions rename functions/classes, only this
    routine should require updates.
    """

    candidates = [

        (
            "GER.CORE.signature_provider",
            "OfficialSignatureProvider",
        ),

        (
            "GER.CORE.signature_provider",
            "SignatureProvider",
        ),

        (
            "GER.CORE.signature_provider",
            "generate_signature",
        ),

        (
            "GER.CORE.pipeline",
            "run_pipeline",
        ),

    ]

    for module_name, member_name in candidates:

        try:

            module = __import__(
                module_name,
                fromlist=[member_name],
            )

            member = getattr(module, member_name)

            if isinstance(member, type):

                obj = member()

                for method in [
                    "generate",
                    "run",
                    "__call__",
                ]:

                    if hasattr(obj, method):

                        result = getattr(obj, method)("Duffing")

                        signature = find_signature(result)

                        if signature is not None:
                            return signature

            elif callable(member):

                try:
                    result = member("Duffing")
                except TypeError:
                    result = member()

                signature = find_signature(result)

                if signature is not None:
                    return signature

        except Exception:
            pass

    raise RuntimeError(
        "Unable to obtain Duffing signature using public APIs."
    )


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------


def vector(sig):

    return [

        float(sig["diameter"]),
        float(sig["convergence"]),
        float(sig["recurrence"]),
        float(sig["drift"]),

    ]


def distance(a, b):

    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main():

    print("=" * 60)
    print("RSG")
    print("S29-E1.2")
    print("Comparative Signature Analysis")
    print("=" * 60)

    reference = load_reference("S28_REFERENCE")

    universe = reference["reference_universe"]

    print()
    print("Reference signatures :", len(universe))

    duffing_signature = load_duffing_signature()

    print()
    print("Candidate signature")
    pprint(duffing_signature)

    candidate = vector(duffing_signature)

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

    for i, (system, d) in enumerate(
        ranking,
        start=1,
    ):

        print(
            f"{i:2d}. "
            f"{system:<20}"
            f"{d:.8f}"
        )

    nearest = ranking[0]

    print()
    print("Nearest neighbour :", nearest[0])
    print("Distance          :", f"{nearest[1]:.8f}")

    distances = [x[1] for x in ranking]

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
