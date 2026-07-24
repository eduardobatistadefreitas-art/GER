"""
============================================================
GER

L3.1 Correlation Matrix

Input / Output

============================================================
"""

from pathlib import Path

import json

import pandas as pd


def ensure_directory(path):

    path = Path(path)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def save_csv(df, filename):

    filename = Path(filename)

    ensure_directory(
        filename.parent
    )

    df.to_csv(
        filename,
        index=True,
    )


def save_json(data, filename):

    filename = Path(filename)

    ensure_directory(
        filename.parent
    )

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


def load_csv(filename):

    return pd.read_csv(
        filename
    )
