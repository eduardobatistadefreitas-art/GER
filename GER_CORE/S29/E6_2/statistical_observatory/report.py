"""
============================================================
GER
S29
E6.2
Statistical Observatory
Report Generator
============================================================

Generates reports from the Statistical Certificate.

This module performs no scientific computation.
Its only responsibility is to serialize the
certificate into standard output formats.

Author
------
GER Project
"""

from __future__ import annotations

import json
from pathlib import Path

# ============================================================
# Version
# ============================================================

REPORT_VERSION = "1.0"

# ============================================================
# Public API
# ============================================================

__all__ = [
    "save_json",
    "save_txt",
    "generate_report",
]

# ============================================================
# JSON
# ============================================================

def save_json(
    certificate: dict,
    filename,
):
    """
    Save certificate as JSON.
    """

    filename = Path(filename)

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            certificate,
            f,
            indent=4,
            ensure_ascii=False,
            default=str,
        )

    return filename


# ============================================================
# TXT
# ============================================================

def save_txt(
    certificate: dict,
    filename,
):
    """
    Save certificate as plain text.
    """

    filename = Path(filename)

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as f:

        f.write("=" * 60 + "\n")
        f.write("GER Statistical Observatory\n")
        f.write("=" * 60 + "\n\n")

        for key, value in certificate.items():

            f.write(f"{key}\n")
            f.write("-" * len(str(key)))
            f.write("\n")

            f.write(str(value))
            f.write("\n\n")

    return filename


# ============================================================
# High-Level API
# ============================================================

def generate_report(
    certificate: dict,
    output_directory,
):
    """
    Generate all report files.
    """

    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_file = save_json(
        certificate,
        output_directory / "statistical_certificate.json",
    )

    txt_file = save_txt(
        certificate,
        output_directory / "statistical_certificate.txt",
    )

    return {

        "json": json_file,

        "txt": txt_file,
    }


# ============================================================
# Self Test
# ============================================================

def main():

    example = {

        "module": "GER",

        "version": REPORT_VERSION,

        "samples": 100,

        "statistics": {},

        "occupancy": {},

        "density": {},

        "concentration": {},

        "stability": {},

        "outliers": {},
    }

    files = generate_report(
        example,
        "./REPORT_TEST",
    )

    print()

    print("=" * 60)
    print("Report Generator")
    print("=" * 60)

    for key, value in files.items():

        print(f"{key:10s}: {value}")

    print()


if __name__ == "__main__":
    main()
