"""
=============================================================
S29_E9/io.py
=============================================================

Input / Output utilities

Trajectory Relaxation Analysis

Responsibilities
----------------
- Locate trajectory.csv
- Load trajectory data
- Validate required columns
- Create output directory
- Export CSV
- Export JSON
- Export TXT

No statistical analysis is performed here.

=============================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .config import (
    AVAILABLE_OBSERVABLES,
)

# ============================================================
# Input
# ============================================================

def load_trajectory(path: str | Path) -> pd.DataFrame:
    """
    Load trajectory.csv.

    Parameters
    ----------
    path
        Path to trajectory.csv.

    Returns
    -------
    pandas.DataFrame
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)

    validate_dataframe(df)

    return df


# ============================================================
# Validation
# ============================================================

def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate input dataframe.
    """

    required = [

        "sigma",

        *AVAILABLE_OBSERVABLES,

    ]

    missing = [

        column

        for column in required

        if column not in df.columns

    ]

    if missing:

        raise ValueError(

            "Missing required columns:\n"

            + "\n".join(missing)

        )


# ============================================================
# Output Directory
# ============================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Create directory if necessary.
    """

    path = Path(path)

    path.mkdir(

        parents=True,

        exist_ok=True,

    )

    return path


# ============================================================
# CSV
# ============================================================

def save_csv(
    df: pd.DataFrame,
    filename: str | Path,
) -> None:
    """
    Save dataframe as CSV.
    """

    df.to_csv(

        filename,

        index=False,

    )


# ============================================================
# JSON
# ============================================================

def save_json(
    data,
    filename: str | Path,
) -> None:
    """
    Save dictionary as JSON.
    """

    with open(

        filename,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False,

        )


# ============================================================
# TXT
# ============================================================

def save_text(
    text: str,
    filename: str | Path,
) -> None:
    """
    Save text report.
    """

    with open(

        filename,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(text)


# ============================================================
# Helpers
# ============================================================

def observable_dataframe(
    df: pd.DataFrame,
    observable: str,
) -> pd.DataFrame:
    """
    Return a two-column dataframe containing:

        sigma
        observable
    """

    if observable not in OBSERVABLES:

        raise ValueError(

            f"Unknown observable: {observable}"

        )

    return df[

        [

            "sigma",

            observable,

        ]

    ].copy()


def list_observables() -> list[str]:
    """
    Return configured observables.
    """

    return list(OBSERVABLES)
