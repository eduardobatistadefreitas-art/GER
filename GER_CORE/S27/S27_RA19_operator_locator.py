import os

OPS = [
    "compute_confinement",
    "compute_convergence",
    "compute_recurrence",
    "compute_drift",
]

ROOT = "/content/GER"

for root, _, files in os.walk(ROOT):

    for file in files:

        if not file.endswith(".py"):
            continue

        path = os.path.join(root, file)

        try:
            text = open(path, encoding="utf-8").read()
        except:
            continue

        for op in OPS:
            if f"def {op}" in text:
                print(op)
                print(path)
                print()
