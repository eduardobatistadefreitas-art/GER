"""
============================================================
GER
S29-E6.2
Input / Output Module
============================================================

This module is responsible for every data exchange performed
by S29-E6.2.

Responsibilities
----------------

• Load signatures from the public Signature Provider.

• Validate loaded signatures.

• Export every experiment artifact.

This module NEVER constructs signatures manually.

Only the public Signature Provider is allowed to generate or
retrieve signatures.

Author
------
Eduardo Batista de Freitas

Framework
---------
GER — Geometria Espectral Relacional

Version
-------
1.0
============================================================
"""

from __future__ import annotations

import json

from pathlib import Path

import pandas as pd

from .config import (
    FILES,
    EXPORT_DIR,
    TABLE_DIR,
    RESULT_DIR,
    SAVE_JSON,
    SAVE_PARQUET,
    SAVE_CSV,
    SAVE_TXT,
    SIGNATURE_PROVIDER_MODULE,
)

# ============================================================
# Dynamic Signature Provider
# ============================================================

import importlib


def load_signature_provider():
    """
    Loads the public Signature Provider dynamically.

    Returns
    -------
    module
    """

    return importlib.import_module(
        SIGNATURE_PROVIDER_MODULE
    )


# ============================================================
# Signature Loading
# ============================================================

def load_signatures():
    """
    Loads all available signatures using the public API.

    Returns
    -------
    list
        Collection of signatures.
    """

    provider = load_signature_provider()

    #
    # The Signature Provider is expected to expose
    # a public function named:
    #
    #     load_signatures()
    #
    # Future implementations only need to preserve
    # this public interface.
    #

    signatures = provider.load_signatures()

    validate_signatures(signatures)

    return signatures


# ============================================================
# Validation
# ============================================================

def validate_signatures(signatures):
    """
    Basic structural validation.

    Parameters
    ----------
    signatures : list
    """

    if signatures is None:
        raise RuntimeError(
            "Signature Provider returned None."
        )

    if len(signatures) == 0:
        raise RuntimeError(
            "No signatures were loaded."
        )

    first_dimension = len(signatures[0])

    for index, signature in enumerate(signatures):

        if len(signature) != first_dimension:

            raise ValueError(

                "Signature dimension mismatch "
                f"at index {index}."

            )


def number_of_signatures(signatures):

    return len(signatures)


def signature_dimension(signatures):

    return len(signatures[0])


# ============================================================
# Export Utilities
# ============================================================

def save_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
):
    """
    Saves a DataFrame.

    CSV and/or Parquet according to configuration.
    """

    if SAVE_CSV:

        dataframe.to_csv(

            TABLE_DIR / filename,

            index=False,

        )

    if SAVE_PARQUET:

        parquet_name = filename.replace(
            ".csv",
            ".parquet",
        )

        dataframe.to_parquet(

            TABLE_DIR / parquet_name,

            index=False,

        )


def save_json(
    data: dict,
    filename: str,
):
    """
    Saves JSON data.
    """

    if not SAVE_JSON:
        return

    with open(

        EXPORT_DIR / filename,

        "w",

        encoding="utf-8",

    ) as file:

        json.dump(

            data,

            file,

            indent=4,

            ensure_ascii=False,

        )


def save_text(
    text: str,
    filename: str,
):
    """
    Saves plain text.
    """

    if not SAVE_TXT:
        return

    with open(

        EXPORT_DIR / filename,

        "w",

        encoding="utf-8",

    ) as file:

        file.write(text)


# ============================================================
# High-Level Export Helpers
# ============================================================

def export_summary(summary):

    save_json(

        summary,

        FILES["summary"],

    )


def export_metrics(df):

    save_dataframe(

        df,

        FILES["metrics"],

    )


def export_statistics(df):

    save_dataframe(

        df,

        FILES["statistics"],

    )


def export_degree_distribution(df):

    save_dataframe(

        df,

        FILES["degree"],

    )


def export_components(df):

    save_dataframe(

        df,

        FILES["components"],

    )


def export_centrality(df):

    save_dataframe(

        df,

        FILES["centrality"],

    )


# ============================================================
# Logging
# ============================================================

class ExperimentLogger:
    """
    Lightweight execution logger.
    """

    def __init__(self):

        self.lines = []

    def write(self, text):

        print(text)

        self.lines.append(text)

    def separator(self):

        self.lines.append("=" * 60)

        print("=" * 60)

    def save(self):

        save_text(

            "\n".join(self.lines),

            FILES["log"],

        )
