"""
============================================================
GER S29-E6.3

MASSIVE UNIVERSE GENERATOR

GER — Geometria Espectral Relacional
============================================================

OBJETIVO

Construir um banco permanente de Universos Relacionais
utilizando EXCLUSIVAMENTE a API pública do GER CORE.

Este experimento NÃO implementa operadores geométricos.

Toda a geometria é produzida pelo próprio CORE.

Fluxo

Universo
    ↓
GER CORE
    ↓
Snapshot
    ↓
Observational Snapshot
    ↓
Trajectory
    ↓
Geometric Signature
    ↓
Structural Certificate
    ↓
Database

Características

✓ API pública apenas
✓ Checkpoint automático
✓ Dashboard único
✓ Banco incremental
✓ Detector de novidades
✓ Recuperação automática
✓ Compatível com futuras versões do CORE

============================================================
"""

import os
import json
import time
import random

from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

from IPython.display import clear_output

# ============================================================
# GER CORE
# ============================================================

from GER.CORE.bootstrap import initialize

from GER.CORE.ger_engine import (
    run_engine,
)

from GER.CORE.experiment_pipeline import (
    run_signature_pipeline,
)

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

# ============================================================
# CONFIGURAÇÃO
# ============================================================

TOTAL_UNIVERSES = 5_000_000

SAVE_INTERVAL = 5000

CHECKPOINT_INTERVAL = 5000

DASHBOARD_INTERVAL = 2.0

RANDOM_SEED = 42

random.seed(RANDOM_SEED)

np.random.seed(RANDOM_SEED)

# ============================================================
# DATABASE
# ============================================================

ROOT = Path(__file__).parent

DATABASE = (
    ROOT /
    "geometric_database" /
    "universe_database"
)

UNIVERSE_DIR = DATABASE / "universes"

SIGNATURE_DIR = DATABASE / "signatures"

CERTIFICATE_DIR = DATABASE / "certificates"

CHECKPOINT_DIR = DATABASE / "checkpoints"

STATISTICS_DIR = DATABASE / "statistics"

LOG_DIR = DATABASE / "logs"

TMP_DIR = DATABASE / "tmp"

for folder in [

    DATABASE,

    UNIVERSE_DIR,

    SIGNATURE_DIR,

    CERTIFICATE_DIR,

    CHECKPOINT_DIR,

    STATISTICS_DIR,

    LOG_DIR,

    TMP_DIR

]:

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

# ============================================================
# FILES
# ============================================================

UNIVERSE_FILE = (
    UNIVERSE_DIR /
    "universes.parquet"
)

SIGNATURE_FILE = (
    SIGNATURE_DIR /
    "signatures.parquet"
)

CERTIFICATE_FILE = (
    CERTIFICATE_DIR /
    "certificates.parquet"
)

CHECKPOINT_FILE = (
    CHECKPOINT_DIR /
    "checkpoint.json"
)

LOG_FILE = (
    LOG_DIR /
    "execution.log"
)

# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(self):

        self.last_update = 0.0

    # --------------------------------------------------------

    def update(

        self,

        processed,

        accepted,

        rejected,

        discoveries,

        speed,

        elapsed,

        eta,

        database_size,

        current_task,

        checkpoint_age

    ):

        now = time.time()

        if (

            now - self.last_update

            <

            DASHBOARD_INTERVAL

        ):

            return

        self.last_update = now

        clear_output(wait=True)

        percent = (

            processed /

            TOTAL_UNIVERSES

        ) * 100

        bars = int(percent / 2)

        print("=" * 60)
        print("GER S29-E6.3")
        print("MASSIVE UNIVERSE GENERATOR")
        print("=" * 60)

        print()

        print(

            "["

            + "█" * bars

            + "░" * (50 - bars)

            + "] "

            + f"{percent:6.2f}%"

        )

        print()

        print(f"Elapsed : {elapsed}")

        print(f"ETA     : {eta}")

        print()

        print("-" * 60)

        print("Universes")

        print("-" * 60)

        print(f"Generated : {processed:,}")

        print(f"Accepted  : {accepted:,}")

        print(f"Rejected  : {rejected:,}")

        print()

        print(f"Speed     : {speed:,.2f} universe/s")

        print()

        print("-" * 60)

        print("Discovery")

        print("-" * 60)

        print(f"New Discoveries : {discoveries:,}")

        print()

        print("-" * 60)

        print("Database")

        print("-" * 60)

        print(f"Size : {database_size:.2f} MB")

        print(f"Checkpoint : {checkpoint_age}")

        print()

        print("-" * 60)

        print("Current Task")

        print("-" * 60)

        print(current_task)

        print()

