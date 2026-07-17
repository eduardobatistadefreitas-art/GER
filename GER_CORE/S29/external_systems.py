"""
=========================================================
GER
GER_CORE / S29

external_systems.py
=========================================================

Biblioteca de sistemas dinâmicos externos.

Este módulo reúne implementações de sistemas clássicos
utilizados para validação da Geometria Espectral
Relacional.

Responsabilidade
----------------
Gerar séries temporais.

Não conhece:

• GER
• Snapshots
• Observatório
• Assinaturas
• Certificados

=========================================================
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "simulate_duffing",
]

EXTERNAL_SYSTEMS_VERSION = "1.0"


# =========================================================
# Utilitário RK4
# =========================================================

def _rk4_step(f, state, dt):
    """
    Executa um passo do integrador RK4.
    """

    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)

    return state + (dt / 6.0) * (
        k1 +
        2.0 * k2 +
        2.0 * k3 +
        k4
    )


# =========================================================
# Duffing Oscillator
# =========================================================

def simulate_duffing(
    *,
    alpha=-1.0,
    beta=1.0,
    delta=0.20,
    gamma=0.30,
    omega=1.20,
    dt=0.01,
    transient=2000,
    samples=5000,
    x0=0.1,
    v0=0.0,
):
    """
    Simula o oscilador de Duffing.

    Retorna
    -------
    time : ndarray

    signal : ndarray
        Coordenada x(t).
    """

    def field(state):

        x, v, t = state

        dx = v

        dv = (
            -delta * v
            - alpha * x
            - beta * x**3
            + gamma * np.cos(omega * t)
        )

        dt_clock = 1.0

        return np.array([
            dx,
            dv,
            dt_clock,
        ])

    state = np.array([
        x0,
        v0,
        0.0,
    ], dtype=float)

    total = transient + samples

    signal = np.empty(samples)

    time = np.empty(samples)

    index = 0

    for i in range(total):

        state = _rk4_step(
            field,
            state,
            dt,
        )

        if i >= transient:

            signal[index] = state[0]

            time[index] = state[2]

            index += 1

    return time, signal
