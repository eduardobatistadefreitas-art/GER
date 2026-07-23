"""
============================================================
GER
S29
E6.2
Statistical Observatory
Input / Output
============================================================

Loads and validates datasets produced by S29_E6.3.

This module is the official interface between the
Universe Generator (E6.3) and the Statistical
Observatory (E6.2).

No statistical computation is performed here.

Author
------
GER Project
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import RESULTS_ROOT

# ============================================================
# Version
# ============================================================

IO_VERSION = "1.0"

# ============================================================
# Default paths
# ============================================================

DEFAULT_EXPERIMENT = RESULTS_ROOT / "S29_E6.3"

UNIVERSES_FILE = (
    DEFAULT_EXPERIMENT /
    "universes" /
    "universes.parquet"
)

SIGNATURES_FILE = (
    DEFAULT_EXPERIMENT /
    "signatures" /
    "signatures.parquet"
)

CERTIFICATES_FILE = (
    DEFAULT_EXPERIMENT /
    "certificates" /
    "certificates.parquet"
)

# ============================================================
# Public API
# ============================================================

__all__ = [
    "load_universes",
    "load_signatures",
    "load_certificates",
    "load_complete_experiment",
]

# ============================================================
# Internal utilities
# ============================================================

def _load_parquet(path: Path) -> pd.DataFrame:
    """
    Load a parquet file.
    """

    if not path.exists():
        raise FileNotFoundError(path)

    return pd.read_parquet(path)


def _validate_dataframe(
    dataframe: pd.DataFrame,
    name: str,
) -> None:
    """
    Basic validation.
    """

    if dataframe.empty:
        raise ValueError(f"{name} is empty.")

    if dataframe.shape[0] == 0:
        raise ValueError(f"{name} contains no rows.")

# ============================================================
# Public loaders
# ============================================================

def load_universes(
    root: Path | str = DEFAULT_EXPERIMENT,
) -> pd.DataFrame:
    """
    Load universe metadata.
    """

    root = Path(root)

    dataframe = _load_parquet(
        root /
        "universes" /
        "universes.parquet"
    )

    _validate_dataframe(
        dataframe,
        "Universe dataset",
    )

    return dataframe


def load_signatures(
    root: Path | str = DEFAULT_EXPERIMENT,
) -> pd.DataFrame:
    """
    Load signature dataset.
    """

    root = Path(root)

    dataframe = _load_parquet(
        root /
        "signatures" /
        "signatures.parquet"
    )

    _validate_dataframe(
        dataframe,
        "Signature dataset",
    )

    return dataframe


def load_certificates(
    root: Path | str = DEFAULT_EXPERIMENT,
) -> pd.DataFrame:
    """
    Load scientific certificates.
    """

    root = Path(root)

    dataframe = _load_parquet(
        root /
        "certificates" /
        "certificates.parquet"
    )

    _validate_dataframe(
        dataframe,
        "Certificate dataset",
    )

    return dataframe


def load_complete_experiment(
    root: Path | str = DEFAULT_EXPERIMENT,
) -> dict:
    """
    Load the complete E6.3 experiment.
    """

    return {

        "universes": load_universes(root),

        "signatures": load_signatures(root),

        "certificates": load_certificates(root),
    }

# ============================================================
# Summary
# ============================================================

def _print_summary(data: dict) -> None:

    print("=" * 60)
    print("GER Statistical Observatory")
    print("Experiment Summary")
    print("=" * 60)
    print()

    for name, dataframe in data.items():

        print(f"{name}")

        print(f"  Rows    : {len(dataframe)}")

        print(f"  Columns : {len(dataframe.columns)}")

        print()

# ============================================================
# Self Test
# ============================================================

def main():

    print("=" * 60)
    print("GER S29 E6.2")
    print("IO Module")
    print("=" * 60)

    print()

    data = load_complete_experiment()

    _print_summary(data)

    print("Datasets loaded successfully.")

    print()


if __name__ == "__main__":
    main()
