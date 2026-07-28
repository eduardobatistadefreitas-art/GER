"""
============================================================

GER
S29-E8

Trajectory Observatory

run.py

PARTE 1

============================================================
"""

from __future__ import annotations

import json
import traceback
from pathlib import Path

from config import *

from storage import ExperimentStorage
from checkpoint import CheckpointManager
from timer import ExperimentTimer

# (serão implementados nas próximas partes)

from trajectory import Trajectory
from metrics import TrajectoryMetrics
from certificate import ExperimentCertificate
from report import ExperimentReport


# ==========================================================
# Banner
# ==========================================================

def banner():

    print()
    print("=" * 60)
    print("GER")
    print(EXPERIMENT_NAME)
    print(EXPERIMENT_TITLE)
    print("=" * 60)
    print()


# ==========================================================
# Inicialização
# ==========================================================

banner()

storage = ExperimentStorage()

storage.initialize()

checkpoint = CheckpointManager(storage)

timer = ExperimentTimer()

trajectory = Trajectory(storage)

metrics = TrajectoryMetrics(storage)

certificate = ExperimentCertificate(storage)

report = ExperimentReport(storage)


# ==========================================================
# Arquivo de configuração
# ==========================================================

configuration = {

    "experiment": EXPERIMENT_NAME,

    "title": EXPERIMENT_TITLE,

    "version": VERSION,

    "parameter_name": PARAMETER_NAME,

    "parameter_start": PARAMETER_START,

    "parameter_stop": PARAMETER_STOP,

    "parameter_step": PARAMETER_STEP,

    "max_states": MAX_STATES,

    "save_every": SAVE_EVERY,

    "checkpoint_every": CHECKPOINT_EVERY,

    "auto_resume": AUTO_RESUME,

    "random_seed": RANDOM_SEED,

}

storage.save_json(

    storage.root / "config.json",

    configuration,

)


# ==========================================================
# Resume
# ==========================================================

start_state = 0

parameter = PARAMETER_START

elapsed = 0.0

if checkpoint.exists():

    if AUTO_RESUME:

        print()

        print("Checkpoint encontrado.")

        data = checkpoint.load()

        start_state = data["state"] + 1

        parameter = data["parameter"] + PARAMETER_STEP

        elapsed = data["elapsed_seconds"]

        print(

            f"Retomando do estado {start_state}"

        )

        print()

else:

    print()

    print("Nova execução.")

    print()


# ==========================================================
# Timer
# ==========================================================

timer.start()

timer.states_completed = start_state


# ==========================================================
# Informações iniciais
# ==========================================================

print("-" * 60)

print("Execution ID :", storage.execution_id)

print("Estados      :", MAX_STATES)

print("Parâmetro    :", PARAMETER_NAME)

print("Inicial      :", parameter)

print("Final        :", PARAMETER_STOP)

print("-" * 60)

print()


# ==========================================================
# Loop principal
# ==========================================================

try:

    for state in range(

        start_state,

        MAX_STATES,

    ):

        if parameter > PARAMETER_STOP:

            break

        # --------------------------------------------
        # O processamento científico será inserido
        # na Parte 2.
        # --------------------------------------------

        # Placeholder temporário

        record = {

            "state": state,

            "parameter": parameter,

        }

        trajectory.append(record)

        timer.update()

          # ==================================================
        # Construção da trajetória
        # ==================================================

        trajectory.append(record)

        # ==================================================
        # Métricas locais
        # ==================================================

        metrics.update(record)

        # ==================================================
        # Salvamento incremental
        # ==================================================

        if (

            state == 0

            or

            state % SAVE_EVERY == 0

        ):

            trajectory.save()

            metrics.save()

        # ==================================================
        # Checkpoint
        # ==================================================

        if (

            state == 0

            or

            state % CHECKPOINT_EVERY == 0

        ):

            checkpoint.save(

                state=state,

                parameter=parameter,

                elapsed=timer.elapsed,

                statistics=timer.benchmark(),

            )

        # ==================================================
        # Dashboard
        # ==================================================

        if SHOW_PROGRESS:

            eta = timer.eta(MAX_STATES)

            print(

                f"\r"

                f"State: {state:8d} | "

                f"{PARAMETER_NAME}: {parameter:.6f} | "

                f"Elapsed: {timer.elapsed:8.1f}s | "

                f"ETA: {eta:8.1f}s | "

                f"States/s: {timer.states_per_second:6.2f}",

                end="",

                flush=True,

            )

        # ==================================================
        # Próximo parâmetro
        # ==================================================

        parameter += PARAMETER_STEP

    print()

    print()

    print("=" * 60)

    print("Execução concluída.")

    print("=" * 60)

