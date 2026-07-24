"""
============================================================
GER

L3.1 Correlation Matrix

Dashboard

============================================================
"""


def print_dashboard(summary):

    print("=" * 60)
    print("GER")
    print("L3.1 - Correlation Matrix")
    print("=" * 60)
    print()

    print(f"Variables : {summary['variables']}")
    print(f"Samples   : {summary['samples']}")
    print()

    print("Methods")

    for method in summary["methods"]:

        print(f"  • {method}")

    print()

    print("Mean Absolute Correlations")

    for method in summary["methods"]:

        value = summary[method]["mean_absolute"]

        print(f"  {method:10s}: {value:.6f}")

    print()

    print("=" * 60)
