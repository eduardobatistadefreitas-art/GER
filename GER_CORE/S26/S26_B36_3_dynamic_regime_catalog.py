"""
============================================================
GER
S26-B36.3

Dynamic Regime Catalog

Este módulo consolida os resultados produzidos pelos
experimentos da B36 em um catálogo científico único.

Responsabilidades
-----------------

- localizar classifier.json
- localizar stationary_scan.json
- construir catálogo
- calcular estatísticas
- gerar certificado estrutural

Este módulo NÃO executa simulações.

============================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import Any
from typing import Optional

import pandas as pd


# ============================================================
# Constantes
# ============================================================

CLASSIFIER_EXPERIMENT = "S26_B36_classifier"

STATIONARY_EXPERIMENT = "S26_B36_stationary_scan"


# ============================================================
# Localização dos resultados
# ============================================================

def find_classifier_results(
    root: Path,
) -> List[Path]:
    """
    Localiza todos os classifier.json existentes.
    """

    return sorted(

        root.glob(
            f"**/{CLASSIFIER_EXPERIMENT}/**/classifier.json"
        )

    )


def find_stationary_results(
    root: Path,
) -> List[Path]:
    """
    Localiza todos os stationary_scan.json existentes.
    """

    return sorted(

        root.glob(
            f"**/{STATIONARY_EXPERIMENT}/**/stationary_scan.json"
        )

    )


# ============================================================
# IO
# ============================================================

def load_json(
    filename: Path,
) -> Dict[str, Any]:

    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


# ============================================================
# Extração
# ============================================================

def extract_classifier_entry(
    filename: Path,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extrai as informações relevantes do classifier.json.
    """

    configuration = data["configuration"]

    classification = data["classification"]

    statistics = classification["statistics"]
    
    run_folder = filename.parent
    
    run_id = run_folder.name
    
    timestamp = run_folder.name

    return {
        
        "run_id":
        run_id,
        
        "timestamp":
        timestamp,
        
        "system":
        "GER",
        
        "beta":
            configuration["beta"],

        "sigma":
            configuration["sigma"],

        "potential":
            configuration["potential"],

        "timesteps":
            configuration["timesteps"],

        "dt":
            configuration["dt"],

        "regime":
            classification["regime"],

        "persistence_score":
            classification["persistence_score"],

        "persistence_variance":
            classification["persistence_variance"],

        "mean_P":
            statistics["mean_P"],

        "mean_Rloc":
            statistics["mean_Rloc"],

        "mean_Dspec":
            statistics["mean_Dspec"],

        "mean_Hshape":
            statistics["mean_Hshape"],

    }


