"""
=============================================================
S29_E9/models.py
=============================================================

Mathematical Models

Trajectory Relaxation Analysis

This module defines every candidate model used by E9.

No fitting is performed here.

=============================================================
"""

from __future__ import annotations

import numpy as np


# ============================================================
# Linear
# ============================================================

def linear(x, a, b):
    """
    y = a + b*x
    """
    return a + b * x


# ============================================================
# Quadratic
# ============================================================

def quadratic(x, a, b, c):
    """
    y = a + b*x + c*x²
    """
    return a + b * x + c * x**2


# ============================================================
# Exponential
# ============================================================

def exponential(x, a, b):
    """
    y = a * exp(b*x)
    """
    return a * np.exp(b * x)


# ============================================================
# Power Law
# ============================================================

def power(x, a, b):
    """
    y = a * x^b
    """
    return a * np.power(x, b)


# ============================================================
# Logarithmic
# ============================================================

def logarithmic(x, a, b):
    """
    y = a + b*log(x)
    """
    return a + b * np.log(x)


# ============================================================
# Inverse
# ============================================================

def inverse(x, a, b):
    """
    y = a + b/x
    """
    return a + b / x


# ============================================================
# Exponential Saturation
# ============================================================

def exp_saturation(x, L, A, k):
    """
    y = L + A*exp(-k*x)
    """
    return L + A * np.exp(-k * x)


# ============================================================
# Michaelis-Menten
# ============================================================

def michaelis_menten(x, a, b):
    """
    y = (a*x)/(b+x)
    """
    return (a * x) / (b + x)


# ============================================================
# Logistic
# ============================================================

def logistic(x, L, k, x0):
    """
    y = L / (1 + exp(-k*(x-x0)))
    """
    return L / (
        1.0 +
        np.exp(
            -k * (x - x0)
        )
    )


# ============================================================
# Registry
# ============================================================

MODEL_REGISTRY = {

    "linear": linear,

    "quadratic": quadratic,

    "exponential": exponential,

    "power": power,

    "logarithmic": logarithmic,

    "inverse": inverse,

    "exp_saturation": exp_saturation,

    "michaelis_menten": michaelis_menten,

    "logistic": logistic,

}


# ============================================================
# Initial Parameters
# ============================================================

INITIAL_PARAMETERS = {

    "linear": (
        1.0,
        1.0,
    ),

    "quadratic": (
        1.0,
        1.0,
        0.0,
    ),

    "exponential": (
        1.0,
        -1.0,
    ),

    "power": (
        1.0,
        -1.0,
    ),

    "logarithmic": (
        1.0,
        1.0,
    ),

    "inverse": (
        1.0,
        1.0,
    ),

    "exp_saturation": (
        0.0,
        1.0,
        1.0,
    ),

    "michaelis_menten": (
        1.0,
        1.0,
    ),

    "logistic": (
        1.0,
        1.0,
        0.5,
    ),

}


# ============================================================
# Model Information
# ============================================================

MODEL_DESCRIPTIONS = {

    "linear":
        "Linear",

    "quadratic":
        "Quadratic Polynomial",

    "exponential":
        "Exponential",

    "power":
        "Power Law",

    "logarithmic":
        "Logarithmic",

    "inverse":
        "Inverse",

    "exp_saturation":
        "Exponential Saturation",

    "michaelis_menten":
        "Michaelis-Menten Saturation",

    "logistic":
        "Logistic Sigmoid",

}


# ============================================================
# Public API
# ============================================================

def get_model(name: str):
    """
    Return model callable.
    """

    if name not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model: {name}"
        )

    return MODEL_REGISTRY[name]


def get_initial_parameters(name: str):
    """
    Return default initial parameters.
    """

    if name not in INITIAL_PARAMETERS:
        raise ValueError(
            f"Unknown model: {name}"
        )

    return INITIAL_PARAMETERS[name]


def get_description(name: str):
    """
    Return human-readable model description.
    """

    if name not in MODEL_DESCRIPTIONS:
        raise ValueError(
            f"Unknown model: {name}"
        )

    return MODEL_DESCRIPTIONS[name]


def available_models() -> list[str]:
    """
    Return available model names.
    """

    return list(MODEL_REGISTRY.keys())


def number_of_parameters(name: str) -> int:
    """
    Return number of free parameters.
    """

    return len(
        get_initial_parameters(name)
    )
