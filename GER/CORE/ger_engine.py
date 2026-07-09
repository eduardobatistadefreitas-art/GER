%%writefile GER_CORE/ger_engine.py
"""
=========================================================
GER CORE
Arquivo : ger_engine.py
=========================================================

Motor numérico principal da Geometria Espectral Relacional.

Responsabilidades
-----------------

• Construção da geometria
• Inicialização do integrador Verlet
• Evolução temporal
• Auditoria automática
• Geração dos snapshots
• Retorno completo da simulação

Versão
-------

GER CORE v1.0
"""

from __future__ import annotations

import numpy as np

from GER_CORE.ger_graph import (
    build_ring_graph,
    spectral_basis,
    gaussian_packet,
)

from GER_CORE.ger_metrics import (
    compute_hamiltonian,
    relative_energy_error,
    check_divergence,
)

from GER_CORE.ger_modal import (
    build_snapshot,
)

from GER_CORE.ger_potential import (
    Potential,
)


# =========================================================
# Inicialização do integrador de Verlet
# =========================================================

def initialize_verlet(
    gamma,
    laplacian,
    beta,
    potential,
    dt,
):
    """
    Constrói o estado anterior necessário pelo
    esquema de Verlet.

    Parameters
    ----------
    gamma : ndarray
        Campo inicial.

    laplacian : ndarray
        Laplaciano da rede.

    beta : float
        Intensidade da não linearidade.

    potential : str
        Identificador do potencial.

    dt : float
        Passo temporal.
    """

    force, _ = Potential.evaluate(
        gamma,
        potential,
    )

    acceleration = (
        -(laplacian @ gamma)
        + beta * force
    )

    gamma_old = (
        gamma
        - 0.5 * dt**2 * acceleration
    )

    return gamma_old


# =========================================================
# Velocidade central
# =========================================================

def central_velocity(
    gamma_new,
    gamma_old,
    dt,
):
    """
    Aproximação centrada da velocidade.
    """

    return (
        gamma_new - gamma_old
    ) / (2.0 * dt)
    # =========================================================
# Motor principal
# =========================================================

def run_engine(
    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    sigma=0.10,
):
    """
    Executa uma simulação completa da Geometria
    Espectral Relacional.

    Retorna um dicionário contendo todos os dados
    necessários para auditorias posteriores.
    """

    # -----------------------------------------------------
    # Construção da geometria
    # -----------------------------------------------------

    _, laplacian, theta = build_ring_graph(n)

    eigenvalues, eigenvectors = spectral_basis(
        laplacian
    )

    # -----------------------------------------------------
    # Condição inicial
    # -----------------------------------------------------

    gamma = gaussian_packet(
        theta,
        center=np.pi,
        sigma=sigma,
    )

    gamma_old = initialize_verlet(
        gamma=gamma,
        laplacian=laplacian,
        beta=beta,
        potential=potential,
        dt=dt,
    )

    velocity = central_velocity(
        gamma,
        gamma_old,
        dt,
    )

    energy_initial = compute_hamiltonian(
        gamma=gamma,
        velocity=velocity,
        laplacian=laplacian,
        beta=beta,
        potential=potential,
    )

    snapshots = []

    diverged = False

    # -----------------------------------------------------
    # Evolução temporal
    # -----------------------------------------------------

    for step in range(timesteps):

        force, _ = Potential.evaluate(
            gamma,
            potential,
        )

        acceleration = (
            -(laplacian @ gamma)
            + beta * force
        )

        gamma_new = (
            2.0 * gamma
            - gamma_old
            + dt**2 * acceleration
        )

        velocity = central_velocity(
            gamma_new,
            gamma_old,
            dt,
        )
                # -------------------------------------------------
        # Auditoria energética
        # -------------------------------------------------

        energy = compute_hamiltonian(
            gamma=gamma_new,
            velocity=velocity,
            laplacian=laplacian,
            beta=beta,
            potential=potential,
        )

        energy_error = relative_energy_error(
            energy_initial,
            energy,
        )

        if check_divergence(
            gamma_new,
            energy_error,
        ):
            diverged = True

        # -------------------------------------------------
        # Snapshot
        # -------------------------------------------------

        if (
            step % snapshot_stride == 0
            or step == timesteps - 1
        ):

            snapshot = build_snapshot(
                step=step,
                time=step * dt,
                gamma=gamma_new,
                velocity=velocity,
                laplacian=laplacian,
                beta=beta,
                potential=potential,
                eigenvectors=eigenvectors,
                theta=theta,
            )

            snapshot["energy_error"] = energy_error

            snapshots.append(snapshot)

        # -------------------------------------------------
        # Atualização temporal
        # -------------------------------------------------

        gamma_old = gamma
        gamma = gamma_new
            # -----------------------------------------------------
    # Estado final
    # -----------------------------------------------------

    final_velocity = central_velocity(
        gamma,
        gamma_old,
        dt,
    )

    final_energy = compute_hamiltonian(
        gamma=gamma,
        velocity=final_velocity,
        laplacian=laplacian,
        beta=beta,
        potential=potential,
    )

    final_error = relative_energy_error(
        energy_initial,
        final_energy,
    )

    # -----------------------------------------------------
    # Retorno
    # -----------------------------------------------------

    return {

        "configuration": {

            "n": n,
            "dt": dt,
            "timesteps": timesteps,
            "beta": beta,
            "potential": potential,
            "sigma": sigma,

        },

        "initial": {

            "energy": energy_initial,

        },

        "final": {

            "energy": final_energy,
            "energy_error": final_error,

        },

        "snapshots": snapshots,

        "gamma": gamma,

        "laplacian": laplacian,

        "eigenvalues": eigenvalues,

        "eigenvectors": eigenvectors,

        "diverged": diverged,

        }
