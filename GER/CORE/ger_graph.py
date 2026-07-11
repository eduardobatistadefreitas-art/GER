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
        2.0*np.pi,
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
    sigma=0.10
):
    """
    Pulso gaussiano inicial.
    """

    return np.exp(
        -(theta-center)**2
        /
        (2*sigma**2)
    )
