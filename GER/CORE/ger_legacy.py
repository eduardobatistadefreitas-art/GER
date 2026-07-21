"""
=========================================================
GER CORE
Arquivo : ger_legacy.py
=========================================================

Legacy execution capture.

Purpose
-------

Automatically captures everything printed to stdout during
legacy experiments (S26, S27, S28, S29...) and saves an
exact copy of the console output.

This module allows all historical experiments to generate
persistent reports without modifying their source code.

Output

GER_RESULTS/

    LEGACY_RESULTS/

        <EXPERIMENT>/

            console_output.txt
"""

from __future__ import annotations

import inspect
import io
import sys
from pathlib import Path


# ==========================================================
# Internal Tee
# ==========================================================

class _Tee(io.TextIOBase):
    """
    Duplicates stdout.

    Everything printed continues to appear in Colab while an
    identical copy is written to disk.
    """

    def __init__(self, terminal, file):

        self._terminal = terminal
        self._file = file

    def write(self, text):

        self._terminal.write(text)
        self._file.write(text)

        return len(text)

    def flush(self):

        self._terminal.flush()
        self._file.flush()


# ==========================================================
# Helpers
# ==========================================================

def _detect_experiment():

    """
    Detects the experiment currently executing.
    """

    for frame in inspect.stack():

        filename = Path(frame.filename)

        if "GER_CORE" in filename.parts:

            return filename.stem

    return "UNKNOWN_EXPERIMENT"


def _results_root():

    """
    Returns GER_RESULTS root.
    """

    return (
        Path("/content/drive/MyDrive")
        / "GER_RESULTS"
        / "LEGACY_RESULTS"
    )


# ==========================================================
# Public API
# ==========================================================

def enable():

    """
    Enables legacy console capture.

    Safe to call multiple times.
    """

    if getattr(enable, "_enabled", False):
        return

    experiment = _detect_experiment()

    folder = _results_root() / experiment
    folder.mkdir(parents=True, exist_ok=True)

    logfile = folder / "console_output.txt"

    terminal = sys.stdout
    file = open(logfile, "w", encoding="utf-8")

    sys.stdout = _Tee(terminal, file)

    enable._enabled = True

    print()
    print("Legacy capture enabled.")
    print(f"Output : {logfile}")
    print()
