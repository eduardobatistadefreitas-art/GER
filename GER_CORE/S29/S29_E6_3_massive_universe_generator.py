"""
============================================================
GER S29-E6.3

MASSIVE UNIVERSE GENERATOR

GER — Geometria Espectral Relacional
============================================================

Objetivos
---------

Gerar milhões de universos relacionais independentes,
armazenando permanentemente:

• Universo
• Assinatura espectral
• Observáveis
• Região geométrica
• Classe geométrica
• Índice de novidade

O experimento foi projetado para execução contínua
por muitas horas ou dias.

Características

✓ Checkpoint automático
✓ Banco incremental
✓ Salvamento em lote
✓ Dashboard único (sem crescimento do terminal)
✓ Recuperação automática
✓ Detector de novidades
✓ Estatísticas em tempo real

============================================================
"""

import os
import sys
import json
import math
import time
import random
import shutil

from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

from scipy.stats import entropy

from IPython.display import clear_output

# ============================================================
# CONFIGURAÇÃO
# ============================================================

RANDOM_SEED = 42

TOTAL_UNIVERSES = 5_000_000

SAVE_BATCH = 5000

CHECKPOINT_INTERVAL = 5000

DASHBOARD_INTERVAL = 2.0

STATISTICS_INTERVAL = 50000

NOVELTY_THRESHOLD = 0.025

MIN_VERTICES = 8
MAX_VERTICES = 64

MIN_EDGES = 10
MAX_EDGES = 256

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
OBSERVABLE_DIR = DATABASE / "observables"
REGION_DIR = DATABASE / "regions"
NOVELTY_DIR = DATABASE / "novelty"

CHECKPOINT_DIR = DATABASE / "checkpoints"
STATISTICS_DIR = DATABASE / "statistics"
LOG_DIR = DATABASE / "logs"
TMP_DIR = DATABASE / "tmp"

