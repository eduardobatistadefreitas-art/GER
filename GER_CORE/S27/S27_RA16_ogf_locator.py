# ============================================================
# GER
#
# S27-RA16
#
# OGF Locator
#
# Locate the implementation of the Geometric
# Fundamental Operators inside the GER project.
# ============================================================

import os

KEYWORDS = [

    "diameter",
    "convergence",
    "recurrence",
    "drift",

    "OGF",

    "signature",

    "geometric_signature",

    "build_signature",

    "compute_signature",

]

ROOT = "/content/GER"

print("=" * 60)
print("GER")
print("S27-RA16")
print("OGF Locator")
print("=" * 60)
print()

for root, _, files in os.walk(ROOT):

    for file in files:

        if not file.endswith(".py"):
            continue

        path = os.path.join(root, file)

        try:

            text = open(
                path,
                encoding="utf-8"
            ).read()

        except:

            continue

        hits = [

            k for k in KEYWORDS

            if k in text

        ]

        if hits:

            print(path)

            print("Hits:", hits)

            print()