except KeyboardInterrupt:

    print()

    print()

    print("Execução interrompida pelo usuário.")

except Exception:

    print()

    print()

    traceback.print_exc()

finally:

    # ======================================================
    # Salvamento final
    # ======================================================

    trajectory.save()

    metrics.save()

    # ======================================================
    # Benchmark
    # ======================================================

    benchmark = timer.benchmark()

    projections = timer.projections()

    storage.save_json(

        storage.file(

            "statistics",

            "benchmark.json",

        ),

        benchmark,

    )

    storage.save_json(

        storage.file(

            "statistics",

            "projection.json",

        ),

        projections,

    )

    # ======================================================
    # Certificado
    # ======================================================

    certificate.generate(

        benchmark=benchmark,

        projections=projections,

        trajectory=trajectory,

        metrics=metrics,

    )

    # ======================================================
    # Relatório
    # ======================================================

    report.generate(

        benchmark=benchmark,

        projections=projections,

        trajectory=trajectory,

        metrics=metrics,

    )

    print()

    print("Resultados salvos em:")

    print(storage.root)

    print()

    print("=" * 60)

    print("S29-E8 finalizado.")

    print("=" * 60)

        # ==================================================
        # GER PIPELINE
        # ==================================================

        #
        # A partir daqui o E8 deixa de ser apenas uma
        # infraestrutura e passa a utilizar o GER.
        #
        # A implementação abaixo pressupõe a existência
        # das APIs oficiais do projeto.
        #

        # ----------------------------------------------
        # 1) Gerar estado do sistema
        # ----------------------------------------------

        simulation = run_engine(

            sigma=parameter,

        )

        # ----------------------------------------------
        # 2) Observatório
        # ----------------------------------------------

        observables = run_persistence_observatory(

            simulation,

        )

        # ----------------------------------------------
        # 3) Assinatura Geométrica
        # ----------------------------------------------

        signature = compute_geometric_signature(

            observables,

            dt=simulation["configuration"]["dt"],

        )

        # ----------------------------------------------
        # 4) Registro científico
        # ----------------------------------------------

        record = {

            "state":
                state,

            "parameter":
                parameter,

            "elapsed":
                timer.elapsed,

            "diameter":
                signature.diameter,

            "convergence":
                signature.convergence,

            "recurrence":
                signature.recurrence,

            "drift":
                signature.drift,

            "signature":
                signature,

            "observables":
                observables,

            "simulation":
                simulation,

        }

        # ----------------------------------------------
        # 5) Trajetória
        # ----------------------------------------------

        trajectory.append(

            record,

        )

        # ----------------------------------------------
        # 6) Métricas locais
        # ----------------------------------------------

        metrics.update(

            trajectory,

        )

        # ----------------------------------------------
        # 7) Salvamento incremental
        # ----------------------------------------------

        if (

            state == 0

            or

            state % SAVE_EVERY == 0

        ):

            trajectory.save()

            metrics.save()

        # ----------------------------------------------
        # 8) Checkpoint
        # ----------------------------------------------

        if (

            state == 0

            or

            state % CHECKPOINT_EVERY == 0

        ):

            checkpoint.save(

                state=state,

                parameter=parameter,

                elapsed=timer.elapsed,

                statistics=timer.benchmark(),

            )

        # ----------------------------------------------
        # 9) Dashboard
        # ----------------------------------------------

        if SHOW_PROGRESS:

            print(

                f"\r"

                f"{state:6d}"

                f" | "

                f"{parameter:.6f}"

                f" | "

                f"D={signature.diameter:.6f}"

                f" "

                f"C={signature.convergence:.6f}"

                f" "

                f"R={signature.recurrence:.6f}"

                f" "

                f"Dr={signature.drift:.6f}"

                f" "

                f"{timer.states_per_second:.2f}"

                f" st/s",

                end="",

                flush=True,

            )

        # ----------------------------------------------
        # 10) Próximo estado
        # ----------------------------------------------

        parameter += PARAMETER_STEP

