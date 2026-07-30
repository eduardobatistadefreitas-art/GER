"""
===============================================================================
S29_E10_1_1_bidimensional_surface_scan.py
===============================================================================

GER — Geometria Espectral Relacional
S29 — E10.1.1

Construção da Malha Bidimensional
(Bidimensional Relational Surface Scan)

-------------------------------------------------------------------------------

OBJETIVO
--------

Primeira exploração multiparamétrica do Espaço Relacional de Assinaturas.

Este experimento NÃO modifica nenhuma etapa científica do pipeline do GER.

Sua função consiste exclusivamente em:

    1. Construir uma malha bidimensional (γ, ω);

    2. Executar o motor oficial do GER para cada ponto;

    3. Executar o Pipeline Observacional oficial;

    4. Receber:
            • Assinatura Geométrica
            • Certificado Estrutural

    5. Persistir os resultados utilizando a infraestrutura oficial
       do projeto.

-------------------------------------------------------------------------------

ARQUITETURA

(γ,ω)

      │

      ▼

run_simulation()

      │

      ▼

Observables

      │

      ▼

run_signature_pipeline()

      │

      ├────► Signature

      └────► Structural Certificate

      │

      ▼

Persistência

-------------------------------------------------------------------------------

SAÍDA

/content/drive/MyDrive/GER_RESULTS/
    S29/
        E10/
            E10_1/

                grid.parquet

                signature_surface.parquet

                certificate_surface.parquet

                surface_metadata.json

                summary.txt

-------------------------------------------------------------------------------

Autor:
Eduardo Batista de Freitas

Projeto:
GER — Geometria Espectral Relacional

Série:
S29

Experimento:
E10.1.1

Versão:
1.0

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
# IMPORTS OFICIAIS DO GER
# =============================================================================

# Motor Numérico

from GER.CORE.ger_engine import run_engine

# Pipeline Observacional

from GER.CORE.experiment_pipeline import run_signature_pipeline

# Persistência Oficial

from GER.CORE.geometry.region_io import RegionIO

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

GRID_SIZE = 21

# Intervalos iniciais
#
# Estes valores são apenas padrões.
#
# Podem ser alterados via argumentos ou edição direta
# antes da execução.

GAMMA_MIN = 0.00
GAMMA_MAX = 2.00

OMEGA_MIN = 0.50
OMEGA_MAX = 2.50


DT = 0.01

STEPS = 5000

POTENTIAL = "A"


# =============================================================================
# DIRETÓRIOS
# =============================================================================

RESULT_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/E10/E10_1"
)

GRID_FILE = RESULT_ROOT / "grid.parquet"

SIGNATURE_FILE = RESULT_ROOT / "signature_surface.parquet"

CERTIFICATE_FILE = RESULT_ROOT / "certificate_surface.parquet"

METADATA_FILE = RESULT_ROOT / "surface_metadata.json"

SUMMARY_FILE = RESULT_ROOT / "summary.txt"


# =============================================================================
# ESTRUTURAS DE DADOS
# =============================================================================

@dataclass(slots=True)
class GridPoint:
    """
    Um ponto da malha bidimensional.
    """

    i: int
    j: int

    gamma: float
    omega: float


@dataclass(slots=True)
class ExecutionResult:
    """
    Resultado completo de um ponto.
    """

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
# METADADOS
# =============================================================================

def build_metadata() -> Dict[str, Any]:
    """
    Constrói o metadata da superfície.
    """

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

        "steps": STEPS,

        "potential": POTENTIAL,

        "pipeline": "run_signature_pipeline",

        "engine": "run_simulation",

    }


# =============================================================================
# DIRETÓRIOS
# =============================================================================

def prepare_output_directory() -> None:
    """
    Cria a estrutura de saída.
    """

    RESULT_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )


# =============================================================================
# MALHA BIDIMENSIONAL
# =============================================================================

def build_parameter_grid() -> List[GridPoint]:
    """
    Constrói a malha bidimensional.
    """

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


# =============================================================================
# GRID
# =============================================================================

def save_grid(
    grid: List[GridPoint],
) -> None:
    """
    Salva a malha.
    """

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
# METADATA
# =============================================================================

def save_metadata() -> None:
    """
    Salva os metadados do experimento.
    """

    metadata = build_metadata()

    with open(

        METADATA_FILE,

        "w",

        encoding="utf8",

    ) as fp:

        json.dump(

            metadata,

            fp,

            indent=4,

            ensure_ascii=False,

        )


# =============================================================================
# COLETORES
# =============================================================================

signature_records: List[Dict[str, Any]] = []

certificate_records: List[Dict[str, Any]] = []

execution_log: List[ExecutionResult] = []


# =============================================================================
# PERSISTÊNCIA INCREMENTAL
# =============================================================================

def flush_signatures() -> None:
    """
    Persiste assinaturas já produzidas.

    A implementação completa será adicionada
    na Parte 2.
    """

    pass


def flush_certificates() -> None:
    """
    Persiste certificados estruturais.

    Implementação Parte 2.
    """

    pass


# =============================================================================
# EXECUÇÃO DE UM PONTO
# =============================================================================

def run_grid_point(
    point: GridPoint,
) -> ExecutionResult:
    """
    Executa um único ponto da malha.

    Implementação completa na Parte 2.
    """

    raise NotImplementedError

# =============================================================================
# EXECUÇÃO DE UM PONTO
# =============================================================================

def run_grid_point(
    point: GridPoint,
) -> ExecutionResult:
    """
    Executa um único ponto da malha bidimensional.
    """

    t0 = time.perf_counter()

    try:

        # ---------------------------------------------------------
        # MOTOR NUMÉRICO
        # ---------------------------------------------------------

        gamma_final, history_dict, observables = run_simulation(

            gamma=point.gamma,

            omega=point.omega,

            potential=POTENTIAL,

            dt=DT,

            steps=STEPS,

            output_dir=None,

        )

        # ---------------------------------------------------------
        # PIPELINE OBSERVACIONAL
        # ---------------------------------------------------------

        signature, certificate = run_signature_pipeline(

            observables=observables,

            dt=DT,

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
    """
    Converte uma assinatura em um registro tabular.

    O objeto Signature pode variar entre versões do GER.
    A serialização abaixo procura preservar automaticamente
    todos os atributos públicos disponíveis.
    """

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

    if hasattr(signature, "__dict__"):

        for key, value in signature.__dict__.items():

            if key.startswith("_"):

                continue

            record[key] = value

    elif isinstance(signature, dict):

        record.update(signature)

    else:

        record["signature"] = str(signature)

    return record


def certificate_to_record(
    result: ExecutionResult,
) -> Dict[str, Any]:
    """
    Converte o certificado estrutural para formato tabular.
    """

    record = {

        "i": result.i,

        "j": result.j,

        "gamma": result.gamma,

        "omega": result.omega,

        "success": result.success,

        "elapsed_seconds": result.elapsed_seconds,

    }

    certificate = result.certificate

    if certificate is None:

        record["certificate"] = None

        return record

    if hasattr(certificate, "__dict__"):

        for key, value in certificate.__dict__.items():

            if key.startswith("_"):

                continue

            record[key] = value

    elif isinstance(certificate, dict):

        record.update(certificate)

    else:

        record["certificate"] = str(certificate)

    return record


# =============================================================================
# PERSISTÊNCIA INCREMENTAL
# =============================================================================

def flush_signatures() -> None:
    """
    Atualiza signature_surface.parquet.
    """

    if not signature_records:

        return

    df = pd.DataFrame(signature_records)

    df.to_parquet(

        SIGNATURE_FILE,

        index=False,

    )


def flush_certificates() -> None:
    """
    Atualiza certificate_surface.parquet.
    """

    if not certificate_records:

        return

    df = pd.DataFrame(certificate_records)

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
    Executa toda a malha bidimensional.
    """

    total = len(grid)

    print()
    print("=" * 80)
    print("E10.1.1 - BIDIMENSIONAL SURFACE SCAN")
    print("=" * 80)
    print()

    print(f"Grid Size : {GRID_SIZE} x {GRID_SIZE}")
    print(f"Experimentos : {total}")
    print()

    for n, point in enumerate(grid, start=1):

        print(

            f"[{n:04d}/{total}] "

            f"γ={point.gamma:.6f} "

            f"ω={point.omega:.6f}"

        )

        result = run_grid_point(point)

        execution_log.append(result)

        if not result.success:

            print("    FAILED")

            print(f"    {result.error}")

            continue

        signature_records.append(

            signature_to_record(result)

        )

        certificate_records.append(

            certificate_to_record(result)

        )

        flush_signatures()

        flush_certificates()

        # ---------------------------------------------------------
        # Persistência oficial do GER
        # ---------------------------------------------------------

        try:

            RegionIO.save_signature_space(
                
                result.signature,
                
                RESULT_ROOT/ f"certificate_{point.i}_{point.j}.json",
            
            )

        except Exception:

            pass

        print("    OK")

    print()
    print("=" * 80)
    print("FIM DA VARREDURA")
    print("=" * 80)
    print()

