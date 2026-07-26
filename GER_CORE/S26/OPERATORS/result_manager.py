import os
import json
from datetime import datetime

import numpy as np

try:
    import pandas as pd
except ImportError:
    pd = None


# ============================================================
# GER
#
# S26 Result Manager
#
# Repositório oficial de resultados da Série S26.
#
# Todos os resultados experimentais devem ser gravados
# diretamente no Google Drive.
#
# Nenhum resultado é salvo no repositório GitHub.
# ============================================================


BASE_RESULTS = "/content/drive/MyDrive/GER_RESULTS/S26"


# ============================================================
# Conversão para JSON
# ============================================================

def _serialize(obj):

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.bool_):
        return bool(obj)

    if isinstance(obj, dict):
        return {
            k: _serialize(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [
            _serialize(v)
            for v in obj
        ]

    if isinstance(obj, tuple):
        return [
            _serialize(v)
            for v in obj
        ]

    return obj


# ============================================================
# Diretório da execução
# ============================================================

def create_output_directory(experiment):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    directory = os.path.join(
        BASE_RESULTS,
        experiment,
        timestamp,
    )

    os.makedirs(
        directory,
        exist_ok=True,
    )

    return directory


# ============================================================
# JSON
# ============================================================

def save_json(
    experiment,
    filename,
    data,
):

    directory = create_output_directory(
        experiment
    )

    filepath = os.path.join(
        directory,
        filename + ".json",
    )

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            _serialize(data),
            f,
            indent=4,
            ensure_ascii=False,
        )

    print()
    print("JSON salvo em:")
    print(filepath)

    return filepath


# ============================================================
# CSV
# ============================================================

def save_csv(
    experiment,
    filename,
    dataframe,
):

    if pd is None:
        raise ImportError(
            "pandas não está disponível."
        )

    directory = create_output_directory(
        experiment
    )

    filepath = os.path.join(
        directory,
        filename + ".csv",
    )

    dataframe.to_csv(
        filepath,
        index=False,
    )

    print()
    print("CSV salvo em:")
    print(filepath)

    return filepath


# ============================================================
# PARQUET
# ============================================================

def save_parquet(
    experiment,
    filename,
    dataframe,
):

    if pd is None:
        raise ImportError(
            "pandas não está disponível."
        )

    directory = create_output_directory(
        experiment
    )

    filepath = os.path.join(
        directory,
        filename + ".parquet",
    )

    dataframe.to_parquet(
        filepath,
        index=False,
    )

    print()
    print("PARQUET salvo em:")
    print(filepath)

    return filepath


# ============================================================
# TXT
# ============================================================

def save_txt(
    experiment,
    filename,
    text,
):

    directory = create_output_directory(
        experiment
    )

    filepath = os.path.join(
        directory,
        filename + ".txt",
    )

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(text)

    print()
    print("TXT salvo em:")
    print(filepath)

    return filepath
