"""
============================================================
GER
S29
E6.2
Statistical Observatory
Statistical Certificate
============================================================

Builds the Statistical Observatory Certificate.

This module does not compute statistics.
It consolidates the outputs produced by the
Statistical Observatory modules into a single
scientific certificate.

Author
------
GER Project
"""

from __future__ import annotations

from datetime import datetime

from .statistics import compute_statistics
from .occupancy import compute_occupancy
from .density import compute_density
from .concentration import compute_concentration
from .stability import compute_stability
from .outliers import compute_outliers

# ============================================================
# Version
# ============================================================

CERTIFICATE_VERSION = "1.0"

# ============================================================
# Public API
# ============================================================

__all__ = [
    "build_certificate",
]

# ============================================================
# Certificate
# ============================================================

def build_certificate(signatures):
    """
    Build the complete Statistical Observatory Certificate.
    """

    statistics = compute_statistics(signatures)

    occupancy = compute_occupancy(signatures)

    density = compute_density(signatures)

    concentration = compute_concentration(signatures)

    stability = compute_stability(signatures)

    outliers = compute_outliers(signatures)

    certificate = {

        "module":

            "GER Statistical Observatory",

        "version":

            CERTIFICATE_VERSION,

        "timestamp":

            datetime.utcnow().isoformat(),

        "samples":

            len(signatures),

        "dimensions":

            list(signatures.columns),

        "statistics":

            statistics["summary"],

        "occupancy":

            occupancy["summary"],

        "density":

            density["summary"],

        "concentration":

            concentration["summary"],

        "stability":

            stability["summary"],

        "outliers":

            outliers["summary"],
    }

    return certificate


# ============================================================
# Printing
# ============================================================

def print_certificate(certificate):

    print("=" * 60)
    print("GER Statistical Observatory")
    print("Certificate")
    print("=" * 60)
    print()

    print(f"Version   : {certificate['version']}")
    print(f"Samples   : {certificate['samples']}")
    print(f"Dimensions: {certificate['dimensions']}")
    print(f"Timestamp : {certificate['timestamp']}")

    print()

    for section in [

        "statistics",

        "occupancy",

        "density",

        "concentration",

        "stability",

        "outliers",

    ]:

        print(section.upper())

        print("-" * len(section))

        print(certificate[section])

        print()
