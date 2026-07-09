%%writefile GER_CORE/ger_engine.py

"""
=========================================================
GER CORE
Arquivo : ger_engine.py
=========================================================

Motor temporal principal da Geometria Espectral Relacional.

Responsável pela evolução dinâmica do campo gamma.

Método de integração:
Verlet de segunda ordem.

O motor apenas coordena os módulos:
- ger_graph
- ger_potential
- ger_metrics
- ger_snapshot
"""

from __future__ import annotations

import numpy as np


from ger_graph import (
    build_ring_graph,
    spectral_basis,
    gaussian_packet
)


from ger_potential import (
    Potential
)


from ger_metrics import (
    compute_hamiltonian,
    relative_energy_error,
    check_divergence
)


from ger_snapshot import (
    build_snapshot
)



# =========================================================
# Inicialização Verlet
# =========================================================

def initialize_verlet(
    gamma,
    laplacian,
    beta,
    potential,
    dt
):
    """
    Primeiro passo reversível do integrador.
    """

    force, _ = Potential.evaluate(
        gamma,
        potential
    )

    acceleration = (
        -(laplacian @ gamma)
        +
        beta * force
    )

    return (
        gamma
        -
        0.5 * dt**2 * acceleration
    )



# =========================================================
# MOTOR PRINCIPAL
# =========================================================

def run_engine(
    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    sigma=0.10
):

    """
    Executa uma simulação completa GER.

    Retorna todos os dados necessários
    para auditorias posteriores.
    """


    # -----------------------------
    # Geometria
    # -----------------------------

    _, L, theta = build_ring_graph(n)


    eigenvalues, eigenvectors = (
        spectral_basis(L)
    )


    # -----------------------------
    # Condição inicial
    # -----------------------------

    gamma = gaussian_packet(
        theta,
        sigma=sigma
    )


    gamma_old = initialize_verlet(
        gamma,
        L,
        beta,
        potential,
        dt
    )


    velocity = (
        gamma - gamma_old
    ) / dt


    energy_initial = compute_hamiltonian(
        gamma,
        velocity,
        L,
        beta,
        potential
    )


    snapshots = []

    diverged = False



    # -----------------------------
    # Evolução temporal
    # -----------------------------

    for step in range(timesteps):


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


        velocity = (
            gamma_new
            -
            gamma_old
        ) / (2.0 * dt)



        energy = compute_hamiltonian(
            gamma,
            velocity,
            L,
            beta,
            potential
        )


        error = relative_energy_error(
            energy_initial,
            energy
        )


        if check_divergence(
            gamma,
            error
        ):

            diverged = True



        if (
            step % snapshot_stride == 0
            or step == timesteps - 1
        ):

            snap = build_snapshot(
                step,
                step * dt,
                gamma,
                velocity,
                L,
                beta,
                potential,
                eigenvectors,
                theta
            )


            snap["energy_error"] = error


            snapshots.append(
                snap
            )



        gamma_old = gamma

        gamma = gamma_new



    # -----------------------------
    # Estado final
    # -----------------------------

    final_velocity = (
        gamma - gamma_old
    ) / dt


    final_energy = compute_hamiltonian(
        gamma,
        final_velocity,
        L,
        beta,
        potential
    )


    final_error = relative_energy_error(
        energy_initial,
        final_energy
    )


    return {

        "configuration": {

            "n": n,

            "dt": dt,

            "timesteps": timesteps,

            "beta": beta,

            "potential": potential
        },


        "initial": {

            "energy":
                energy_initial
        },


        "final": {

            "energy":
                final_energy,

            "energy_error":
                final_error
        },


        "snapshots":
            snapshots,


        "gamma":
            gamma,


        "laplacian":
            L,


        "eigenvalues":
            eigenvalues,


        "eigenvectors":
            eigenvectors,


        "diverged":
            diverged
    }
