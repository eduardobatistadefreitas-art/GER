"""
====================================================================
GER
S29 — E10.1.3.F
Propagation Certificate
====================================================================

Objetivo
--------
Emitir o certificado científico da campanha E10.1.3.

Este módulo constitui a etapa final da investigação da propagação de
perturbações sobre a superfície relacional.

Nenhum novo processamento experimental é realizado.

Nenhuma nova métrica é calculada.

Todo o conteúdo produzido aqui é derivado exclusivamente dos
resultados obtidos pelos módulos anteriores.

--------------------------------------------------------------------
Entrada
--------------------------------------------------------------------

Este módulo utiliza exclusivamente os produtos consolidados da
campanha E10.1.3.

Principal arquivo:

    response_atlas.parquet

Também podem ser utilizados os resumos produzidos durante as etapas
anteriores para compor o relatório final.

Nenhuma chamada ao run_e10_engine() é realizada.

--------------------------------------------------------------------
Objetivos Científicos
--------------------------------------------------------------------

Produzir um documento objetivo contendo:

• identificação da campanha;

• parâmetros experimentais;

• dimensão da malha;

• perturbação utilizada;

• indicadores globais de resposta;

• indicadores globais de propagação;

• indicadores globais de estabilidade;

• estatísticas consolidadas;

• validações estruturais;

• inventário dos produtos gerados.

O certificado representa o encerramento formal da campanha
experimental.

--------------------------------------------------------------------
Escopo
--------------------------------------------------------------------

Este módulo não interpreta os resultados em termos físicos.

Também não produz conclusões cosmológicas nem formula hipóteses.

Seu papel consiste em registrar, de forma reproduzível, tudo aquilo
que foi efetivamente observado durante a campanha experimental.

Toda inferência científica permanece responsabilidade dos documentos
de análise do programa GER.

--------------------------------------------------------------------
Produtos
--------------------------------------------------------------------

Produz:

propagation_certificate.json

propagation_certificate.txt

propagation_certificate.md

experiment_inventory.json

campaign_manifest.json

--------------------------------------------------------------------
Conteúdo do Certificado
--------------------------------------------------------------------

O certificado deverá registrar, entre outras informações:

• identificação da campanha;

• data de execução;

• versão do experimento;

• tamanho da malha;

• número de execuções;

• estatísticas globais;

• integridade estrutural;

• consistência dos arquivos;

• localização dos produtos.

Esses elementos permitem reproduzir e auditar integralmente a
campanha.

--------------------------------------------------------------------
Encerramento da Campanha
--------------------------------------------------------------------

A emissão deste certificado encerra formalmente a E10.1.3.

Os módulos seguintes da série S29 utilizarão este certificado como
registro oficial da campanha de propagação de perturbações.

====================================================================
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

EXPERIMENT_NAME = "S29_E10_1_3_F"

CAMPAIGN_NAME = "Perturbation Propagation"

CAMPAIGN_VERSION = "1.0"

GRID_SIZE = 21


# ============================================================
# DIRETÓRIOS
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

ATLAS_DIR = (
    ROOT
    / "E10_1_3_E_ResponseAtlas"
)

OUTPUT_DIR = (
    ROOT
    / "E10_1_3_F_PropagationCertificate"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ATLAS_FILE = (
    ATLAS_DIR
    / "response_atlas.parquet"
)

ATLAS_SUMMARY = (
    ATLAS_DIR
    / "response_atlas_summary.json"
)


# ============================================================
# PRODUTOS
# ============================================================

CERTIFICATE_JSON = (
    OUTPUT_DIR
    / "propagation_certificate.json"
)

CERTIFICATE_TXT = (
    OUTPUT_DIR
    / "propagation_certificate.txt"
)

CERTIFICATE_MD = (
    OUTPUT_DIR
    / "propagation_certificate.md"
)

MANIFEST_FILE = (
    OUTPUT_DIR
    / "campaign_manifest.json"
)

INVENTORY_FILE = (
    OUTPUT_DIR
    / "experiment_inventory.json"
)


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(slots=True)
class CampaignCertificate:

    campaign: str

    version: str

    execution_date: str

    grid_size: int

    number_of_points: int

    number_of_variables: int

    stable_fraction: float

    response_mean: float

    propagation_mean: float

    stability_mean: float


# ============================================================
# UTILIDADES
# ============================================================

def load_atlas():

    return pd.read_parquet(
        ATLAS_FILE
    )


def load_summary():

    with open(

        ATLAS_SUMMARY,

        "r",
        encoding="utf-8",

    ) as fp:

        return json.load(fp)


def save_json(
    data,
    filepath,
):

    with open(

        filepath,

        "w",

        encoding="utf-8",

    ) as fp:

        json.dump(

            data,

            fp,

            indent=4,

            ensure_ascii=False,

        )


# ============================================================
# VALIDAÇÃO
# ============================================================

def validate_campaign(
    atlas,
):
    """
    Verificações estruturais finais
    da campanha.
    """

    expected = GRID_SIZE * GRID_SIZE

    if len(atlas) != expected:

        raise RuntimeError(

            f"Expected {expected} records."

        )

    if atlas.isna().sum().sum():

        raise RuntimeError(

            "Missing values detected."

        )

    duplicated = atlas.duplicated(

        subset=[

            "row",
            "col",

        ]

    ).sum()

    if duplicated:

        raise RuntimeError(

            "Duplicate coordinates detected."

        )

    return True


# ============================================================
# INICIALIZAÇÃO
# ============================================================

print("=" * 72)
print("GER")
print("S29 - E10.1.3.F")
print("Propagation Certificate")
print("=" * 72)

print(f"[OK] Atlas        : {ATLAS_DIR}")
print(f"[OK] Output       : {OUTPUT_DIR}")
print(f"[OK] Grid         : {GRID_SIZE} x {GRID_SIZE}")
print(f"[OK] Campaign     : {CAMPAIGN_NAME}")
print(f"[OK] Version      : {CAMPAIGN_VERSION}")

# ============================================================
# CERTIFICADO
# ============================================================

def build_certificate():
    """
    Constrói o certificado científico
    da campanha E10.1.3.
    """

    atlas = load_atlas()

    validate_campaign(atlas)

    summary = load_summary()

    certificate = CampaignCertificate(

        campaign=CAMPAIGN_NAME,

        version=CAMPAIGN_VERSION,

        execution_date=datetime.now().isoformat(),

        grid_size=GRID_SIZE,

        number_of_points=summary[
            "number_of_points"
        ],

        number_of_variables=summary[
            "number_of_variables"
        ],

        stable_fraction=summary[
            "stable_fraction"
        ],

        response_mean=summary[
            "response_norm_mean"
        ],

        propagation_mean=summary[
            "propagation_index_mean"
        ],

        stability_mean=summary[
            "stability_index_mean"
        ],

    )

    return atlas, summary, certificate


# ============================================================
# MANIFESTO
# ============================================================

def build_manifest():

    return {

        "campaign": CAMPAIGN_NAME,

        "experiment": EXPERIMENT_NAME,

        "version": CAMPAIGN_VERSION,

        "grid_size": GRID_SIZE,

        "modules": [

            "E10_1_3_A_perturbation_calibration",

            "E10_1_3_B_response_field",

            "E10_1_3_C_propagation_analysis",

            "E10_1_3_D_stability_map",

            "E10_1_3_E_response_atlas",

            "E10_1_3_F_propagation_certificate",

        ],

        "generated_at":

            datetime.now().isoformat(),

    }


# ============================================================
# INVENTÁRIO
# ============================================================

def build_inventory():

    inventory = {

        "campaign_root":

            str(ROOT),

        "products": [

            "E10_1_3_A_PerturbationCalibration",

            "E10_1_3_B_ResponseField",

            "E10_1_3_C_PropagationAnalysis",

            "E10_1_3_D_StabilityMap",

            "E10_1_3_E_ResponseAtlas",

            "E10_1_3_F_PropagationCertificate",

        ],

    }

    return inventory


# ============================================================
# SERIALIZAÇÃO
# ============================================================

def certificate_to_dict(
    certificate,
):

    return {

        "campaign":

            certificate.campaign,

        "version":

            certificate.version,

        "execution_date":

            certificate.execution_date,

        "grid_size":

            certificate.grid_size,

        "number_of_points":

            certificate.number_of_points,

        "number_of_variables":

            certificate.number_of_variables,

        "stable_fraction":

            certificate.stable_fraction,

        "response_mean":

            certificate.response_mean,

        "propagation_mean":

            certificate.propagation_mean,

        "stability_mean":

            certificate.stability_mean,

    }

# ============================================================
# EXPORTAÇÃO
# ============================================================

def write_text_certificate(
    certificate,
):

    with open(

        CERTIFICATE_TXT,

        "w",

        encoding="utf-8",

    ) as fp:

        fp.write(
            "====================================================\n"
        )

        fp.write(
            "GER\n"
        )

        fp.write(
            "S29 - E10.1.3\n"
        )

        fp.write(
            "Propagation Certificate\n"
        )

        fp.write(
            "====================================================\n\n"
        )

        fp.write(
            f"Campaign              : {certificate.campaign}\n"
        )

        fp.write(
            f"Version               : {certificate.version}\n"
        )

        fp.write(
            f"Execution Date        : {certificate.execution_date}\n\n"
        )

        fp.write(
            f"Grid Size             : {certificate.grid_size} x {certificate.grid_size}\n"
        )

        fp.write(
            f"Points                : {certificate.number_of_points}\n"
        )

        fp.write(
            f"Variables             : {certificate.number_of_variables}\n\n"
        )

        fp.write(
            f"Mean Response         : {certificate.response_mean:.6e}\n"
        )

        fp.write(
            f"Mean Propagation      : {certificate.propagation_mean:.6e}\n"
        )

        fp.write(
            f"Mean Stability        : {certificate.stability_mean:.6e}\n"
        )

        fp.write(
            f"Stable Fraction       : {certificate.stable_fraction:.6f}\n"
        )


def write_markdown_certificate(
    certificate,
):

    with open(

        CERTIFICATE_MD,

        "w",

        encoding="utf-8",

    ) as fp:

        fp.write("# GER\n\n")

        fp.write(
            "## S29 — E10.1.3 Propagation Certificate\n\n"
        )

        fp.write(
            f"- Campaign: **{certificate.campaign}**\n"
        )

        fp.write(
            f"- Version: **{certificate.version}**\n"
        )

        fp.write(
            f"- Execution: **{certificate.execution_date}**\n"
        )

        fp.write(
            f"- Grid: **{certificate.grid_size} × {certificate.grid_size}**\n"
        )

        fp.write(
            f"- Points: **{certificate.number_of_points}**\n"
        )

        fp.write(
            f"- Variables: **{certificate.number_of_variables}**\n"
        )

        fp.write(
            f"- Mean Response: **{certificate.response_mean:.6e}**\n"
        )

        fp.write(
            f"- Mean Propagation: **{certificate.propagation_mean:.6e}**\n"
        )

        fp.write(
            f"- Mean Stability: **{certificate.stability_mean:.6e}**\n"
        )

        fp.write(
            f"- Stable Fraction: **{certificate.stable_fraction:.6f}**\n"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    atlas, summary, certificate = build_certificate()

    certificate_dict = certificate_to_dict(
        certificate
    )

    manifest = build_manifest()

    inventory = build_inventory()

    save_json(

        certificate_dict,

        CERTIFICATE_JSON,

    )

    save_json(

        manifest,

        MANIFEST_FILE,

    )

    save_json(

        inventory,

        INVENTORY_FILE,

    )

    write_text_certificate(

        certificate,

    )

    write_markdown_certificate(

        certificate,

    )

    print()

    print("=" * 72)
    print("PROPAGATION CERTIFICATE COMPLETED")
    print("=" * 72)

    print(
        f"Campaign        : {certificate.campaign}"
    )

    print(
        f"Version         : {certificate.version}"
    )

    print(
        f"Grid            : {certificate.grid_size} x {certificate.grid_size}"
    )

    print(
        f"Points          : {certificate.number_of_points}"
    )

    print(
        f"Stable Fraction : {certificate.stable_fraction:.6f}"
    )

    print()

    print(
        f"Results saved to:\n{OUTPUT_DIR}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    main()
