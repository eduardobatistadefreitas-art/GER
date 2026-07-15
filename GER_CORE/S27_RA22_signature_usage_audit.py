import os

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

        if "dict(signature)" in text:

            print(path)
