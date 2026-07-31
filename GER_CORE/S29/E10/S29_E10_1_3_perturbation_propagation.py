"""
====================================================================
GER
S29
E10.1.3
Perturbation Propagation
====================================================================

Objetivo
--------
Executar integralmente a campanha E10.1.3.

Este arquivo constitui o ponto de entrada ("driver") da campanha de
propagação de perturbações da superfície relacional.

Nenhum cálculo científico é implementado aqui.

Toda a lógica experimental encontra-se distribuída nos módulos
especializados da série E10.1.3.

Este script apenas coordena sua execução na ordem correta.

--------------------------------------------------------------------
Fluxo Experimental
--------------------------------------------------------------------

A campanha é composta pelas seguintes etapas:

E10.1.3.A

    Perturbation Calibration

    Determina automaticamente a magnitude da perturbação
    utilizada na campanha.

↓

E10.1.3.B

    Response Field

    Executa toda a malha relacional utilizando a
    perturbação calibrada.

↓

E10.1.3.C

    Propagation Analysis

    Caracteriza quantitativamente a propagação da resposta.

↓

E10.1.3.D

    Stability Map

    Constrói o mapa global de estabilidade da superfície.

↓

E10.1.3.E

    Response Atlas

    Integra todos os observáveis produzidos durante
    a campanha.

↓

E10.1.3.F

    Propagation Certificate

    Emite o certificado científico final da campanha.

--------------------------------------------------------------------
Objetivos Científicos
--------------------------------------------------------------------

A campanha E10.1.3 investiga:

• resposta da superfície relacional;

• propagação de perturbações;

• organização espacial da resposta;

• estabilidade estrutural;

• atlas integrado da superfície;

• certificação completa do experimento.

Este script não interpreta os resultados.

Sua responsabilidade é apenas garantir que todas as etapas sejam
executadas na sequência correta.

--------------------------------------------------------------------
Produtos Produzidos
--------------------------------------------------------------------

Ao término da campanha estarão disponíveis:

• Perturbation Calibration

• Response Field

• Propagation Analysis

• Stability Map

• Response Atlas

• Propagation Certificate

Cada módulo permanece responsável pelos próprios arquivos.

--------------------------------------------------------------------
Arquitetura
--------------------------------------------------------------------

Este arquivo não acessa diretamente o CORE.

Toda interação com o motor experimental permanece encapsulada nos
módulos especializados da série E10.1.3.

Assim, este orquestrador permanece independente da implementação
interna do GER.

====================================================================
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import traceback

# ============================================================
# MÓDULOS DA CAMPANHA
# ============================================================

from GER_CORE.S29.E10.E10_1_3_A_perturbation_calibration import (
    main as run_calibration,
)

from GER_CORE.S29.E10.E10_1_3_B_response_field import (
    main as run_response_field,
)

from GER_CORE.S29.E10.E10_1_3_C_propagation_analysis import (
    main as run_propagation_analysis,
)

from GER_CORE.S29.E10.E10_1_3_D_stability_map import (
    main as run_stability_map,
)

from GER_CORE.S29.E10.E10_1_3_E_response_atlas import (
    main as run_response_atlas,
)

from GER_CORE.S29.E10.E10_1_3_F_propagation_certificate import (
    main as run_propagation_certificate,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

CAMPAIGN_NAME = "S29_E10_1_3"

CAMPAIGN_TITLE = (
    "Perturbation Propagation"
)

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

LOG_FILE = (
    ROOT
    / "S29_E10_1_3_execution_log.txt"
)

MANIFEST_FILE = (
    ROOT
    / "S29_E10_1_3_campaign_manifest.txt"
)


# ============================================================
# UTILIDADES
# ============================================================

def timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def write_log(message):

    print(message)

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8",

    ) as fp:

        fp.write(message + "\n")


def write_manifest():

    with open(

        MANIFEST_FILE,

        "w",

        encoding="utf-8",

    ) as fp:

        fp.write(
            "GER\n"
        )

        fp.write(
            "S29 - E10.1.3\n"
        )

        fp.write(
            "Perturbation Propagation\n\n"
        )

        fp.write(
            f"Campaign : {CAMPAIGN_NAME}\n"
        )

        fp.write(
            f"Started  : {timestamp()}\n\n"
        )

        fp.write("Execution Order\n")
        fp.write("------------------------------\n")

        fp.write(
            "1. Perturbation Calibration\n"
        )

        fp.write(
            "2. Response Field\n"
        )

        fp.write(
            "3. Propagation Analysis\n"
        )

        fp.write(
            "4. Stability Map\n"
        )

        fp.write(
            "5. Response Atlas\n"
        )

        fp.write(
            "6. Propagation Certificate\n"
        )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

ROOT.mkdir(
    parents=True,
    exist_ok=True,
)

print("=" * 72)
print("GER")
print("S29 - E10.1.3")
print(CAMPAIGN_TITLE)
print("=" * 72)

write_manifest()

write_log("")
write_log("=" * 72)
write_log("CAMPAIGN INITIALIZED")
write_log("=" * 72)
write_log(f"Started : {timestamp()}")
write_log("")

# ============================================================
# EXECUÇÃO DAS ETAPAS
# ============================================================

CAMPAIGN_STEPS = [

    (
        "E10.1.3.A",
        "Perturbation Calibration",
        run_calibration,
    ),

    (
        "E10.1.3.B",
        "Response Field",
        run_response_field,
    ),

    (
        "E10.1.3.C",
        "Propagation Analysis",
        run_propagation_analysis,
    ),

    (
        "E10.1.3.D",
        "Stability Map",
        run_stability_map,
    ),

    (
        "E10.1.3.E",
        "Response Atlas",
        run_response_atlas,
    ),

    (
        "E10.1.3.F",
        "Propagation Certificate",
        run_propagation_certificate,
    ),

]


def execute_step(
    step_number,
    total_steps,
    code,
    title,
    function,
):
    """
    Executa uma etapa da campanha.
    """

    separator = "=" * 72

    write_log("")
    write_log(separator)

    write_log(
        f"STEP {step_number}/{total_steps}"
    )

    write_log(
        f"{code} - {title}"
    )

    write_log(separator)

    start = datetime.now()

    try:

        function()

        elapsed = (
            datetime.now()
            - start
        ).total_seconds()

        write_log(
            f"[OK] Completed in {elapsed:.2f} s"
        )

        return {

            "code": code,

            "title": title,

            "status": "SUCCESS",

            "elapsed_seconds": elapsed,

        }

    except Exception:

        elapsed = (
            datetime.now()
            - start
        ).total_seconds()

        write_log(
            "[ERROR] Campaign interrupted."
        )

        write_log(
            traceback.format_exc()
        )

        return {

            "code": code,

            "title": title,

            "status": "FAILED",

            "elapsed_seconds": elapsed,

        }


# ============================================================
# EXECUÇÃO COMPLETA
# ============================================================

def run_campaign():
    """
    Executa toda a campanha E10.1.3.
    """

    total = len(CAMPAIGN_STEPS)

    results = []

    campaign_start = datetime.now()

    for index, step in enumerate(

        CAMPAIGN_STEPS,
        start=1,

    ):

        result = execute_step(

            index,
            total,
            step[0],
            step[1],
            step[2],

        )

        results.append(result)

        if result["status"] != "SUCCESS":

            write_log("")
            write_log(
                "Campaign terminated due to failure."
            )

            return {

                "success": False,

                "results": results,

                "elapsed_seconds": (
                    datetime.now()
                    - campaign_start
                ).total_seconds(),

            }

    return {

        "success": True,

        "results": results,

        "elapsed_seconds": (
            datetime.now()
            - campaign_start
        ).total_seconds(),

    }

# ============================================================
# RELATÓRIO FINAL
# ============================================================

def print_campaign_summary(report):
    """
    Exibe o resumo final da campanha.
    """

    print()
    print("=" * 72)
    print("CAMPAIGN SUMMARY")
    print("=" * 72)

    for result in report["results"]:

        print(

            f"{result['code']:<10}"

            f"{result['status']:<10}"

            f"{result['elapsed_seconds']:10.2f} s"

        )

    print()

    print(
        f"Total Time : "
        f"{report['elapsed_seconds']:.2f} s"
    )

    print(
        f"Status     : "
        f"{'SUCCESS' if report['success'] else 'FAILED'}"
    )

    print("=" * 72)


def write_campaign_summary(report):
    """
    Acrescenta o resumo ao log da campanha.
    """

    write_log("")
    write_log("=" * 72)
    write_log("CAMPAIGN SUMMARY")
    write_log("=" * 72)

    for result in report["results"]:

        write_log(

            f"{result['code']} | "

            f"{result['status']} | "

            f"{result['elapsed_seconds']:.2f} s"

        )

    write_log("")

    write_log(

        f"Total Time : "
        f"{report['elapsed_seconds']:.2f} s"

    )

    write_log(

        f"Status     : "
        f"{'SUCCESS' if report['success'] else 'FAILED'}"

    )

    write_log("=" * 72)


# ============================================================
# MAIN
# ============================================================

def main():

    campaign_start = timestamp()

    write_log("")
    write_log(
        f"Campaign started at {campaign_start}"
    )

    report = run_campaign()

    write_campaign_summary(report)

    print_campaign_summary(report)

    campaign_end = timestamp()

    write_log("")
    write_log(
        f"Campaign finished at {campaign_end}"
    )

    write_log(
        f"Results directory : {ROOT}"
    )

    print()

    print("=" * 72)

    if report["success"]:

        print(
            "S29 E10.1.3 COMPLETED SUCCESSFULLY"
        )

    else:

        print(
            "S29 E10.1.3 TERMINATED WITH ERRORS"
        )

    print("=" * 72)

    print(f"Results : {ROOT}")

    print("=" * 72)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    main()