def extract_stationary_entry(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extrai os observáveis geométricos produzidos
    pelo Stationary Scan.
    """

    signature = data["signature"]

    return {

        "diameter":
            signature["diameter"],

        "convergence":
            signature["convergence"],

        "recurrence":
            signature["recurrence"],

        "drift":
            signature["drift"],

    }

# ============================================================
# Merge
# ============================================================

def merge_classifier_stationary(
    classifier: Dict[str, Any],
    stationary: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Une as informações de classificação
    e assinatura geométrica em um único registro.
    """

    record = dict(classifier)

    if stationary is None:

        record["diameter"] = None
        record["convergence"] = None
        record["recurrence"] = None
        record["drift"] = None

    else:

        record.update(stationary)

    return record


# ============================================================
# Construção do catálogo
# ============================================================

def build_catalog(
    classifier_files: List[Path],
    stationary_files: List[Path],
) -> pd.DataFrame:
    """
    Constrói o catálogo científico oficial.

    Nesta primeira versão os arquivos são
    pareados pela ordem cronológica.
    """

    records = []

    total = min(
        len(classifier_files),
        len(stationary_files),
    )

    for run_id in range(total):
        
        classifier = extract_classifier_entry(
            classifier_files[run_id],
            load_json(
                classifier_files[run_id]
            )
        )

        stationary = extract_stationary_entry(
            load_json(
                stationary_files[run_id]
            )
        )

        record = merge_classifier_stationary(
            classifier,
            stationary,
        )


        records.append(record)

    return pd.DataFrame(records)


# ============================================================
# Estatísticas
# ============================================================

def compute_catalog_statistics(
    catalog: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Calcula estatísticas globais do catálogo.
    """

    statistics = {

        "number_of_runs":
            int(len(catalog)),

        "regime_distribution":
            catalog["regime"].value_counts().to_dict(),

        "mean_persistence":
            float(
                catalog["persistence_score"].mean()
            ),

        "std_persistence":
            float(
                catalog["persistence_score"].std()
            ),

        "beta_range": {

            "min":
                float(catalog["beta"].min()),

            "max":
                float(catalog["beta"].max()),

        },

        "sigma_range": {

            "min":
                float(catalog["sigma"].min()),

            "max":
                float(catalog["sigma"].max()),

        },

        "potential_distribution":
            catalog["potential"].value_counts().to_dict(),

    }

    return statistics


# ============================================================
# Certificado
# ============================================================

def build_catalog_certificate(
    catalog: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Constrói o certificado estrutural
    do catálogo.
    """

    duplicated = bool(

        catalog.duplicated().any()

    )

    missing = bool(

        catalog.isnull().values.any()

    )

    certificate = {

        "CatalogIntegrity":

            "PASS"
            if len(catalog) > 0
            else "FAIL",

        "NumberRuns":

            len(catalog),

        "DuplicateRuns":

            "FAIL"
            if duplicated
            else "PASS",

        "MissingFields":

            "FAIL"
            if missing
            else "PASS",

        "GeometryAvailable":

            "PASS"
            if "diameter" in catalog.columns
            else "FAIL",

        "ClassificationAvailable":

            "PASS"
            if "regime" in catalog.columns
            else "FAIL",

        "Consistency":

            "PASS"
            if (
                not duplicated
                and
                not missing
            )
            else "FAIL",

    }

    return certificate


# ============================================================
# Salvamento
# ============================================================

def save_catalog(
    output_directory: Path,
    catalog: pd.DataFrame,
    statistics: Dict[str, Any],
    certificate: Dict[str, Any],
):
    """
    Salva todos os produtos científicos do catálogo.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    catalog.to_csv(
        output_directory / "dynamic_regime_catalog.csv",
        index=False,
    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    catalog.to_json(
        output_directory / "dynamic_regime_catalog.json",
        orient="records",
        indent=4,
    )

    # --------------------------------------------------------
    # Estatísticas
    # --------------------------------------------------------

    with open(
        output_directory / "catalog_statistics.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            statistics,
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # Certificado
    # --------------------------------------------------------

    with open(
        output_directory / "catalog_certificate.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            certificate,
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # Relatório
    # --------------------------------------------------------

    report = []

    report.append("=" * 60)
    report.append("GER")
    report.append("S26-B36.3")
    report.append("Dynamic Regime Catalog")
    report.append("=" * 60)
    report.append("")

    report.append(
        f"Number of Runs : {statistics['number_of_runs']}"
    )

    report.append("")

    report.append("Regime Distribution")

    for regime, count in statistics[
        "regime_distribution"
    ].items():

        report.append(
            f"  {regime}: {count}"
        )

    report.append("")

    report.append(
        f"Mean Persistence : {statistics['mean_persistence']:.6f}"
    )

    report.append(
        f"Std Persistence  : {statistics['std_persistence']:.6f}"
    )

    report.append("")

    report.append("Certificate")

    for key, value in certificate.items():

        report.append(
            f"{key}: {value}"
        )

    with open(
        output_directory / "catalog_report.txt",
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "\n".join(report)
        )


# ============================================================
# API Pública
# ============================================================

def run_dynamic_regime_catalog(
    results_root,
    output_directory,
):
    """
    Constrói o catálogo oficial de regimes.

    Parameters
    ----------
    results_root

        Diretório contendo GER_RESULTS.

    output_directory

        Diretório onde o catálogo será salvo.

    Returns
    -------
    dict
    """

    results_root = Path(results_root)

    output_directory = Path(output_directory)

    classifier_files = find_classifier_results(
        results_root
    )

    stationary_files = find_stationary_results(
        results_root
    )

    catalog = build_catalog(
        classifier_files,
        stationary_files,
    )

    statistics = compute_catalog_statistics(
        catalog
    )

    certificate = build_catalog_certificate(
        catalog
    )

    save_catalog(
        output_directory,
        catalog,
        statistics,
        certificate,
    )

    return {

        "catalog": catalog,

        "statistics": statistics,

        "certificate": certificate,

        "classifier_files": len(
            classifier_files
        ),

        "stationary_files": len(
            stationary_files
        ),

    }


# ============================================================
# Fim do módulo
# ============================================================
