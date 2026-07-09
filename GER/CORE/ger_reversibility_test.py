%%writefile GER_CORE/ger_reversibility_test.py

"""
=========================================================
GER CORE
Arquivo : ger_reversibility_test.py
=========================================================

Auditoria rigorosa de reversibilidade temporal.

Método:

1. Evolui o sistema para frente.
2. Captura estado final.
3. Inverte a velocidade.
4. Evolui novamente.
5. Compara com o estado inicial.

Não modifica o motor.
Apenas audita o integrador.
=========================================================
"""

from __future__ import annotations

import numpy as np


from GER_CORE.ger_graph import (
    build_ring_graph,
    spectral_basis,
    gaussian_packet
)


from GER_CORE.ger_engine import (
    initialize_verlet
)


from GER_CORE.ger_potential import (
    Potential
)



# =========================================================
# Norma relativa
# =========================================================

def relative_error(a, b):

    return (
        np.linalg.norm(a - b)
        /
        (np.linalg.norm(a) + 1e-15)
    )



# =========================================================
# Evolução simples Verlet reversível
# =========================================================

def verlet_step(
    gamma,
    gamma_old,
    L,
    beta,
    potential,
    dt
):

    force, _ = Potential.evaluate(
        gamma,
        potential
    )

    acceleration = (
        -(L @ gamma)
        +
        beta * force
    )

    gamma_new = (
        2.0 * gamma
        -
        gamma_old
        +
        dt**2 * acceleration
    )

    return gamma_new



# =========================================================
# Teste principal
# =========================================================

def test_reversibility(
    n=384,
    timesteps=2000,
    dt=5e-5,
    beta=1.0,
    potential="A",
    sigma=0.10
):


    _, L, theta = build_ring_graph(n)


    gamma_initial = gaussian_packet(
        theta,
        sigma=sigma
    )


    gamma = gamma_initial.copy()


    gamma_old = initialize_verlet(
        gamma,
        L,
        beta,
        potential,
        dt
    )


    # -------------------------
    # Evolução para frente
    # -------------------------

    for _ in range(timesteps):

        gamma_new = verlet_step(
            gamma,
            gamma_old,
            L,
            beta,
            potential,
            dt
        )

        gamma_old = gamma
        gamma = gamma_new



    gamma_final = gamma.copy()



    # velocidade aproximada final

    velocity_final = (
        gamma
        -
        gamma_old
    ) / dt



    # reconstrução reversa

    gamma_reverse_old = (
        gamma_final
        +
        dt * velocity_final
    )


    gamma_reverse = gamma_final.copy()



    # -------------------------
    # Evolução reversa
    # -------------------------

    for _ in range(timesteps):

        gamma_new = verlet_step(
            gamma_reverse,
            gamma_reverse_old,
            L,
            beta,
            potential,
            dt
        )

        gamma_reverse_old = gamma_reverse
        gamma_reverse = gamma_new



    error = relative_error(
        gamma_reverse,
        gamma_initial
    )


    return error
