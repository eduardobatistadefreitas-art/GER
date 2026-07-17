"""
=========================================================
GER
S29

External Systems Package
=========================================================
"""

from .duffing import simulate_duffing
from .harmonic import simulate_harmonic
from .white_noise import simulate_white_noise

__all__ = [
    "simulate_duffing",
    "simulate_harmonic",
    "simulate_white_noise",
]
