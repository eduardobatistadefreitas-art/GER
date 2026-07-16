"""
============================================================
RSG
Signature Dataset
============================================================

Official Reference Signature Space used throughout the
S28 series.

Every experiment must import the signatures from this
module instead of defining them locally.
"""

import numpy as np
from scipy.spatial.distance import cdist


# ============================================================
# Reference Signature Space
# ============================================================

SIGNATURES = {
    "Harmonic": (1.992115, 0.083005, 0.022109),
    "Damped": (1.999804, 0.618431, 0.027211),
    "Van der Pol": (1.560891, 0.291408, 0.035714),
    "Logistic": (0.010717, 0.003313, 1.000000),
    "Lorenz": (0.419313, 0.079386, 0.137755),
    "Double Pendulum": (1.301499, 0.388995, 0.069728),
}


# ============================================================
# Dataset utilities
# ============================================================

def names():

    return list(SIGNATURES.keys())


def vectors():

    return np.array(list(SIGNATURES.values()), dtype=float)


def dataframe():

    import pandas as pd

    return pd.DataFrame(
        vectors(),
        index=names(),
        columns=[
            "Diameter",
            "Convergence",
            "Recurrence",
        ],
    )


def distance_matrix():

    X = vectors()

    return cdist(
        X,
        X,
        metric="euclidean",
    )


def dimension():

    return len(next(iter(SIGNATURES.values())))


def size():

    return len(SIGNATURES)
