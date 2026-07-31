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
espaço de parâmetros da arquitetura E10.

Fluxo oficial:

    E10 Engine
          ↓
    Persistence Observatory (S26-B35)
          ↓
    Signature Pipeline
          ↓
    Structural Certificate

Toda a evolução numérica permanece delegada ao GER CORE.

===============================================================================
"""

from __future__ import annotations

import json
import time

from dataclasses import asdict
from dataclasses import dataclass

from datetime import datetime

from pathlib import Path

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd


# =============================================================================
# GER CORE
# =============================================================================

from GER.CORE.bootstrap import initialize

from GER.CORE.experiment_pipeline import (
    run_signature_pipeline,
)

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S29.E10.e10_engine import (
    run_e10_engine,
)


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

GRID_SIZE = 21

GAMMA_MIN = 0.0
GAMMA_MAX = 2.0

OMEGA_MIN = 0.5
OMEGA_MAX = 2.5

N = 384

TIMESTEPS = 2000

DT = 2.5e-4

BETA = 1.0

POTENTIAL = "A"

SNAPSHOT_STRIDE = 50


# =============================================================================
# RESULTADOS
# =============================================================================

RESULT_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/E10/E10_1_1"
)

GRID_FILE = RESULT_ROOT / "grid.parquet"

SIGNATURE_FILE = RESULT_ROOT / "signature_surface.parquet"

CERTIFICATE_FILE = RESULT_ROOT / "certificate_surface.parquet"

SUMMARY_FILE = RESULT_ROOT / "summary.txt"

METADATA_FILE = RESULT_ROOT / "metadata.json"


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

    observables: Optional[Any]

    engine: Optional[Any]

    error: Optional[str]


# =============================================================================
# COLETORES
# =============================================================================

signature_records: List[Dict[str, Any]] = []

certificate_records: List[Dict[str, Any]] = []

execution_log: List[ExecutionResult] = []


# =============================================================================
# METADATA
# =============================================================================

def build_metadata():

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

        "n": N,

        "timesteps": TIMESTEPS,

        "dt": DT,

        "beta": BETA,

        "potential": POTENTIAL,

        "snapshot_stride": SNAPSHOT_STRIDE,

        "engine": "run_e10_engine",

        "pipeline": "run_signature_pipeline",

    }


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

def build_parameter_grid():

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
# EXECUÇÃO DE UM PONTO DA MALHA
# =============================================================================

def run_grid_point(
    point: GridPoint,
) -> ExecutionResult:
    """
    Executa um único ponto da superfície bidimensional.
    """

    print(
        f"γ={point.gamma:.6f}   ω={point.omega:.6f}"
    )

    t0 = time.perf_counter()

    try:

        # ---------------------------------------------------------------------
        # Motor E10
        # ---------------------------------------------------------------------

        engine_result = run_e10_engine(

            n=N,

            timesteps=TIMESTEPS,

            dt=DT,

            beta=BETA,

            potential=POTENTIAL,

            snapshot_stride=SNAPSHOT_STRIDE,

            gamma=point.gamma,

            omega=point.omega,

        )

        # ---------------------------------------------------------------------
        # Observatório de Persistência (S26-B35)
        # ---------------------------------------------------------------------

        observables = run_persistence_observatory(

            snapshots=engine_result["snapshots"],

            dt=DT,

        )

        # ---------------------------------------------------------------------
        # Assinatura Geométrica
        # ---------------------------------------------------------------------

        pipeline = run_signature_pipeline(

            observables,

            DT,

        )

        signature = pipeline["signature"]

        certificate = pipeline["certificate"]

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

            observables=observables,

            engine=engine_result,

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

            observables=None,

            engine=None,

            error=str(exc),

        )


# =============================================================================
# CONVERSORES
# =============================================================================

def signature_to_dict(signature):

    if signature is None:
        return {}

    if hasattr(signature, "to_dict"):
        return signature.to_dict()

    if isinstance(signature, dict):
        return signature

    return {

        "diameter": signature.diameter,

        "convergence": signature.convergence,

        "recurrence": signature.recurrence,

        "drift": signature.drift,

    }


def certificate_to_dict(certificate):

    if certificate is None:
        return {}

    if isinstance(certificate, dict):
        return certificate

    if hasattr(certificate, "to_dict"):
        return certificate.to_dict()

    return dict(certificate)


def signature_to_record(
    result: ExecutionResult,
):

    record = {

        "i": result.i,

        "j": result.j,

        "gamma": result.gamma,

        "omega": result.omega,

    }

    record.update(

        signature_to_dict(

            result.signature,

        )

    )

    return record


def certificate_to_record(
    result: ExecutionResult,
):

    record = {

        "i": result.i,

        "j": result.j,

        "gamma": result.gamma,

        "omega": result.omega,

    }

    record.update(

        certificate_to_dict(

            result.certificate,

        )

    )

    return record


# =============================================================================
# PERSISTÊNCIA
# =============================================================================

def flush_signatures():

    if not signature_records:
        return

    pd.DataFrame(

        signature_records,

    ).to_parquet(

        SIGNATURE_FILE,

        index=False,

    )


def flush_certificates():

    if not certificate_records:
        return

    import json

    df = pd.DataFrame(

        certificate_records,

    )

    for column in (

        "signature",

        "relations",

        "deductions",

        "consistency",

        "summary",

    ):

        if column in df.columns:

            df[column] = df[column].apply(

                lambda value: json.dumps(

                    value,

                    ensure_ascii=False,

                    default=str,

                )

            )

    df.to_parquet(

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

        result.success

        for result in execution_log

    )

    failed = processed - successful

    coverage = (

        successful / expected

        if expected

        else 0.0

    )

    elapsed = sum(

        result.elapsed_seconds

        for result in execution_log

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

def write_summary(
    audit,
):

    with open(

        SUMMARY_FILE,

        "w",

        encoding="utf8",

    ) as fp:

        fp.write("=" * 80 + "\n")

        fp.write("GER\n")

        fp.write("S29 - E10.1.1\n")

        fp.write("Bidimensional Surface Scan\n")

        fp.write("=" * 80 + "\n\n")

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

            f"Processed .......... "

            f"{audit['processed_points']}\n"

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

def print_final_report(
    audit,
):

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

        f"Processed .......... "

        f"{audit['processed_points']}"

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

    print(

        f"Elapsed ............ "

        f"{audit['elapsed_seconds']:.2f} s"

    )

    print(

        f"Average ............ "

        f"{audit['average_seconds']:.3f} s"

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

    # -------------------------------------------------------------------------
    # Inicialização do GER CORE
    # -------------------------------------------------------------------------

    initialize()

    # -------------------------------------------------------------------------
    # Preparação
    # -------------------------------------------------------------------------

    prepare_output_directory()

    save_metadata()

    print("Building parameter grid...")

    grid = build_parameter_grid()

    save_grid(grid)

    print(f"Grid points : {len(grid)}")

    print()

    # -------------------------------------------------------------------------
    # Execução
    # -------------------------------------------------------------------------

    run_surface_scan(grid)

    # -------------------------------------------------------------------------
    # Auditoria
    # -------------------------------------------------------------------------

    audit = audit_surface()

    # -------------------------------------------------------------------------
    # Persistência
    # -------------------------------------------------------------------------

    flush_signatures()

    flush_certificates()

    write_summary(audit)

    # -------------------------------------------------------------------------
    # Relatório final
    # -------------------------------------------------------------------------

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
