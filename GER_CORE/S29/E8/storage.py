"""
============================================================

GER
S29-E8

Trajectory Observatory

storage.py

============================================================

Gerenciamento de armazenamento.

Responsabilidades
-----------------

• Criação automática das pastas
• Identificação única da execução
• Escrita segura
• Salvamento JSON
• Salvamento TXT
• Salvamento CSV
• Registro de metadados

============================================================
"""

from __future__ import annotations

import csv
import json
import shutil
import uuid

from datetime import datetime
from pathlib import Path

from .config import *

# ==========================================================
# Execução
# ==========================================================

class ExperimentStorage:

    def __init__(self):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        short_id = str(uuid.uuid4())[:8]

        self.execution_id = (
            f"{timestamp}_{short_id}"
        )

        self.root = (
            RESULTS_ROOT
            / EXPERIMENT_NAME
            / self.execution_id
        )

        self.folders = {

            "trajectory":
                self.root / "trajectory",

            "checkpoints":
                self.root / "checkpoints",

            "statistics":
                self.root / "statistics",

            "reports":
                self.root / "reports",

            "logs":
                self.root / "logs",

        }

    # ======================================================
    # Criação da estrutura
    # ======================================================

    def initialize(self):

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        for folder in self.folders.values():

            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

        self.save_metadata()

    # ======================================================
    # Metadata
    # ======================================================

    def save_metadata(self):

        metadata = {

            "experiment": EXPERIMENT_NAME,

            "title": EXPERIMENT_TITLE,

            "version": VERSION,

            "execution_id": self.execution_id,

            "timestamp":
                datetime.now().isoformat(),

        }

        self.save_json(
            self.root / "metadata.json",
            metadata,
        )

    # ======================================================
    # JSON
    # ======================================================

    def save_json(
        self,
        filename,
        data,
    ):

        filename = Path(filename)

        tmp = filename.with_suffix(".tmp")

        with open(
            tmp,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                data,
                fp,
                indent=4,
                ensure_ascii=False,
            )

        shutil.move(tmp, filename)

    # ======================================================
    # TXT
    # ======================================================

    def save_text(
        self,
        filename,
        text,
    ):

        filename = Path(filename)

        tmp = filename.with_suffix(".tmp")

        with open(
            tmp,
            "w",
            encoding="utf-8",
        ) as fp:

            fp.write(text)

        shutil.move(tmp, filename)

    # ======================================================
    # CSV
    # ======================================================

    def save_csv(
        self,
        filename,
        rows,
        header=None,
    ):

        filename = Path(filename)

        tmp = filename.with_suffix(".tmp")

        with open(
            tmp,
            "w",
            newline="",
            encoding="utf-8",
        ) as fp:

            writer = csv.writer(fp)

            if header is not None:

                writer.writerow(header)

            writer.writerows(rows)

        shutil.move(tmp, filename)

    # ======================================================
    # Caminhos
    # ======================================================

    def path(self, folder):

        return self.folders[folder]

    def file(
        self,
        folder,
        name,
    ):

        return self.folders[folder] / name