# ============================================================
# CHECKPOINT
# ============================================================

class Checkpoint:

    def __init__(self):

        self.data = {

            "processed":0,

            "accepted":0,

            "rejected":0,

            "discoveries":0,

            "last_checkpoint":time.time()

        }

    def exists(self):

        return CHECKPOINT_FILE.exists()

    def load(self):

        with open(
            CHECKPOINT_FILE,
            "r"
        ) as f:

            self.data = json.load(f)

    def save(self):

        self.data[
            "last_checkpoint"
        ] = time.time()

        with open(
            CHECKPOINT_FILE,
            "w"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4
            )
            # ============================================================
# LOGGER
# ============================================================

class EventLogger:

    def __init__(self):

        self.file = LOG_FILE

    # --------------------------------------------------------

    def log(self, message):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(

            self.file,

            "a",

            encoding="utf-8"

        ) as f:

            f.write(
                f"[{now}] {message}\n"
            )

# ============================================================
# DATABASE WRITER
# ============================================================

class DatabaseWriter:

    def __init__(self):

        self.universes = []

        self.signatures = []

        self.certificates = []

    # --------------------------------------------------------

    def append(

        self,

        universe,

        signature,

        certificate

    ):

        self.universes.append(
            universe
        )

        self.signatures.append(
            signature
        )

        self.certificates.append(
            certificate
        )

    # --------------------------------------------------------

    def flush(self):

        self._append(

            UNIVERSE_FILE,

            self.universes

        )

        self._append(

            SIGNATURE_FILE,

            self.signatures

        )

        self._append(

            CERTIFICATE_FILE,

            self.certificates

        )

        self.universes.clear()

        self.signatures.clear()

        self.certificates.clear()

   # --------------------------------------------------------

    def _append(

        self,

        file,

        rows

    ):

        if len(rows) == 0:

            return

        def sanitize(obj):

            if isinstance(obj, dict):

                if len(obj) == 0:

                    return None

                return {

                    k: sanitize(v)

                    for k, v in obj.items()

                }

            if isinstance(obj, list):

                return [

                    sanitize(v)

                    for v in obj

                ]

            return obj

        rows = [

            sanitize(row)

            for row in rows

        ]

        df = pd.DataFrame(rows)

        if file.exists():

            old = pd.read_parquet(file)

            df = pd.concat(

                [

                    old,

                    df

                ],

                ignore_index=True

            )

        df.to_parquet(

            file,

            index=False

        )

# ============================================================
# UNIVERSE GENERATOR
# ============================================================

class UniverseGenerator:

    """
    Responsabilidade única:

    Produzir um universo relacional.

    Este módulo NÃO calcula
    qualquer observável.

    Ele apenas fornece a entrada
    para o GER CORE.
    """

    def __init__(self):

        self.identifier = 0

    # --------------------------------------------------------

    def generate(self):

        self.identifier += 1

        vertices = random.randint(

            8,

            64

        )

        probability = random.uniform(

            0.05,

            0.35

        )

        seed = random.randint(

            0,

            2**31

        )

        return {

            "UniverseID":
                self.identifier,

            "n":
                vertices,

            "timesteps":
                2000,

            "dt":
                2.5e-4,

            "beta":
                1.0,

            "potential":
                "A",

            "snapshot_stride":
                50,

            "sigma":
                0.10,

            "Seed":
                seed,

            "Probability":
                probability,

        }

