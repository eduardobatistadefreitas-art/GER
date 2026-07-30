"""
===============================================================================
S29_E10_1_1_bidimensional_surface_scan.py
===============================================================================

GER — Geometria Espectral Relacional

S29 — E10.1.1

Bidimensional Surface Scan

-------------------------------------------------------------------------------

OBJETIVO

Construir uma malha bidimensional (γ, ω) para exploração do
espaço de parâmetros do módulo Ω.

Nesta primeira implementação o arquivo contém apenas:

    • Configuração do experimento
    • Construção da malha
    • Estruturas de dados
    • Preparação da persistência

A execução será implementada nas próximas partes.

===============================================================================
"""

from __future__ import annotations

import json

from dataclasses import dataclass
from dataclasses import asdict

from datetime import datetime

from pathlib import Path

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd


# =============================================================================
# GER
# =============================================================================

from GER_CORE.S29.E10.e10_engine import run_e10_engine

from GER.CORE.experiment_pipeline import run_signature_pipeline


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

GRID_SIZE = 21

GAMMA_MIN = 0.00
GAMMA_MAX = 2.00

OMEGA_MIN = 0.50
OMEGA_MAX = 2.50

DT = 2.5e-4

TIMESTEPS = 2000

POTENTIAL = "A"


# =============================================================================
# RESULTADOS
# =============================================================================

RESULT_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/E10/E10_1_1"
)

GRID_FILE = RESULT_ROOT / "grid.parquet"

SIGNATURE_FILE = RESULT_ROOT / "signature_surface.parquet"

CERTIFICATE_FILE = RESULT_ROOT / "certificate_surface.parquet"

METADATA_FILE = RESULT_ROOT / "surface_metadata.json"

SUMMARY_FILE = RESULT_ROOT / "summary.txt"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass(slots=True)
class GridPoint:

    i: int

    j: int

    gamma: float

    omega: float


@dataclass(slots=True)
class ExecutionResult:

    i: int

    j: int

    gamma: float

    omega: float

    success: bool

    elapsed_seconds: float

    signature: Optional[Any]

    certificate: Optional[Any]

    error: Optional[str]


# =============================================================================
# METADATA
# =============================================================================

def build_metadata() -> Dict[str, Any]:

    return {

        "series": "S29",

        "experiment": "E10.1.1",

        "name": "Bidimensional Surface Scan",

        "created_at": datetime.utcnow().isoformat(),

        "grid_size": GRID_SIZE,

        "gamma_min": GAMMA_MIN,

        "gamma_max": GAMMA_MAX,

        "omega_min": OMEGA_MIN,

        "omega_max": OMEGA_MAX,

        "dt": DT,

        "timesteps": TIMESTEPS,

        "potential": POTENTIAL,

        "engine": "run_e10_engine",

        "pipeline": "run_signature_pipeline",

    }


# =============================================================================
# DIRETÓRIOS
# =============================================================================

def prepare_output_directory():

    RESULT_ROOT.mkdir(

        parents=True,

        exist_ok=True,

    )


def save_metadata():

    with open(

        METADATA_FILE,

        "w",

        encoding="utf8",

    ) as fp:

        json.dump(

            build_metadata(),

            fp,

            indent=4,

            ensure_ascii=False,

        )


# =============================================================================
# GRID
# =============================================================================

def build_parameter_grid() -> List[GridPoint]:

    gammas = np.linspace(

        GAMMA_MIN,

        GAMMA_MAX,

        GRID_SIZE,

    )

    omegas = np.linspace(

        OMEGA_MIN,

        OMEGA_MAX,

        GRID_SIZE,

    )

    grid: List[GridPoint] = []

    for i, gamma in enumerate(gammas):

        for j, omega in enumerate(omegas):

            grid.append(

                GridPoint(

                    i=i,

                    j=j,

                    gamma=float(gamma),

                    omega=float(omega),

                )

            )

    return grid


def save_grid(

    grid: List[GridPoint],

):

    df = pd.DataFrame(

        [

            asdict(point)

            for point in grid

        ]

    )

    df.to_parquet(

        GRID_FILE,

        index=False,

    )


# =============================================================================
# COLETORES
# =============================================================================

