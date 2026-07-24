"""
============================================================
GER

L3.1 Correlation Matrix

Report

============================================================
"""

from pathlib import Path


def write_report(summary, filename):

    filename = Path(filename)

    filename.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(

        filename,

        "w",

        encoding="utf-8",

    ) as f:

        f.write("=" * 60 + "\n")
        f.write("GER\n")
        f.write("L3.1 - Correlation Matrix\n")
        f.write("=" * 60 + "\n\n")

        f.write(
            f"Variables : {summary['variables']}\n"
        )

        f.write(
            f"Samples   : {summary['samples']}\n\n"
        )

        for method in summary["methods"]:

            stats = summary[method]

            f.write("-" * 60 + "\n")

            f.write(
                f"{method.upper()}\n\n"
            )

            for key, value in stats.items():

                f.write(
                    f"{key:20s}: {value}\n"
                )

            f.write("\n")
