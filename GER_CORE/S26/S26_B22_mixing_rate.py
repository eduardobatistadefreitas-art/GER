"""
=========================================================
GER CORE
S26-B.2.2

Taxa de Mistura Espectral

=========================================================

Esta auditoria calcula as taxas temporais das principais
grandezas espectrais produzidas pelo Observatório GER.

Não executa simulações.

Recebe apenas o histórico produzido pela auditoria
S26_B21_modal_transfer.

=========================================================
"""

from __future__ import annotations

import numpy as np


# =========================================================
# Derivada temporal simples
# ==========================================================
def temporal_derivative(values, times):
    """
    Calcula dX/dt por diferenças finitas.
    """

    values = np.asarray(values, dtype=float)
    times = np.asarray(times, dtype=float)

    derivative = np.zeros_like(values)

    derivative[0] = 0.0

    for i in range(1, len(values)):

        dt = times[i] - times[i - 1]

        if dt == 0.0:

            derivative[i] = 0.0

        else:

            derivative[i] = (
                values[i] - values[i - 1]
            ) / dt

    return derivative


# =========================================================
# Auditoria principal
# ==========================================================
def compute_mixing_rate(history):
    """
    Calcula as taxas temporais da mistura espectral.
    """

    time = np.array([
        h["time"]
        for h in history
    ])

    entropy = np.array([
        h["entropy"]
        for h in history
    ])

    width = np.array([
        h["modal_width"]
        for h in history
    ])

    participation = np.array([
        h["participation"]
        for h in history
    ])

    dSdt = temporal_derivative(
        entropy,
        time
    )

    dWdt = temporal_derivative(
        width,
        time
    )

    dPRdt = temporal_derivative(
        participation,
        time
    )

    result = []

    for i in range(len(history)):

        result.append({

            "step":
                history[i]["step"],

            "time":
                history[i]["time"],

            "dSdt":
                dSdt[i],

            "dWdt":
                dWdt[i],

            "dPRdt":
                dPRdt[i]

        })

    return result


# =========================================================
# Impressão resumida
# ==========================================================
def print_mixing_rate(result):

    for r in result:

        print(

            f"step: {r['step']:5d}"

            f" | dS/dt: {r['dSdt']:.6e}"

            f" | dW/dt: {r['dWdt']:.6e}"

            f" | dPR/dt: {r['dPRdt']:.6e}"

        )
