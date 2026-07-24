"""
============================================================
GER
S29
E6.2
Statistical Observatory
Runner
============================================================

Main execution pipeline for the Statistical Observatory.

Responsibilities
----------------
1. Load experiment data.
2. Build the Statistical Certificate.
3. Generate report files.
4. Display the dashboard.

Author
------
GER Project
"""

from __future__ import annotations

from pathlib import Path

from .io import load_signatures
from .certificate import build_certificate
from .report import generate_report
from .dashboard import show_dashboard

# ============================================================
# Version
# ============================================================

RUNNER_VERSION = "1.0"

# ============================================================
# Defaults
# ============================================================

DEFAULT_OUTPUT = Path("./STATISTICAL_OBSERVATORY")

# ============================================================
# Public API
# ============================================================

__all__ = [
    "run",
]

# ============================================================
# Runner
# ============================================================

def run(
    output_directory=DEFAULT_OUTPUT,
):
    """
    Execute the complete Statistical Observatory.
    """

    print("=" * 60)
    print("GER")
    print("S29")
    print("E6.2")
    print("Statistical Observatory")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print("Loading signatures...")

    signatures = load_signatures()

    print(f"Loaded {len(signatures)} signatures.")
    print()

    # --------------------------------------------------------
    # Certificate
    # --------------------------------------------------------

    print("Building certificate...")

    certificate = build_certificate(
        signatures
    )

    print("Done.")
    print()

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print("Generating reports...")

    reports = generate_report(
        certificate,
        output_directory,
    )

    print("Done.")
    print()

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    show_dashboard(
        certificate
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()

    print("=" * 60)
    print("Generated Files")
    print("=" * 60)

    for name, path in reports.items():

        print(f"{name:10s}: {path}")

    print()

    return {

        "certificate": certificate,

        "reports": reports,

    }


# ============================================================
# Main
# ============================================================

def main():

    run()


if __name__ == "__main__":
    main()