signature_records: List[Dict[str, Any]] = []

certificate_records: List[Dict[str, Any]] = []

execution_log: List[ExecutionResult] = []

# =============================================================================
# EXECUÇÃO DE UM PONTO
# =============================================================================

import time


def run_grid_point(
    point: GridPoint,
) -> ExecutionResult:
    """
    Executa um único ponto da superfície (γ, ω).
    """

    t0 = time.perf_counter()

    try:

        # ---------------------------------------------------------
        # MOTOR E10
        # ---------------------------------------------------------

        result = run_e10_engine(

            timesteps=TIMESTEPS,

            dt=DT,

            potential=POTENTIAL,

        )

        # ---------------------------------------------------------
        # PIPELINE OBSERVACIONAL
        # ---------------------------------------------------------

        signature, certificate = run_signature_pipeline(

            result,

        )

        elapsed = time.perf_counter() - t0

        return ExecutionResult(

            i=point.i,

            j=point.j,

            gamma=point.gamma,

            omega=point.omega,

            success=True,

            elapsed_seconds=elapsed,

            signature=signature,

            certificate=certificate,

            error=None,

        )

    except Exception as exc:

        elapsed = time.perf_counter() - t0

        return ExecutionResult(

            i=point.i,

            j=point.j,

            gamma=point.gamma,

            omega=point.omega,

            success=False,

            elapsed_seconds=elapsed,

            signature=None,

            certificate=None,

            error=str(exc),

        )


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================

def signature_to_record(
    result: ExecutionResult,
) -> Dict[str, Any]:

    record = {

        "i": result.i,

        "j": result.j,

        "gamma": result.gamma,

        "omega": result.omega,

        "elapsed_seconds": result.elapsed_seconds,

    }

    signature = result.signature

    if signature is None:

        return record

    if isinstance(signature, dict):

        record.update(signature)

        return record

    if hasattr(signature, "__dict__"):

        for key, value in signature.__dict__.items():

            if key.startswith("_"):

                continue

            record[key] = value

        return record

    record["signature"] = str(signature)

    return record


def certificate_to_record(
    result: ExecutionResult,
) -> Dict[str, Any]:

    record = {

        "i": result.i,

        "j": result.j,

        "gamma": result.gamma,

        "omega": result.omega,

        "elapsed_seconds": result.elapsed_seconds,

        "success": result.success,

    }

    certificate = result.certificate

    if certificate is None:

        return record

    if isinstance(certificate, dict):

        record.update(certificate)

        return record

    if hasattr(certificate, "__dict__"):

        for key, value in certificate.__dict__.items():

            if key.startswith("_"):

                continue

            record[key] = value

        return record

    record["certificate"] = str(certificate)

    return record


# =============================================================================
# PERSISTÊNCIA INCREMENTAL
# =============================================================================

def flush_signatures():

    if not signature_records:

        return

    pd.DataFrame(

        signature_records

    ).to_parquet(

        SIGNATURE_FILE,

        index=False,

    )


def flush_certificates():

    if not certificate_records:

        return

    pd.DataFrame(

        certificate_records

    ).to_parquet(

        CERTIFICATE_FILE,

        index=False,

    )

# =============================================================================
# EXECUÇÃO DA SUPERFÍCIE
# =============================================================================

def run_surface_scan(
    grid: List[GridPoint],
) -> None:
    """
    Executa toda a superfície bidimensional.
    """

    total = len(grid)

    print()
    print("=" * 80)
    print("E10.1.1 - BIDIMENSIONAL SURFACE SCAN")
    print("=" * 80)
    print()

    print(f"Grid ............... {GRID_SIZE} x {GRID_SIZE}")
    print(f"Total Points ....... {total}")
    print()

    for n, point in enumerate(grid, start=1):

        print(

            f"[{n:04d}/{total}] "

            f"γ={point.gamma:.4f} "

            f"ω={point.omega:.4f}"

        )

        result = run_grid_point(point)

        execution_log.append(result)

        if result.success:

            signature_records.append(

                signature_to_record(result)

            )

            certificate_records.append(

                certificate_to_record(result)

            )

            flush_signatures()

            flush_certificates()

            print("    OK")

        else:

            print("    FAILED")

            print(f"    {result.error}")

    print()
    print("=" * 80)
    print("SURFACE FINISHED")
    print("=" * 80)