# =============================================================================
# AUDITORIA
# =============================================================================

def audit_surface() -> Dict[str, Any]:
    """
    Auditoria estrutural da malha executada.
    """

    total_expected = GRID_SIZE * GRID_SIZE

    total_processed = len(execution_log)

    successful = sum(
        r.success
        for r in execution_log
    )

    failed = total_processed - successful

    coverage = (
        successful / total_expected
        if total_expected
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

    missing = []

    processed = {

        (r.i, r.j)

        for r in execution_log

        if r.success

    }

    for i in range(GRID_SIZE):

        for j in range(GRID_SIZE):

            if (i, j) not in processed:

                missing.append((i, j))

    return {

        "expected_points": total_expected,

        "processed_points": total_processed,

        "successful_points": successful,

        "failed_points": failed,

        "coverage": coverage,

        "total_elapsed_seconds": elapsed,

        "average_elapsed_seconds": average,

        "missing_points": missing,

    }


# =============================================================================
# SUMMARY
# =============================================================================

def write_summary(
    audit: Dict[str, Any],
) -> None:
    """
    Gera summary.txt
    """

    with open(

        SUMMARY_FILE,

        "w",

        encoding="utf8",

    ) as fp:

        fp.write("=" * 78 + "\n")
        fp.write("GER\n")
        fp.write("S29 - E10.1.1\n")
        fp.write("BIDIMENSIONAL SURFACE SCAN\n")
        fp.write("=" * 78 + "\n\n")

        fp.write(
            f"Execution Date : "
            f"{datetime.utcnow().isoformat()} UTC\n"
        )

        fp.write(
            f"Grid Size      : "
            f"{GRID_SIZE} x {GRID_SIZE}\n"
        )

        fp.write(
            f"Expected       : "
            f"{audit['expected_points']}\n"
        )

        fp.write(
            f"Processed      : "
            f"{audit['processed_points']}\n"
        )

        fp.write(
            f"Successful     : "
            f"{audit['successful_points']}\n"
        )

        fp.write(
            f"Failed         : "
            f"{audit['failed_points']}\n"
        )

        fp.write(
            f"Coverage       : "
            f"{audit['coverage']:.3%}\n"
        )

        fp.write(
            f"Elapsed (s)    : "
            f"{audit['total_elapsed_seconds']:.3f}\n"
        )

        fp.write(
            f"Average (s)    : "
            f"{audit['average_elapsed_seconds']:.3f}\n"
        )

        fp.write("\n")

        fp.write(
            f"Gamma Range    : "
            f"[{GAMMA_MIN}, {GAMMA_MAX}]\n"
        )

        fp.write(
            f"Omega Range    : "
            f"[{OMEGA_MIN}, {OMEGA_MAX}]\n"
        )

        fp.write(
            f"Potential      : "
            f"{POTENTIAL}\n"
        )

        fp.write(
            f"dt             : "
            f"{DT}\n"
        )

        fp.write(
            f"steps          : "
            f"{STEPS}\n"
        )

        fp.write("\n")

        if audit["missing_points"]:

            fp.write("Missing Points\n")
            fp.write("-" * 40 + "\n")

            for point in audit["missing_points"]:

                fp.write(f"{point}\n")

        else:

            fp.write(
                "All grid points processed successfully.\n"
            )


# =============================================================================
# RELATÓRIO FINAL
# =============================================================================

def print_final_report(
    audit: Dict[str, Any],
) -> None:
    """
    Relatório final.
    """

    print()
    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)

    print()

    print(
        f"Grid Size ............... {GRID_SIZE} x {GRID_SIZE}"
    )

    print(
        f"Expected Points ......... {audit['expected_points']}"
    )

    print(
        f"Successful .............. {audit['successful_points']}"
    )

    print(
        f"Failed .................. {audit['failed_points']}"
    )

    print(
        f"Coverage ................ {audit['coverage']:.3%}"
    )

    print(
        f"Elapsed ................. "
        f"{audit['total_elapsed_seconds']:.2f} s"
    )

    print(
        f"Average / Point ......... "
        f"{audit['average_elapsed_seconds']:.3f} s"
    )

    print()

    print("Files")

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

def main() -> None:

    print()
    print("=" * 80)
    print("GER")
    print("S29 - E10.1.1")
    print("Bidimensional Surface Scan")
    print("=" * 80)

    prepare_output_directory()

    save_metadata()

    print()
    print("Building parameter grid...")

    grid = build_parameter_grid()

    save_grid(grid)

    print(
        f"{len(grid)} grid points generated."
    )

    print()

    run_surface_scan(grid)

    audit = audit_surface()

    write_summary(audit)

    print_final_report(audit)


# =============================================================================

if __name__ == "__main__":

    main()
