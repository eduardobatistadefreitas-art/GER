"""
============================================================
GER
S29
E6.2
Statistical Observatory
Dashboard
============================================================

Terminal dashboard for the Statistical Observatory.

This module performs no scientific computation.
It only formats and displays the Statistical
Certificate.

Author
------
GER Project
"""

from __future__ import annotations

# ============================================================
# Version
# ============================================================

DASHBOARD_VERSION = "1.0"

# ============================================================
# Public API
# ============================================================

__all__ = [
    "show_dashboard",
]

# ============================================================
# Helpers
# ============================================================

def _print_section(title, data):

    print()
    print(title)
    print("=" * len(title))

    if isinstance(data, dict):

        for key, value in data.items():

            if isinstance(value, dict):

                print()

                print(f"[{key}]")

                for k, v in value.items():
                    print(f"  {k:30s}: {v}")

            else:

                print(f"{key:30s}: {value}")

    else:

        print(data)


# ============================================================
# Dashboard
# ============================================================

def show_dashboard(
    certificate: dict,
):
    """
    Display the complete Statistical Observatory
    Certificate.
    """

    print("=" * 70)
    print("GER Statistical Observatory Dashboard")
    print("=" * 70)

    print()

    print(f"Version    : {certificate.get('version')}")
    print(f"Samples    : {certificate.get('samples')}")
    print(f"Timestamp  : {certificate.get('timestamp')}")

    dimensions = certificate.get(
        "dimensions",
        [],
    )

    print(f"Dimensions : {', '.join(dimensions)}")

    sections = [

        "statistics",

        "occupancy",

        "density",

        "concentration",

        "stability",

        "outliers",

    ]

    for section in sections:

        if section in certificate:

            _print_section(

                section.upper(),

                certificate[section],

            )

    print()
    print("=" * 70)
    print("End of Dashboard")
    print("=" * 70)


# ============================================================
# Self Test
# ============================================================

def main():

    certificate = {

        "version": "1.0",

        "samples": 100,

        "timestamp": "2026-07-21",

        "dimensions": [

            "diameter",

            "convergence",

            "recurrence",

            "drift",

        ],

        "statistics": {

            "variables": 4,

        },

        "occupancy": {

            "occupation_ratio": 0.97,

        },

        "density": {

            "mean_density": -2.11,

        },

        "concentration": {

            "dynamic_range": 0.84,

        },

        "stability": {

            "diameter_mean": {

                "mean": 0.83,

                "std": 0.02,

            }

        },

        "outliers": {

            "outliers": 3,

        },

    }

    show_dashboard(certificate)


if __name__ == "__main__":
    main()
