"""
=============================================================
S29_E10_1_2_surface_geometry.py
=============================================================

GER
S29 - E10.1.2

Surface Geometry Pipeline

Executa automaticamente toda a cadeia de análise
geométrica da superfície produzida pela E10.1.1.

Fluxo

A -> Gradient
B -> Continuity
C -> Boundaries
D -> Connected Regions
E -> Effective Dimension
F -> Geometry Certificate

=============================================================
"""

from __future__ import annotations

import time

from E10_1_2_A_gradient import main as run_gradient
from E10_1_2_B_continuity import main as run_continuity
from E10_1_2_C_boundaries import main as run_boundaries
from E10_1_2_D_connected_regions import (
    main as run_connected_regions,
)
from E10_1_2_E_dimension import main as run_dimension
from E10_1_2_F_geometry_certificate import (
    main as run_certificate,
)


# ============================================================
# IDENTIFICAÇÃO
# ============================================================

SERIES = "S29"
EXPERIMENT = "E10.1.2"
TITLE = "Surface Geometry"


# ============================================================
# PIPELINE
# ============================================================

PIPELINE = [

    (
        "A - Gradient",
        run_gradient,
    ),

    (
        "B - Continuity",
        run_continuity,
    ),

    (
        "C - Boundaries",
        run_boundaries,
    ),

    (
        "D - Connected Regions",
        run_connected_regions,
    ),

    (
        "E - Effective Dimension",
        run_dimension,
    ),

    (
        "F - Geometry Certificate",
        run_certificate,
    ),

]


# ============================================================
# CABEÇALHO
# ============================================================

def header():

    print("=" * 70)
    print("GER")
    print(f"{SERIES} - {EXPERIMENT}")
    print(TITLE)
    print("=" * 70)

    print("\nPipeline:\n")

    for name, _ in PIPELINE:
        print(f"   • {name}")

    print("\n" + "=" * 70)

# ============================================================
# EXECUÇÃO DO PIPELINE
# ============================================================

def run_pipeline():

    print("\nIniciando execução...\n")

    total_start = time.perf_counter()

    execution_log = []

    for index, (name, function) in enumerate(
        PIPELINE,
        start=1,
    ):

        print("-" * 70)
        print(f"[{index}/{len(PIPELINE)}] {name}")
        print("-" * 70)

        start = time.perf_counter()

        try:

            function()

            elapsed = (
                time.perf_counter() - start
            )

            execution_log.append({

                "step": name,
                "status": "PASS",
                "time": elapsed,

            })

            print(
                f"\nConcluído em "
                f"{elapsed:.2f} s"
            )

        except Exception as exc:

            elapsed = (
                time.perf_counter() - start
            )

            execution_log.append({

                "step": name,
                "status": "FAIL",
                "time": elapsed,
                "error": str(exc),

            })

            print("\nERRO:")
            print(exc)

            raise

    total_elapsed = (
        time.perf_counter() - total_start
    )

    return execution_log, total_elapsed

# ============================================================
# RESUMO DA EXECUÇÃO
# ============================================================

def execution_summary(
    execution_log,
    total_elapsed,
):

    print("\n")
    print("=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)

    passed = sum(
        item["status"] == "PASS"
        for item in execution_log
    )

    failed = sum(
        item["status"] == "FAIL"
        for item in execution_log
    )

    for item in execution_log:

        print(
            f"{item['status']:>5} | "
            f"{item['time']:8.2f} s | "
            f"{item['step']}"
        )

    print("-" * 70)

    print(
        f"Total modules : {len(execution_log)}"
    )

    print(
        f"Successful    : {passed}"
    )

    print(
        f"Failed        : {failed}"
    )

    print(
        f"Total time    : {total_elapsed:.2f} s"
    )

    print("=" * 70)

    return {

        "modules": len(execution_log),

        "passed": passed,

        "failed": failed,

        "total_time": total_elapsed,

        "status": (
            "PASS"
            if failed == 0
            else "FAIL"
        ),

    }

# ============================================================
# MAIN
# ============================================================

def main():

    header()

    execution_log, total_elapsed = run_pipeline()

    summary = execution_summary(
        execution_log,
        total_elapsed,
    )

    print("\n")
    print("=" * 70)
    print("GER")
    print(f"{SERIES} - {EXPERIMENT}")
    print(TITLE)
    print("=" * 70)

    print(
        f"Status        : {summary['status']}"
    )

    print(
        f"Módulos       : {summary['modules']}"
    )

    print(
        f"Sucesso       : {summary['passed']}"
    )

    print(
        f"Falhas        : {summary['failed']}"
    )

    print(
        f"Tempo total   : "
        f"{summary['total_time']:.2f} s"
    )

    if summary["status"] == "PASS":

        print("\nResultado:")

        print(
            "Toda a cadeia de geometria da superfície "
            "foi executada com sucesso."
        )

        print(
            "O certificado geométrico consolidado foi "
            "gerado pela etapa F."
        )

    else:

        print("\nResultado:")

        print(
            "O pipeline terminou com falhas."
        )

        print(
            "Verifique o módulo indicado no "
            "Execution Summary."
        )

    print("=" * 70)
    print("Fim da execução.")
    print("=" * 70)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()
