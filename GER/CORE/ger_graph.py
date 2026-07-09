"""
=========================================================
GER CORE
Arquivo : ger_graph.py
=========================================================

Geometria discreta da Geometria Espectral Relacional.

Este módulo implementa:

• Grafo periódico F₁
• Laplaciano discreto
• Base espectral
• Distância periódica
• Pacotes gaussianos iniciais

Todas as funções aqui são independentes da dinâmica.
"""

from __future__ import annotations

import numpy as np
import scipy.linalg as la


# =========================================================
# Construção do Grafo
# =========================================================

def build_ring_graph(n: int):
    """
    Constrói o grafo periódico F₁.

    Parameters
    ----------
    n : int
        Número de vértices.

    Returns
    -------
    adjacency : ndarray
        Matriz de adjacência.

    laplacian : ndarray
        Laplaciano discreto.

    theta : ndarray
        Coordenadas angulares dos vértices.
    """

    if n < 3:
        raise ValueError(
            "O grafo periódico deve possuir pelo menos 3 vértices."
        )

    adjacency = np.zeros((n, n))

    for i in range(n):

        adjacency[i, (i + 1) % n] = 1.0
        adjacency[i, (i - 1) % n] = 1.0

    degree = np.diag(np.sum(adjacency, axis=1))

    laplacian = degree - adjacency

    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        n,
        endpoint=False
    )

    return adjacency, laplacian, theta


# =========================================================
# Base Espectral
# =========================================================

def spectral_basis(laplacian):
    """
    Calcula a base espectral do Laplaciano.

    Parameters
    ----------
    laplacian : ndarray

    Returns
    -------
    eigenvalues : ndarray

    eigenvectors : ndarray
    """

    eigenvalues, eigenvectors = la.eigh(laplacian)

    eigenvalues[np.abs(eigenvalues) < 1e-12] = 0.0

    return eigenvalues, eigenvectors


# =========================================================
# Distância Periódica
# =========================================================

def periodic_distance(theta, center):
    """
    Distância angular mínima em uma circunferência.

    Parameters
    ----------
    theta : ndarray

    center : float

    Returns
    -------
    ndarray
    """

    delta = np.abs(theta - center)

    return np.minimum(
        delta,
        2.0 * np.pi - delta
    )


# =========================================================
# Pacote Inicial
# =========================================================

def gaussian_packet(
    theta,
    center=np.pi,
    sigma=0.10
):
    """
    Constrói um pacote gaussiano periódico.

    Parameters
    ----------
    theta : ndarray

    center : float

    sigma : float

    Returns
    -------
    gamma : ndarray
    """

    distance = periodic_distance(
        theta,
        center
    )

    gamma = np.exp(
        -(distance ** 2) /
        (2.0 * sigma ** 2)
    )

    gamma /= np.max(gamma)

    return gamma
