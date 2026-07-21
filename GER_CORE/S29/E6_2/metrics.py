# ============================================================
# RSG
#
# S29-E6.2
#
# metrics.py
#
# Metric operators for the Relational Signature Space.
#
# These functions operate exclusively on a SignatureCollection
# and contain no I/O or reporting logic.
#
# ============================================================

from __future__ import annotations

import numpy as np


# ============================================================
# Internal utilities
# ============================================================


def _signature_matrix(collection):
    """
    Converts a SignatureCollection into an (N,D) numpy matrix.
    """

    rows = []

    for signature in collection:

        if hasattr(signature, "to_numpy"):
            rows.append(signature.to_numpy())

        else:
            rows.append(signature.to_tuple())

    return np.asarray(rows, dtype=float)


# ============================================================
# Pairwise distances
# ============================================================


def distance_matrix(collection):
    """
    Computes the complete Euclidean distance matrix.
    """

    X = _signature_matrix(collection)

    diff = X[:, None, :] - X[None, :, :]

    return np.linalg.norm(diff, axis=2)


# ============================================================
# Metric observables
# ============================================================


def eccentricities(collection):
    """
    Maximum distance from each signature to every other signature.
    """

    D = distance_matrix(collection)

    return D.max(axis=1)


def metric_diameter(collection):
    """
    Metric diameter of the Signature Space.
    """

    D = distance_matrix(collection)

    return float(D.max())


def metric_radius(collection):
    """
    Metric radius of the Signature Space.
    """

    return float(eccentricities(collection).min())


def metric_center(collection):
    """
    Returns the metric-center signature.
    """

    ecc = eccentricities(collection)

    index = int(np.argmin(ecc))

    return collection[index]


def peripheral_signatures(collection):
    """
    Returns the peripheral signatures.
    """

    ecc = eccentricities(collection)

    maximum = ecc.max()

    indices = np.where(np.isclose(ecc, maximum))[0]

    return [collection[i] for i in indices]


# ============================================================
# Pairwise statistics
# ============================================================


def pairwise_distances(collection):
    """
    Returns the upper-triangular pairwise distances.
    """

    D = distance_matrix(collection)

    n = D.shape[0]

    values = []

    for i in range(n):

        for j in range(i + 1, n):

            values.append(D[i, j])

    return np.asarray(values, dtype=float)


def minimum_pairwise_distance(collection):

    return float(pairwise_distances(collection).min())


def maximum_pairwise_distance(collection):

    return float(pairwise_distances(collection).max())


def mean_pairwise_distance(collection):

    return float(pairwise_distances(collection).mean())
  # ============================================================
# Global metric summary
# ============================================================


def metric_summary(collection):
    """
    Computes the complete metric characterization of the
    current Relational Signature Space.
    """

    return {
        "n_signatures": len(collection),
        "diameter": metric_diameter(collection),
        "radius": metric_radius(collection),
        "center": metric_center(collection),
        "peripheral": peripheral_signatures(collection),
        "minimum_distance": minimum_pairwise_distance(collection),
        "maximum_distance": maximum_pairwise_distance(collection),
        "mean_distance": mean_pairwise_distance(collection),
    }


# ============================================================
# Validation
# ============================================================


def validate_metric_space(collection):
    """
    Basic consistency checks.
    """

    D = distance_matrix(collection)

    if D.shape[0] != D.shape[1]:
        raise ValueError(
            "Distance matrix must be square."
        )

    if not np.allclose(D, D.T):
        raise ValueError(
            "Distance matrix is not symmetric."
        )

    if not np.allclose(np.diag(D), 0.0):
        raise ValueError(
            "Distance matrix diagonal is not zero."
        )

    return True


# ============================================================
# Demonstration
# ============================================================


def main():

    print("=" * 60)
    print("RSG S29-E6.2")
    print("Metric Operators")
    print("=" * 60)
    print()
    print("Available functions")
    print("-" * 60)

    print("distance_matrix()")
    print("pairwise_distances()")
    print("eccentricities()")
    print("metric_diameter()")
    print("metric_radius()")
    print("metric_center()")
    print("peripheral_indices()")
    print("minimum_pairwise_distance()")
    print("maximum_pairwise_distance()")
    print("mean_pairwise_distance()")
    print("metric_summary()")
    print("validate_metric_space()")

    print()
    print("=" * 60)
    print("READY")
    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
