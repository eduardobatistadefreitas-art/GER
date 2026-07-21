"""
============================================================
GER CORE

Dashboard

GER — Geometria Espectral Relacional
============================================================

Dashboard padrão do GER.

Objetivos

• Atualização única no Colab
• Sem poluição da saída
• Barra de progresso
• Atualização temporizada
• Layout padronizado

============================================================
"""

from __future__ import annotations

import time

from IPython.display import clear_output


class Dashboard:

    """
    Dashboard padrão do GER.
    """

    # --------------------------------------------------------

    def __init__(

        self,

        title,

        subtitle,

        update_interval=2.0,

    ):

        self.title = title

        self.subtitle = subtitle

        self.update_interval = update_interval

        self.last_update = 0.0

    # --------------------------------------------------------

    def update(

        self,

        progress,

        total,

        elapsed,

        eta,

        sections,

    ):

        now = time.time()

        if (

            now - self.last_update

            <

            self.update_interval

        ):

            return

        self.last_update = now

        clear_output(wait=True)

        percent = (

            100.0

            *

            progress

            /

            max(total, 1)

        )

        bars = int(percent / 2)

        bars = max(

            0,

            min(

                50,

                bars,

            ),

        )

        print("=" * 60)
        print(self.title)
        print(self.subtitle)
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

        for section, values in sections.items():

            print("-" * 60)
            print(section)
            print("-" * 60)

            for key, value in values.items():

                print(f"{key:<12}: {value}")

            print()

    # --------------------------------------------------------

    def finish(

        self,

        sections,

    ):

        clear_output(wait=True)

        print("=" * 60)
        print(self.title)
        print(self.subtitle)
        print("=" * 60)

        print()

        print("EXECUTION FINISHED")

        print()

        for section, values in sections.items():

            print(section)

            for key, value in values.items():

                print(f"{key:<12}: {value}")

            print()