# ============================================================
# CORE ADAPTER
# ============================================================
class GERCoreAdapter:

    """
    Único ponto de contato entre
    os experimentos S29 e o CORE.
    """

    def __init__(self):

        initialize()

    def analyse(
        self,
        universe,
    ):

        engine = run_engine(

            n=universe["n"],

            timesteps=universe["timesteps"],

            dt=universe["dt"],

            beta=universe["beta"],

            potential=universe["potential"],

            snapshot_stride=universe["snapshot_stride"],

            sigma=universe["sigma"],

        )

        observables = run_persistence_observatory(

            engine["snapshots"],

            universe["dt"],

        )

        result = run_signature_pipeline(

            observables,

            universe["dt"],

        )

        return (

            result["signature"],

            result["certificate"],

        )
# ============================================================
# DISCOVERY MANAGER
# ============================================================

class DiscoveryManager:

    """
    Controla apenas estatísticas
    de descobertas.

    Não interfere na geometria.
    """

    def __init__(self):

        self.known = set()

        self.total = 0

    # --------------------------------------------------------

    def update(

        self,

        signature

    ):

        key = tuple(

            round(v, 8)

            for v in signature.values()

        )

        if key in self.known:

            return False

        self.known.add(key)

        self.total += 1

        return True
        # ============================================================
# STATISTICS
# ============================================================

class Statistics:

    def __init__(self):

        self.signature_rows = []

    # --------------------------------------------------------

    def update(self, signature):

        self.signature_rows.append(signature)

    # --------------------------------------------------------

    def export(self):

        if len(self.signature_rows) == 0:

            return

        df = pd.DataFrame(
            self.signature_rows
        )

        df.describe().T.to_csv(

            STATISTICS_DIR /
            "signature_statistics.csv"

        )

        df.corr(
            numeric_only=True
        ).to_csv(

            STATISTICS_DIR /
            "signature_correlation.csv"

        )

# ============================================================
# MASSIVE UNIVERSE GENERATOR
# ============================================================

class MassiveUniverseGenerator:

    def __init__(self):

        self.dashboard = Dashboard()

        self.logger = EventLogger()

        self.database = DatabaseWriter()

        self.statistics = Statistics()

        self.discovery = DiscoveryManager()

        self.generator = UniverseGenerator()

        self.core = GERCoreAdapter()

        self.checkpoint = Checkpoint()

        if self.checkpoint.exists():

            self.checkpoint.load()

            self.logger.log(
                "Checkpoint restored."
            )

        self.processed = self.checkpoint.data[
            "processed"
        ]

        self.accepted = self.checkpoint.data[
            "accepted"
        ]

        self.rejected = self.checkpoint.data[
            "rejected"
        ]

        self.discoveries = self.checkpoint.data[
            "discoveries"
        ]

        self.start_time = time.time()

        self.last_checkpoint = time.time()

    # --------------------------------------------------------

    def elapsed(self):

        elapsed = int(

            time.time()

            -

            self.start_time

        )

        h = elapsed // 3600

        m = (elapsed % 3600) // 60

        s = elapsed % 60

        return f"{h:02}:{m:02}:{s:02}"

    # --------------------------------------------------------

    def eta(self):

        if self.processed == 0:

            return "--:--:--"

        elapsed = (

            time.time()

            -

            self.start_time

        )

        speed = self.processed / elapsed

        remaining = (

            TOTAL_UNIVERSES

            -

            self.processed

        )

        seconds = int(

            remaining /

            max(speed, 1e-9)

        )

        h = seconds // 3600

        m = (seconds % 3600) // 60

        s = seconds % 60

        return f"{h:02}:{m:02}:{s:02}"

    # --------------------------------------------------------

    def speed(self):

        elapsed = max(

            time.time()

            -

            self.start_time,

            1e-9

        )

        return self.processed / elapsed

    # --------------------------------------------------------

    def database_size(self):

        total = 0

        for root, _, files in os.walk(DATABASE):

            for file in files:

                total += os.path.getsize(

                    os.path.join(

                        root,

                        file

                    )

                )

        return total / (1024 * 1024)

    # --------------------------------------------------------

    def checkpoint_age(self):

        age = int(

            time.time()

            -

            self.last_checkpoint

        )

        return f"{age} s"

    # --------------------------------------------------------

    def save_checkpoint(self):

        self.checkpoint.data = {

            "processed":
                self.processed,

            "accepted":
                self.accepted,

            "rejected":
                self.rejected,

            "discoveries":
                self.discoveries,

            "last_checkpoint":
                time.time()

        }

        self.checkpoint.save()

        self.last_checkpoint = time.time()

        self.logger.log(
            "Checkpoint saved."
        )

    # --------------------------------------------------------

    def flush(self):

        self.database.flush()

        self.statistics.export()

    # --------------------------------------------------------

    def process_universe(self):

        universe = self.generator.generate()

        try:

            signature, certificate = (

                self.core.analyse(

                    universe

                )

            )

        except Exception as error:

            self.rejected += 1

            self.processed += 1

            self.logger.log(

                f"CORE ERROR : {error}"

            )

            return

        self.database.append(

            universe,

            signature.to_dict(),

            certificate,

        )

        self.statistics.update(

            signature.to_dict()

        )

        if self.discovery.update(

            signature.to_dict()

        ):

            self.discoveries += 1

            self.logger.log(

                f"NEW SIGNATURE : "

                f"{universe['UniverseID']}"

            )

        self.accepted += 1

        self.processed += 1
        # ============================================================
