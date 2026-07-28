"""
============================================================

GER
S29-E8

Trajectory Observatory

checkpoint.py

============================================================

Checkpoint Manager

Responsabilidades
-----------------

• Salvamento automático
• Retomada automática
• Verificação de integridade
• Compatibilidade de configuração
• Recuperação após interrupção

============================================================
"""

from __future__ import annotations

import hashlib
import json

from pathlib import Path

from .config import *


# ==========================================================
# Hash da configuração
# ==========================================================

def configuration_hash():

    config = {

        "version": VERSION,

        "parameter": PARAMETER_NAME,

        "start": PARAMETER_START,

        "stop": PARAMETER_STOP,

        "step": PARAMETER_STEP,

        "max_states": MAX_STATES,

        "save_every": SAVE_EVERY,

        "checkpoint_every": CHECKPOINT_EVERY,

    }

    payload = json.dumps(
        config,
        sort_keys=True,
    )

    return hashlib.sha256(
        payload.encode()
    ).hexdigest()


# ==========================================================
# Checkpoint Manager
# ==========================================================

class CheckpointManager:

    def __init__(self, storage):

        self.storage = storage

        self.filename = storage.file(
            "checkpoints",
            "checkpoint.json",
        )

    # ======================================================
    # Existe?
    # ======================================================

    def exists(self):

        return self.filename.exists()

    # ======================================================
    # Salvar
    # ======================================================

    def save(

        self,

        state,

        parameter,

        elapsed,

        statistics=None,

    ):

        checkpoint = {

            "experiment": EXPERIMENT_NAME,

            "version": VERSION,

            "execution_id":

                self.storage.execution_id,

            "configuration_hash":

                configuration_hash(),

            "state":

                state,

            "parameter":

                parameter,

            "elapsed_seconds":

                elapsed,

            "statistics":

                statistics or {},

        }

        self.storage.save_json(

            self.filename,

            checkpoint,

        )

    # ======================================================
    # Carregar
    # ======================================================

    def load(self):

        if not self.exists():

            return None

        with open(

            self.filename,

            "r",

            encoding="utf-8",

        ) as fp:

            return json.load(fp)

    # ======================================================
    # Compatibilidade
    # ======================================================

    def validate(self):

        checkpoint = self.load()

        if checkpoint is None:

            return False

        current = configuration_hash()

        return (

            checkpoint["configuration_hash"]

            == current

        )

    # ======================================================
    # Estado inicial
    # ======================================================

    def initial_state(self):

        if (

            not AUTO_RESUME

            or

            not self.exists()

        ):

            return 0

        if not self.validate():

            raise RuntimeError(

                "Checkpoint incompatível "

                "com a configuração atual."

            )

        checkpoint = self.load()

        return checkpoint["state"] + 1