for directory in [

    DATABASE,

    UNIVERSE_DIR,
    SIGNATURE_DIR,
    OBSERVABLE_DIR,
    REGION_DIR,
    NOVELTY_DIR,

    CHECKPOINT_DIR,
    STATISTICS_DIR,
    LOG_DIR,
    TMP_DIR

]:

    directory.mkdir(
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

OBSERVABLE_FILE = (
    OBSERVABLE_DIR /
    "observables.parquet"
)

REGION_FILE = (
    REGION_DIR /
    "regions.parquet"
)

NOVELTY_FILE = (
    NOVELTY_DIR /
    "novelty.parquet"
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

        classes,

        new_classes,

        discoveries,

        speed,

        eta,

        elapsed,

        db_size,

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

        print("=" * 60)
        print("GER S29-E6.3")
        print("MASSIVE UNIVERSE GENERATOR")
        print("=" * 60)

        print()

        percent = (
            processed /
            TOTAL_UNIVERSES
        ) * 100

        bars = int(percent / 2)

        print(

            "["

            + "█" * bars

            + "░" * (50 - bars)

            + "]"

            + f" {percent:6.2f}%"

        )

        print()

        print(
            f"Elapsed : {elapsed}"
        )

        print(
            f"ETA     : {eta}"
        )

        print()

        print("-" * 60)
        print("Universes")
        print("-" * 60)

        print(
            f"Generated : {processed:,}"
        )

        print(
            f"Accepted  : {accepted:,}"
        )

        print(
            f"Rejected  : {rejected:,}"
        )

        print()

        print(
            f"Speed : {speed:,.1f} universe/s"
        )

        print()

        print("-" * 60)
        print("Discovery")
        print("-" * 60)

        print(
            f"Known Classes : {classes:,}"
        )

        print(
            f"New Classes   : {new_classes:,}"
        )

        print(
            f"Novel Worlds  : {discoveries:,}"
        )

        print()

        print("-" * 60)
        print("Database")
        print("-" * 60)

        print(
            f"Size : {db_size:.2f} MB"
        )

        print(
            f"Checkpoint : {checkpoint_age}"
        )

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

            "classes":0,

            "discoveries":0,

            "new_classes":0,

            "last_checkpoint":time.time()

        }

    # --------------------------------------------------------

    def exists(self):

        return CHECKPOINT_FILE.exists()

    # --------------------------------------------------------

    def load(self):

        with open(
            CHECKPOINT_FILE,
            "r"
        ) as f:

            self.data = json.load(f)

    # --------------------------------------------------------

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
# DATABASE WRITER
# ============================================================

class DatabaseWriter:

    def __init__(self):

        self.universes = []

        self.signatures = []

        self.observables = []

        self.regions = []

        self.novelty = []

    # --------------------------------------------------------

    def append(

        self,

        universe,

        signature,

        observables,

        region,

        novelty

    ):

        self.universes.append(
            universe
        )

        self.signatures.append(
            signature
        )

        self.observables.append(
            observables
        )

        self.regions.append(
            region
        )

        self.novelty.append(
            novelty
        )
      # ============================================================
# DATABASE WRITER (continuação)
# ============================================================

    def flush(self):

        self._append_parquet(
            UNIVERSE_FILE,
            self.universes
        )

        self._append_parquet(
            SIGNATURE_FILE,
            self.signatures
        )

        self._append_parquet(
            OBSERVABLE_FILE,
            self.observables
        )

        self._append_parquet(
            REGION_FILE,
            self.regions
        )

        self._append_parquet(
            NOVELTY_FILE,
            self.novelty
        )

        self.universes.clear()
        self.signatures.clear()
        self.observables.clear()
        self.regions.clear()
        self.novelty.clear()

    # --------------------------------------------------------

    def _append_parquet(
        self,
        file,
        rows
    ):

        if len(rows) == 0:
            return

        df = pd.DataFrame(rows)

        if file.exists():

            old = pd.read_parquet(file)

            df = pd.concat(
                [old, df],
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
    Primeira implementação.

    Gera grafos relacionais aleatórios.

    Futuramente poderá ser substituído por:

        • Erdős-Rényi
        • Watts-Strogatz
        • Barabási-Albert
        • Scale-Free
        • Small World
        • Regular
        • Hierárquicos
        • GER Native
    """

    def __init__(self):

        self.identifier = 0

    # --------------------------------------------------------

    def generate(self):

        self.identifier += 1

        vertices = random.randint(
            MIN_VERTICES,
            MAX_VERTICES
        )

        edges = random.randint(
            MIN_EDGES,
            MAX_EDGES
        )

        density = edges / max(
            vertices * (vertices - 1) / 2,
            1
        )

        adjacency = np.random.randint(

            0,

            2,

            (vertices, vertices)

        )

        adjacency = np.triu(
            adjacency,
            1
        )

        adjacency = (
            adjacency +
            adjacency.T
        )

        return {

            "UniverseID":self.identifier,

            "Vertices":vertices,

            "Edges":edges,

            "Density":density,

            "Adjacency":adjacency.tolist()

        }

# ============================================================
# SIGNATURE ENGINE
# ============================================================

class SignatureEngine:

    """
    Placeholder.

    Na integração definitiva,
    este módulo chamará diretamente
    o núcleo do GER.
    """

    def compute(

        self,

        universe

    ):

        vertices = universe["Vertices"]

        edges = universe["Edges"]

        density = universe["Density"]

        diameter = (
            vertices /
            np.sqrt(edges)
        )

        convergence = (
            density *
            random.uniform(
                0.5,
                1.5
            )
        )

        recurrence = random.random()

        harmonic = (
            convergence /
            (
                recurrence +
                0.001
            )
        )

        return {

            "Diameter":diameter,

            "Convergence":convergence,

            "Recurrence":recurrence,

            "Harmonic":harmonic

        }

# ============================================================
# OBSERVABLES
# ============================================================

class ObservableExtractor:

    def extract(

        self,

        universe,

        signature

    ):

        entropy_value = entropy(

            np.random.rand(32)

        )

        average_degree = (

            2 *
            universe["Edges"]

        ) / universe["Vertices"]

        return {

            "Vertices":
                universe["Vertices"],

            "Edges":
                universe["Edges"],

            "Density":
                universe["Density"],

            "AverageDegree":
                average_degree,

            "Diameter":
                signature["Diameter"],

            "Convergence":
                signature["Convergence"],

            "Recurrence":
                signature["Recurrence"],

            "Harmonic":
                signature["Harmonic"],

            "Entropy":
                entropy_value

        }

# ============================================================
# REGION CLASSIFIER
# ============================================================

class RegionClassifier:

    """
    Classificação provisória.

    Depois será substituída
    pela classificação geométrica
    produzida pelo próprio GER.
    """

    def classify(

        self,

        observables

    ):

        d = observables["Diameter"]

        c = observables["Convergence"]

        r = observables["Recurrence"]

        key = (

            int(d * 5),

            int(c * 10),

            int(r * 10)

        )

        return str(key)

# ============================================================
# NOVELTY DETECTOR
# ============================================================

class NoveltyDetector:

    """
    Detector incremental.

    Guarda apenas os centroides
    das assinaturas conhecidas.
    """

    def __init__(self):

        self.reference = []

        self.class_count = 0

    # --------------------------------------------------------

    def evaluate(

        self,

        signature

    ):

        vector = np.array([

            signature["Diameter"],

            signature["Convergence"],

            signature["Recurrence"],

            signature["Harmonic"]

        ])

        if len(self.reference) == 0:

            self.reference.append(vector)

            self.class_count += 1

            return 1.0, True

        distances = [

            np.linalg.norm(

                vector - x

            )

            for x in self.reference

        ]

        minimum = min(distances)

        novelty = minimum / (
            1.0 + minimum
        )

        if novelty > NOVELTY_THRESHOLD:

            self.reference.append(vector)

            self.class_count += 1

            return novelty, True

        return novelty, False
      # ============================================================
# STATISTICS
# ============================================================

class Statistics:

    def __init__(self):

        self.rows = []

    # --------------------------------------------------------

    def update(self, observables):

        self.rows.append(observables)

    # --------------------------------------------------------

    def export(self):

        if len(self.rows) == 0:
            return

        df = pd.DataFrame(self.rows)

        summary = df.describe().T

        summary.to_csv(

            STATISTICS_DIR /
            "summary.csv"

        )

        correlation = df.corr(
            numeric_only=True
        )

        correlation.to_csv(

            STATISTICS_DIR /
            "correlation.csv"

        )

# ============================================================
# LOGGER
# ============================================================

class EventLogger:

    def __init__(self):

        self.file = LOG_FILE

    # --------------------------------------------------------

    def log(self, text):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(

            self.file,

            "a",

            encoding="utf-8"

        ) as f:

            f.write(
                f"[{now}] {text}\n"
            )

# ============================================================
# MASSIVE UNIVERSE ENGINE
# ============================================================

class MassiveUniverseGenerator:

    def __init__(self):

        self.dashboard = Dashboard()

        self.generator = UniverseGenerator()

        self.signature = SignatureEngine()

        self.extractor = ObservableExtractor()

        self.classifier = RegionClassifier()

        self.novelty = NoveltyDetector()

        self.statistics = Statistics()

        self.database = DatabaseWriter()

        self.logger = EventLogger()

        self.checkpoint = Checkpoint()

        if self.checkpoint.exists():

            self.checkpoint.load()

            self.logger.log(
                "Checkpoint restored."
            )

        data = self.checkpoint.data

        self.processed = data["processed"]
        self.accepted = data["accepted"]
        self.rejected = data["rejected"]

        self.discoveries = data["discoveries"]
        self.new_classes = data["new_classes"]

        self.start_time = time.time()

        self.last_checkpoint = time.time()

    # --------------------------------------------------------

    def elapsed(self):

        seconds = int(

            time.time() -
            self.start_time

        )

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        return f"{h:02}:{m:02}:{s:02}"

    # --------------------------------------------------------

    def eta(self):

        if self.processed == 0:

            return "--:--:--"

        elapsed = (

            time.time() -
            self.start_time

        )

        remaining = (

            TOTAL_UNIVERSES -
            self.processed

        )

        speed = self.processed / elapsed

        if speed <= 0:

            return "--:--:--"

        seconds = int(
            remaining / speed
        )

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        return f"{h:02}:{m:02}:{s:02}"

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

        dt = int(

            time.time() -

            self.last_checkpoint

        )

        return f"{dt} s"

    # --------------------------------------------------------

    def save_checkpoint(self):

        self.checkpoint.data = {

            "processed":self.processed,

            "accepted":self.accepted,

            "rejected":self.rejected,

            "classes":self.novelty.class_count,

            "discoveries":self.discoveries,

            "new_classes":self.new_classes,

            "last_checkpoint":time.time()

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

    def process(self):

        universe = self.generator.generate()

        signature = self.signature.compute(

            universe

        )

        observables = self.extractor.extract(

            universe,

            signature

        )

        region = self.classifier.classify(

            observables

        )

        novelty_score, discovered = (

            self.novelty.evaluate(

                signature

            )

        )

        self.database.append(

            universe,

            signature,

            observables,

            region,

            {

                "UniverseID":
                    universe["UniverseID"],

                "Novelty":
                    novelty_score,

                "Discovered":
                    discovered

            }

        )

        self.statistics.update(
            observables
        )

        self.processed += 1
        self.accepted += 1

        if discovered:

            self.discoveries += 1
            self.new_classes += 1

            self.logger.log(

                f"NEW CLASS | "

                f"Universe={universe['UniverseID']} "

                f"Novelty={novelty_score:.5f}"

            )

        if (
            self.accepted %
            SAVE_BATCH
            ==
            0
        ):

            self.flush()

        if (
            self.processed %
            CHECKPOINT_INTERVAL
            ==
            0
        ):

            self.save_checkpoint()

        elapsed_seconds = (

            time.time() -
            self.start_time

        )

        speed = (

            self.processed /

            max(
                elapsed_seconds,
                1e-9
            )

        )

        self.dashboard.update(

            processed=self.processed,

            accepted=self.accepted,

            rejected=self.rejected,

            classes=self.novelty.class_count,

            new_classes=self.new_classes,

            discoveries=self.discoveries,

            speed=speed,

            eta=self.eta(),

            elapsed=self.elapsed(),

            db_size=self.database_size(),

            current_task="Generating relational universes...",

            checkpoint_age=self.checkpoint_age()

        )
      # ============================================================
# MAIN LOOP
# ============================================================

    def run(self):

        self.logger.log(
            "Massive Universe Generator started."
        )

        while self.processed < TOTAL_UNIVERSES:

            self.process()

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

        print(f"Generated Universes : {self.processed:,}")
        print(f"Accepted            : {self.accepted:,}")
        print(f"Rejected            : {self.rejected:,}")

        print()

        print(f"Known Classes       : {self.novelty.class_count:,}")
        print(f"New Discoveries     : {self.discoveries:,}")

        print()

        print(f"Database Size       : {self.database_size():.2f} MB")

        print()

        print("Database")

        print(" ", DATABASE)

        print()

        self.logger.log(
            "Execution finished."
        )

# ============================================================
# ENTRY POINT
# ============================================================

def main():

    print()

    print("=" * 60)
    print("INITIALIZING MASSIVE UNIVERSE GENERATOR")
    print("=" * 60)

    print()

    engine = MassiveUniverseGenerator()

    engine.run()

# ============================================================

if __name__ == "__main__":

    main()

# ============================================================
# END
# ============================================================
