"""
======================================================================
GER
S26-B36.3

Dynamic Regime Catalog

Pipeline oficial

1) Search Results
2) Build Catalog
3) Compute Statistics
4) Build Certificate
5) Save Results

Este módulo apenas orquestra a construção do catálogo.

Toda a lógica científica permanece encapsulada em:

GER_CORE/S26/S26_B36_3_dynamic_regime_catalog.py

======================================================================
"""

from pathlib import Path
from pprint import pprint

from GER_CORE.S26.S26_B36_3_dynamic_regime_catalog import (
    run_dynamic_regime_catalog,
)


# ============================================================
# Runner
# ============================================================

def run_B36_dynamic_regime_catalog(

    results_root="/content/drive/MyDrive/GER_RESULTS",

    output_directory="/content/drive/MyDrive/GER_RESULTS/S26/S26_B36_3_dynamic_regime_catalog",

):

    print()
    print("=" * 70)
    print("GER")
    print("S26-B36.3")
    print("Dynamic Regime Catalog")
    print("=" * 70)

    results_root = Path(results_root)

    output_directory = Path(output_directory)

    # --------------------------------------------------------
    # Search Results
    # --------------------------------------------------------

    print()
    print("1) Searching classifier results...")

    result = run_dynamic_regime_catalog(
        results_root=results_root,
        output_directory=output_directory,
    )

    print("OK")

    # --------------------------------------------------------
    # Catalog Summary
    # --------------------------------------------------------

    catalog = result["catalog"]

    statistics = result["statistics"]

    certificate = result["certificate"]

    print()

    print("=" * 70)
    print("Catalog Summary")
    print("=" * 70)

    print()

    print(
        "Classifier Files :",
        result["classifier_files"],
    )

    print(
        "Stationary Files :",
        result["stationary_files"],
    )

    print()

    print(
        "Catalog Entries  :",
        len(catalog),
    )

    print()

    print("=" * 70)
    print("Statistics")
    print("=" * 70)

    pprint(
        statistics,
        sort_dicts=False,
    )

    print()

    print("=" * 70)
    print("Catalog Certificate")
    print("=" * 70)

    pprint(
        certificate,
        sort_dicts=False,
    )

    print()

    print("=" * 70)
    print("First Catalog Entries")
    print("=" * 70)

    if len(catalog) == 0:

        print()

        print("Catalog is empty.")

    else:

        print()

        print(

            catalog.head(
                min(
                    10,
                    len(catalog),
                )
            )

        )

      # --------------------------------------------------------
    # Catalog Summary
    # --------------------------------------------------------

    catalog = result["catalog"]

    statistics = result["statistics"]

    certificate = result["certificate"]

    print()

    print("=" * 70)
    print("Catalog Summary")
    print("=" * 70)

    print()

    print(
        "Classifier Files :",
        result["classifier_files"],
    )

    print(
        "Stationary Files :",
        result["stationary_files"],
    )

    print()

    print(
        "Catalog Entries  :",
        len(catalog),
    )

    print()

    print("=" * 70)
    print("Statistics")
    print("=" * 70)

    pprint(
        statistics,
        sort_dicts=False,
    )

    print()

    print("=" * 70)
    print("Catalog Certificate")
    print("=" * 70)

    pprint(
        certificate,
        sort_dicts=False,
    )

    print()

    print("=" * 70)
    print("First Catalog Entries")
    print("=" * 70)

    if len(catalog) == 0:

        print()

        print("Catalog is empty.")

    else:

        print()

        print(

            catalog.head(
                min(
                    10,
                    len(catalog),
                )
            )

        )
    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()

    print("5) Results saved.")

    print()

    print("Output directory:")

    print(output_directory)

    print()

    print("=" * 70)
    print("Dynamic Regime Catalog Finished")
    print("=" * 70)

    return result


# ============================================================
# Execução direta
# ============================================================

def main():

    run_B36_dynamic_regime_catalog()


# ============================================================

if __name__ == "__main__":

    main()
  