# ==========================================================
# TRAJECTORY
# (Implementação temporária incorporada ao run.py)
# ==========================================================

import csv
import math


class Trajectory:

    def __init__(self, storage):

        self.storage = storage

        self.records = []

        self.csv_file = storage.file(
            "trajectory",
            "trajectory.csv",
        )

        self.json_file = storage.file(
            "trajectory",
            "trajectory.json",
        )

        self.initialized = False

    # ------------------------------------------------------

    def append(self, record):

        self.records.append(record)

    # ------------------------------------------------------

    def __len__(self):

        return len(self.records)

    # ------------------------------------------------------

    def __getitem__(self, index):

        return self.records[index]

    # ------------------------------------------------------

    def last(self):

        if not self.records:

            return None

        return self.records[-1]

    # ------------------------------------------------------

    def previous(self):

        if len(self.records) < 2:

            return None

        return self.records[-2]

    # ------------------------------------------------------

    def initialize_csv(self):

        if self.initialized:

            return

        with open(

            self.csv_file,

            "w",

            newline="",

            encoding="utf-8",

        ) as fp:

            writer = csv.writer(fp)

            writer.writerow(

                [

                    "State",

                    "Parameter",

                    "Diameter",

                    "Convergence",

                    "Recurrence",

                    "Drift",

                    "Elapsed",

                ]

            )

        self.initialized = True

    # ------------------------------------------------------

    def append_csv(self, record):

        self.initialize_csv()

        with open(

            self.csv_file,

            "a",

            newline="",

            encoding="utf-8",

        ) as fp:

            writer = csv.writer(fp)

            writer.writerow(

                [

                    record["state"],

                    record["parameter"],

                    record["diameter"],

                    record["convergence"],

                    record["recurrence"],

                    record["drift"],

                    record["elapsed"],

                ]

            )

    # ------------------------------------------------------

    def save(self):

        serializable = []

        for r in self.records:

            serializable.append(

                {

                    "state":

                        r["state"],

                    "parameter":

                        r["parameter"],

                    "diameter":

                        r["diameter"],

                    "convergence":

                        r["convergence"],

                    "recurrence":

                        r["recurrence"],

                    "drift":

                        r["drift"],

                    "elapsed":

                        r["elapsed"],

                }

            )

        self.storage.save_json(

            self.json_file,

            serializable,

        )

    # ------------------------------------------------------

    def export_last(self):

        if not self.records:

            return

        self.append_csv(

            self.records[-1]

        )

    # ------------------------------------------------------

    def signature_vector(self, record):

        return [

            record["diameter"],

            record["convergence"],

            record["recurrence"],

            record["drift"],

        ]

    # ------------------------------------------------------

    def displacement(self):

        if len(self.records) < 2:

            return 0.0

        a = self.signature_vector(

            self.records[-2]

        )

        b = self.signature_vector(

            self.records[-1]

        )

        return math.sqrt(

            sum(

                (

                    x - y

                ) ** 2

                for x, y in zip(

                    a,

                    b,

                )

            )

        )

    # ------------------------------------------------------

    def path_length(self):

        if len(self.records) < 2:

            return 0.0

        total = 0.0

        previous = self.records[0]

        for current in self.records[1:]:

            pa = self.signature_vector(previous)

            pb = self.signature_vector(current)

            total += math.sqrt(

                sum(

                    (

                        x - y

                    ) ** 2

                    for x, y in zip(

                        pa,

                        pb,

                    )

                )

            )

            previous = current

        return total

    # ------------------------------------------------------

    def summary(self):

        return {

            "states":

                len(self.records),

            "path_length":

                self.path_length(),

            "last_step":

                self.displacement(),

        }


# ==========================================================
# Pequena alteração no loop principal
#
# Logo após:
#
# trajectory.append(record)
#
# adicionar:
#
# trajectory.export_last()
#
# Assim o CSV é atualizado continuamente e,
# mesmo que o Colab caia, praticamente nada
# é perdido.
# ==========================================================
