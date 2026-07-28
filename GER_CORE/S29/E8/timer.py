"""
============================================================

GER
S29-E8

Trajectory Observatory

timer.py

============================================================

Temporizador oficial do experimento.

Responsabilidades
-----------------

• Tempo total
• Tempo por estado
• Estados por segundo
• ETA
• Benchmark
• Estatísticas de desempenho

============================================================
"""

from __future__ import annotations

import time


class ExperimentTimer:

    def __init__(self):

        self.start_time = None

        self.last_time = None

        self.states_completed = 0

    # ======================================================
    # Início
    # ======================================================

    def start(self):

        now = time.perf_counter()

        self.start_time = now

        self.last_time = now

    # ======================================================
    # Estado concluído
    # ======================================================

    def update(self):

        self.states_completed += 1

        self.last_time = time.perf_counter()

    # ======================================================
    # Tempo total
    # ======================================================

    @property
    def elapsed(self):

        return (
            time.perf_counter()
            - self.start_time
        )

    # ======================================================
    # Tempo médio
    # ======================================================

    @property
    def average_time(self):

        if self.states_completed == 0:

            return 0.0

        return (
            self.elapsed
            / self.states_completed
        )

    # ======================================================
    # Estados por segundo
    # ======================================================

    @property
    def states_per_second(self):

        if self.elapsed == 0:

            return 0.0

        return (
            self.states_completed
            / self.elapsed
        )

    # ======================================================
    # ETA
    # ======================================================

    def eta(
        self,
        total_states,
    ):

        remaining = (

            total_states

            - self.states_completed

        )

        return (

            remaining

            * self.average_time

        )

    # ======================================================
    # Benchmark
    # ======================================================

    def benchmark(self):

        return {

            "states_completed":

                self.states_completed,

            "elapsed_seconds":

                self.elapsed,

            "average_time_per_state":

                self.average_time,

            "states_per_second":

                self.states_per_second,

        }

    # ======================================================
    # Projeções
    # ======================================================

    def projections(

        self,

        targets=(

            10000,

            25000,

            50000,

            100000,

            250000,

        ),

    ):

        avg = self.average_time

        result = {}

        for n in targets:

            result[str(n)] = (

                n * avg

            )

        return result
