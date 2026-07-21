"""
GER/CORE/ger_results.py

GER Results Repository

Centralized access to the GER_RESULTS directory.

This module is intentionally lightweight.
It knows where experiment results are stored and provides
basic discovery/loading utilities for other GER modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd


class ResultsRepository:
    """
    Repository for GER experiment results.

    Default structure:

        /content/drive/MyDrive/GER_RESULTS/
            S29_E6.1/
                signatures.parquet
                observables.parquet
                ...
            RH_E3/
                ...
    """

    DEFAULT_ROOT = Path("/content/drive/MyDrive/GER_RESULTS")

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) if root else self.DEFAULT_ROOT

    # ============================================================
    # Repository
    # ============================================================

    def exists(self) -> bool:
        """Return True if the results repository exists."""
        return self.root.exists()

    def get_root(self) -> Path:
        """Return repository root."""
        return self.root

    # ============================================================
    # Experiment discovery
    # ============================================================

    def list_experiments(self) -> List[str]:
        """
        Return all experiment folders.
        """

        if not self.exists():
            return []

        return sorted(
            p.name
            for p in self.root.iterdir()
            if p.is_dir()
        )

    def has_experiment(self, experiment: str) -> bool:
        """
        Return True if experiment exists.
        """

        return (self.root / experiment).is_dir()

    def get_experiment_path(self, experiment: str) -> Path:
        """
        Return experiment directory.
        """

        path = self.root / experiment

        if not path.exists():
            raise FileNotFoundError(
                f"Experiment '{experiment}' not found."
            )

        return path

    # ============================================================
    # File discovery
    # ============================================================

    def list_files(self, experiment: str) -> List[str]:
        """
        Return files inside an experiment directory.
        """

        path = self.get_experiment_path(experiment)

        return sorted(
            p.name
            for p in path.iterdir()
            if p.is_file()
        )

    def file_exists(self, experiment: str, filename: str) -> bool:
        """
        Check if a file exists.
        """

        return (self.get_experiment_path(experiment) / filename).exists()

    def get_file_path(self, experiment: str, filename: str) -> Path:
        """
        Return file path.
        """

        path = self.get_experiment_path(experiment) / filename

        if not path.exists():
            raise FileNotFoundError(
                f"'{filename}' not found in '{experiment}'."
            )

        return path

    # ============================================================
    # Loaders
    # ============================================================

    def load_parquet(self, experiment: str, filename: str):
        """
        Load a parquet file.
        """

        return pd.read_parquet(
            self.get_file_path(experiment, filename)
        )

    def load_csv(self, experiment: str, filename: str):
        """
        Load a CSV file.
        """

        return pd.read_csv(
            self.get_file_path(experiment, filename)
        )

    def load_json(self, experiment: str, filename: str):
        """
        Load a JSON file.
        """

        with open(
            self.get_file_path(experiment, filename),
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def read_text(self, experiment: str, filename: str) -> str:
        """
        Read a text file.
        """

        return self.get_file_path(
            experiment,
            filename,
        ).read_text(encoding="utf-8")
