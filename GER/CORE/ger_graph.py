"""
=========================================================
GER CORE
Arquivo : ger_graph.py
=========================================================

Módulo de construção geométrica.

Responsável por:

- Grafo periódico F1
- Matriz Laplaciana
- Coordenadas angulares
- Base espectral
- Condição inicial gaussiana
- Operador Canônico da Família 2
"""

from __future__ import annotations

import numpy as np
import scipy.linalg as la


# =========================================================
# Construção da rede
# =========================================================

def build_ring_graph(n):
    """
    Constrói o grafo periódico F1.

    Retorna:

    A:
        matriz de adjacência

    L:
        Laplaciano discreto

    theta:
        coordenadas angulares
    """

    A = np.zeros((n, n))

    for i in range(n):

        A[i, (i + 1) % n] = 1.0
        A[i, (i - 1) % n] = 1.0

    D = np.diag(
        np.sum(A, axis=1)
    )

    L = D - A

    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        n,
        endpoint=False
    )

    return A, L, theta


# =========================================================
# Base espectral
# =========================================================

def spectral_basis(L):
    """
    Diagonalização do Laplaciano.
    """

    eigenvalues, eigenvectors = la.eigh(L)

    eigenvalues[
        np.abs(eigenvalues) < 1e-12
    ] = 0.0

    return eigenvalues, eigenvectors


# =========================================================
# Condição inicial
# =========================================================

def gaussian_packet(
    theta,
    center=np.pi,
    sigma=0.10,
    omega=0.0,
):
    """
    Pulso gaussiano inicial.

    Parameters
    ----------
    theta :
        Coordenadas angulares.

    center :
        Centro do pacote.

    sigma :
        Largura do pacote.

    omega :
        Parâmetro de deformação da Família 2.

        omega = 0
            Recupera exatamente o comportamento da Família 1.

        omega != 0
            Produz a deformação canônica

                σ → σ(1 + ω)
    """

    sigma_eff = sigma * (1.0 + omega)

    if sigma_eff <= 0.0:

        raise ValueError(
            "Effective sigma must be positive."
        )

    return np.exp(

        -(theta - center) ** 2

        /

        (2.0 * sigma_eff ** 2)

    )


# =========================================================
# Operador Canônico - Família 2
# =========================================================

def gaussian_packet_family2(
    theta,
    center=np.pi,
    sigma=0.10,
    omega=0.0,
):
    """
    Operador Canônico da Família 2.

    Alias explícito da implementação oficial do GER CORE.

    U₂(ω):

        σ → σ(1 + ω)

    Mantém compatibilidade total com a Família 1 quando
    omega = 0.
    """

    return gaussian_packet(

        theta=theta,

        center=center,

        sigma=sigma,

        omega=omega,

    )