# =============================================================================
# AUDITORIA
# =============================================================================

def audit_surface():

    expected = GRID_SIZE * GRID_SIZE

    processed = len(execution_log)

    successful = sum(

        r.success

        for r in execution_log

    )

    failed = processed - successful

    coverage = (

        successful / expected

        if expected

        else 0.0

    )

    elapsed = sum(

        r.elapsed_seconds

        for r in execution_log

    )

    average = (

        elapsed / successful

        if successful

        else 0.0

    )

    return {

        "expected_points": expected,

        "processed_points": processed,

        "successful_points": successful,

        "failed_points": failed,

        "coverage": coverage,

        "elapsed_seconds": elapsed,

        "average_seconds": average,

    }


# =============================================================================
# SUMMARY
# =============================================================================

def write_summary(audit):

    with open(

        SUMMARY_FILE,

        "w",

        encoding="utf8",

    ) as fp:

        fp.write("=" * 78 + "\n")

        fp.write("GER\n")

        fp.write("S29 - E10.1.1\n")

        fp.write("Bidimensional Surface Scan\n")

        fp.write("=" * 78 + "\n\n")

        fp.write(

            f"Created ............ "

            f"{datetime.utcnow().isoformat()} UTC\n"

        )

        fp.write(

            f"Grid ............... "

            f"{GRID_SIZE} x {GRID_SIZE}\n"

        )

        fp.write(

            f"Expected ........... "

            f"{audit['expected_points']}\n"

        )

        fp.write(

            f"Successful ......... "

            f"{audit['successful_points']}\n"

        )

        fp.write(

            f"Failed ............. "

            f"{audit['failed_points']}\n"

        )

        fp.write(

            f"Coverage ........... "

            f"{audit['coverage']:.2%}\n"

        )

        fp.write(

            f"Elapsed ............ "

            f"{audit['elapsed_seconds']:.2f} s\n"

        )

        fp.write(

            f"Average ............ "

            f"{audit['average_seconds']:.3f} s\n"

        )


# =============================================================================
# RELATÓRIO
# =============================================================================

def print_final_report(audit):

    print()

    print("=" * 80)

    print("FINAL REPORT")

    print("=" * 80)

    print()

    print(

        f"Expected ........... "

        f"{audit['expected_points']}"

    )

    print(

        f"Successful ......... "

        f"{audit['successful_points']}"

    )

    print(

        f"Failed ............. "

        f"{audit['failed_points']}"

    )

    print(

        f"Coverage ........... "

        f"{audit['coverage']:.2%}"

    )

    print()

    print("Generated Files")

    print(f"  {GRID_FILE}")

    print(f"  {SIGNATURE_FILE}")

    print(f"  {CERTIFICATE_FILE}")

    print(f"  {METADATA_FILE}")

    print(f"  {SUMMARY_FILE}")

    print()

    print("=" * 80)

    print("E10.1.1 COMPLETED")

    print("=" * 80)

# =============================================================================
# MAIN
# =============================================================================

def main():

    print()
    print("=" * 80)
    print("GER")
    print("S29 - E10.1.1")
    print("Bidimensional Surface Scan")
    print("=" * 80)
    print()

    # ---------------------------------------------------------
    # Preparação
    # ---------------------------------------------------------

    prepare_output_directory()

    save_metadata()

    print("Building parameter grid...")

    grid = build_parameter_grid()

    save_grid(grid)

    print(f"Grid points : {len(grid)}")

    print()

    # ---------------------------------------------------------
    # Execução
    # ---------------------------------------------------------

    run_surface_scan(grid)

    # ---------------------------------------------------------
    # Auditoria
    # ---------------------------------------------------------

    audit = audit_surface()

    # ---------------------------------------------------------
    # Persistência final
    # ---------------------------------------------------------

    write_summary(audit)

    # ---------------------------------------------------------
    # Relatório
    # ---------------------------------------------------------

    print_final_report(audit)

    print()

    print("=" * 80)
    print("EXPERIMENT FINISHED")
    print("=" * 80)
    print()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    main()
