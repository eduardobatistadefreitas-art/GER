# ============================================================
# GER
#
# S27-RA27
#
# Partition Universe Audit
#
# Objective:
# Discover which mathematical object represents
# the universe elements used by the Partition Theory.
# ============================================================

import os

ROOT = "/content/GER"

KEYWORDS = [

    "build_partition(",

    "Partition(",

    ".block_of(",

    "contains(",

    "same_partition(",

    "meet(",

]

print("=" * 60)
print("GER")
print("S27-RA27")
print("Partition Universe Audit")
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

        except Exception:

            continue

        hits = [

            k

            for k in KEYWORDS

            if k in text

        ]

        if hits:

            print(path)

            print("Hits:", hits)

            print()