# MAIN LOOP
# ============================================================

    def run(self):

        self.logger.log(
            "Massive Universe Generator started."
        )

        while self.processed < TOTAL_UNIVERSES:

            self.process_universe()

            # ----------------------------------------------

            if (
                self.accepted > 0
                and
                self.accepted % SAVE_INTERVAL == 0
            ):

                self.flush()

            # ----------------------------------------------

            if (
                self.processed > 0
                and
                self.processed % CHECKPOINT_INTERVAL == 0
            ):

                self.save_checkpoint()

            # ----------------------------------------------

            self.dashboard.update(

                processed=self.processed,

                accepted=self.accepted,

                rejected=self.rejected,

                discoveries=self.discoveries,

                speed=self.speed(),

                elapsed=self.elapsed(),

                eta=self.eta(),

                database_size=self.database_size(),

                current_task="GER CORE → Signature Provider",

                checkpoint_age=self.checkpoint_age()

            )

        self.finish()

    # --------------------------------------------------------

    def finish(self):

        self.flush()

        self.save_checkpoint()

        clear_output(wait=True)

        print("=" * 60)
        print("GER S29-E6.3")
        print("MASSIVE UNIVERSE GENERATOR")
        print("=" * 60)

        print()

        print("EXECUTION FINISHED")

        print()

        print(f"Processed    : {self.processed:,}")
        print(f"Accepted     : {self.accepted:,}")
        print(f"Rejected     : {self.rejected:,}")

        print()

        print(f"Discoveries  : {self.discoveries:,}")

        print()

        print(
            f"Database Size : "
            f"{self.database_size():.2f} MB"
        )

        print()

        print("Database")

        print(" ", DATABASE)

        print()

        self.logger.log(
            "Execution finished."
        )

# ============================================================
# MAIN
# ============================================================

def validate_core():

    """
    Verifica se o CORE está disponível.
    """

    try:

        initialize()

        print("[OK] GER CORE initialized")

    except Exception as error:

        print()

        print("=" * 60)
        print("GER CORE INITIALIZATION FAILED")
        print("=" * 60)

        print()

        raise RuntimeError(error)

# ============================================================

def main():

    print("=" * 60)
    print("GER S29-E6.3")
    print("MASSIVE UNIVERSE GENERATOR")
    print("=" * 60)

    print()

    validate_core()

    print()

    generator = MassiveUniverseGenerator()

    generator.run()

# ============================================================

if __name__ == "__main__":

    main()

# ============================================================
# END
# ============================================================
